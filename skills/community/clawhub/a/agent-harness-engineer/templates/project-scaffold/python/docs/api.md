# API文档

## Agent Core API

### AgentCore

```python
class AgentCore:
    def __init__(self, llm_config: Dict[str, Any])
    """初始化Agent
    
    Args:
        llm_config: LLM配置
            - provider: 供应商 (anthropic | openai | azure | local)
            - model: 模型名称
            - api_key: API密钥
            - base_url: 自定义API端点
            - max_tokens: 最大token数
            - temperature: 温度参数
    """
    
    async def run(self, user_input: str) -> str
    """运行Agent
    
    Args:
        user_input: 用户输入
        
    Returns:
        Agent响应
    """
    
    def reset(self)
    """重置Agent状态"""
```

## LLM Client API

### LLMClient

```python
class LLMClient(ABC):
    async def chat(
        self,
        messages: List[Message],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> LLMResponse
    """发送聊天请求
    
    Args:
        messages: 消息列表
        tools: 工具定义列表
        
    Returns:
        LLM响应
    """
    
    def validate_config(self) -> bool
    """验证配置是否有效"""
```

### create_llm_client

```python
def create_llm_client(config: Dict[str, Any]) -> LLMClient
"""根据配置创建对应的LLM客户端

Args:
    config: 配置字典
        
Returns:
    LLMClient实例
"""
```

## Tool Registry API

### ToolRegistry

```python
class ToolRegistry:
    def register(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable,
        is_concurrency_safe: bool = False
    )
    """注册工具
    
    Args:
        name: 工具名称
        description: 工具描述
        input_schema: 输入参数Schema
        handler: 处理函数
        is_concurrency_safe: 是否支持并发执行
    """
    
    def execute(self, name: str, input_data: Dict[str, Any]) -> Any
    """执行工具
    
    Args:
        name: 工具名称
        input_data: 输入参数
        
    Returns:
        工具执行结果
    """
```

## Permission API

### PermissionManager

```python
class PermissionManager:
    def __init__(self, config: Dict[str, Any] = None)
    """初始化权限管理器
    
    Args:
        config: 权限配置
            - mode: 权限模式 (allow | deny | ask)
            - rules: 权限规则列表
    """
    
    def check_permission(self, tool_name: str, tool_input: Dict[str, Any]) -> bool
    """检查权限
    
    Args:
        tool_name: 工具名称
        tool_input: 工具输入
        
    Returns:
        True if allowed, False if denied
    """
```

### SandboxManager

```python
class SandboxManager:
    def __init__(self, config: Dict[str, Any] = None)
    """初始化沙箱管理器
    
    Args:
        config: 沙箱配置
            - enabled: 是否启用
            - allowed_directories: 允许的目录列表
            - denied_patterns: 拒绝的模式列表
    """
    
    def validate_path(self, path: str) -> bool
    """验证路径是否在允许范围内"""
    
    def validate_command(self, command: str) -> bool
    """验证命令是否安全"""
```

## Session API

### SessionManager

```python
class SessionManager:
    def __init__(self, storage_path: str = "memory/sessions")
    """初始化会话管理器
    
    Args:
        storage_path: 会话存储路径
    """
    
    def create_session(self) -> str
    """创建新会话
    
    Returns:
        会话ID
    """
    
    def add_event(self, event_type: str, content: str, metadata: Dict[str, Any] = None)
    """添加事件"""
    
    def get_session_history(self, session_id: str) -> List[SessionEvent]
    """获取会话历史"""
    
    def list_sessions(self) -> List[str]
    """列出所有会话"""
```

## Memory API

### MemoryManager

```python
class MemoryManager:
    def __init__(self, storage_path: str = "memory")
    """初始化记忆管理器
    
    Args:
        storage_path: 记忆存储路径
    """
    
    def add_short_term(self, content: str, metadata: Dict[str, Any] = None)
    """添加短期记忆"""
    
    def add_long_term(self, category: str, content: str)
    """添加长期记忆"""
    
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[str]
    """获取相关记忆"""
    
    def consolidate(self)
    """整合记忆"""
```
