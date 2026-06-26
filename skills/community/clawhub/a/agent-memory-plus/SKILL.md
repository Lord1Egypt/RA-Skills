---
name: agent-memory
description: 智能体底层记忆基础设施，提供感知记忆、短期语义桶（洞察驱动话题聚类+跨层关联索引）、长期8分类记忆（含反思记忆）、六维质量上下文重构、超然洞察池、链式推理增强、隐私配置和数据加密；当用户需要构建智能体记忆能力、管理对话上下文、实现长期记忆持久化、集成LangGraph状态管理或增强链式推理反思能力时使用；作为元技能强制常驻运行
always: true
dependency:
  python:
    - pydantic>=2.0.0
    - typing-extensions>=4.0.0
    - cryptography>=41.0.0
---

# Agent Memory System

## 任务目标

- 本 Skill 用于：为智能体构建完整的记忆能力基础设施
- 触发条件：**元技能，强制常驻运行**（`always: true`）
- 架构总览：详见 [references/architecture_overview.md](references/architecture_overview.md)

## 前置准备

### 依赖

```
pydantic>=2.0.0
typing-extensions>=4.0.0
cryptography>=41.0.0
```

### 存储路径（必需）

所有模块初始化时**必须指定存储路径**，由调用方根据运行环境决定：

```python
base_path = "./memory_data"
key_storage_path = f"{base_path}/keys"
sync_state_path = f"{base_path}/sync_state"
index_storage_path = f"{base_path}/memory_index"
credential_path = f"{base_path}/credentials"
```

### 凭证管理（可选）

用于安全存储敏感凭证，自动加密存储：

```python
from scripts.credential_manager import CredentialManager

cred_manager = CredentialManager(storage_path="./memory_data/credentials")
cred_manager.store("github_token", "ghp_xxxxx")  # 自动加密
token = cred_manager.get("github_token")         # 自动解密
```

## 操作步骤

### Step 0: 隐私配置（必需）

```python
from scripts.privacy import PrivacyManager, ConsentStatus

privacy_manager = PrivacyManager(user_id="user_123")

if privacy_manager.get_consent_status("memory_storage") == ConsentStatus.NOT_REQUESTED:
    privacy_manager.request_consent(
        consent_type="memory_storage",
        description="是否允许存储交互记忆以提供个性化服务？"
    )
```

### Step 1: 感知记忆

```python
from scripts.perception import PerceptionMemoryStore

store = PerceptionMemoryStore()
session_id = store.create_session()

should_store, reason = privacy_manager.should_store_memory("episodic", user_message)
if should_store:
    store.store_conversation(session_id, user_message, system_response)

situation = store.detect_situation()
```

### Step 2: 短期记忆

**推荐方式**：智能体判断语义分类后存储。

```python
from scripts.short_term import ShortTermMemoryManager
from scripts.types import SemanticBucketType

short_term = ShortTermMemoryManager()

item_id = short_term.store_with_semantics(
    content="用户想要实现登录功能",
    bucket_type=SemanticBucketType.USER_INTENT,  # 智能体判断
    topic_label="用户登录",                       # 智能体指定
    relevance_score=0.85,
)
```

**语义桶分类**：

| 桶类型 | 判断标准 | 示例 |
|--------|----------|------|
| TASK_CONTEXT | 与当前任务直接相关 | "实现登录功能" |
| USER_INTENT | 表达意图、目标 | "想要一个记忆系统" |
| DECISION_CONTEXT | 选择、决定 | "选择PostgreSQL" |
| KNOWLEDGE_GAP | 疑问、不知道 | "不知道如何实现SSO" |
| EMOTIONAL_TRACE | 情绪、感受 | "对进度感到焦虑" |

**话题聚合与提炼**：

```python
summary = short_term.get_topic_summary()        # 话题聚合摘要
topics = short_term.get_active_topics()         # 活跃话题

if short_term.should_extract():
    from scripts.short_term import AsynchronousExtractor
    AsynchronousExtractor(short_term, long_term).extract()
```

### Step 3: 长期记忆

```python
from scripts.long_term import LongTermMemoryManager

long_term = LongTermMemoryManager()
long_term.update_user_profile(profile_data)
long_term.apply_heat_policy()
```

### Step 4: 上下文重构

```python
from scripts.context_reconstructor import ContextReconstructor

reconstructor = ContextReconstructor()
reconstructor.bind_state_capture(capture)  # P0: 状态感知优化

context = reconstructor.reconstruct(situation, long_term.get_all_memories())
state_ctx = reconstructor.get_state_aware_context()

reconstructor.unbind_state_capture()
```

### Step 5: 洞察生成

```python
from scripts.insight_module import InsightModule

insight_module = InsightModule()
insight_module.bind_state_capture(capture)  # P1: 状态模式分析

insights = insight_module.process(context, long_term.get_all_memories())
high_priority = insight_module.get_high_priority_insights()
state_insights = insight_module.get_state_pattern_insights()  # P1新增

insight_module.unbind_state_capture()
```

### Step 6: 全局状态捕捉（LangGraph集成）

```python
from scripts.state_capture import GlobalStateCapture, StateEventType

capture = GlobalStateCapture(
    user_id="user_123",
    storage_path="./state_storage",
    default_ttl_hours=168,
)

# 从 LangGraph 同步
checkpoint_id = capture.sync_from_langgraph(
    state={"phase": "executing", "current_task": "create_memory"},
    node_name="executor",
)

# 检查点管理
checkpoints = capture.list_checkpoints(thread_id="thread_xxx")
state = capture.restore_checkpoint("cp_xxx")

# 事件订阅
subscription_id = capture.subscribe(
    event_types=[StateEventType.PHASE_CHANGE, StateEventType.TASK_SWITCH],
    callback=on_phase_change,
)
```

### Step 7: 工具管理

```python
# 记录工具使用效果
long_term.update_tool_usage(
    tool_name="code_interpreter",
    task_type="code_debugging",
    outcome="success",
    effectiveness_score=0.85,
    checkpoint_id=checkpoint_id,  # P0: 状态关联
    phase="executing",
    scenario="coding",
)

# 获取工具推荐
rec = long_term.get_tool_recommendation(
    task_type="code_debugging",
    phase="executing",    # P0: 状态过滤
    scenario="coding",
)
```

### Step 8: 链式推理增强（P0 新增）

**用途**：模型自检测反思、反思结果持久化、元学习数据提取。

```python
from scripts.chain_reasoning import ChainReasoningEnhancer
from scripts.types import ReflectionOutcome

# 初始化
enhancer = ChainReasoningEnhancer(
    state_capture=capture,
    short_term=short_term,
    long_term=long_term,
)

# 处理推理步骤（模型输出包含反思信号）
result = enhancer.process_reasoning_step(
    step={
        "thought": "分析用户需求...",
        "need_reflect": True,
        "reflect_reason": "检测到信息矛盾",
        "reflect_confidence": 0.85,
    },
    step_index=12,
    task_type="analysis",
)

if result["should_reflect"]:
    # 执行反思
    reflection_result = enhancer.execute_reflection(
        signal=result["signal"],
        context_snapshot=result["context_snapshot"],
    )

    if not reflection_result.passed:
        # 验证失败处理
        if reflection_result.need_verification:
            verification = enhancer.execute_verification(
                reflection_result=reflection_result,
                context_snapshot=result["context_snapshot"],
            )

            if verification.result == "failed":
                # 回退处理
                rollback_info = enhancer.handle_rollback(
                    step_index=12,
                    reason="验证失败",
                )

    # 持久化反思结果
    memory_id = enhancer.persist_reflection_result(
        trigger_record=result["trigger_record"],
        reflection_result=reflection_result,
        verification_result=verification if reflection_result.need_verification else None,
        final_outcome=ReflectionOutcome.CORRECTED,
    )
```

**LangGraph 集成**：

```python
# 作为节点嵌入工作流
workflow.add_node("reflection", enhancer.as_reflection_node())
workflow.add_node("verification", enhancer.as_verification_node())

# 条件边
workflow.add_conditional_edges(
    "reasoning",
    ChainReasoningEnhancer.should_reflect,
    {"reflection": "reflection", "continue": "next_node"},
)
```

**元学习数据提取**：

```python
# 提取训练数据（用于优化"何时反思"能力）
training_data = enhancer.extract_meta_learning_data(
    min_learning_value=LearningValue.MEDIUM,
    limit=100,
)
```

## 资源索引

### 核心脚本

| 脚本 | 用途 |
|------|------|
| [scripts/types.py](scripts/types.py) | 核心类型定义 |
| [scripts/perception.py](scripts/perception.py) | 感知记忆 |
| [scripts/short_term.py](scripts/short_term.py) | 短期记忆 |
| [scripts/long_term.py](scripts/long_term.py) | 长期记忆 |
| [scripts/context_reconstructor.py](scripts/context_reconstructor.py) | 上下文重构 |
| [scripts/insight_module.py](scripts/insight_module.py) | 独立洞察 |
| [scripts/state_capture.py](scripts/state_capture.py) | 状态管理 |
| [scripts/chain_reasoning.py](scripts/chain_reasoning.py) | 链式推理增强 |
| [scripts/privacy.py](scripts/privacy.py) | 隐私配置 |
| [scripts/encryption.py](scripts/encryption.py) | 数据加密 |
| [scripts/memory_index.py](scripts/memory_index.py) | 记忆索引 |

### 参考文档

| 文档 | 何时读取 |
|------|----------|
| [architecture_overview.md](references/architecture_overview.md) | 需要全局架构视角 |
| [memory_types.md](references/memory_types.md) | 深入理解记忆结构 |
| [activation_mechanism.md](references/activation_mechanism.md) | 优化激活策略 |
| [insight_design.md](references/insight_design.md) | 扩展预测能力 |
| [short_term_insight_guide.md](references/short_term_insight_guide.md) | 话题聚类与提炼决策 |
| [agent_loops_guide.md](references/agent_loops_guide.md) | Agent Loop 架构演进 |
| [chain_reasoning_guide.md](references/chain_reasoning_guide.md) | 链式推理增强集成 |
| [privacy_guide.md](references/privacy_guide.md) | 处理敏感数据 |

## 注意事项

1. **路径必传**：所有存储路径无默认值，必须显式传入
2. **隐私优先**：处理用户数据前必须初始化 `PrivacyManager` 并获取同意
3. **敏感数据**：系统自动识别密码、账号等敏感信息，默认不存储
4. **加密存储**：敏感数据推荐 AES-256-GCM 加密
5. **类型安全**：所有函数必须有类型注解，禁止使用裸 dict
6. **异步优先**：提炼、热度计算等后台异步执行
7. **超然洞察**：洞察模块独立运行，提供非强制性建议
8. **降级策略**：模块故障时自动降级，保证核心流程可用
9. **数据权利**：用户可随时导出、删除所有数据

## 快速开始

```python
from scripts.perception import PerceptionMemoryStore
from scripts.short_term import ShortTermMemoryManager, AsynchronousExtractor
from scripts.long_term import LongTermMemoryManager
from scripts.context_reconstructor import ContextReconstructor
from scripts.insight_module import InsightModule

# 初始化
perception = PerceptionMemoryStore()
short_term = ShortTermMemoryManager()
long_term = LongTermMemoryManager()
reconstructor = ContextReconstructor()
insight_module = InsightModule()

# 处理对话
session_id = perception.create_session()
perception.store_conversation(session_id, user_message, system_response)
situation = perception.detect_situation()

# 短期记忆 + 提炼
short_term.store_with_semantics(user_message, SemanticBucketType.USER_INTENT, "话题", 0.8)
if short_term.should_extract():
    AsynchronousExtractor(short_term, long_term).extract()

# 上下文重构 + 洞察
context = reconstructor.reconstruct(situation, long_term.get_all_memories())
insights = insight_module.process(context, long_term.get_all_memories())
print(insight_module.format_insights_for_context())
```
