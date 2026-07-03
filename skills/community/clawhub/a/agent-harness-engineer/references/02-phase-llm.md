# Phase 2: LLM抽象层

## 设计原理

### 1. 供应商无关性（Provider-Agnostic Design）
核心依赖抽象接口而非具体实现，解除与单一供应商的强耦合。
```
高层模块（AgentCore） → ILLMClient（抽象）→ AnthropicClient / OpenAIClient / ...
```
- 切换供应商仅修改配置文件，无需改动业务代码
- 可测试性：注入 Mock 客户端即可独立测试 Agent 逻辑

### 2. 懒加载模式（Lazy Import Pattern）
重型 SDK 模块不在模块顶层导入，仅在构造函数或首次调用时按需加载。

**核心原则**：
- 工厂函数按需 `import` 供应商模块（非顶层导入）
- 客户端实例缓存于工厂内部，避免重复初始化
- 未使用的供应商模块零导入开销
- 结构：`_client_cache: Dict[str, LLMClient] = {}` → 首次`get_client()`时按需`import`并缓存

**动机**：Claude Code 源码中大型模块（OpenTelemetry, gRPC, analytics）均采用此模式降低冷启动延迟。在 Python 中同样适用：仅在用户选择了某个供应商时才 `import` 对应的 SDK，未使用的供应商零开销。

### 3. Prompt 缓存稳定性（Cache Stability）
当启用 Anthropic 的 Prompt Caching 时，发送给 API 的 content block 顺序必须保持稳定不变。
- **稳定前缀**：内置工具定义按固定排序（如字母序），确保它们始终占据缓存前缀位置
- **最小缓存长度**：单个 cache breakpoint 至少 ~1024 tokens 才有命中价值
- **缓存失效条件**：前缀中任何一位变化 → 整个缓存失效 → 需重建

### 4. 抽象 vs 具体：何时有抽象、何时直接调用
| 规模 | 模式 | 抽象层 | 理由 |
|------|------|--------|------|
| Minimal | 单供应商直接导入 | 无 | 过度抽象徒增复杂度 |
| Professional | 工厂 + 多供应商 | 有 | 需要灵活切换 |
| Enterprise | 懒加载 + 多区域 | 有 | 高可用 + 成本控制 |

---

## 抽象接口层

### 数据结构

```python
@dataclass
class Message:
    """标准化消息，所有供应商客户端统一使用此格式"""
    role: str          # "system" | "user" | "assistant" | "tool"
    content: str
    # ⚠ AI构建提示: 可扩展 name 字段用于 tool role 的 tool_call_id

@dataclass
class ToolCall:
    """工具调用的标准化表示"""
    id: str
    name: str
    arguments: Dict[str, Any]

@dataclass
class StreamChunk:
    """流式响应的单个 chunk"""
    content: str                        # 增量文本
    tool_call: Optional[ToolCall]       # 增量工具调用（部分构建中）
    finish_reason: Optional[str]        # "stop" | "tool_calls" | "length"

@dataclass
class LLMResponse:
    """完整响应的标准化表示"""
    content: str
    tool_calls: List[ToolCall]
    usage: Dict[str, int]               # {"prompt_tokens", "completion_tokens", "total_tokens"}
    model: str
    finish_reason: str
```

### 核心抽象：ILLMClient

```python
class ILLMClient(ABC):
    """
    LLM 客户端统一接口。
    所有供应商实现必须继承此类并实现所有 @abstractmethod。
    """

    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        tools: Optional[List[Dict]] = None,
    ) -> LLMResponse:
        """发送非流式聊天请求，返回完整响应"""
        ...

    @abstractmethod
    async def chat_stream(
        self,
        messages: List[Message],
        tools: Optional[List[Dict]] = None,
    ) -> AsyncIterator[StreamChunk]:
        """发送流式聊天请求，返回异步迭代器"""

    @abstractmethod
    def chat_sync(
        self,
        messages: List[Message],
        tools: Optional[List[Dict]] = None,
    ) -> LLMResponse:
        """同步聊天接口——内部调用 asyncio.run(self.chat(...))"""

    @abstractmethod
    def count_tokens(self, messages: List[Message]) -> int:
        """估算消息列表的 token 数（不调用 API）"""
```

### 重试策略抽象：IRetryPolicy

```python
class IRetryPolicy(ABC):
    """
    可插拔的重试策略，独立于供应商客户端。
    """
    @abstractmethod
    def should_retry(self, exception: Exception, attempt: int) -> bool:
        """根据异常类型和当前尝试次数决定是否重试"""
        ...

    @abstractmethod
    def backoff_delay(self, attempt: int) -> float:
        """计算第 n 次重试的等待秒数（指数退避 / 固定 / jitter）"""
        ...

    @property
    @abstractmethod
    def max_retries(self) -> int:
        """最大重试次数"""
        ...
```

### Token 计数抽象：ITokenCounter

```python
class ITokenCounter(ABC):
    """
    供应商无关的 token 计数接口。
    """
    @abstractmethod
    def count(self, text: str, model: str) -> int:
        """估算给定文本在指定模型下的 token 数"""
        ...

    @abstractmethod
    def count_messages(self, messages: List[Message], model: str) -> int:
        """估算整个消息列表的 token 数（含 role 前缀开销）"""
        ...
```

### 模型校验抽象：IModelValidator

```python
class IModelValidator(ABC):
    """
    校验模型名称是否有效、是否支持所需特性。
    """
    @abstractmethod
    async def validate(self, model: str) -> ModelCapability:
        """返回模型的可用性及能力描述"""
        ...

@dataclass
class ModelCapability:
    available: bool
    supports_tools: bool
    supports_vision: bool
    supports_streaming: bool
    max_context_tokens: int
    max_output_tokens: int
```

---

## AI构建提示

```
⚠ 以下为 AI 实现时的指引——根据使用者声明的规模决定实现深度。
```

### ⚠ 规模：Minimal（25–50行代码）
- 不需要抽象层。直接在业务代码中 `import openai` 并调用
- 不需要 ILLMClient、不需要 factory
- 实现清单：单个 sync chat 函数 + 硬编码 API key

### ⚠ 规模：Professional（200–400行代码）
1. **ILLMClient 实现**：
   - `AnthropicClient`：封装 `anthropic.AsyncAnthropic`，实现 `chat` / `chat_stream`
   - `OpenAIClient`：封装 `openai.AsyncOpenAI`，实现 `chat` / `chat_stream`
   - `LocalClient`：封装 `httpx` 调用 Ollama / vLLM 的 OpenAI-compatible endpoint
   - 每个实现中 `chat_sync` = `asyncio.run(self.chat(...))`
2. **SimpleRetryPolicy**：实现 `should_retry`（429/5xx 可重试，4xx 不可重试）和指数退避（1s, 2s, 4s, 8s...）
3. **SimpleTokenCounter**：调用 tiktoken 编码器估算 token（各供应商使用不同编码器）
4. **ProviderFactory**：
   ```python
   # 伪代码
   def create(config: dict) -> ILLMClient:
       provider_map = {"anthropic": AnthropicClient, "openai": OpenAIClient, "local": LocalClient}
       # 从 config["provider"] 查找类 → 实例化 → 注入 retry_policy → 返回
   ```
5. 在 `chat` 方法内集成重试：
   ```python
   while attempt <= retry_policy.max_retries:
       try: return await self._do_api_call(...)
       except Exception as e:
           if not retry_policy.should_retry(e, attempt): raise
           await asyncio.sleep(retry_policy.backoff_delay(attempt))
           attempt += 1
   ```

### ⚠ 规模：Enterprise（500–800行代码）
在上述 Professional 基础上增加：
1. **LazyProviderProxy**：包装所有供应商，仅在被选中时才 `import` 对应 SDK
   ```python
   class LazyProviderProxy:
       def __init__(self, provider_name, config):
           self._name = provider_name
           self._config = config
           self._delegate = None
       async def chat(self, ...):
           if self._delegate is None:
               self._delegate = self._load_provider()   # 触发 import
           return await self._delegate.chat(...)
   ```
2. **PromptCacheManager**：
   - 缓存稳定的 system prompt + tool definitions 的序列化结果
   - 计算缓存前缀 token 数，仅 >= 1024 时启用 `cache_control`
   - 检测缓存命中/未命中，日志记录命中率
3. **MultiRegionFailover**：
   - 配置多个 endpoint region（如 us-east / eu-west）
   - 主区域失败 → 自动切换备用区域
   - 健康检查：定期 ping 各区域延迟
4. **智能 Token 计数**：根据模型自动选择 tiktoken / anthropic tokenizer / 本地回退（字符数/4）

---

## 规模适应性指南

### Minimal：单供应商
```
场景：个人项目 / 原型 / 固定使用一个 LLM
方案：直接在代码中 import openai，无抽象
风险：切换供应商 = 改全部调用点
代价：代码量 25 行
```

### Professional：3供应商 + 工厂
```
场景：SaaS 产品 / 需要灵活切换 / 多供应商对比
方案：ILLMClient 抽象 + ProviderFactory + 简单重试
收益：配置文件切换供应商，5 分钟支持新供应商
代价：3个客户端实现 ~200 行 + 工厂 ~30 行 + 重试 ~40 行
```

### Enterprise：懒加载 + 缓存 + 区域容灾
```
场景：高可用服务 / 成本敏感 / 多区域部署
方案：LazyProviderProxy + PromptCacheManager + MultiRegionFailover
收益：冷启动延迟降低 40%，缓存命中降低 API 成本，单区域故障零影响
代价：整体 ~600 行，需运维监控配合
```

---

## 检查清单

- [ ] `ILLMClient` 抽象接口是否定义了 `chat` / `chat_stream` / `chat_sync` / `count_tokens`
- [ ] `IRetryPolicy` 是否独立于客户端，支持可插拔
- [ ] `ITokenCounter` 是否独立于供应商 SDK
- [ ] `IModelValidator` 是否可校验模型能力（tools/vision/streaming）
- [ ] 所有具体实现中，没有在模块顶层 `import anthropic` / `import openai`（Professional+ 规模使用懒加载）
- [ ] 工厂函数仅依赖 `ILLMClient` 接口，不依赖具体类
- [ ] 工具调用格式统一为 `ToolCall`，各供应商客户端内部转换
- [ ] 流式响应使用 `AsyncIterator[StreamChunk]`，前端可逐块渲染
- [ ] 重试逻辑仅对 429 / 5xx / 网络异常触发，4xx 直接抛出
- [ ] Token 计数不发起网络请求（纯本地估算）
- [ ] (Enterprise) Prompt Cache 前缀 >= 1024 tokens 才启用 breakpoint
- [ ] (Enterprise) 懒加载 Proxy 的 `import` 延迟到首次 `chat()` 调用

---

## 常见陷阱

### 陷阱1：抽象过度——一个供应商也建 5 层类
**症状**：只有 Anthropic，但建了 ILLMClient → AnthropicClient → AnthropicConfig → ...  
**修正**：Minimal 规模直接 `import anthropic`，等有第二个供应商时再抽象。

### 陷阱2：顶层 import 所有 SDK
**症状**：`provider.py` 顶部 `import anthropic; import openai; import httpx`  
**修正**：懒惰导入。未使用的 SDK 不应被加载。  
**实现**（伪代码）：
```
def _init_client(self):
    if self._client is not None: return
    spec = importlib.util.find_spec(self._sdk_package)
    if spec is None: raise MissingSDKError(f"pip install {self._sdk_package}")
    module = importlib.import_module(self._sdk_package)
    self._client = module.AsyncClient(...)
```

### 陷阱3：缓存前缀不稳定
**症状**：启用 Prompt Caching 但命中率始终为 0  
**原因**：工具定义列表每次顺序不同 / system prompt 包含时间戳 / context 中有动态 id  
**修正**：工具定义排序固定（`sorted(tools, key=lambda t: t["function"]["name"])`），所有动态内容放缓存 breakpoint 之后。

### 陷阱4：不同供应商的 "停止原因" 字符串不一致
**症状**：Anthropic 返回 `"end_turn"` / `"tool_use"`，OpenAI 返回 `"stop"` / `"tool_calls"`  
**修正**：在供应商客户端内部统一映射为 `LLMResponse.finish_reason`（`"stop" | "tool_calls" | "length"`）。

### 陷阱5：同步接口中直接调用 async 方法
**症状**：`chat_sync` 内部调用 `self.chat(...)` 报 `RuntimeWarning: coroutine was never awaited`  
**修正**：
```python
def chat_sync(self, ...):
    import asyncio
    try:
        loop = asyncio.get_running_loop()
        # 已有运行中的事件循环 → 使用 nest_asyncio 或线程池
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, self.chat(...)).result()
    except RuntimeError:
        return asyncio.run(self.chat(...))
```

### 陷阱6：本地模型伪造成 JSON 格式的工具调用
**症状**：Ollama/LocalAI 模型不支持原生 tool_use，将工具调用作为 JSON 字符串嵌入 `content` 中  
**修正**：`LocalClient` 需检测并解析 content 中的 JSON 模式工具调用：
```python
# 伪代码
def _parse_tool_calls(self, content: str) -> List[ToolCall]:
    # 匹配 ```json { "name": "xxx", "arguments": {...} } ```
    # 如果匹配到 → 提取为 ToolCall，清空 content 中的 JSON 片段
    # 如果未匹配 → 返回空列表
```

---

## 下一步

完成 Phase 2 后，进入 **Phase 3: 工具系统**（参考 `references/03-phase-tools.md`）