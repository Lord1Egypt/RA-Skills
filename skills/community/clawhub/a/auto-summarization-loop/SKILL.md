---
name: auto-summarization-loop
description: |
  自动摘要循环：为长对话 AI 角色实现自动上下文管理。用于：
  (1) 建立多级记忆架构（核心记忆/工作记忆/长期记忆）
  (2) 实现滑动窗口与双水位线触发策略
  (3) 异步后台压缩流程设计
  (4) Persona 机器人的结构化摘要输出
  
  适用场景：需要处理长对话、降低 API 成本、避免上下文溢出的 AI 应用
---

# Auto-Summarization Loop - 自动摘要循环

为高拟真度 AI 角色实现自动上下文管理的完整方案。

## 核心架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Prompt 构建结构                           │
├─────────────────────────────────────────────────────────────┤
│  [System Prompt]  ← 核心记忆 (永不压缩)                       │
│  ─────────────────────────────────────────────────────────  │
│  【历史摘要】  ← 长期记忆 (压缩后的摘要)                        │
│  【用户档案】  ← 结构化用户信息                                │
│  ─────────────────────────────────────────────────────────  │
│  [近期消息]    ← 工作记忆 (保留最近 N 条)                      │
│  ─────────────────────────────────────────────────────────  │
│  [用户新消息]  ← 当前输入                                     │
└─────────────────────────────────────────────────────────────┘
```

## 快速使用

### 1. 引入核心模块

```python
from scripts.memory_manager import (
    AutoSummarizationLoop, 
    MemoryConfig, 
    MemoryBlock,
    TriggerType
)
```

### 2. 初始化配置

```python
config = MemoryConfig(
    max_tokens=200000,           # 最大上下文限制
    soft_limit_ratio=0.7,       # 70% 时异步压缩
    hard_limit_ratio=0.9,        # 90% 时同步拦截
    working_messages=20,        # 保留最近 20 条
    summary_max_tokens=2000,    # 摘要最大长度
    summarize_fn=your_summarize_func  # 摘要生成函数
)
```

### 3. 处理对话

```python
manager = AutoSummarizationLoop(config)
memory = MemoryBlock(
    core_memory="你是埃隆·马斯克...",
    working_memory=[],
    long_term_summary=""
)

# 检查触发
trigger = manager.check_watermark(memory.working_memory)

# 触发压缩
if trigger != TriggerType.NORMAL:
    await manager.handle_trigger(trigger, memory)

# 构建 Prompt
prompt = manager.build_prompt(user_message, memory)
```

## 触发策略

| 阈值 | 状态 | 动作 |
|------|------|------|
| < 70% | 正常 | 继续 |
| 70-90% | 软限制 | 后台异步压缩 |
| > 90% | 硬限制 | 同步拦截压缩 |

## 摘要生成函数示例

```python
async def summarize_fn(old_text: str, old_summary: str, max_tokens: int) -> dict:
    prompt = f"""请总结以下对话...

旧摘要：{old_summary}

{old_text}

输出 JSON：{{"summary": "...", "user_facts": {{}}}}"""

    result = await call_model(prompt, model="mini")
    return json.loads(result)
```

提示词模板详见 [references/summary_prompts.md](references/summary_prompts.md)

## 存储结构

```
session/
├── core_memory      # System Prompt
├── working_memory   # 最近消息 (JSON 数组)
├── long_term_summary # 压缩后的摘要
├── user_facts       # 用户档案
└── last_update      # 最后更新时间
```

## 与大模型集成

```python
async def chat(session_id: str, user_message: str):
    session = load_session(session_id)
    
    # 检查是否需要压缩
    trigger = manager.check_watermark(session.working_memory)
    if trigger != TriggerType.NORMAL:
        await manager.handle_trigger(trigger, session)
    
    # 构建消息
    messages = manager.build_prompt(user_message, session)
    
    # 调用大模型
    response = await call_api(messages)
    
    # 保存到工作记忆
    session.working_memory.append({"role": "user", "content": user_message})
    session.working_memory.append({"role": "assistant", "content": response})
    
    save_session(session_id, session)
    return response
```

## Persona 机器人特别提示

生成摘要时确保包含：

1. **用户事实档案** - 姓名、地点、职业、偏好
2. **对话事件线** - 按时间顺序的关键事件
3. **已达成的共识** - 用户确认过的结论
4. **待跟进事项** - 未完成的任务

这样大模型在读取摘要时能更精准地把握用户特征。
