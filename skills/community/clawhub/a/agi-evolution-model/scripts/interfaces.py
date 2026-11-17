"""
AGI进化模型接口定义

本模块定义了AGI进化模型中所有模块间交互的统一接口规范，
确保模块间交互的一致性和可维护性。

作者: AGI Evolution Team
版本: 1.0.0
"""

from typing import Protocol, Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# ==================== 枚举类型 ====================

class IntentionalityType(Enum):
    """意向性类型"""
    USER_QUERY = "user_query"
    SYSTEM_EVENT = "system_event"
    EXTERNAL_SIGNAL = "external_signal"


class ErrorSeverity(Enum):
    """错误严重程度"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CognitiveErrorType(Enum):
    """认知性错误类型"""
    HALLUCINATION = "hallucination"
    REASONING_JUMP = "reasoning_jump"
    KNOWLEDGE_MISSING = "knowledge_missing"
    BIAS_INFLUENCE = "bias_influence"


class DimensionType(Enum):
    """五维智力维度类型"""
    ALGORITHMIC = "algorithmic"
    NARRATIVE = "narrative"
    SYSTEM = "system"
    EXECUTIVE = "executive"
    META = "meta"


# ==================== 数据类定义 ====================

@dataclass
class TraceContext:
    """追踪上下文"""
    trace_id: str
    span_id: str = ""
    parent_span_id: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class ValidationResult:
    """参数校验结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    
    @classmethod
    def success(cls) -> 'ValidationResult':
        """创建成功结果"""
        return cls(is_valid=True, errors=[], warnings=[])
    
    @classmethod
    def failure(cls, errors: List[str], warnings: List[str] = None) -> 'ValidationResult':
        """创建失败结果"""
        return cls(is_valid=False, errors=errors, warnings=warnings or [])


@dataclass
class IntentionalityData:
    """意向性数据"""
    type: IntentionalityType
    content: str
    context: Dict[str, Any]
    trace_context: TraceContext
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class ErrorWisdomEntry:
    """错误智慧条目"""
    id: str
    trace_id: str
    error_type: str
    error_subtype: str
    error_code: str
    error_description: str
    root_cause: str
    solution: str
    prevention_strategy: str
    severity: ErrorSeverity
    timestamp: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        if self.metadata is None:
            self.metadata = {}


@dataclass
class DimensionTag:
    """维度标签"""
    dimension: DimensionType
    intensity: float
    confidence: float
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


@dataclass
class CognitiveInsight:
    """认知洞察"""
    insight_type: str
    content: str
    confidence: float
    source: str
    trace_context: TraceContext
    timestamp: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        if self.metadata is None:
            self.metadata = {}


# ==================== 接口协议定义 ====================

class MemoryStoreProtocol(Protocol):
    """记忆存储接口协议"""
    
    def store(self, data: Dict[str, Any], trace_context: TraceContext = None) -> bool:
        """存储数据"""
        ...
    
    def analyze(self, trace_context: TraceContext = None) -> Dict[str, Any]:
        """分析数据"""
        ...
    
    def get_narrative_content(self) -> str:
        """获取叙事内容"""
        ...
    
    def get_narrative_summary(self) -> Dict[str, Any]:
        """获取叙事摘要"""
        ...


class ErrorWisdomManagerProtocol(Protocol):
    """错误智慧库管理接口协议"""
    
    def record_error(
        self,
        error_type: str,
        error_subtype: str,
        error_code: str,
        error_description: str,
        root_cause: str,
        solution: str,
        prevention_strategy: str,
        trace_id: str,
        severity: str = "mild",
        trigger_scenario: str = "",
        metadata: dict = None
    ) -> str:
        """记录错误"""
        ...
    
    def query_prevention(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """查询预防知识"""
        ...
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计数据"""
        ...


class IntentionalityCollectorProtocol(Protocol):
    """意向性收集接口协议"""
    
    def collect_from_user(self, content: str, context: Dict[str, Any] = None) -> IntentionalityData:
        """收集用户意向性"""
        ...
    
    def collect_from_system(self, event_type: str, content: str, context: Dict[str, Any] = None) -> IntentionalityData:
        """收集系统意向性"""
        ...
    
    def collect_from_external(self, source: str, content: str, context: Dict[str, Any] = None) -> IntentionalityData:
        """收集外部意向性"""
        ...


class IntentionalityClassifierProtocol(Protocol):
    """意向性分类接口协议"""
    
    def classify(self, data: IntentionalityData) -> Dict[str, Any]:
        """分类意向性"""
        ...


class IntentionalityAnalyzerProtocol(Protocol):
    """意向性分析接口协议"""
    
    def analyze(self, classification: Dict[str, Any], data: IntentionalityData) -> Dict[str, Any]:
        """分析意向性"""
        ...


class CognitiveErrorDetectorProtocol(Protocol):
    """认知性错误检测接口协议"""
    
    def detect(self, user_query: str, agent_response: str, trace_context: TraceContext = None) -> Optional[Dict[str, Any]]:
        """检测认知性错误"""
        ...


class DimensionTaggerProtocol(Protocol):
    """维度标签生成接口协议"""
    
    def generate_tags(self, raw_data: Dict[str, Any], model: Any = None) -> List[DimensionTag]:
        """生成维度标签"""
        ...


class ElevationAdvisorProtocol(Protocol):
    """升维建议接口协议"""
    
    def advise(self, current_dimensions: List[DimensionTag], model: Any = None) -> Dict[str, Any]:
        """提供升维建议"""
        ...


class LoggingManagerProtocol(Protocol):
    """日志管理接口协议"""
    
    def get_logger(self, name: str) -> Any:
        """获取日志记录器"""
        ...
    
    def set_level(self, level: str) -> None:
        """设置日志级别"""
        ...
    
    def add_handler(self, handler: Any) -> None:
        """添加日志处理器"""
        ...


class ValidationFrameworkProtocol(Protocol):
    """参数校验框架接口协议"""
    
    def validate(self, data: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
        """校验数据"""
        ...
    
    def register_schema(self, name: str, schema: Dict[str, Any]) -> None:
        """注册校验模式"""
        ...


class MetricsCollectorProtocol(Protocol):
    """指标收集接口协议"""
    
    def record_metric(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        """记录指标"""
        ...
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取指标"""
        ...


class HealthCheckerProtocol(Protocol):
    """健康检查接口协议"""
    
    def check(self) -> Dict[str, Any]:
        """执行健康检查"""
        ...
    
    def get_status(self) -> str:
        """获取健康状态"""
        ...


# ==================== 工厂函数 ====================

def create_trace_context(trace_id: str = None) -> TraceContext:
    """创建追踪上下文"""
    import uuid
    if not trace_id:
        trace_id = str(uuid.uuid4())
    return TraceContext(trace_id=trace_id)


def create_validation_result(is_valid: bool, errors: List[str] = None, warnings: List[str] = None) -> ValidationResult:
    """创建校验结果"""
    return ValidationResult(
        is_valid=is_valid,
        errors=errors or [],
        warnings=warnings or []
    )


# ==================== 版本信息 ====================

__version__ = "1.0.0"
__all__ = [
    # 枚举类型
    'IntentionalityType',
    'ErrorSeverity',
    'CognitiveErrorType',
    'DimensionType',
    
    # 数据类
    'TraceContext',
    'ValidationResult',
    'IntentionalityData',
    'ErrorWisdomEntry',
    'DimensionTag',
    'CognitiveInsight',
    
    # 接口协议
    'MemoryStoreProtocol',
    'ErrorWisdomManagerProtocol',
    'IntentionalityCollectorProtocol',
    'IntentionalityClassifierProtocol',
    'IntentionalityAnalyzerProtocol',
    'CognitiveErrorDetectorProtocol',
    'DimensionTaggerProtocol',
    'ElevationAdvisorProtocol',
    'LoggingManagerProtocol',
    'ValidationFrameworkProtocol',
    'MetricsCollectorProtocol',
    'HealthCheckerProtocol',
    
    # 工厂函数
    'create_trace_context',
    'create_validation_result',
]
