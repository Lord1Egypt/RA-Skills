"""
Observability Module
P0: Structured logging, metrics, alerts, tracing
"""
import sys
import os
import json
import time
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from functools import wraps
import logging
import traceback

# ============ Configuration ============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
METRICS_ENABLE = True
ALERT_WEBHOOK = os.getenv("ALERT_WEBHOOK", "")
TRACE_SAMPLE_RATE = 0.1
MASK_SENSITIVE_LOGS = True


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class TraceContext:
    """追踪上下文"""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    model_version: str = "v2.0.0"
    environment: str = "dev"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class StructuredLogger:
    """结构化日志器"""
    
    def __init__(self, name: str = "ai_model_team"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Console handler
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(handler)
    
    def _mask_sensitive(self, data: Dict) -> Dict:
        """脱敏敏感信息"""
        if not MASK_SENSITIVE_LOGS:
            return data
        
        sensitive_keys = [
            "api_key", "secret", "password", "token", 
            "secret_key", "api_password", "authorization"
        ]
        
        result = {}
        for k, v in data.items():
            k_lower = k.lower()
            if any(s in k_lower for s in sensitive_keys):
                result[k] = "***REDACTED***"
            elif isinstance(v, dict):
                result[k] = self._mask_sensitive(v)
            else:
                result[k] = v
        return result
    
    def _format(self, level: LogLevel, message: str, context: Optional[TraceContext] = None, **kwargs) -> Dict:
        """格式化日志输出"""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level.value,
            "message": message,
            "logger": "ai_model_team"
        }
        
        if context:
            log_entry["trace_id"] = context.trace_id
            log_entry["request_id"] = context.request_id
            log_entry["model_version"] = context.model_version
        
        if kwargs:
            safe_kwargs = self._mask_sensitive(kwargs) if isinstance(kwargs, dict) else kwargs
            log_entry["data"] = safe_kwargs
        
        return log_entry
    
    def _emit(self, level: LogLevel, message: str, context: Optional[TraceContext] = None, **kwargs):
        """发送日志"""
        log_entry = self._format(level, message, context, **kwargs)
        log_line = json.dumps(log_entry, ensure_ascii=False)
        
        if level == LogLevel.DEBUG:
            self.logger.debug(log_line)
        elif level == LogLevel.INFO:
            self.logger.info(log_line)
        elif level == LogLevel.WARNING:
            self.logger.warning(log_line)
        elif level == LogLevel.ERROR:
            self.logger.error(log_line)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(log_line)
    
    def debug(self, message: str, context: Optional[TraceContext] = None, **kwargs):
        self._emit(LogLevel.DEBUG, message, context, **kwargs)
    
    def info(self, message: str, context: Optional[TraceContext] = None, **kwargs):
        self._emit(LogLevel.INFO, message, context, **kwargs)
    
    def warning(self, message: str, context: Optional[TraceContext] = None, **kwargs):
        self._emit(LogLevel.WARNING, message, context, **kwargs)
    
    def error(self, message: str, context: Optional[TraceContext] = None, **kwargs):
        self._emit(LogLevel.ERROR, message, context, **kwargs)
        if kwargs.get("exc_info"):
            self.logger.error(traceback.format_exc())
    
    def critical(self, message: str, context: Optional[TraceContext] = None, **kwargs):
        self._emit(LogLevel.CRITICAL, message, context, **kwargs)


# Global logger
_logger: Optional[StructuredLogger] = None

def get_logger() -> StructuredLogger:
    global _logger
    if _logger is None:
        _logger = StructuredLogger()
    return _logger


@dataclass
class Metrics:
    """指标数据"""
    name: str
    value: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    tags: Dict[str, str] = field(default_factory=dict)
    unit: str = ""


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.metrics: List[Metrics] = []
        self.counters: Dict[str, float] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = {}
    
    def increment(self, name: str, value: float = 1, tags: Optional[Dict] = None):
        """递增计数器"""
        key = f"{name}:{json.dumps(tags or {}, sort_keys=True)}"
        self.counters[key] = self.counters.get(key, 0) + value
        
        self.metrics.append(Metrics(
            name=name,
            value=self.counters[key],
            tags=tags or {},
            unit="count"
        ))
    
    def gauge(self, name: str, value: float, tags: Optional[Dict] = None):
        """设置仪表值"""
        key = f"{name}:{json.dumps(tags or {}, sort_keys=True)}"
        self.gauges[key] = value
        
        self.metrics.append(Metrics(
            name=name,
            value=value,
            tags=tags or {},
            unit="gauge"
        ))
    
    def histogram(self, name: str, value: float, tags: Optional[Dict] = None):
        """记录直方图"""
        key = f"{name}:{json.dumps(tags or {}, sort_keys=True)}"
        if key not in self.histograms:
            self.histograms[key] = []
        self.histograms[key].append(value)
        
        self.metrics.append(Metrics(
            name=name,
            value=value,
            tags=tags or {},
            unit="histogram"
        ))
    
    def timing(self, name: str, duration_ms: float, tags: Optional[Dict] = None):
        """记录时间"""
        self.histogram(f"{name}.duration_ms", duration_ms, tags)
    
    def get_all(self) -> List[Dict]:
        """获取所有指标"""
        return [
            {
                "name": m.name,
                "value": m.value,
                "timestamp": m.timestamp,
                "tags": m.tags,
                "unit": m.unit
            }
            for m in self.metrics[-100:]  # 最近 100 条
        ]
    
    def reset(self):
        """重置指标"""
        self.metrics.clear()
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()


# Global metrics collector
_metrics: Optional[MetricsCollector] = None

def get_metrics() -> MetricsCollector:
    global _metrics
    if _metrics is None:
        _metrics = MetricsCollector()
    return _metrics


class AlertManager:
    """告警管理器"""
    
    def __init__(self, webhook_url: str = ""):
        self.webhook_url = webhook_url or ALERT_WEBHOOK
        self.alert_history: List[Dict] = []
        self.cooldowns: Dict[str, float] = {}  # alert_name -> next_allowed_ts
    
    def _should_alert(self, alert_name: str, cooldown_sec: float = 300) -> bool:
        """检查是否应该告警（防止频繁告警）"""
        now = time.time()
        if alert_name in self.cooldowns:
            if now < self.cooldowns[alert_name]:
                return False
        self.cooldowns[alert_name] = now + cooldown_sec
        return True
    
    def send(self, alert_name: str, level: str, message: str, 
             context: Optional[TraceContext] = None, cooldown_sec: float = 300):
        """
        发送告警
        
        Args:
            alert_name: 告警名称
            level: 级别 (critical/error/warning/info)
            message: 告警消息
            context: 追踪上下文
            cooldown_sec: 冷却时间（秒）
        """
        if not self._should_alert(alert_name, cooldown_sec):
            return
        
        alert = {
            "alert_name": alert_name,
            "level": level,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": context.trace_id if context else None,
            "model_version": context.model_version if context else None
        }
        
        self.alert_history.append(alert)
        
        # 记录到日志
        logger = get_logger()
        if level == "critical":
            logger.critical(f"ALERT: {alert_name} - {message}", context=context)
        elif level == "error":
            logger.error(f"ALERT: {alert_name} - {message}", context=context)
        elif level == "warning":
            logger.warning(f"ALERT: {alert_name} - {message}", context=context)
        
        # 发送 webhook
        if self.webhook_url:
            self._send_webhook(alert)
    
    def _send_webhook(self, alert: Dict):
        """发送 webhook 告警"""
        try:
            import requests
            payload = {
                "text": f"[{alert['level'].upper()}] {alert['alert_name']}: {alert['message']}",
                "alert": alert
            }
            requests.post(
                self.webhook_url,
                json=payload,
                timeout=5,
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            get_logger().error(f"Failed to send webhook: {e}")
    
    def alert_data_source_failure(self, source: str, error: str, context: Optional[TraceContext] = None):
        """数据源断流告警"""
        self.send(
            alert_name="data_source_failure",
            level="error",
            message=f"Data source failure: {source} - {error}",
            context=context,
            cooldown_sec=300
        )
    
    def alert_model_load_failure(self, model: str, error: str, context: Optional[TraceContext] = None):
        """模型加载失败告警"""
        self.send(
            alert_name="model_load_failure",
            level="critical",
            message=f"Model load failure: {model} - {error}",
            context=context,
            cooldown_sec=600
        )
    
    def alert_prediction_timeout(self, model: str, duration_ms: float, context: Optional[TraceContext] = None):
        """预测超时告警"""
        self.send(
            alert_name="prediction_timeout",
            level="warning",
            message=f"Prediction timeout: {model} took {duration_ms}ms",
            context=context,
            cooldown_sec=180
        )
    
    def alert_high_failure_rate(self, failure_rate: float, threshold: float = 0.1, context: Optional[TraceContext] = None):
        """高失败率告警"""
        self.send(
            alert_name="high_failure_rate",
            level="error",
            message=f"High failure rate: {failure_rate:.1%} (threshold: {threshold:.1%})",
            context=context,
            cooldown_sec=300
        )
    
    def alert_risk_circuit_breaker(self, reason: str, context: Optional[TraceContext] = None):
        """熔断告警"""
        self.send(
            alert_name="risk_circuit_breaker",
            level="critical",
            message=f"Risk circuit breaker triggered: {reason}",
            context=context,
            cooldown_sec=600
        )


# Global alert manager
_alert_manager: Optional[AlertManager] = None

def get_alerts() -> AlertManager:
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager


def trace_function(func: Callable) -> Callable:
    """函数追踪装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        context = TraceContext()
        logger = get_logger()
        metrics = get_metrics()
        
        logger.info(f"Entering {func.__name__}", context=context)
        
        try:
            result = func(*args, **kwargs)
            
            duration_ms = (time.time() - start_time) * 1000
            metrics.timing(f"{func.__name__}.duration_ms", duration_ms)
            metrics.increment(f"{func.__name__}.success", tags={"function": func.__name__})
            
            logger.info(f"Exiting {func.__name__}", context=context, 
                       duration_ms=duration_ms, status="success")
            
            return result
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            metrics.increment(f"{func.__name__}.error", tags={"function": func.__name__, "error": type(e).__name__})
            
            logger.error(f"Exception in {func.__name__}: {str(e)}", 
                        context=context, duration_ms=duration_ms,
                        exc_info=True)
            
            # 发送告警
            alerts = get_alerts()
            alerts.alert_prediction_timeout(func.__name__, duration_ms, context)
            
            raise
    
    return wrapper


def input_hash(data: Any) -> str:
    """计算输入数据的哈希（用于追踪）"""
    try:
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()[:16]
    except:
        return "hash_error"
