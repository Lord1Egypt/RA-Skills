"""
Drift Detection
P2: Input distribution, hit rate, residual drift monitoring
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone
from scipy import stats

# ============ Configuration ============
DRIFT_THRESHOLD_PSI = 0.2  # Population Stability Index threshold
DRIFT_THRESHOLD_KL = 0.1  # KL Divergence threshold
ALERT_ON_CONSECUTIVE = 3  # Alert after N consecutive drifts


@dataclass
class DriftReport:
    """漂移报告"""
    timestamp: str
    feature_name: str
    drift_detected: bool
    drift_type: str  # input/performance/structural
    metric_name: str
    current_value: float
    baseline_value: float
    drift_percentage: float
    severity: str  # low/moderate/high/critical
    consecutive_count: int
    recommendation: str


class DriftDetector:
    """漂移检测器"""
    
    def __init__(
        self,
        baseline_window: int = 100,
        monitoring_window: int = 50,
        alert_threshold: float = DRIFT_THRESHOLD_PSI
    ):
        self.baseline_window = baseline_window
        self.monitoring_window = monitoring_window
        self.alert_threshold = alert_threshold
        
        # Baseline statistics
        self.baseline_stats: Dict[str, Dict] = {}
        
        # Monitoring history
        self.drift_history: List[DriftReport] = []
        self.consecutive_drifts: Dict[str, int] = {}
    
    def compute_psi(
        self,
        expected: np.ndarray,
        actual: np.ndarray,
        buckets: int = 10
    ) -> float:
        """
        计算 Population Stability Index (PSI)
        
        PSI < 0.1: No significant change
        PSI 0.1-0.2: Significant change, monitor
        PSI > 0.2: Major change, alert
        """
        # Create buckets
        breakpoints = np.linspace(expected.min(), expected.max(), buckets + 1)
        
        expected_counts = np.histogram(expected, breakpoints=breakpoints)[0]
        actual_counts = np.histogram(actual, breakpoints=breakpoints)[0]
        
        # Avoid division by zero
        expected_counts = np.where(expected_counts == 0, 1, expected_counts)
        actual_counts = np.where(actual_counts == 0, 1, actual_counts)
        
        # Normalize
        expected_pct = expected_counts / expected_counts.sum()
        actual_pct = actual_counts / actual_counts.sum()
        
        # Calculate PSI
        psi = np.sum(
            (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
        )
        
        return psi
    
    def compute_kl_divergence(
        self,
        expected: np.ndarray,
        actual: np.ndarray
    ) -> float:
        """
        计算 KL Divergence
        """
        # Bin the data
        bins = 20
        expected_bins = np.histogram(expected, bins=bins, density=True)[0]
        actual_bins = np.histogram(actual, bins=bins, density=True)[0]
        
        # Avoid log(0)
        expected_bins = np.where(expected_bins == 0, 1e-6, expected_bins)
        actual_bins = np.where(actual_bins == 0, 1e-6, actual_bins)
        
        # Normalize
        expected_bins = expected_bins / expected_bins.sum()
        actual_bins = actual_bins / actual_bins.sum()
        
        return np.sum(expected_bins * np.log(expected_bins / actual_bins))
    
    def compute_distribution_stats(self, data: np.ndarray) -> Dict[str, float]:
        """计算分布统计"""
        return {
            "mean": float(np.mean(data)),
            "std": float(np.std(data)),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "median": float(np.median(data)),
            "q25": float(np.percentile(data, 25)),
            "q75": float(np.percentile(data, 75)),
            "skewness": float(stats.skew(data)),
            "kurtosis": float(stats.kurtosis(data))
        }
    
    def set_baseline(self, feature_name: str, data: np.ndarray):
        """设置基准分布"""
        self.baseline_stats[feature_name] = {
            "data": data,
            "stats": self.compute_distribution_stats(data),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sample_size": len(data)
        }
        
        if feature_name not in self.consecutive_drifts:
            self.consecutive_drifts[feature_name] = 0
    
    def detect_input_drift(
        self,
        feature_name: str,
        current_data: np.ndarray
    ) -> DriftReport:
        """
        检测输入漂移
        
        Returns:
            DriftReport with drift detection results
        """
        if feature_name not in self.baseline_stats:
            # No baseline, set it
            self.set_baseline(feature_name, current_data)
            return DriftReport(
                timestamp=datetime.now(timezone.utc).isoformat(),
                feature_name=feature_name,
                drift_detected=False,
                drift_type="input",
                metric_name="psi",
                current_value=0.0,
                baseline_value=0.0,
                drift_percentage=0.0,
                severity="none",
                consecutive_count=0,
                recommendation="Baseline established"
            )
        
        baseline = self.baseline_stats[feature_name]
        baseline_data = baseline["data"]
        
        # Use recent window for comparison
        baseline_sample = baseline_data[-self.monitoring_window:] if len(baseline_data) > self.monitoring_window else baseline_data
        current_sample = current_data[-self.monitoring_window:] if len(current_data) > self.monitoring_window else current_data
        
        # Compute PSI
        psi = self.compute_psi(baseline_sample, current_sample)
        
        # Compute KL divergence
        kl = self.compute_kl_divergence(baseline_sample, current_sample)
        
        # Determine drift
        drift_detected = psi > self.alert_threshold or kl > DRIFT_THRESHOLD_KL
        
        # Update consecutive count
        if drift_detected:
            self.consecutive_drifts[feature_name] += 1
        else:
            self.consecutive_drifts[feature_name] = 0
        
        consecutive = self.consecutive_drifts[feature_name]
        
        # Determine severity
        if psi < 0.1:
            severity = "none"
        elif psi < 0.15:
            severity = "low"
        elif psi < 0.2:
            severity = "moderate"
        elif psi < 0.3:
            severity = "high"
        else:
            severity = "critical"
        
        # Generate recommendation
        if severity == "none":
            recommendation = "Distribution stable"
        elif severity in ["low", "moderate"]:
            recommendation = "Monitor closely, consider retraining soon"
        else:
            recommendation = "Alert! Model retraining recommended"
        
        report = DriftReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            feature_name=feature_name,
            drift_detected=drift_detected and consecutive >= ALERT_ON_CONSECUTIVE,
            drift_type="input",
            metric_name="psi",
            current_value=round(psi, 4),
            baseline_value=round(kl, 4),
            drift_percentage=round((psi - 0.1) / 0.1 * 100, 2) if psi > 0.1 else 0.0,
            severity=severity,
            consecutive_count=consecutive,
            recommendation=recommendation
        )
        
        self.drift_history.append(report)
        return report
    
    def detect_performance_drift(
        self,
        metric_name: str,
        historical_values: List[float],
        recent_values: List[float],
        threshold: float = 0.1
    ) -> DriftReport:
        """
        检测性能漂移 (如命中率下降)
        
        Args:
            metric_name: 指标名 (e.g., "hit_rate", "accuracy")
            historical_values: 历史指标值
            recent_values: 最近指标值
            threshold: 下降阈值 (e.g., 0.1 = 10% drop)
        """
        if len(historical_values) < 10 or len(recent_values) < 5:
            return DriftReport(
                timestamp=datetime.now(timezone.utc).isoformat(),
                feature_name=metric_name,
                drift_detected=False,
                drift_type="performance",
                metric_name=metric_name,
                current_value=np.mean(recent_values) if recent_values else 0,
                baseline_value=np.mean(historical_values) if historical_values else 0,
                drift_percentage=0.0,
                severity="none",
                consecutive_count=0,
                recommendation="Insufficient data for drift detection"
            )
        
        # Compute drop
        hist_mean = np.mean(historical_values)
        recent_mean = np.mean(recent_values)
        
        if hist_mean > 0:
            drop_pct = (hist_mean - recent_mean) / hist_mean
        else:
            drop_pct = 0
        
        drift_detected = drop_pct > threshold
        
        # Determine severity
        if drop_pct < 0.05:
            severity = "none"
        elif drop_pct < 0.1:
            severity = "low"
        elif drop_pct < 0.2:
            severity = "moderate"
        elif drop_pct < 0.3:
            severity = "high"
        else:
            severity = "critical"
        
        # Update consecutive
        if drift_detected:
            key = f"perf_{metric_name}"
            self.consecutive_drifts[key] = self.consecutive_drifts.get(key, 0) + 1
            consecutive = self.consecutive_drifts[key]
        else:
            key = f"perf_{metric_name}"
            self.consecutive_drifts[key] = 0
            consecutive = 0
        
        return DriftReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            feature_name=metric_name,
            drift_detected=drift_detected and consecutive >= ALERT_ON_CONSECUTIVE,
            drift_type="performance",
            metric_name=metric_name,
            current_value=round(recent_mean, 4),
            baseline_value=round(hist_mean, 4),
            drift_percentage=round(drop_pct * 100, 2),
            severity=severity,
            consecutive_count=consecutive,
            recommendation="Consider model retraining" if severity in ["high", "critical"] else "Monitor"
        )
    
    def get_drift_summary(self) -> Dict:
        """获取漂移摘要"""
        if not self.drift_history:
            return {"status": "no_data"}
        
        recent = self.drift_history[-10:]  # Last 10 reports
        input_drifts = [r for r in recent if r.drift_type == "input"]
        perf_drifts = [r for r in recent if r.drift_type == "performance"]
        
        return {
            "total_checks": len(self.drift_history),
            "input_drifts_detected": sum(1 for r in input_drifts if r.drift_detected),
            "performance_drifts_detected": sum(1 for r in perf_drifts if r.drift_detected),
            "current_consecutive": dict(self.consecutive_drifts),
            "latest_input_drift": input_drifts[-1].to_dict() if input_drifts else None,
            "latest_perf_drift": perf_drifts[-1].to_dict() if perf_drifts else None
        }
    
    def reset_baseline(self, feature_name: str = None):
        """重置基准"""
        if feature_name:
            if feature_name in self.baseline_stats:
                del self.baseline_stats[feature_name]
            if feature_name in self.consecutive_drifts:
                del self.consecutive_drifts[feature_name]
        else:
            self.baseline_stats.clear()
            self.consecutive_drifts.clear()


class DriftMonitor:
    """漂移监控器 - 便捷封装"""
    
    def __init__(self):
        self.detector = DriftDetector()
        self.input_features = ["close", "vol", "funding_rate", "oi"]
    
    def check_all_inputs(self, data_dict: Dict[str, np.ndarray]) -> List[DriftReport]:
        """检查所有输入特征"""
        reports = []
        for feature, data in data_dict.items():
            if feature in self.input_features:
                report = self.detector.detect_input_drift(feature, data)
                reports.append(report)
        return reports
    
    def check_hit_rate_drift(
        self,
        metric_name: str,
        historical: List[float],
        recent: List[float]
    ) -> DriftReport:
        """检查命中率漂移"""
        return self.detector.detect_performance_drift(metric_name, historical, recent)
    
    def get_status(self) -> Dict:
        """获取监控状态"""
        summary = self.detector.get_drift_summary()
        
        # Overall status
        if summary.get("input_drifts_detected", 0) > 0 or summary.get("performance_drifts_detected", 0) > 0:
            status = "alert"
        else:
            status = "healthy"
        
        return {
            "status": status,
            "details": summary
        }
