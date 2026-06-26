"""
Ensemble Calibration & Dynamic Weighting
P1: Confidence calibration, market-state aware weighting
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from sklearn.isotonic import IsotonicRegression
from sklearn.calibration import CalibratedClassifierCV

# ============ Configuration ============
WEIGHT_KRONOS = 0.30
WEIGHT_CHRONOS2 = 0.25
WEIGHT_TIMESFM = 0.25
WEIGHT_FINBERT = 0.20
CALIBRATION_METHOD = "isotonic"


@dataclass
class ModelPrediction:
    """单个模型的预测"""
    model_name: str
    signal: str  # bullish/bearish/neutral
    raw_confidence: float  # 0-1
    calibrated_confidence: float  # 校准后的置信度
    direction_prob: float  # 上涨概率
    features: Dict


@dataclass
class EnsembleResult:
    """集成结果"""
    fused_signal: str
    fused_confidence: float
    direction_prob: float
    contributions: Dict[str, float]  # 各模型贡献
    market_state: str  # trending/range/volatile
    calibration_applied: bool


class ConfidenceCalibrator:
    """置信度校准器"""
    
    def __init__(self, method: str = CALIBRATION_METHOD):
        self.method = method
        self.calibrators: Dict[str, IsotonicRegression] = {}
        self.is_fitted = False
    
    def fit(self, predictions: List[ModelPrediction], actual_outcomes: List[bool]):
        """
        训练校准器
        
        Args:
            predictions: 历史预测列表
            actual_outcomes: 实际结果 (True=预测正确)
        """
        if len(predictions) < 30:
            return  # 数据不足，跳过校准
        
        # 按模型分组
        model_preds: Dict[str, List[float]] = {}
        model_outcomes: Dict[str, List[bool]] = {}
        
        for pred, outcome in zip(predictions, actual_outcomes):
            model = pred.model_name
            if model not in model_preds:
                model_preds[model] = []
                model_outcomes[model] = []
            model_preds[model].append(pred.raw_confidence)
            model_outcomes[model].append(outcome)
        
        # 为每个模型训练校准器
        for model, confs in model_preds.items():
            if len(confs) >= 10:
                calibrator = IsotonicRegression(out_of_order=True)
                calibrator.fit(confs, model_outcomes[model])
                self.calibrators[model] = calibrator
        
        self.is_fitted = True
    
    def calibrate(self, pred: ModelPrediction) -> ModelPrediction:
        """校准单个预测的置信度"""
        if not self.is_fitted or pred.model_name not in self.calibrators:
            pred.calibrated_confidence = pred.raw_confidence
            return pred
        
        calibrator = self.calibrators[pred.model_name]
        pred.calibrated_confidence = max(0.0, min(1.0, calibrator.predict([pred.raw_confidence])[0]))
        return pred


class MarketStateDetector:
    """市场状态检测"""
    
    @staticmethod
    def detect(df_price, lookback: int = 50) -> str:
        """
        检测市场状态
        
        Returns:
            trending: 趋势市场
            range: 震荡市场  
            volatile: 高波动市场
        """
        if len(df_price) < lookback:
            return "unknown"
        
        prices = df_price["close"].values[-lookback:]
        
        # 计算趋势强度 (简单线性回归斜率)
        x = np.arange(len(prices))
        slope = np.polyfit(x, prices, 1)[0]
        slope_pct = slope / np.mean(prices)
        
        # 计算波动率
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns)
        
        # 计算趋势一致性
        positive_returns = np.sum(returns > 0) / len(returns)
        
        # 判断状态
        if abs(slope_pct) > 0.001 and abs(positive_returns - 0.5) > 0.15:
            return "trending"
        elif volatility > 0.03:
            return "volatile"
        else:
            return "range"
    
    @staticmethod
    def get_dynamic_weights(market_state: str) -> Dict[str, float]:
        """根据市场状态获取动态权重"""
        if market_state == "trending":
            # 趋势市场：强化 Kronos (识别趋势) 和 Chronos (宏观周期)
            return {
                "kronos": 0.35,
                "chronos2": 0.30,
                "timesfm": 0.20,
                "finbert": 0.15
            }
        elif market_state == "volatile":
            # 高波动：降低 FinBERT (情绪噪音大)，提高 TimesFM (稳健)
            return {
                "kronos": 0.25,
                "chronos2": 0.25,
                "timesfm": 0.35,
                "finbert": 0.15
            }
        elif market_state == "range":
            # 震荡市场：提高 FinBERT (情绪驱动)
            return {
                "kronos": 0.25,
                "chronos2": 0.20,
                "timesfm": 0.25,
                "finbert": 0.30
            }
        else:
            # 默认：基础权重
            return {
                "kronos": WEIGHT_KRONOS,
                "chronos2": WEIGHT_CHRONOS2,
                "timesfm": WEIGHT_TIMESFM,
                "finbert": WEIGHT_FINBERT
            }


class DynamicWeightedEnsemble:
    """动态加权集成器"""
    
    def __init__(self, calibrator: Optional[ConfidenceCalibrator] = None):
        self.calibrator = calibrator or ConfidenceCalibrator()
        self.market_state = "unknown"
        self.base_weights = {
            "kronos": WEIGHT_KRONOS,
            "chronos2": WEIGHT_CHRONOS2,
            "timesfm": WEIGHT_TIMESFM,
            "finbert": WEIGHT_FINBERT
        }
    
    def update_market_state(self, df_price) -> str:
        """更新市场状态"""
        self.market_state = MarketStateDetector.detect(df_price)
        return self.market_state
    
    def get_dynamic_weights(self) -> Dict[str, float]:
        """获取动态权重"""
        return MarketStateDetector.get_dynamic_weights(self.market_state)
    
    def fuse(self, predictions: List[ModelPrediction], use_calibration: bool = True) -> EnsembleResult:
        """
        融合多个模型的预测
        
        Args:
            predictions: 模型预测列表
            use_calibration: 是否使用置信度校准
        """
        # 校准
        if use_calibration and self.calibrator.is_fitted:
            predictions = [self.calibrator.calibrate(p) for p in predictions]
        else:
            for p in predictions:
                p.calibrated_confidence = p.raw_confidence
        
        # 获取动态权重
        weights = self.get_dynamic_weights()
        
        # 转换为模型名映射
        pred_by_model = {p.model_name: p for p in predictions}
        
        # 加权融合
        total_weight = 0
        weighted_direction = 0
        contributions = {}
        
        for model_name, base_weight in weights.items():
            if model_name not in pred_by_model:
                continue
            
            pred = pred_by_model[model_name]
            
            # 信号转为数值
            if pred.signal == "bullish":
                signal_val = 1
            elif pred.signal == "bearish":
                signal_val = -1
            else:
                signal_val = 0
            
            # 加权
            effective_weight = base_weight * pred.calibrated_confidence
            weighted_direction += signal_val * effective_weight
            total_weight += effective_weight
            
            contributions[model_name] = {
                "weight": base_weight,
                "confidence": pred.calibrated_confidence,
                "effective_weight": effective_weight,
                "signal": pred.signal
            }
        
        # 归一化
        if total_weight > 0:
            normalized_direction = weighted_direction / total_weight
        else:
            normalized_direction = 0
        
        # 融合信号
        if normalized_direction > 0.2:
            fused_signal = "bullish"
        elif normalized_direction < -0.2:
            fused_signal = "bearish"
        else:
            fused_signal = "neutral"
        
        # 融合置信度
        fused_confidence = min(0.95, abs(normalized_direction) * total_weight * 100)
        
        # 上涨概率
        direction_prob = (normalized_direction + 1) / 2  # [-1, 1] -> [0, 1]
        
        return EnsembleResult(
            fused_signal=fused_signal,
            fused_confidence=fused_confidence,
            direction_prob=direction_prob,
            contributions=contributions,
            market_state=self.market_state,
            calibration_applied=use_calibration and self.calibrator.is_fitted
        )


def create_ensemble(
    predictions: List[ModelPrediction],
    market_state: str = "unknown"
) -> EnsembleResult:
    """
    便捷函数：创建集成结果
    """
    ensemble = DynamicWeightedEnsemble()
    ensemble.market_state = market_state
    return ensemble.fuse(predictions)
