#!/usr/bin/env python3
"""
Pro Athlete Analytics - 职业运动员级别分析系统
基于 Intervals.icu API

方法论来源：
- TrainingPeaks TSS/CTL/ATL/TSB 系统
- TRIMP (Training Impulse) 训练负荷理论
- Banister Impulse-Response 模型
- 功率/心率区间训练理论
- 疲劳 - 适应曲线
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent))
from intervals_api_client import create_client, IntervalsICUClient

# ================= 专业阈值标准 =================
class ProfessionalThresholds:
    """职业运动员标准阈值"""
    
    # TSB (训练压力平衡) 区间
    TSB_OPTIMAL = (5, 15)      # 最佳竞技状态
    TSB_FRESH = (0, 5)         # 状态良好
    TSB_FATIGUED = (-10, 0)    # 轻度疲劳
    TSB_EXHAUSTED = (-30, -10) # 过度疲劳
    TSB_DANGER = (-float('inf'), -30)  # 危险区域
    
    # CTL (慢性训练负荷) 标准 - 按运动类型
    CTL_TENNIS_PRO = (80, 120)     # 职业网球选手
    CTL_TENNIS_AMATEUR = (30, 60)  # 业余高手
    CTL_CYCLING_PRO = (150, 250)   # 职业自行车
    CTL_RUNNING_PRO = (100, 150)   # 职业跑步
    
    # ATL/CTL 比率
    ATL_CTL_RATIO_FRESH = 0.8      # 新鲜状态
    ATL_CTL_RATIO_FATIGUED = 1.2   # 疲劳状态
    ATL_CTL_RATIO_OVERREACH = 1.5  # 过度训练风险
    
    # 心率区间 (%最大心率)
    HR_Z1_RECOVERY = (0, 0.60)     # 恢复区
    HR_Z2_AEROBIC = (0.60, 0.70)   # 有氧基础
    HR_Z3_TEMPO = (0.70, 0.80)     # 节奏区
    HR_Z4_THRESHOLD = (0.80, 0.90) # 阈值区
    HR_Z5_VO2MAX = (0.90, 1.00)    # 最大摄氧区
    
    # 睡眠建议
    SLEEP_OPTIMAL = (8, 9)         # 最佳睡眠 (小时)
    SLEEP_MINIMUM = 7              # 最低要求
    SLEEP_DEPRIVATION = 6          # 睡眠不足
    
    # HRV (心率变异性) 评估
    HRV_EXCELLENT = 100            # ms, 优秀
    HRV_GOOD = 60                  # ms, 良好
    HRV_FAIR = 40                  # ms, 一般
    HRV_POOR = 20                  # ms, 较差
    
    # 营养目标 (按目标分类)
    # 减脂：热量缺口 500kcal/天，蛋白质 2.0g/kg
    NUTRITION_FAT_LOSS = {'calorie_deficit': 500, 'protein_g_per_kg': 2.0, 'carbs_ratio': 0.35, 'fat_ratio': 0.30}
    # 增肌：热量盈余 300kcal/天，蛋白质 1.8g/kg
    NUTRITION_MUSCLE_GAIN = {'calorie_surplus': 300, 'protein_g_per_kg': 1.8, 'carbs_ratio': 0.50, 'fat_ratio': 0.25}
    # 维持：平衡，蛋白质 1.6g/kg
    NUTRITION_MAINTENANCE = {'protein_g_per_kg': 1.6, 'carbs_ratio': 0.45, 'fat_ratio': 0.30}
    # 耐力训练：高碳水，蛋白质 1.4g/kg
    NUTRITION_ENDURANCE = {'protein_g_per_kg': 1.4, 'carbs_ratio': 0.60, 'fat_ratio': 0.20}

# ================= 数据类 =================
@dataclass
class AthleteProfile:
    """运动员档案"""
    athlete_id: str
    name: str
    weight: Optional[float] = None  # kg
    height: Optional[float] = None  # cm
    age: Optional[int] = None
    sex: str = 'M'
    ftp: Optional[float] = None     # 功能阈值功率
    lthr: Optional[float] = None    # 乳酸阈心率
    max_hr: Optional[float] = None  # 最大心率
    resting_hr: Optional[float] = None  # 静息心率
    vo2max: Optional[float] = None  # 最大摄氧量

@dataclass
class TrainingMetrics:
    """训练指标"""
    ctl: float  # 慢性训练负荷 (体能)
    atl: float  # 急性训练负荷 (疲劳)
    tsb: float  # 训练压力平衡 (状态)
    ramp_rate: float  # 负荷增长率
    
@dataclass
class WellnessMetrics:
    """健康指标"""
    hrv: Optional[float] = None
    resting_hr: Optional[float] = None
    sleep_secs: Optional[int] = None
    sleep_score: Optional[float] = None
    weight: Optional[float] = None
    steps: Optional[int] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None

@dataclass
class ActivityAnalysis:
    """活动分析"""
    id: str
    name: str
    type: str
    date: str
    duration: float  # seconds
    distance: float  # meters
    calories: float
    training_load: float
    avg_hr: Optional[float] = None
    max_hr: Optional[float] = None
    elevation: float = 0.0

class UserGoal:
    """用户目标分类"""
    FAT_LOSS = "fat_loss"           # 减脂
    MUSCLE_GAIN = "muscle_gain"     # 增肌
    MAINTENANCE = "maintenance"     # 维持
    ENDURANCE = "endurance"         # 耐力提升
    STRENGTH = "strength"           # 力量提升
    PERFORMANCE = "performance"     # 运动表现

# ================= 分析引擎 =================
class ProAthleteAnalytics:
    """职业运动员分析引擎"""
    
    def __init__(self, client: IntervalsICUClient):
        self.client = client
        self.thresholds = ProfessionalThresholds()
        self.profile = self._load_profile()
    
    def _load_profile(self) -> AthleteProfile:
        """加载运动员档案"""
        # 获取基本信息
        athlete_data = self.client._request('GET', f'/athlete/{self.client.athlete_id}') or {}
        summary = self.client.get_athlete_summary() or {}
        
        return AthleteProfile(
            athlete_id=self.client.athlete_id,
            name=summary.get('athlete_name', 'Unknown'),
            weight=summary.get('weight') or athlete_data.get('weight'),
            height=athlete_data.get('height'),
            age=athlete_data.get('age'),
            sex=athlete_data.get('sex', 'M'),
            ftp=athlete_data.get('ftp'),
            lthr=athlete_data.get('lthr'),
            max_hr=athlete_data.get('maxHr'),
            resting_hr=athlete_data.get('restingHr'),
            vo2max=athlete_data.get('vo2max')
        )
    
    def get_training_metrics(self) -> TrainingMetrics:
        """获取训练指标"""
        summary = self.client.get_athlete_summary() or {}
        
        return TrainingMetrics(
            ctl=summary.get('fitness', 0),
            atl=summary.get('fatigue', 0),
            tsb=summary.get('form', 0),
            ramp_rate=summary.get('rampRate', 0)
        )
    
    def get_wellness_metrics(self, date: str = None) -> WellnessMetrics:
        """获取健康指标"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        wellness = self.client.get_wellness(date) or {}
        
        return WellnessMetrics(
            hrv=wellness.get('hrv'),
            resting_hr=wellness.get('restingHR'),
            sleep_secs=wellness.get('sleepSecs'),
            sleep_score=wellness.get('sleepScore'),
            weight=wellness.get('weight'),
            steps=wellness.get('steps'),
            calories=wellness.get('kcalConsumed'),
            protein=wellness.get('protein'),
            carbs=wellness.get('carbohydrates'),
            fat=wellness.get('fatTotal')
        )
    
    def get_activities(self, days: int = 7) -> List[ActivityAnalysis]:
        """获取活动分析"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        activities = self.client.get_activities(start_date, end_date) or []
        
        result = []
        for act in activities:
            result.append(ActivityAnalysis(
                id=act.get('id', ''),
                name=act.get('name', 'Unnamed'),
                type=act.get('type', 'Unknown'),
                date=act.get('start_date_local', '')[:10],
                duration=act.get('icu_recording_time') or act.get('moving_time') or 0,
                distance=act.get('distance') or act.get('icu_distance') or 0,
                calories=act.get('calories') or 0,
                training_load=act.get('icu_training_load') or 0,
                avg_hr=act.get('average_heartrate'),
                max_hr=act.get('max_heartrate'),
                elevation=act.get('total_elevation_gain') or 0
            ))
        
        return result
    
    def assess_readiness(self) -> Dict:
        """评估竞技状态准备度"""
        metrics = self.get_training_metrics()
        wellness = self.get_wellness_metrics()
        
        scores = {}
        
        # 1. TSB 评分 (40% 权重)
        tsb_score = self._calculate_tsb_score(metrics.tsb)
        scores['tsb'] = {'score': tsb_score, 'weight': 0.4}
        
        # 2. HRV 评分 (20% 权重)
        hrv_score = self._calculate_hrv_score(wellness.hrv)
        scores['hrv'] = {'score': hrv_score, 'weight': 0.2}
        
        # 3. 睡眠评分 (20% 权重)
        sleep_score = self._calculate_sleep_score(wellness.sleep_secs)
        scores['sleep'] = {'score': sleep_score, 'weight': 0.2}
        
        # 4. 静息心率评分 (10% 权重)
        rhr_score = self._calculate_rhr_score(wellness.resting_hr, self.profile.resting_hr)
        scores['rhr'] = {'score': rhr_score, 'weight': 0.1}
        
        # 5. ATL/CTL比率评分 (10% 权重)
        ratio_score = self._calculate_fatigue_ratio_score(metrics.atl, metrics.ctl)
        scores['ratio'] = {'score': ratio_score, 'weight': 0.1}
        
        # 计算总分
        total_score = sum(item['score'] * item['weight'] for item in scores.values())
        
        return {
            'total_score': total_score,
            'scores': scores,
            'readiness_level': self._get_readiness_level(total_score),
            'recommendation': self._get_readiness_recommendation(total_score, metrics, wellness)
        }
    
    def _calculate_tsb_score(self, tsb: float) -> float:
        """计算 TSB 评分 (0-100)"""
        if tsb > self.thresholds.TSB_OPTIMAL[1]:
            return 100
        elif tsb > self.thresholds.TSB_OPTIMAL[0]:
            return 90 + 10 * (tsb - self.thresholds.TSB_OPTIMAL[0]) / (self.thresholds.TSB_OPTIMAL[1] - self.thresholds.TSB_OPTIMAL[0])
        elif tsb > self.thresholds.TSB_FRESH[0]:
            return 70 + 20 * (tsb - self.thresholds.TSB_FRESH[0]) / (self.thresholds.TSB_OPTIMAL[0] - self.thresholds.TSB_FRESH[0])
        elif tsb > self.thresholds.TSB_FATIGUED[0]:
            return 40 + 30 * (tsb - self.thresholds.TSB_FATIGUED[0]) / (self.thresholds.TSB_FRESH[0] - self.thresholds.TSB_FATIGUED[0])
        elif tsb > self.thresholds.TSB_EXHAUSTED[0]:
            return 10 + 30 * (tsb - self.thresholds.TSB_EXHAUSTED[0]) / (self.thresholds.TSB_FATIGUED[0] - self.thresholds.TSB_EXHAUSTED[0])
        else:
            return 0
    
    def _calculate_hrv_score(self, hrv: Optional[float]) -> float:
        """计算 HRV 评分"""
        if hrv is None:
            return 50  # 无数据
        
        if hrv >= self.thresholds.HRV_EXCELLENT:
            return 100
        elif hrv >= self.thresholds.HRV_GOOD:
            return 70 + 30 * (hrv - self.thresholds.HRV_GOOD) / (self.thresholds.HRV_EXCELLENT - self.thresholds.HRV_GOOD)
        elif hrv >= self.thresholds.HRV_FAIR:
            return 40 + 30 * (hrv - self.thresholds.HRV_FAIR) / (self.thresholds.HRV_GOOD - self.thresholds.HRV_FAIR)
        elif hrv >= self.thresholds.HRV_POOR:
            return 20 + 20 * (hrv - self.thresholds.HRV_POOR) / (self.thresholds.HRV_FAIR - self.thresholds.HRV_POOR)
        else:
            return max(0, 20 * hrv / self.thresholds.HRV_POOR)
    
    def _calculate_sleep_score(self, sleep_secs: Optional[int]) -> float:
        """计算睡眠评分"""
        if sleep_secs is None:
            return 50
        
        sleep_hrs = sleep_secs / 3600
        
        if sleep_hrs >= self.thresholds.SLEEP_OPTIMAL[1]:
            return 100
        elif sleep_hrs >= self.thresholds.SLEEP_OPTIMAL[0]:
            return 90 + 10 * (sleep_hrs - self.thresholds.SLEEP_OPTIMAL[0]) / (self.thresholds.SLEEP_OPTIMAL[1] - self.thresholds.SLEEP_OPTIMAL[0])
        elif sleep_hrs >= self.thresholds.SLEEP_MINIMUM:
            return 60 + 30 * (sleep_hrs - self.thresholds.SLEEP_MINIMUM) / (self.thresholds.SLEEP_OPTIMAL[0] - self.thresholds.SLEEP_MINIMUM)
        elif sleep_hrs >= self.thresholds.SLEEP_DEPRIVATION:
            return 30 + 30 * (sleep_hrs - self.thresholds.SLEEP_DEPRIVATION) / (self.thresholds.SLEEP_MINIMUM - self.thresholds.SLEEP_DEPRIVATION)
        else:
            return max(0, 30 * sleep_hrs / self.thresholds.SLEEP_DEPRIVATION)
    
    def _calculate_rhr_score(self, current_rhr: Optional[float], baseline_rhr: Optional[float]) -> float:
        """计算静息心率评分"""
        if current_rhr is None:
            return 50
        
        # 如果没有基准值，用当前值作为基准
        baseline = baseline_rhr or current_rhr
        
        # 静息心率越低越好，升高表示疲劳
        delta = current_rhr - baseline
        
        if delta <= -2:
            return 100  # 比基准低，状态好
        elif delta <= 0:
            return 90 + 10 * (delta + 2) / 2
        elif delta <= 3:
            return 70 + 20 * (0 - delta) / 3
        elif delta <= 7:
            return 40 + 30 * (3 - delta) / 4
        else:
            return max(0, 40 - 10 * (delta - 7))
    
    def _calculate_fatigue_ratio_score(self, atl: float, ctl: float) -> float:
        """计算疲劳比率评分"""
        if ctl <= 0:
            return 50
        
        ratio = atl / ctl
        
        if ratio <= self.thresholds.ATL_CTL_RATIO_FRESH:
            return 100
        elif ratio <= 1.0:
            return 80 + 20 * (ratio - self.thresholds.ATL_CTL_RATIO_FRESH) / (1.0 - self.thresholds.ATL_CTL_RATIO_FRESH)
        elif ratio <= self.thresholds.ATL_CTL_RATIO_FATIGUED:
            return 50 + 30 * (ratio - 1.0) / (self.thresholds.ATL_CTL_RATIO_FATIGUED - 1.0)
        elif ratio <= self.thresholds.ATL_CTL_RATIO_OVERREACH:
            return 20 + 30 * (ratio - self.thresholds.ATL_CTL_RATIO_FATIGUED) / (self.thresholds.ATL_CTL_RATIO_OVERREACH - self.thresholds.ATL_CTL_RATIO_FATIGUED)
        else:
            return max(0, 20 - 20 * (ratio - self.thresholds.ATL_CTL_RATIO_OVERREACH))
    
    def _get_readiness_level(self, score: float) -> str:
        """获取准备度等级"""
        if score >= 90:
            return "🟢 巅峰状态 (Peak)"
        elif score >= 75:
            return "🟡 状态良好 (Good)"
        elif score >= 60:
            return "🟠 轻度疲劳 (Fatigued)"
        elif score >= 40:
            return "🔴 过度疲劳 (Overreached)"
        else:
            return "🟣 力竭状态 (Exhausted)"
    
    def _get_readiness_recommendation(self, score: float, metrics: TrainingMetrics, wellness: WellnessMetrics) -> str:
        """生成准备度建议"""
        if score >= 90:
            return "🔥 巅峰状态！适合高强度训练、比赛或测试个人纪录"
        elif score >= 75:
            return "💪 状态良好，可以进行正常训练，逐步提升强度"
        elif score >= 60:
            return "⚠️ 轻度疲劳，建议中等强度训练，注重恢复"
        elif score >= 40:
            return "🛑 过度疲劳，需要减量训练，增加恢复时间"
        else:
            return "😴 力竭状态！立即停止训练，充分休息 2-3 天"
    
    def predict_performance(self, days: int = 7) -> Dict:
        """预测未来表现（基于 CTL/ATL 模型）"""
        metrics = self.get_training_metrics()
        
        # 简化预测模型
        # CTL 变化 = 当前 CTL * exp(-days/42) + 假设训练负荷 * (1 - exp(-days/42))
        # ATL 变化 = 当前 ATL * exp(-days/7) + 假设训练负荷 * (1 - exp(-days/7))
        
        predictions = []
        for day in range(1, days + 1):
            # 假设每天训练负荷为 20 (中等强度)
            assumed_load = 20
            
            ctl_decay = math.exp(-day / 42)
            atl_decay = math.exp(-day / 7)
            
            pred_ctl = metrics.ctl * ctl_decay + assumed_load * (1 - ctl_decay)
            pred_atl = metrics.atl * atl_decay + assumed_load * (1 - atl_decay)
            pred_tsb = pred_ctl - pred_atl
            
            predictions.append({
                'day': day,
                'ctl': pred_ctl,
                'atl': pred_atl,
                'tsb': pred_tsb,
                'readiness': 'Good' if pred_tsb > 0 else 'Fatigued'
            })
        
        return {
            'current': {
                'ctl': metrics.ctl,
                'atl': metrics.atl,
                'tsb': metrics.tsb
            },
            'predictions': predictions,
            'optimal_training_window': self._find_optimal_window(predictions)
        }
    
    def _find_optimal_window(self, predictions: List[Dict]) -> str:
        """找出最佳训练窗口"""
        for pred in predictions:
            if self.thresholds.TSB_OPTIMAL[0] <= pred['tsb'] <= self.thresholds.TSB_OPTIMAL[1]:
                return f"第{pred['day']}天 (TSB={pred['tsb']:.1f})"
        return "当前 TSB 过低，建议先恢复"
    
    def predict_sport_performance(self, sport_type: str = None, days: int = 14) -> Dict:
        """
        基于运动类型的训练表现预测
        
        Args:
            sport_type: 运动类型 (Tennis, Cycling, Running 等)
            days: 预测天数
        
        Returns:
            表现预测数据
        """
        if sport_type is None:
            # 自动检测主要运动类型
            activities = self.get_activities(30)
            if activities:
                from collections import Counter
                types = [act.type for act in activities]
                sport_type = Counter(types).most_common(1)[0][0]
            else:
                sport_type = "General"
        
        metrics = self.get_training_metrics()
        
        # 不同运动类型的表现预测模型
        sport_models = {
            'Tennis': {
                'peak_tsb': (5, 15),      # 网球最佳 TSB 区间
                'ctl_decay': 42,           # CTL 衰减常数
                'performance_factors': {
                    'tsb_weight': 0.4,
                    'ctl_weight': 0.3,
                    'hrv_weight': 0.2,
                    'sleep_weight': 0.1
                }
            },
            'Cycling': {
                'peak_tsb': (10, 20),
                'ctl_decay': 45,
                'performance_factors': {
                    'tsb_weight': 0.5,
                    'ctl_weight': 0.35,
                    'hrv_weight': 0.1,
                    'sleep_weight': 0.05
                }
            },
            'Running': {
                'peak_tsb': (5, 15),
                'ctl_decay': 40,
                'performance_factors': {
                    'tsb_weight': 0.45,
                    'ctl_weight': 0.3,
                    'hrv_weight': 0.15,
                    'sleep_weight': 0.1
                }
            },
            'Workout': {
                'peak_tsb': (0, 10),
                'ctl_decay': 35,
                'performance_factors': {
                    'tsb_weight': 0.35,
                    'ctl_weight': 0.25,
                    'hrv_weight': 0.25,
                    'sleep_weight': 0.15
                }
            },
            'General': {
                'peak_tsb': (5, 15),
                'ctl_decay': 42,
                'performance_factors': {
                    'tsb_weight': 0.4,
                    'ctl_weight': 0.3,
                    'hrv_weight': 0.2,
                    'sleep_weight': 0.1
                }
            }
        }
        
        model = sport_models.get(sport_type, sport_models['General'])
        wellness = self.get_wellness_metrics()
        
        predictions = []
        for day in range(1, days + 1):
            # 预测 CTL/ATL/TSB
            ctl_decay = math.exp(-day / model['ctl_decay'])
            atl_decay = math.exp(-day / 7)
            
            assumed_load = 20  # 假设中等强度训练
            pred_ctl = metrics.ctl * ctl_decay + assumed_load * (1 - ctl_decay)
            pred_atl = metrics.atl * atl_decay + assumed_load * (1 - atl_decay)
            pred_tsb = pred_ctl - pred_atl
            
            # 计算表现评分 (0-100)
            tsb_score = self._calculate_performance_tsb_score(pred_tsb, model['peak_tsb'])
            hrv_score = self._calculate_hrv_score(wellness.hrv) if wellness.hrv else 50
            sleep_score = self._calculate_sleep_score(wellness.sleep_secs) if wellness.sleep_secs else 50
            
            perf_score = (
                tsb_score * model['performance_factors']['tsb_weight'] +
                min(100, metrics.ctl * 2) * model['performance_factors']['ctl_weight'] +  # CTL 贡献
                hrv_score * model['performance_factors']['hrv_weight'] +
                sleep_score * model['performance_factors']['sleep_weight']
            )
            
            predictions.append({
                'day': day,
                'ctl': pred_ctl,
                'atl': pred_atl,
                'tsb': pred_tsb,
                'performance_score': perf_score,
                'level': self._get_performance_level(perf_score)
            })
        
        return {
            'sport_type': sport_type,
            'current': {
                'ctl': metrics.ctl,
                'atl': metrics.atl,
                'tsb': metrics.tsb,
                'performance_score': self._calculate_performance_tsb_score(metrics.tsb, model['peak_tsb'])
            },
            'predictions': predictions,
            'peak_performance_window': self._find_peak_window(predictions, model['peak_tsb'])
        }
    
    def _calculate_performance_tsb_score(self, tsb: float, peak_range: tuple) -> float:
        """计算基于 TSB 的表现评分"""
        optimal_min, optimal_max = peak_range
        
        if optimal_min <= tsb <= optimal_max:
            return 100
        elif tsb > optimal_max:
            return max(0, 100 - 5 * (tsb - optimal_max))
        elif tsb > 0:
            return 70 + 30 * (tsb - 0) / (optimal_min - 0)
        elif tsb > -10:
            return 40 + 30 * (tsb + 10) / 10
        elif tsb > -20:
            return 20 + 20 * (tsb + 20) / 10
        else:
            return max(0, 20 + tsb)
    
    def _get_performance_level(self, score: float) -> str:
        """获取表现水平等级"""
        if score >= 90:
            return "🟢 巅峰状态"
        elif score >= 75:
            return "🟡 优秀"
        elif score >= 60:
            return "🟠 良好"
        elif score >= 40:
            return "🔴 一般"
        else:
            return "🟣 较差"
    
    def _find_peak_window(self, predictions: List[Dict], peak_range: tuple) -> str:
        """找出最佳表现窗口"""
        for pred in predictions:
            if pred['tsb'] >= peak_range[0] and pred['tsb'] <= peak_range[1]:
                return f"第{pred['day']}天 (TSB={pred['tsb']:.1f}, 表现{pred['performance_score']:.0f}分)"
        
        # 如果没有最佳窗口，找最接近的
        best = min(predictions, key=lambda p: abs(p['tsb'] - peak_range[0]))
        return f"第{best['day']}天 (接近最佳，TSB={best['tsb']:.1f})"
    
    def generate_training_plan(self, days: int = 7, goal: str = None) -> Dict:
        """
        生成近期训练计划
        
        Args:
            days: 计划天数
            goal: 训练目标 (recover, maintain, build, peak)
        
        Returns:
            训练计划
        """
        metrics = self.get_training_metrics()
        readiness = self.assess_readiness()
        
        # 根据当前状态自动选择目标
        if goal is None:
            if metrics.tsb < -20:
                goal = 'recover'
            elif metrics.tsb < -10:
                goal = 'active_recovery'
            elif metrics.tsb < 0:
                goal = 'maintain'
            elif metrics.tsb < 10:
                goal = 'build'
            else:
                goal = 'peak'
        
        # 不同目标的训练计划模板
        plan_templates = {
            'recover': {
                'description': '恢复期训练计划',
                'weekly_load': 50,  # 周训练负荷
                'sessions': [
                    {'day': 1, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '完全休息'},
                    {'day': 2, 'type': 'Active Recovery', 'duration': 30, 'intensity': 'Z1', 'description': '轻度活动（散步/拉伸）'},
                    {'day': 3, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '完全休息'},
                    {'day': 4, 'type': 'Easy', 'duration': 45, 'intensity': 'Z1-Z2', 'description': '低强度有氧'},
                    {'day': 5, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '完全休息'},
                    {'day': 6, 'type': 'Easy', 'duration': 60, 'intensity': 'Z2', 'description': '中等有氧'},
                    {'day': 7, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '完全休息'},
                ]
            },
            'active_recovery': {
                'description': '主动恢复训练计划',
                'weekly_load': 80,
                'sessions': [
                    {'day': 1, 'type': 'Easy', 'duration': 45, 'intensity': 'Z1-Z2', 'description': '低强度恢复'},
                    {'day': 2, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                    {'day': 3, 'type': 'Easy', 'duration': 60, 'intensity': 'Z2', 'description': '有氧基础'},
                    {'day': 4, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                    {'day': 5, 'type': 'Moderate', 'duration': 60, 'intensity': 'Z2-Z3', 'description': '中等强度'},
                    {'day': 6, 'type': 'Easy', 'duration': 45, 'intensity': 'Z1-Z2', 'description': '轻松活动'},
                    {'day': 7, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                ]
            },
            'maintain': {
                'description': '维持期训练计划',
                'weekly_load': 120,
                'sessions': [
                    {'day': 1, 'type': 'Moderate', 'duration': 60, 'intensity': 'Z2-Z3', 'description': '中等强度有氧'},
                    {'day': 2, 'type': 'Intervals', 'duration': 45, 'intensity': 'Z3-Z4', 'description': '间歇训练'},
                    {'day': 3, 'type': 'Easy', 'duration': 45, 'intensity': 'Z1-Z2', 'description': '恢复性训练'},
                    {'day': 4, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                    {'day': 5, 'type': 'Moderate', 'duration': 75, 'intensity': 'Z2-Z3', 'description': '节奏训练'},
                    {'day': 6, 'type': 'Sport Specific', 'duration': 90, 'intensity': 'Z2-Z4', 'description': '专项训练'},
                    {'day': 7, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                ]
            },
            'build': {
                'description': '增能期训练计划',
                'weekly_load': 180,
                'sessions': [
                    {'day': 1, 'type': 'Threshold', 'duration': 75, 'intensity': 'Z3-Z4', 'description': '阈值训练'},
                    {'day': 2, 'type': 'Intervals', 'duration': 60, 'intensity': 'Z4-Z5', 'description': '高强度间歇'},
                    {'day': 3, 'type': 'Easy', 'duration': 45, 'intensity': 'Z1-Z2', 'description': '主动恢复'},
                    {'day': 4, 'type': 'Tempo', 'duration': 90, 'intensity': 'Z3', 'description': '节奏训练'},
                    {'day': 5, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                    {'day': 6, 'type': 'Long', 'duration': 120, 'intensity': 'Z2-Z3', 'description': '长距离有氧'},
                    {'day': 7, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                ]
            },
            'peak': {
                'description': '巅峰期训练计划',
                'weekly_load': 150,  # 减量
                'sessions': [
                    {'day': 1, 'type': 'Sharpening', 'duration': 60, 'intensity': 'Z3-Z4', 'description': '强度保持'},
                    {'day': 2, 'type': 'Intervals', 'duration': 45, 'intensity': 'Z4', 'description': '短间歇'},
                    {'day': 3, 'type': 'Easy', 'duration': 30, 'intensity': 'Z1', 'description': '轻松活动'},
                    {'day': 4, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                    {'day': 5, 'type': 'Activation', 'duration': 30, 'intensity': 'Z2-Z3', 'description': '激活训练'},
                    {'day': 6, 'type': 'Race/Test', 'duration': 0, 'intensity': 'Race', 'description': '比赛/测试'},
                    {'day': 7, 'type': 'Rest', 'duration': 0, 'intensity': 'N/A', 'description': '休息'},
                ]
            }
        }
        
        template = plan_templates.get(goal, plan_templates['maintain'])
        
        # 根据运动类型调整
        activities = self.get_activities(30)
        if activities:
            from collections import Counter
            primary_sport = Counter([act.type for act in activities]).most_common(1)[0][0]
            
            # 调整训练描述
            for session in template['sessions']:
                if session['type'] == 'Sport Specific':
                    session['description'] = f'{primary_sport} 专项训练'
                elif session['type'] == 'Race/Test':
                    session['description'] = f'{primary_sport} 测试/比赛'
        
        return {
            'goal': goal,
            'plan': template,
            'rationale': self._get_plan_rationale(goal, metrics, readiness)
        }
    
    def _get_plan_rationale(self, goal: str, metrics: TrainingMetrics, readiness: Dict) -> str:
        """解释训练计划的理由"""
        rationales = {
            'recover': f'当前 TSB={metrics.tsb:.1f}，处于过度疲劳状态。需要完全恢复，避免过度训练风险。',
            'active_recovery': f'当前 TSB={metrics.tsb:.1f}，轻度疲劳。主动恢复有助于加速恢复过程。',
            'maintain': f'当前 TSB={metrics.tsb:.1f}，状态稳定。维持当前训练量，避免退步。',
            'build': f'当前 TSB={metrics.tsb:.1f}，状态良好。可以逐步增加训练负荷，提升体能。',
            'peak': f'当前 TSB={metrics.tsb:.1f}，接近最佳状态。减量训练，准备比赛/测试。'
        }
        return rationales.get(goal, '根据当前状态生成的训练计划')
    
    def calculate_nutrition_targets(self, goal: str = None) -> Dict:
        """
        计算营养摄入目标
        
        Args:
            goal: 目标类型 (fat_loss, muscle_gain, maintenance, endurance)
        
        Returns:
            营养目标数据
        """
        wellness = self.get_wellness_metrics()
        
        # 获取用户数据
        weight = self.profile.weight or wellness.weight or 75  # 默认 75kg
        height = self.profile.height or 175  # 默认 175cm
        age = self.profile.age or 30  # 默认 30 岁
        sex = self.profile.sex or 'M'
        
        # 计算 BMR (Mifflin-St Jeor 公式)
        if sex == 'M':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # 根据活动水平计算 TDEE
        metrics = self.get_training_metrics()
        activity_multiplier = 1.2  # 久坐
        if metrics.ctl > 50:
            activity_multiplier = 1.55  # 中等活动
        elif metrics.ctl > 80:
            activity_multiplier = 1.725  # 高活动
        elif metrics.ctl > 100:
            activity_multiplier = 1.9  # 极高活动
        
        tdee = bmr * activity_multiplier
        
        # 根据目标调整
        if goal is None:
            # 根据体型自动推荐
            bmi = weight / ((height/100) ** 2)
            if bmi > 25:
                goal = UserGoal.FAT_LOSS
            else:
                goal = UserGoal.MAINTENANCE
        
        nutrition_configs = {
            UserGoal.FAT_LOSS: ProfessionalThresholds.NUTRITION_FAT_LOSS,
            UserGoal.MUSCLE_GAIN: ProfessionalThresholds.NUTRITION_MUSCLE_GAIN,
            UserGoal.MAINTENANCE: ProfessionalThresholds.NUTRITION_MAINTENANCE,
            UserGoal.ENDURANCE: ProfessionalThresholds.NUTRITION_ENDURANCE,
        }
        
        config = nutrition_configs.get(goal, ProfessionalThresholds.NUTRITION_MAINTENANCE)
        
        # 计算目标热量
        if 'calorie_deficit' in config:
            target_calories = tdee - config['calorie_deficit']
        elif 'calorie_surplus' in config:
            target_calories = tdee + config['calorie_surplus']
        else:
            target_calories = tdee
        
        # 计算宏量营养素
        protein_g = config['protein_g_per_kg'] * weight
        protein_calories = protein_g * 4
        
        fat_ratio = config.get('fat_ratio', 0.30)
        fat_calories = target_calories * fat_ratio
        fat_g = fat_calories / 9
        
        carbs_ratio = config.get('carbs_ratio', 1 - config['protein_g_per_kg'] * 4 / target_calories - fat_ratio)
        carbs_calories = target_calories * carbs_ratio
        carbs_g = carbs_calories / 4
        
        return {
            'goal': goal,
            'bmr': bmr,
            'tdee': tdee,
            'target_calories': target_calories,
            'protein': {
                'grams': protein_g,
                'calories': protein_calories,
                'ratio': protein_calories / target_calories
            },
            'carbs': {
                'grams': carbs_g,
                'calories': carbs_calories,
                'ratio': carbs_ratio
            },
            'fat': {
                'grams': fat_g,
                'calories': fat_calories,
                'ratio': fat_ratio
            },
            'comparison': self._compare_with_current_intake(wellness, target_calories, protein_g, carbs_g, fat_g)
        }
    
    def _compare_with_current_intake(self, wellness: WellnessMetrics, target_cal: float, target_protein: float, target_carbs: float, target_fat: float) -> Dict:
        """比较当前摄入与目标"""
        current_cal = wellness.calories or 0
        current_protein = wellness.protein or 0
        current_carbs = wellness.carbs or 0
        current_fat = wellness.fat or 0
        
        return {
            'calories': {
                'current': current_cal,
                'target': target_cal,
                'difference': current_cal - target_cal,
                'status': '✅' if abs(current_cal - target_cal) < 200 else '⚠️' if abs(current_cal - target_cal) < 500 else '❌'
            },
            'protein': {
                'current': current_protein,
                'target': target_protein,
                'difference': current_protein - target_protein,
                'status': '✅' if abs(current_protein - target_protein) < 20 else '⚠️' if abs(current_protein - target_protein) < 40 else '❌'
            },
            'carbs': {
                'current': current_carbs,
                'target': target_carbs,
                'difference': current_carbs - target_carbs,
                'status': '✅' if abs(current_carbs - target_carbs) < 30 else '⚠️' if abs(current_carbs - target_carbs) < 60 else '❌'
            },
            'fat': {
                'current': current_fat,
                'target': target_fat,
                'difference': current_fat - target_fat,
                'status': '✅' if abs(current_fat - target_fat) < 15 else '⚠️' if abs(current_fat - target_fat) < 30 else '❌'
            }
        }
    
    def generate_report(self, include_prediction: bool = True, include_plan: bool = True, include_nutrition: bool = True) -> str:
        """生成完整分析报告"""
        metrics = self.get_training_metrics()
        wellness = self.get_wellness_metrics()
        readiness = self.assess_readiness()
        prediction = self.predict_performance(7) if include_prediction else None
        activities = self.get_activities(7)
        
        report = []
        report.append("\n" + "="*60)
        report.append("🏆 职业运动员级别身体状态分析报告")
        report.append(f"运动员：{self.profile.name} | {self.profile.athlete_id}")
        report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("="*60 + "\n")
        
        # 1. 竞技状态准备度
        report.append("═══════ 📊 竞技状态准备度 ═══")
        report.append(f"综合评分：{readiness['total_score']:.1f}/100")
        report.append(f"状态等级：{readiness['readiness_level']}")
        report.append(f"训练建议：{readiness['recommendation']}")
        report.append("")
        
        # 详细评分
        report.append("详细评分:")
        report.append(f"  TSB 状态：   {readiness['scores']['tsb']['score']:.0f}/100 (权重 40%)")
        report.append(f"  HRV 恢复：   {readiness['scores']['hrv']['score']:.0f}/100 (权重 20%)")
        report.append(f"  睡眠质量：   {readiness['scores']['sleep']['score']:.0f}/100 (权重 20%)")
        report.append(f"  静息心率：   {readiness['scores']['rhr']['score']:.0f}/100 (权重 10%)")
        report.append(f"  疲劳比率：   {readiness['scores']['ratio']['score']:.0f}/100 (权重 10%)")
        report.append("")
        
        # 2. 训练负荷分析
        report.append("═══════ 🏋️ 训练负荷分析 ═══")
        report.append(f"CTL (体能):    {metrics.ctl:.1f} 小时")
        report.append(f"ATL (疲劳):    {metrics.atl:.1f} 小时")
        report.append(f"TSB (状态):    {metrics.tsb:.1f}")
        report.append(f"Ramp Rate:     {metrics.ramp_rate:.4f}")
        report.append(f"ATL/CTL 比率：  {metrics.atl/metrics.ctl:.2f}" if metrics.ctl > 0 else "ATL/CTL 比率：N/A")
        report.append("")
        
        # 3. 恢复指标
        report.append("═══════ 💤 恢复指标 ═══")
        if wellness.hrv:
            hrv_status = "优秀" if wellness.hrv >= 60 else "一般" if wellness.hrv >= 40 else "较差"
            report.append(f"HRV:           {wellness.hrv:.1f} ms ({hrv_status})")
        if wellness.resting_hr:
            report.append(f"静息心率：     {wellness.resting_hr} bpm")
        if wellness.sleep_secs:
            sleep_hrs = wellness.sleep_secs / 3600
            sleep_status = "充足" if sleep_hrs >= 8 else "不足" if sleep_hrs < 7 else "一般"
            report.append(f"睡眠：         {sleep_hrs:.1f} 小时 ({sleep_status})")
        report.append("")
        
        # 4. 营养摄入
        report.append("═══════ 🍽️ 营养摄入 (今日) ═══")
        if wellness.calories:
            report.append(f"热量：         {wellness.calories:.0f} kcal")
        if wellness.protein:
            # 按体重计算蛋白质需求 (运动员 1.6-2.2g/kg)
            protein_per_kg = wellness.protein / self.profile.weight if self.profile.weight else 0
            report.append(f"蛋白质：       {wellness.protein:.1f}g ({protein_per_kg:.1f}g/kg)")
        if wellness.carbs:
            report.append(f"碳水：         {wellness.carbs:.1f}g")
        if wellness.fat:
            report.append(f"脂肪：         {wellness.fat:.1f}g")
        report.append("")
        
        # 5. 近期训练
        report.append("═══════ 🏃 近 7 天训练 ═══")
        total_load = sum(act.training_load for act in activities)
        total_duration = sum(act.duration for act in activities)
        total_calories = sum(act.calories for act in activities)
        
        report.append(f"训练次数：     {len(activities)} 次")
        report.append(f"总训练负荷：   {total_load}")
        report.append(f"总训练时间：   {total_duration/3600:.2f} 小时")
        report.append(f"总消耗热量：   {total_calories:.0f} kcal")
        report.append("")
        
        if activities:
            report.append("训练详情:")
            for act in activities[-5:]:
                duration_min = act.duration / 60
                report.append(f"  [{act.date}] {act.name}")
                report.append(f"           {duration_min:.0f}分钟 | 负荷{act.training_load} | {act.calories:.0f}kcal")
        report.append("")
        
        # 6. 表现预测
        report.append("═══════ 🔮 未来 7 天预测 ═══")
        report.append(f"当前 TSB:      {prediction['current']['tsb']:.1f}")
        report.append(f"最佳训练窗口：{prediction['optimal_training_window']}")
        report.append("")
        
        report.append("TSB 趋势预测:")
        for pred in prediction['predictions'][:5]:  # 显示前 5 天
            status_icon = "🟢" if pred['tsb'] > 0 else "🔴"
            report.append(f"  第{pred['day']}天：{status_icon} TSB={pred['tsb']:.1f}")
        report.append("")
        
        # 7. 综合建议
        report.append("═══════ 💡 综合建议 ═══")
        
        # 基于 TSB 的训练强度建议
        if metrics.tsb > 10:
            report.append("📈 训练强度：可以进行高强度间歇训练、阈值训练")
        elif metrics.tsb > 0:
            report.append("📊 训练强度：中等强度有氧训练，混合一些高强度")
        elif metrics.tsb > -10:
            report.append("📉 训练强度：低强度恢复训练，避免高强度")
        else:
            report.append("🛑 训练强度：完全休息或主动恢复（散步、拉伸）")
        
        # 基于睡眠的恢复建议
        if wellness.sleep_secs and wellness.sleep_secs < 7*3600:
            report.append("😴 恢复建议：今晚务必保证 8 小时以上睡眠")
        
        # 基于营养的建议
        if wellness.protein and self.profile.weight:
            protein_per_kg = wellness.protein / self.profile.weight
            if protein_per_kg < 1.6:
                report.append(f"🍗 营养建议：增加蛋白质摄入至 {1.6*self.profile.weight:.0f}g/天 (当前{protein_per_kg:.1f}g/kg)")
        
        report.append("")
        report.append("="*60)
        
        # 8. 运动表现预测（新功能 1）
        if include_prediction:
            report.append("\n═══════ 📈 运动表现预测 ═══")
            sport_pred = self.predict_sport_performance(days=7)
            report.append(f"主要运动：{sport_pred['sport_type']}")
            report.append(f"当前表现评分：{sport_pred['current']['performance_score']:.0f}/100 ({self._get_performance_level(sport_pred['current']['performance_score'])})")
            report.append(f"最佳表现窗口：{sport_pred['peak_performance_window']}")
            report.append("")
            report.append("未来 7 天表现趋势:")
            for pred in sport_pred['predictions'][:5]:
                icon = "🟢" if pred['performance_score'] >= 75 else "🟡" if pred['performance_score'] >= 60 else "🔴"
                report.append(f"  第{pred['day']}天：{icon} {pred['level']} ({pred['performance_score']:.0f}分) TSB={pred['tsb']:.1f}")
            report.append("")
        
        # 9. 训练计划推荐（新功能 2）
        if include_plan:
            report.append("\n═══════ 📋 推荐训练计划 ═══")
            training_plan = self.generate_training_plan(days=7)
            report.append(f"计划目标：{training_plan['goal']} - {training_plan['plan']['description']}")
            report.append(f"周训练负荷：{training_plan['plan']['weekly_load']}")
            report.append(f"制定理由：{training_plan['rationale']}")
            report.append("")
            report.append("每日安排:")
            for session in training_plan['plan']['sessions']:
                if session['duration'] > 0:
                    report.append(f"  第{session['day']}天：{session['type']} - {session['duration']}分钟 ({session['intensity']})")
                    report.append(f"           {session['description']}")
                else:
                    report.append(f"  第{session['day']}天：{session['type']} - {session['description']}")
            report.append("")
        
        # 10. 营养摄入目标（新功能 3）
        if include_nutrition:
            report.append("\n═══════ 🍽️ 营养摄入目标 ═══")
            
            # 根据用户情况自动选择目标
            wellness = self.get_wellness_metrics()
            weight = self.profile.weight or wellness.weight or 75
            bmi = weight / ((1.75) ** 2)  # 假设身高 175cm
            
            if bmi > 24:
                goal = UserGoal.FAT_LOSS
                goal_name = "减脂"
            else:
                goal = UserGoal.MAINTENANCE
                goal_name = "维持"
            
            nutrition = self.calculate_nutrition_targets(goal)
            
            report.append(f"目标：{goal_name}")
            report.append(f"BMR (基础代谢): {nutrition['bmr']:.0f} kcal")
            report.append(f"TDEE (每日消耗): {nutrition['tdee']:.0f} kcal")
            report.append(f"目标热量：{nutrition['target_calories']:.0f} kcal/天")
            report.append("")
            report.append("宏量营养素目标:")
            report.append(f"  蛋白质：{nutrition['protein']['grams']:.0f}g ({nutrition['protein']['calories']:.0f}kcal, {nutrition['protein']['ratio']*100:.0f}%)")
            report.append(f"  碳水：  {nutrition['carbs']['grams']:.0f}g ({nutrition['carbs']['calories']:.0f}kcal, {nutrition['carbs']['ratio']*100:.0f}%)")
            report.append(f"  脂肪：  {nutrition['fat']['grams']:.0f}g ({nutrition['fat']['calories']:.0f}kcal, {nutrition['fat']['ratio']*100:.0f}%)")
            report.append("")
            
            # 比较当前摄入
            if wellness.calories or wellness.protein:
                report.append("当前摄入 vs 目标:")
                comp = nutrition['comparison']
                report.append(f"  热量：  {comp['calories']['current']:.0f} / {comp['calories']['target']:.0f} kcal {comp['calories']['status']} ({comp['calories']['difference']:+.0f})")
                report.append(f"  蛋白质：{comp['protein']['current']:.1f} / {comp['protein']['target']:.1f}g {comp['protein']['status']} ({comp['protein']['difference']:+.1f})")
                report.append(f"  碳水：  {comp['carbs']['current']:.1f} / {comp['carbs']['target']:.1f}g {comp['carbs']['status']} ({comp['carbs']['difference']:+.1f})")
                report.append(f"  脂肪：  {comp['fat']['current']:.1f} / {comp['fat']['target']:.1f}g {comp['fat']['status']} ({comp['fat']['difference']:+.1f})")
                report.append("")
                report.append("图例：✅ 达标  ⚠️ 接近  ❌ 不足/过量")
            report.append("")
        
        report.append("="*60)
        report.append("报告生成完毕")
        report.append("="*60 + "\n")
        
        return "\n".join(report)

# ================= 主程序 =================
def main():
    """主程序入口"""
    client = create_client()
    if not client:
        print("❌ 无法创建 API 客户端")
        sys.exit(1)
    
    analytics = ProAthleteAnalytics(client)
    report = analytics.generate_report()
    print(report)

if __name__ == "__main__":
    main()
