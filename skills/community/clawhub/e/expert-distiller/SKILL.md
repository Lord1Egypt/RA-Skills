---
name: adaptive-expert-interview
description: Use when conducting an in-depth adaptive interview with a domain expert to extract structured Q&A pairs. Triggers include need to capture expert knowledge, decision frameworks, and cognitive boundaries through progressive questioning.
requirements: Python 3.9+
binaries:
  - python
---

# 自适应专家访谈

## Overview

通过多轮对话对领域专家进行自适应深度访谈，自动生成从易到难的问题，挖掘决策风格和领域认知，输出标准化的问答对。

## When to Use

- 需要从领域专家身上提取结构化知识
- 希望将隐性经验转化为显性原则
- 需要采集标准化的问答对供后续分析

## Workflow

### 1. 初始化访谈

收集用户输入（领域、专家定位、目标数量、聚焦关键词），然后运行：

```bash
python interview_engine.py init \
  --domain "领域名称" \
  --expert "专家定位描述" \
  --target 50 \
  --keywords "关键词1,关键词2" \
  --output ./interview_state.json
```

向用户展示预计时长和流程说明。

### 2. 获取状态上下文

每轮提问前，获取当前状态：

```bash
python interview_engine.py status --state ./interview_state.json
```

### 3. 生成问题

1. 读取 `prompts/generate_question.txt` 模板
2. 将状态信息填充到模板变量中
3. 将填充后的 Prompt 发送给 LLM
4. LLM 返回 JSON 格式的问题
5. 向用户展示问题

### 4. 获取回答

等待用户回答。

### 5. 分析回答

1. 读取 `prompts/analyze_response.txt` 模板
2. 填充当前问题和用户回答
3. 发送给 LLM 分析
4. LLM 返回 JSON 格式的分析结果

### 6. 更新状态

运行：

```bash
python interview_engine.py update \
  --state ./interview_state.json \
  --q-id 1 \
  --question "问题文本" \
  --answer "回答文本" \
  --analysis '{"dimension": "typical_cases", "needs_follow_up": false, "quality": "high"}'
```

引擎会自动：
- 更新进度
- 追踪话题覆盖
- 控制追问次数
- 检查阶段切换
- 判断是否进入快速模式

### 7. 循环

重复步骤 2-6，直到达到目标数量。

### 8. 导出结果

```bash
python interview_engine.py export \
  --state ./interview_state.json \
  --format jsonl \
  --output ./interview_result.jsonl
```

## 中断恢复

如果访谈需要中断：

```bash
python interview_engine.py snapshot \
  --state ./interview_state.json \
  --output ./interview_backup.json
```

## 优先级规则

执行时遵循以下优先级：
1. **不中断访谈** - 永远推进对话
2. **完成目标数量** - 达到设定目标
3. **控制时长** - 在承诺时间内完成
4. **挖掘深度** - 时间允许时追问

## 输出格式

JSON Lines，每行一个对象：

```json
{"q_id": 1, "phase": "warmup", "type": "choice", "dimension": "core_principles", "question": "...", "answer": "...", "timestamp": "..."}
```
