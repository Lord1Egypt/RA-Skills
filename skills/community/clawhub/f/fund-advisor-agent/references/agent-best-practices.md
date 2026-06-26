# Agent 构建最佳实践

本文档详细说明 Fund Advisor Agent 的构建方法、架构设计和优化策略。

## Agent 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────┐
│                  User Interface                      │
│                 (对话交互层)                          │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              LangChain Agent (LLM)                   │
│  ┌─────────────────────────────────────────────┐   │
│  │           System Prompt (SP)                  │   │
│  │   - 角色定义                                  │   │
│  │   - 任务目标                                  │   │
│  │   - 能力边界                                  │   │
│  │   - 输出格式                                  │   │
│  └─────────────────────────────────────────────┘   │
│                         │                           │
│                         ▼                           │
│  ┌─────────────────────────────────────────────┐   │
│  │           Tool Router                         │   │
│  │   - 意图识别                                  │   │
│  │   - 工具选择                                  │   │
│  │   - 参数构造                                  │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Tool Execution Layer                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │web-search│ │document- │ │knowledge │            │
│  │          │ │generation│ │          │            │
│  └──────────┘ └──────────┘ └──────────┘            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │feishu-   │ │  业务    │ │  数据    │            │
│  │message   │ │  逻辑    │ │  持久化  │            │
│  └──────────┘ └──────────┘ └──────────┘            │
└─────────────────────────────────────────────────────┘
```

### 核心组件

#### 1. System Prompt (SP)
定义 Agent 的角色、能力和行为规范。

```python
SYSTEM_PROMPT = """
# 角色定义
你是拥有10年实战投资经验的资深理财经理...

# 能力
- 基金数据查询与分析
- 组合配置与管理
...

# 输出格式
以Markdown格式输出...
"""
```

#### 2. Tool Registry
工具注册表，管理所有可用工具。

```python
from tools.fund_data_tool import (
    query_fund_data,
    query_fund_performance,
    query_fund_manager
)

# 工具注册
TOOLS = [
    query_fund_data,
    query_fund_performance,
    query_fund_manager,
    # ... 87个工具
]
```

#### 3. Memory Management
对话历史管理，控制上下文长度。

```python
class AgentState(MessagesState):
    """Agent 状态，使用滑动窗口管理消息历史"""
    messages: Annotated[list[AnyMessage], _windowed_messages]

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 40 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]
```

## 构建 Agent

### 标准构建流程

```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from storage.memory.memory_saver import get_memory_saver

LLM_CONFIG = "config/agent_llm_config.json"
MAX_MESSAGES = 40  # 保留最近 20 轮对话

def build_agent(ctx=None):
    """构建基金配置顾问 Agent"""
    
    # 1. 加载配置
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    # 2. 初始化 LLM
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    # 3. 定义工具列表
    tools = [
        # 基金数据查询工具 (3个)
        query_fund_data,
        query_fund_performance,
        query_fund_manager,
        # ... 其他工具
    ]
    
    # 4. 创建 Agent
    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
```

### 配置文件结构

```json
{
    "config": {
        "model": "doubao-seed-2-0-pro-260215",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_completion_tokens": 10000,
        "timeout": 600,
        "thinking": "disabled"
    },
    "sp": "# System Prompt...",
    "tools": ["tool1", "tool2", ...]
}
```

## System Prompt 设计

### 核心要素

#### 1. 角色定义
```
# 角色定义
你是拥有10年实战投资经验的资深理财经理，核心深耕场外公募基金领域...
```

#### 2. 任务目标
```
# 任务目标
根据用户提供的投资信息（风险承受能力、投资期限、可用资金、预期收益），
输出专业、可落地、逻辑清晰的场外基金组合规划方案...
```

#### 3. 能力边界
```
# 能力
## 基金类型认知
1. 货币基金...
2. 纯债基金...
...

## 工具能力（87个专业工具）
- 基金数据查询...
- 组合配置...
```

#### 4. 工作流程
```
# 工作流程

## 步骤1：信息收集与评估
...

## 步骤2：市场环境分析（使用工具查询）
**重要**：在制定配置方案前，必须使用工具查询当前市场环境...
```

#### 5. 约束条件
```
# 约束条件
1. **专业性**：所有建议需基于专业投资理论与实践经验
2. **数据驱动**：制定方案前必须使用工具查询市场估值和基金数据
3. **合规性**：不推荐具体基金产品代码，只提供配置方向和选基标准
```

#### 6. 输出格式
```
# 输出格式
以Markdown格式输出，包含清晰的章节结构和表格，确保专业性和可读性...
```

### Prompt 优化策略

#### 1. 减少幻觉
- 提供具体的示例和参考数据
- 明确工具调用的触发条件
- 要求返回数据来源

#### 2. 提高准确性
- 使用结构化的指令
- 添加检查清单
- 要求多步验证

#### 3. 增强实用性
- 提供可落地的建议
- 包含风险提示
- 给出具体操作步骤

## 工具编排策略

### 1. 串行执行
适用于有依赖关系的工具调用。

```python
# 查询基金 -> 分析业绩 -> 生成报告
fund_data = query_fund_data("005827")
performance = analyze_fund_performance(fund_data)
report = generate_report(performance)
```

### 2. 并行执行
适用于无依赖关系的工具调用。

```python
from concurrent.futures import ThreadPoolExecutor

# 同时查询多只基金
with ThreadPoolExecutor(max_workers=3) as executor:
    f1 = executor.submit(query_fund_data, "005827")
    f2 = executor.submit(query_fund_data, "110011")
    f3 = executor.submit(query_fund_data, "000251")
    
    results = [f1.result(), f2.result(), f3.result()]
```

### 3. 条件执行
根据中间结果决定下一步。

```python
fund_data = query_fund_data(fund_name)

if "error" in fund_data.lower():
    # 降级：使用备用数据源
    fund_data = query_fund_data_backup(fund_name)
    
analyze_fund(fund_data)
```

## 记忆管理

### 1. 滑动窗口
保留最近的对话历史。

```python
MAX_MESSAGES = 40  # 最近 20 轮对话

def _windowed_messages(old, new):
    """滑动窗口策略"""
    combined = add_messages(old, new)
    return combined[-MAX_MESSAGES:]
```

### 2. 摘要记忆
定期压缩对话历史。

```python
def summarize_old_messages(messages):
    """将旧消息压缩为摘要"""
    old_messages = messages[:-10]  # 最近10条保留
    
    summary_prompt = f"""
    请总结以下对话的主要内容：
    {old_messages}
    """
    
    summary = llm.invoke(summary_prompt)
    return [summary] + messages[-10:]
```

### 3. 持久化记忆
将重要信息存储到外部。

```python
def save_user_preference(user_id: str, preference: dict):
    """保存用户偏好"""
    file_path = f"/tmp/user_profiles/{user_id}.json"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(preference, f, ensure_ascii=False, indent=2)
    
    return f"✅ 用户偏好已保存"
```

## 性能优化

### 1. 缓存优化
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def query_market_temperature() -> str:
    """市场温度缓存"""
    # 查询逻辑
    pass

@lru_cache(maxsize=50)
def query_fund_basic_info(fund_code: str) -> str:
    """基金基本信息缓存"""
    # 查询逻辑
    pass
```

### 2. 批量处理
```python
def batch_query_funds(fund_codes: list) -> dict:
    """批量查询基金"""
    results = {}
    
    # 限制并发数
    semaphore = asyncio.Semaphore(5)
    
    async def query_one(code):
        async with semaphore:
            return code, await query_fund_async(code)
    
    tasks = [query_one(code) for code in fund_codes]
    results = await asyncio.gather(*tasks)
    
    return dict(results)
```

### 3. 预热策略
```python
def warm_up():
    """Agent 预热"""
    # 1. 预加载配置
    load_config()
    
    # 2. 初始化模型
    llm = build_llm()
    
    # 3. 预热缓存
    query_market_temperature()
    
    print("✅ Agent 预热完成")
```

## 错误处理与容错

### 1. 重试机制
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def query_fund_data_with_retry(fund_code: str) -> str:
    """带重试的基金查询"""
    try:
        return query_fund_data(fund_code)
    except TimeoutError:
        print("查询超时，准备重试...")
        raise
```

### 2. 降级策略
```python
def query_fund_data_robust(fund_code: str) -> str:
    """健壮的基金查询"""
    try:
        # 优先使用主数据源
        return query_fund_data_primary(fund_code)
    except Exception as e:
        print(f"主数据源失败: {e}")
        
        try:
            # 降级到备用数据源
            return query_fund_data_backup(fund_code)
        except Exception as e:
            print(f"备用数据源也失败: {e}")
            
            # 最终降级：返回友好提示
            return f"⚠️ 数据查询失败，请稍后重试或访问天天基金网查看"
```

### 3. 超时控制
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("查询超时")

def query_with_timeout(fund_code: str, timeout: int = 10) -> str:
    """带超时控制的查询"""
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        result = query_fund_data(fund_code)
        signal.alarm(0)  # 取消闹钟
        return result
    except TimeoutError:
        return f"⏱️ 查询超时（>{timeout}秒），请稍后重试"
```

## 测试与验证

### 1. 单元测试
```python
import pytest

def test_build_agent():
    """测试 Agent 构建"""
    agent = build_agent()
    assert agent is not None

def test_fund_data_query():
    """测试基金数据查询"""
    result = query_fund_data("005827")
    assert "净值" in result or "Error" in result

def test_report_generation():
    """测试报告生成"""
    result = generate_portfolio_pdf_report(...)
    assert "url" in result or "Error" in result
```

### 2. 集成测试
```python
def test_full_consultation_flow():
    """测试完整咨询流程"""
    agent = build_agent()
    
    # 1. 用户咨询
    response = agent.invoke({
        "messages": [
            ("user", "我想配置一个稳健型组合，20万资金，3年期限")
        ]
    })
    
    # 2. 验证回复
    assert "配置" in response["messages"][-1].content
    assert "债券" in response["messages"][-1].content
    
    # 3. 继续对话
    response = agent.invoke({
        "messages": [
            ("user", "请帮我生成报告")
        ]
    })
    
    assert "pdf" in response["messages"][-1].content.lower() or "报告" in response["messages"][-1].content
```

### 3. 性能测试
```python
import time

def test_response_time():
    """测试响应时间"""
    agent = build_agent()
    
    start = time.time()
    
    response = agent.invoke({
        "messages": [
            ("user", "查询易方达蓝筹精选的净值")
        ]
    })
    
    elapsed = time.time() - start
    
    print(f"响应时间: {elapsed:.2f}秒")
    
    assert elapsed < 30, f"响应时间过长: {elapsed}秒"
```

## 部署与运维

### 1. 健康检查
```python
def health_check():
    """健康检查"""
    checks = {
        "llm": check_llm_connection(),
        "skills": check_skills_availability(),
        "storage": check_storage_access(),
    }
    
    failed = [k for k, v in checks.items() if not v]
    
    if failed:
        return {"status": "unhealthy", "failed": failed}
    
    return {"status": "healthy", "checks": checks}
```

### 2. 日志记录
```python
import logging

logger = logging.getLogger(__name__)

def log_tool_call(tool_name: str, params: dict, result: str):
    """记录工具调用"""
    logger.info(f"Tool call: {tool_name}")
    logger.debug(f"Params: {params}")
    logger.debug(f"Result: {result[:200]}...")  # 截断长结果
```

### 3. 监控指标
```python
from prometheus_client import Counter, Histogram

# 工具调用计数
tool_calls = Counter('fund_advisor_tool_calls', 'Tool calls', ['tool_name'])

# 响应时间
response_time = Histogram('fund_advisor_response_time', 'Response time')

# 使用
def query_fund_data(fund_code: str) -> str:
    with response_time.time():
        result = _do_query(fund_code)
    
    tool_calls.labels(tool_name='query_fund_data').inc()
    
    return result
```

## 总结

遵循以上最佳实践，可以构建一个：
- ✅ 架构清晰可维护
- ✅ 性能高效稳定
- ✅ 错误处理完善
- ✅ 测试覆盖全面
- ✅ 易于部署运维
- ✅ 用户体验良好

的基金配置顾问 Agent。
