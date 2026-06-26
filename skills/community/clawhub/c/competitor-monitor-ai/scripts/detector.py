#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常检测模块
用于检测数据异常波动和爆款
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class AlertLevel(Enum):
    """告警级别"""
    CRITICAL = "critical"  # 严重
    HIGH = "high"          # 高
    MEDIUM = "medium"      # 中
    LOW = "low"            # 低
    INFO = "info"          # 信息


class AlertType(Enum):
    """告警类型"""
    SPIKE = "spike"                    # 数据暴增
    DROP = "drop"                      # 数据骤降
    TREND_UP = "trend_up"              # 持续上升
    TREND_DOWN = "trend_down"          # 持续下降
    BURST = "burst"                    # 爆款检测
    THRESHOLD = "threshold"            # 阈值触发


@dataclass
class Alert:
    """告警对象"""
    task_id: str
    timestamp: str
    level: AlertLevel
    type: AlertType
    metric: str
    message: str
    details: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return {
            'task_id': self.task_id,
            'timestamp': self.timestamp,
            'level': self.level.value,
            'type': self.type.value,
            'metric': self.metric,
            'message': self.message,
            'details': self.details
        }


class AnomalyDetector:
    """异常检测器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化检测器
        
        Args:
            config: 检测配置
        """
        self.config = config or {}
        self.history_data = []
        
    def load_history(self, data: List[Dict]):
        """加载历史数据"""
        self.history_data = sorted(data, key=lambda x: x.get('timestamp', ''))
    
    def detect(self, current_data: Dict[str, Any], task_config: Dict) -> List[Alert]:
        """
        检测异常
        
        Args:
            current_data: 当前数据
            task_config: 任务配置
            
        Returns:
            告警列表
        """
        alerts = []
        task_id = current_data.get('task_id', 'unknown')
        timestamp = current_data.get('timestamp', datetime.now().isoformat())
        
        # 获取阈值配置
        thresholds = task_config.get('alert_threshold', {})
        
        # 对每个指标进行检测
        for metric, current_value in current_data.get('data', {}).items():
            if not isinstance(current_value, (int, float)):
                continue
            
            metric_threshold = thresholds.get(metric, {})
            
            # 1. 增长率检测
            spike_alert = self._detect_spike(
                task_id, timestamp, metric, current_value, metric_threshold
            )
            if spike_alert:
                alerts.append(spike_alert)
            
            # 2. 持续趋势检测
            trend_alert = self._detect_trend(
                task_id, timestamp, metric, current_value, metric_threshold
            )
            if trend_alert:
                alerts.append(trend_alert)
            
            # 3. 绝对值阈值检测
            threshold_alert = self._detect_threshold(
                task_id, timestamp, metric, current_value, metric_threshold
            )
            if threshold_alert:
                alerts.append(threshold_alert)
        
        # 4. 爆款检测（综合多个指标）
        burst_alert = self._detect_burst(
            task_id, timestamp, current_data.get('data', {}), task_config
        )
        if burst_alert:
            alerts.append(burst_alert)
        
        return alerts
    
    def _detect_spike(self, task_id: str, timestamp: str, metric: str,
                      current_value: float, threshold: Dict) -> Optional[Alert]:
        """检测数据暴增/骤降"""
        increase_percent = threshold.get('increase_percent', 50)
        decrease_percent = threshold.get('decrease_percent', 50)
        min_value = threshold.get('min_value', 0)
        window = threshold.get('window', 3)  # 默认取最近3条数据
        
        # 获取历史数据
        if len(self.history_data) < window:
            return None
        
        # 计算历史平均值
        recent_data = self.history_data[-window:]
        historical_values = [
            d.get('data', {}).get(metric) 
            for d in recent_data 
            if d.get('data', {}).get(metric) is not None
        ]
        
        if not historical_values:
            return None
        
        avg_value = sum(historical_values) / len(historical_values)
        
        if avg_value == 0:
            return None
        
        change_percent = ((current_value - avg_value) / avg_value) * 100
        
        # 检测暴增
        if change_percent >= increase_percent and current_value >= min_value:
            return Alert(
                task_id=task_id,
                timestamp=timestamp,
                level=AlertLevel.HIGH if change_percent >= 100 else AlertLevel.MEDIUM,
                type=AlertType.SPIKE,
                metric=metric,
                message=f"{metric} 暴增 {change_percent:.1f}%",
                details={
                    'current': current_value,
                    'average': avg_value,
                    'change_percent': change_percent,
                    'threshold': increase_percent
                }
            )
        
        # 检测骤降
        if change_percent <= -decrease_percent:
            return Alert(
                task_id=task_id,
                timestamp=timestamp,
                level=AlertLevel.MEDIUM,
                type=AlertType.DROP,
                metric=metric,
                message=f"{metric} 骤降 {abs(change_percent):.1f}%",
                details={
                    'current': current_value,
                    'average': avg_value,
                    'change_percent': change_percent,
                    'threshold': decrease_percent
                }
            )
        
        return None
    
    def _detect_trend(self, task_id: str, timestamp: str, metric: str,
                      current_value: float, threshold: Dict) -> Optional[Alert]:
        """检测持续趋势"""
        trend_window = threshold.get('trend_window', 5)
        trend_threshold = threshold.get('trend_threshold', 3)  # 连续几次同向变化
        
        if len(self.history_data) < trend_window:
            return None
        
        # 获取最近的趋势窗口数据
        recent_data = self.history_data[-trend_window:] + [{'data': {metric: current_value}}]
        
        values = [
            d.get('data', {}).get(metric) 
            for d in recent_data 
            if d.get('data', {}).get(metric) is not None
        ]
        
        if len(values) < trend_threshold + 1:
            return None
        
        # 计算变化方向
        directions = []
        for i in range(1, len(values)):
            if values[i] > values[i-1]:
                directions.append(1)  # 上升
            elif values[i] < values[i-1]:
                directions.append(-1)  # 下降
            else:
                directions.append(0)  # 持平
        
        # 检测连续上升
        consecutive_up = 0
        for d in directions:
            if d == 1:
                consecutive_up += 1
                if consecutive_up >= trend_threshold:
                    return Alert(
                        task_id=task_id,
                        timestamp=timestamp,
                        level=AlertLevel.LOW,
                        type=AlertType.TREND_UP,
                        metric=metric,
                        message=f"{metric} 连续 {consecutive_up} 次上升",
                        details={
                            'current': current_value,
                            'consecutive_count': consecutive_up,
                            'values': values[-consecutive_up-1:]
                        }
                    )
            else:
                consecutive_up = 0
        
        # 检测连续下降
        consecutive_down = 0
        for d in directions:
            if d == -1:
                consecutive_down += 1
                if consecutive_down >= trend_threshold:
                    return Alert(
                        task_id=task_id,
                        timestamp=timestamp,
                        level=AlertLevel.LOW,
                        type=AlertType.TREND_DOWN,
                        metric=metric,
                        message=f"{metric} 连续 {consecutive_down} 次下降",
                        details={
                            'current': current_value,
                            'consecutive_count': consecutive_down,
                            'values': values[-consecutive_down-1:]
                        }
                    )
            else:
                consecutive_down = 0
        
        return None
    
    def _detect_threshold(self, task_id: str, timestamp: str, metric: str,
                          current_value: float, threshold: Dict) -> Optional[Alert]:
        """检测绝对值阈值"""
        min_threshold = threshold.get('min_threshold')
        max_threshold = threshold.get('max_threshold')
        
        # 检测超过上限
        if max_threshold and current_value >= max_threshold:
            return Alert(
                task_id=task_id,
                timestamp=timestamp,
                level=AlertLevel.MEDIUM,
                type=AlertType.THRESHOLD,
                metric=metric,
                message=f"{metric} 超过阈值 {current_value} >= {max_threshold}",
                details={
                    'current': current_value,
                    'threshold': max_threshold,
                    'type': 'max'
                }
            )
        
        # 检测低于下限
        if min_threshold and current_value <= min_threshold:
            return Alert(
                task_id=task_id,
                timestamp=timestamp,
                level=AlertLevel.LOW,
                type=AlertType.THRESHOLD,
                metric=metric,
                message=f"{metric} 低于阈值 {current_value} <= {min_threshold}",
                details={
                    'current': current_value,
                    'threshold': min_threshold,
                    'type': 'min'
                }
            )
        
        return None
    
    def _detect_burst(self, task_id: str, timestamp: str, data: Dict[str, float],
                      task_config: Dict) -> Optional[Alert]:
        """检测爆款（综合多个指标）"""
        burst_config = task_config.get('burst_detection', {})
        
        if not burst_config.get('enabled', False):
            return None
        
        min_metrics = burst_config.get('min_metrics', 2)  # 至少几个指标同时触发
        thresholds = burst_config.get('threshold', {})
        
        triggered_metrics = []
        
        for metric, threshold_value in thresholds.items():
            current_value = data.get(metric)
            if current_value and current_value >= threshold_value:
                triggered_metrics.append({
                    'metric': metric,
                    'value': current_value,
                    'threshold': threshold_value
                })
        
        if len(triggered_metrics) >= min_metrics:
            return Alert(
                task_id=task_id,
                timestamp=timestamp,
                level=AlertLevel.CRITICAL,
                type=AlertType.BURST,
                metric='multiple',
                message=f"🔥 检测到爆款！{len(triggered_metrics)} 个指标同时爆发",
                details={
                    'triggered_metrics': triggered_metrics,
                    'min_required': min_metrics,
                    'all_data': data
                }
            )
        
        return None
    
    def calculate_statistics(self, metric: str, window: int = 7) -> Dict:
        """计算统计数据"""
        if len(self.history_data) < 2:
            return {}
        
        values = [
            d.get('data', {}).get(metric) 
            for d in self.history_data[-window:]
            if d.get('data', {}).get(metric) is not None
        ]
        
        if not values:
            return {}
        
        n = len(values)
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / n
        std_dev = math.sqrt(variance)
        
        return {
            'count': n,
            'mean': mean,
            'std_dev': std_dev,
            'min': min(values),
            'max': max(values),
            'latest': values[-1]
        }


def main():
    """测试入口"""
    # 模拟历史数据
    history = [
        {'timestamp': '2024-01-15T10:00:00', 'data': {'likes': 1000, 'comments': 100}},
        {'timestamp': '2024-01-15T12:00:00', 'data': {'likes': 1100, 'comments': 110}},
        {'timestamp': '2024-01-15T14:00:00', 'data': {'likes': 1050, 'comments': 105}},
    ]
    
    # 当前数据（模拟暴增）
    current = {
        'task_id': 'test_001',
        'timestamp': '2024-01-15T16:00:00',
        'data': {'likes': 5000, 'comments': 500}
    }
    
    # 任务配置
    config = {
        'alert_threshold': {
            'likes': {'increase_percent': 50, 'min_value': 1000},
            'comments': {'increase_percent': 50, 'min_value': 100}
        },
        'burst_detection': {
            'enabled': True,
            'min_metrics': 2,
            'threshold': {
                'likes': 3000,
                'comments': 300
            }
        }
    }
    
    # 检测
    detector = AnomalyDetector()
    detector.load_history(history)
    alerts = detector.detect(current, config)
    
    # 输出结果
    print(f"检测到 {len(alerts)} 个异常:")
    for alert in alerts:
        print(f"\n[{alert.level.value.upper()}] {alert.type.value}")
        print(f"  指标: {alert.metric}")
        print(f"  消息: {alert.message}")
        print(f"  详情: {json.dumps(alert.details, ensure_ascii=False)}")


if __name__ == '__main__':
    main()
