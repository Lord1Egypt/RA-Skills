
# 日志记录
import logging
logger = logging.getLogger(__name__)
"""
监控指标模块

提供统一的监控指标收集和上报接口。

版本: 1.0.0
作者: AGI Evolution Team
"""

__version__ = '1.0.0'
__author__ = 'AGI Evolution Team'

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import time
import json
from interfaces import TraceContext, create_trace_context


@dataclass
class Metric:
    """指标数据结构"""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'value': self.value,
            'labels': self.labels,
            'timestamp': self.timestamp
        }


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        """初始化指标收集器"""
        self.metrics: List[Metric] = []
        self.counters: Dict[str, float] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = {}
    
    def increment_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """
        增加计数器
        
        Args:
            name: 指标名称
            value: 增加值
            labels: 标签
        """
        if name not in self.counters:
            self.counters[name] = 0.0
        
        self.counters[name] += value
        
        metric = Metric(
            name=name,
            value=self.counters[name],
            labels=labels or {}
        )
        self.metrics.append(metric)
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """
        设置仪表盘
        
        Args:
            name: 指标名称
            value: 值
            labels: 标签
        """
        self.gauges[name] = value
        
        metric = Metric(
            name=name,
            value=value,
            labels=labels or {}
        )
        self.metrics.append(metric)
    
    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """
        观察直方图
        
        Args:
            name: 指标名称
            value: 值
            labels: 标签
        """
        if name not in self.histograms:
            self.histograms[name] = []
        
        self.histograms[name].append(value)
        
        metric = Metric(
            name=name,
            value=value,
            labels=labels or {}
        )
        self.metrics.append(metric)
    
    def get_counter(self, name: str) -> float:
        """
        获取计数器值
        
        Args:
            name: 指标名称
        
        Returns:
            计数器值
        """
        return self.counters.get(name, 0.0)
    
    def get_gauge(self, name: str) -> float:
        """
        获取仪表盘值
        
        Args:
            name: 指标名称
        
        Returns:
            仪表盘值
        """
        return self.gauges.get(name, 0.0)
    
    def get_histogram_stats(self, name: str) -> Dict[str, float]:
        """
        获取直方图统计
        
        Args:
            name: 指标名称
        
        Returns:
            统计信息（count, sum, avg, min, max）
        """
        if name not in self.histograms:
            return {'count': 0, 'sum': 0.0, 'avg': 0.0, 'min': 0.0, 'max': 0.0}
        
        values = self.histograms[name]
        if not values:
            return {'count': 0, 'sum': 0.0, 'avg': 0.0, 'min': 0.0, 'max': 0.0}
        
        return {
            'count': len(values),
            'sum': sum(values),
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values)
        }
    
    def get_all_metrics(self) -> List[Dict[str, Any]]:
        """
        获取所有指标
        
        Returns:
            指标列表
        """
        return [m.to_dict() for m in self.metrics]
    
    def reset(self):
        """重置所有指标"""
        self.metrics.clear()
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()
    
    def export_json(self) -> str:
        """
        导出为JSON格式
        
        Returns:
            JSON字符串
        """
        return json.dumps({
            'counters': self.counters,
            'gauges': self.gauges,
            'histograms': {k: self.get_histogram_stats(k) for k in self.histograms},
            'metrics': self.get_all_metrics()
        }, ensure_ascii=False, indent=2)


class Timer:
    """计时器"""
    
    def __init__(self, metrics_collector: MetricsCollector, metric_name: str, labels: Optional[Dict[str, str]] = None):
        """
        初始化计时器
        
        Args:
            metrics_collector: 指标收集器
            metric_name: 指标名称
            labels: 标签
        """
        self.metrics_collector = metrics_collector
        self.metric_name = metric_name
        self.labels = labels
        self.start_time = None
    
    def __enter__(self):
        """进入计时"""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出计时"""
        if self.start_time is not None:
            duration = time.time() - self.start_time
            self.metrics_collector.observe_histogram(
                self.metric_name,
                duration,
                self.labels
            )


# 全局指标收集器实例
_global_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """获取全局指标收集器"""
    return _global_metrics_collector


def increment_counter(name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None):
    """增加计数器（全局）"""
    _global_metrics_collector.increment_counter(name, value, labels)


def set_gauge(name: str, value: float, labels: Optional[Dict[str, str]] = None):
    """设置仪表盘（全局）"""
    _global_metrics_collector.set_gauge(name, value, labels)


def observe_histogram(name: str, value: float, labels: Optional[Dict[str, str]] = None):
    """观察直方图（全局）"""
    _global_metrics_collector.observe_histogram(name, value, labels)


def timer(metric_name: str, labels: Optional[Dict[str, str]] = None) -> Timer:
    """创建计时器（全局）"""
    return Timer(_global_metrics_collector, metric_name, labels)


if __name__ == '__main__':
    # 测试监控指标
    print('监控指标模块测试')
    
    collector = MetricsCollector()
    
    # 测试计数器
    collector.increment_counter('requests_total', 1, {'method': 'GET', 'path': '/api/test'})
    collector.increment_counter('requests_total', 1, {'method': 'GET', 'path': '/api/test'})
    collector.increment_counter('requests_total', 1, {'method': 'POST', 'path': '/api/test'})
    
    print(f'✓ 计数器: {collector.get_counter("requests_total")}')
    
    # 测试仪表盘
    collector.set_gauge('memory_usage', 1024.5, {'unit': 'MB'})
    collector.set_gauge('cpu_usage', 0.75, {'unit': 'percent'})
    
    print(f'✓ 仪表盘: memory={collector.get_gauge("memory_usage")}, cpu={collector.get_gauge("cpu_usage")}')
    
    # 测试直方图
    collector.observe_histogram('request_duration', 0.1, {'method': 'GET'})
    collector.observe_histogram('request_duration', 0.2, {'method': 'GET'})
    collector.observe_histogram('request_duration', 0.15, {'method': 'GET'})
    
    stats = collector.get_histogram_stats('request_duration')
    print(f'✓ 直方图统计: {stats}')
    
    # 测试计时器
    with timer('operation_duration', {'operation': 'test'}):
        time.sleep(0.1)
    
    stats = collector.get_histogram_stats('operation_duration')
    print(f'✓ 计时器统计: {stats}')
    
    # 测试导出
    json_output = collector.export_json()
    print(f'✓ JSON导出: {len(json_output)} 字符')
    
    print('监控指标模块测试完成')
