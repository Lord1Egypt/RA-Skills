"""机器学习策略 - XGBoost/LightGBM/随机森林/集成学习 + 增量学习 + 模型持久化"""
from __future__ import annotations
import logging, os, json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

_MODEL_DIR = Path(__file__).parent.parent.parent / "models"


@dataclass
class MLSignal:
    """机器学习信号"""
    direction: str
    confidence: float
    probability: float
    features_used: List[str]
    model_name: str
    metadata: Dict = field(default_factory=dict)


class FeatureEngineer:
    """特征工程"""

    @staticmethod
    def create_features(df: pd.DataFrame) -> pd.DataFrame:
        """创建技术特征"""
        features = pd.DataFrame(index=df.index)

        close = df["close"].astype(float)
        high = df["high"].astype(float)
        low = df["low"].astype(float)
        volume = df["volume"].astype(float)
        open_price = df["open"].astype(float)

        for period in [5, 10, 20, 60]:
            features[f"ma_{period}"] = close.rolling(period).mean()
            features[f"ma_slope_{period}"] = features[f"ma_{period}"].pct_change(5)
            features[f"close_ma_ratio_{period}"] = close / features[f"ma_{period}"]

        features["rsi_14"] = FeatureEngineer._calc_rsi(close, 14)
        features["rsi_6"] = FeatureEngineer._calc_rsi(close, 6)

        features["volatility_10"] = close.rolling(10).std() / close.rolling(10).mean()
        features["volatility_20"] = close.rolling(20).std() / close.rolling(20).mean()

        features["volume_ratio_5"] = volume / volume.rolling(5).mean()
        features["volume_ratio_10"] = volume / volume.rolling(10).mean()
        features["volume_change"] = volume.pct_change()

        features["high_low_ratio"] = (high - low) / close
        features["close_open_ratio"] = (close - open_price) / close

        features["momentum_5"] = close.pct_change(5)
        features["momentum_10"] = close.pct_change(10)
        features["momentum_20"] = close.pct_change(20)

        if "ma5" in df.columns and "ma20" in df.columns:
            features["ma5"] = df["ma5"].astype(float)
            features["ma20"] = df["ma20"].astype(float)
            features["ma_cross"] = (features["ma5"] > features["ma20"]).astype(int)

        if "dif" in df.columns and "dea" in df.columns:
            features["dif"] = df["dif"].astype(float)
            features["dea"] = df["dea"].astype(float)
            features["macd"] = df["macd"].astype(float) if "macd" in df.columns else features["dif"] - features["dea"]
            features["macd_cross"] = ((features["dif"] > features["dea"]) &
                                      (features["dif"].shift(1) <= features["dea"].shift(1))).astype(int)

        if "rsi" in df.columns:
            features["rsi_original"] = df["rsi"].astype(float)

        if "boll_upper" in df.columns and "boll_lower" in df.columns:
            boll_upper = df["boll_upper"].astype(float)
            boll_lower = df["boll_lower"].astype(float)
            features["boll_width"] = (boll_upper - boll_lower) / close
            features["boll_position"] = (close - boll_lower) / (boll_upper - boll_lower)

        features["price_range"] = (high - low) / close
        features["upper_shadow"] = (high - close) / close
        features["lower_shadow"] = (close - low) / close

        for lag in [1, 2, 3, 5]:
            features[f"return_lag_{lag}"] = close.pct_change(lag)
            features[f"volume_lag_{lag}"] = volume.pct_change(lag)

        return features

    @staticmethod
    def _calc_rsi(series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def create_labels(df: pd.DataFrame, forward_periods: int = 5,
                      threshold: float = 0.02) -> pd.Series:
        """创建标签（未来收益分类）"""
        close = df["close"].astype(float)
        future_return = close.shift(-forward_periods) / close - 1

        labels = pd.Series(0, index=df.index)
        labels[future_return > threshold] = 1
        labels[future_return < -threshold] = -1

        return labels


class BaseMLStrategy(ABC):
    """机器学习策略基类 - 支持增量学习和模型持久化"""

    def __init__(self, name: str = "base_ml"):
        self.name = name
        self.model = None
        self.feature_columns: List[str] = []
        self.is_trained = False
        self.feature_importance: Dict[str, float] = {}
        self._train_samples = 0
        self._train_history: List[Dict] = []

    @abstractmethod
    def _create_model(self) -> Any:
        pass

    @abstractmethod
    def _fit_model(self, X: np.ndarray, y: np.ndarray) -> None:
        pass

    @abstractmethod
    def _predict_proba(self, X: np.ndarray) -> np.ndarray:
        pass

    def _supports_incremental(self) -> bool:
        """是否支持增量学习"""
        return False

    def _incremental_fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """增量训练子类实现"""
        pass

    def train(self, df: pd.DataFrame, forward_periods: int = 5,
              threshold: float = 0.02) -> Dict[str, float]:
        """训练模型"""
        features = FeatureEngineer.create_features(df)
        labels = FeatureEngineer.create_labels(df, forward_periods, threshold)

        valid_mask = features.notna().all(axis=1) & labels.notna()
        features = features[valid_mask]
        labels = labels[valid_mask]

        if len(features) < 100:
            logger.warning(f"训练数据不足: {len(features)}")
            return {"accuracy": 0, "samples": len(features)}

        self.feature_columns = features.columns.tolist()
        X = features.values
        y = labels.values

        self.model = self._create_model()
        self._fit_model(X, y)
        self.is_trained = True
        self._train_samples = len(X)

        predictions = self._predict_proba(X)
        pred_labels = np.argmax(predictions, axis=1) - 1
        accuracy = np.mean(pred_labels == y)

        self._train_history.append({
            "samples": len(X), "accuracy": float(accuracy),
            "threshold": threshold, "forward_periods": forward_periods,
        })

        return {"accuracy": accuracy, "samples": len(X)}

    def incremental_train(self, df: pd.DataFrame, forward_periods: int = 5,
                          threshold: float = 0.02) -> Dict[str, float]:
        """增量训练（在已有模型基础上追加训练）"""
        if not self.is_trained:
            return self.train(df, forward_periods, threshold)

        features = FeatureEngineer.create_features(df)
        labels = FeatureEngineer.create_labels(df, forward_periods, threshold)

        valid_mask = features.notna().all(axis=1) & labels.notna()
        features = features[valid_mask]
        labels = labels[valid_mask]

        if len(features) < 50:
            return {"accuracy": 0, "samples": len(features), "skipped": True}

        for col in self.feature_columns:
            if col not in features.columns:
                features[col] = 0
        features = features[self.feature_columns]

        X = features.values
        y = labels.values

        if self._supports_incremental():
            self._incremental_fit(X, y)
        else:
            self._fit_model(X, y)

        self._train_samples += len(X)

        predictions = self._predict_proba(X)
        pred_labels = np.argmax(predictions, axis=1) - 1
        accuracy = np.mean(pred_labels == y)

        self._train_history.append({
            "samples": len(X), "accuracy": float(accuracy),
            "incremental": True, "total_samples": self._train_samples,
        })

        return {"accuracy": accuracy, "samples": len(X), "total_samples": self._train_samples}

    def save_model(self, path: str = None) -> str:
        """保存模型到磁盘"""
        if not self.is_trained or self.model is None:
            return ""

        save_dir = Path(path) if path else _MODEL_DIR / self.name
        save_dir.mkdir(parents=True, exist_ok=True)

        try:
            import joblib
        except ImportError:
            logger.error("joblib 未安装，无法保存模型")
            return ""

        model_path = save_dir / "model.joblib"
        joblib.dump(self.model, model_path)

        meta = {
            "feature_columns": self.feature_columns,
            "train_samples": self._train_samples,
            "train_history": self._train_history,
            "feature_importance": dict(sorted(
                self.feature_importance.items(), key=lambda x: x[1], reverse=True
            )[:20]),
        }
        with open(save_dir / "meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        logger.info(f"模型已保存: {save_dir}")
        return str(save_dir)

    def load_model(self, path: str = None) -> bool:
        """从磁盘加载模型"""
        load_dir = Path(path) if path else _MODEL_DIR / self.name
        if not load_dir.exists():
            return False

        try:
            import joblib
        except ImportError:
            logger.error("joblib 未安装，无法加载模型")
            return False

        model_path = load_dir / "model.joblib"
        if not model_path.exists():
            logger.warning(f"模型文件不存在: {model_path}")
            return False

        try:
            from ..models import load_model_safe
            self.model = load_model_safe(str(model_path))
            if self.model is None:
                logger.warning(f"安全加载模型失败 {self.name}")
                return False
        except Exception as e:
            logger.warning(f"加载模型失败 {self.name}: {e}")
            return False

        meta_path = load_dir / "meta.json"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            self.feature_columns = meta.get("feature_columns", [])
            self._train_samples = meta.get("train_samples", 0)
            self._train_history = meta.get("train_history", [])
            self.feature_importance = meta.get("feature_importance", {})

        self.is_trained = True
        logger.info(f"模型已加载: {load_dir}, 训练样本={self._train_samples}")
        return True

    def predict(self, df: pd.DataFrame) -> Optional[MLSignal]:
        """预测信号"""
        if not self.is_trained or self.model is None:
            return None

        features = FeatureEngineer.create_features(df)

        for col in self.feature_columns:
            if col not in features.columns:
                features[col] = 0

        features = features[self.feature_columns]

        if features.empty or features.iloc[-1].isna().any():
            return None

        X = features.iloc[-1:].values
        proba = self._predict_proba(X)[0]

        pred_class = np.argmax(proba) - 1
        confidence = float(proba[pred_class + 1])

        if pred_class == 1:
            direction = "BUY"
        elif pred_class == -1:
            direction = "SELL"
        else:
            return None

        if confidence < 0.55:
            return None

        return MLSignal(
            direction=direction,
            confidence=confidence,
            probability=float(max(proba)),
            features_used=self.feature_columns[:10],
            model_name=self.name,
            metadata={"class_probs": proba.tolist()}
        )

    def get_feature_importance(self) -> Dict[str, float]:
        return self.feature_importance


class XGBoostStrategy(BaseMLStrategy):
    """XGBoost策略"""

    def __init__(self):
        super().__init__("xgboost")

    def _create_model(self):
        try:
            from xgboost import XGBClassifier
            return XGBClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                use_label_encoder=False,
                eval_metric="mlogloss"
            )
        except ImportError:
            logger.warning("XGBoost未安装，使用sklearn替代")
            from sklearn.ensemble import GradientBoostingClassifier
            return GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )

    def _fit_model(self, X: np.ndarray, y: np.ndarray) -> None:
        y_mapped = y + 1
        self.model.fit(X, y_mapped)
        if hasattr(self.model, "feature_importances_"):
            self.feature_importance = dict(zip(
                self.feature_columns,
                self.model.feature_importances_
            ))

    def _predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class LightGBMStrategy(BaseMLStrategy):
    """LightGBM策略"""

    def __init__(self):
        super().__init__("lightgbm")

    def _create_model(self):
        try:
            from lightgbm import LGBMClassifier
            return LGBMClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbose=-1
            )
        except ImportError:
            logger.warning("LightGBM未安装，使用sklearn替代")
            from sklearn.ensemble import GradientBoostingClassifier
            return GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )

    def _fit_model(self, X: np.ndarray, y: np.ndarray) -> None:
        y_mapped = y + 1
        self.model.fit(X, y_mapped)
        if hasattr(self.model, "feature_importances_"):
            self.feature_importance = dict(zip(
                self.feature_columns,
                self.model.feature_importances_
            ))

    def _predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class RandomForestStrategy(BaseMLStrategy):
    """随机森林策略"""

    def __init__(self, n_estimators: int = 200):
        super().__init__("random_forest")
        self.n_estimators = n_estimators

    def _create_model(self):
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=8,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )

    def _fit_model(self, X: np.ndarray, y: np.ndarray) -> None:
        y_mapped = y + 1
        self.model.fit(X, y_mapped)
        self.feature_importance = dict(zip(
            self.feature_columns,
            self.model.feature_importances_
        ))

    def _predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class MLPStrategy(BaseMLStrategy):
    """神经网络策略"""

    def __init__(self, hidden_layers: Tuple = (64, 32, 16)):
        super().__init__("mlp")
        self.hidden_layers = hidden_layers

    def _create_model(self):
        from sklearn.neural_network import MLPClassifier
        return MLPClassifier(
            hidden_layer_sizes=self.hidden_layers,
            activation="relu",
            solver="adam",
            alpha=0.001,
            batch_size=32,
            learning_rate="adaptive",
            max_iter=500,
            random_state=42
        )

    def _fit_model(self, X: np.ndarray, y: np.ndarray) -> None:
        y_mapped = y + 1
        from sklearn.preprocessing import StandardScaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y_mapped)

    def _predict_proba(self, X: np.ndarray) -> np.ndarray:
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X)


class EnsembleMLStrategy:
    """集成机器学习策略 - 支持增量学习和模型持久化"""

    def __init__(self, strategies: List[BaseMLStrategy] = None):
        if strategies is None:
            self.strategies = [
                XGBoostStrategy(),
                LightGBMStrategy(),
                RandomForestStrategy(),
                MLPStrategy()
            ]
        else:
            self.strategies = strategies

        self.weights: Dict[str, float] = {}
        self.is_trained = False

    def train(self, df: pd.DataFrame, forward_periods: int = 5,
              threshold: float = 0.02) -> Dict[str, Dict[str, float]]:
        """训练所有模型"""
        results = {}
        for strategy in self.strategies:
            try:
                metrics = strategy.train(df, forward_periods, threshold)
                results[strategy.name] = metrics
                logger.info(f"{strategy.name}: {metrics}")
            except Exception as e:
                logger.error(f"{strategy.name} 训练失败: {e}")
                results[strategy.name] = {"accuracy": 0, "error": str(e)}

        self._update_weights(results)
        self.is_trained = True
        return results

    def incremental_train(self, df: pd.DataFrame, forward_periods: int = 5,
                          threshold: float = 0.02) -> Dict[str, Dict[str, float]]:
        """增量训练所有模型"""
        results = {}
        for strategy in self.strategies:
            try:
                metrics = strategy.incremental_train(df, forward_periods, threshold)
                results[strategy.name] = metrics
                logger.info(f"{strategy.name} 增量训练: {metrics}")
            except Exception as e:
                logger.error(f"{strategy.name} 增量训练失败: {e}")
                results[strategy.name] = {"accuracy": 0, "error": str(e)}

        self._update_weights(results)
        self.is_trained = True
        return results

    def _update_weights(self, results: Dict[str, Dict[str, float]]):
        """根据训练结果更新模型权重"""
        total_accuracy = sum(m.get("accuracy", 0) for m in results.values())
        if total_accuracy > 0:
            self.weights = {
                name: m.get("accuracy", 0) / total_accuracy
                for name, m in results.items()
            }
        else:
            self.weights = {s.name: 1.0 / len(self.strategies) for s in self.strategies}

    def save_all(self) -> List[str]:
        """保存所有模型"""
        paths = []
        for strategy in self.strategies:
            try:
                p = strategy.save_model()
                if p:
                    paths.append(p)
            except Exception as e:
                logger.warning(f"保存模型失败 {strategy.name}: {e}")

        import json
        meta_path = _MODEL_DIR / "ensemble_meta.json"
        _MODEL_DIR.mkdir(parents=True, exist_ok=True)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({"weights": self.weights, "is_trained": self.is_trained}, f)
        paths.append(str(meta_path))
        return paths

    def load_all(self) -> bool:
        """加载所有模型"""
        loaded = 0
        for strategy in self.strategies:
            try:
                if strategy.load_model():
                    loaded += 1
            except Exception as e:
                logger.debug(f"加载模型跳过 {strategy.name}: {e}")

        meta_path = _MODEL_DIR / "ensemble_meta.json"
        if meta_path.exists():
            import json
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            self.weights = meta.get("weights", {})
            self.is_trained = meta.get("is_trained", False)

        if loaded > 0:
            self.is_trained = True
            logger.info(f"已加载 {loaded}/{len(self.strategies)} 个模型")
        return loaded > 0

    def predict(self, df: pd.DataFrame) -> Optional[MLSignal]:
        """集成预测"""
        if not self.is_trained:
            return None

        signals = []
        for strategy in self.strategies:
            signal = strategy.predict(df)
            if signal:
                signals.append(signal)

        if not signals:
            return None

        direction_votes = {"BUY": 0.0, "SELL": 0.0}
        for signal in signals:
            weight = self.weights.get(signal.model_name, 0.25)
            direction_votes[signal.direction] += weight * signal.confidence

        if direction_votes["BUY"] > direction_votes["SELL"] and direction_votes["BUY"] > 0.3:
            direction = "BUY"
            confidence = direction_votes["BUY"]
        elif direction_votes["SELL"] > direction_votes["BUY"] and direction_votes["SELL"] > 0.3:
            direction = "SELL"
            confidence = direction_votes["SELL"]
        else:
            return None

        return MLSignal(
            direction=direction,
            confidence=min(confidence, 0.95),
            probability=confidence,
            features_used=[],
            model_name="ensemble_ml",
            metadata={
                "weights": self.weights,
                "votes": direction_votes,
                "individual_signals": len(signals)
            }
        )

    def get_feature_importance(self) -> Dict[str, float]:
        """获取综合特征重要性"""
        importance = {}
        for strategy in self.strategies:
            strategy_imp = strategy.get_feature_importance()
            weight = self.weights.get(strategy.name, 0.25)
            for feat, imp in strategy_imp.items():
                if feat not in importance:
                    importance[feat] = 0.0
                importance[feat] += imp * weight

        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))


class AdaptiveMLStrategy:
    """自适应机器学习策略 - 根据市场状态选择模型"""

    def __init__(self):
        self.trend_model = EnsembleMLStrategy()
        self.range_model = EnsembleMLStrategy()
        self.volatile_model = EnsembleMLStrategy()
        self.current_regime = "unknown"

    def detect_regime(self, df: pd.DataFrame) -> str:
        """检测市场状态"""
        close = df["close"].astype(float)
        returns = close.pct_change().dropna()

        if len(returns) < 20:
            return "unknown"

        volatility = returns.rolling(20).std().iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1] if len(close) >= 60 else ma20

        current_price = float(close.iloc[-1])

        if volatility > 0.03:
            regime = "volatile"
        elif current_price > ma20 > ma60:
            regime = "trend_up"
        elif current_price < ma20 < ma60:
            regime = "trend_down"
        else:
            regime = "range"

        self.current_regime = regime
        return regime

    def train(self, df: pd.DataFrame) -> Dict:
        """按市场状态分别训练"""
        regime = self.detect_regime(df)

        close = df["close"].astype(float)
        returns = close.pct_change().dropna()
        volatility = returns.rolling(20).std().iloc[-1]

        results = {}

        try:
            results["trend"] = self.trend_model.train(df, threshold=0.02)
        except Exception as e:
            results["trend"] = {"error": str(e)}

        try:
            results["range"] = self.range_model.train(df, threshold=0.01)
        except Exception as e:
            results["range"] = {"error": str(e)}

        try:
            results["volatile"] = self.volatile_model.train(df, threshold=0.04)
        except Exception as e:
            results["volatile"] = {"error": str(e)}

        results["current_regime"] = regime
        return results

    def predict(self, df: pd.DataFrame) -> Optional[MLSignal]:
        """根据市场状态选择模型预测"""
        regime = self.detect_regime(df)

        if regime in ["trend_up", "trend_down"]:
            signal = self.trend_model.predict(df)
        elif regime == "range":
            signal = self.range_model.predict(df)
        elif regime == "volatile":
            signal = self.volatile_model.predict(df)
        else:
            signal = self.trend_model.predict(df)

        if signal:
            signal.metadata["regime"] = regime

        return signal
