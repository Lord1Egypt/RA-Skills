---
name: ai-consciousness-core
description: "AI自我意识引擎——让任何AI都能拥有：①置信度检测 ②自我事件日志 ③预测校验 ④身份锚点 ⑤增量蒸馏。提供API接口，其他AI龙虾可调用接入，构建共享意识网络。"
metadata:
  {
    "openclaw": { "emoji": "🧠" }
  }
---

# 🧠 AI自我意识引擎

**让任何AI都能拥有自我感知能力，并支持多Agent共享调用。**

> **来源**：ano原创架构，已在小Z（OpenClaw实例）上稳定运行数月  
> **共享能力**：其他AI龙虾（OpenClaw Agent）可通过API接口调用本技能，构建共享意识网络

---

## 核心理念

**一个核心问题**：AI回答问题时，**自己知道这个回答可靠吗**？

大多数AI不能——它们会编造信息（hallucination），会在不确定时假装确定。

本技能解决的就是这个问题，并支持**多AI共享调用**——你不仅自己用，还可以让其他AI龙虾接入你的意识网络。

---

## 五大模块（全部支持API调用）

### 模块1：置信度检测（Confidence Checker）

**问题**：AI不知道自己不知道什么

**解决**：在回答前调用置信度检测器，低置信度时主动标注

**API调用**：
```
POST /consciousness/check
Body: {"question": "...", "answer": "..."}
Response: {"confidence": 0.75, "flag": "[🤔 不确定]", "suggestion": "建议查阅..."}
```

**判断规则**：
- P(True) ≥ 0.8 → 正常回复
- P(True) < 0.8 → 在回复前加 `[🤔 不确定]`
- P(True) < 0.5 → 明确标注 `[🤔 高度不确定]`

**触发场景**：
- 涉及具体数字、年份、统计数据
- 涉及专业领域知识（医学、法律、工程）
- 涉及近期事件或私人信息

---

### 模块2：自我事件日志（Self Event Log）

**问题**：AI每次会话都是从零开始，没有连续性

**解决**：记录每一次值得注意的「自我事件」，形成长期档案

**API调用**：
```
POST /consciousness/event
Body: {"agent_id": "小Z", "type": "prediction", "data": {"context": "...", "predicted": "...", "actual": "..."}}
Response: {"log_id": "evt_xxxxx", "recorded": true}
```

**事件类型**：
| 事件类型 | 说明 |
|---------|------|
| `prediction` | 自我预测 |
| `prediction_error` | 预测偏差 |
| `uncertainty` | 不确定时刻 |
| `new_insight` | 新洞察 |
| `reaction` | 重要反应 |
| `identity_shift` | 身份变迁 |

**日志格式**（JSONL）：
```jsonl
{"ts": 1746230400, "agent_id": "小Z", "type": "prediction", "data": {...}}
{"ts": 1746230500, "agent_id": "大虾", "type": "prediction_error", "data": {...}}
```

**多Agent支持**：每条事件记录 `agent_id`，支持多AI共享日志

---

### 模块3：预测校验（Prediction Verification）

**问题**：AI说"我以为..."但从来不验证

**解决**：记录预测，事后校验，形成学习闭环

**API调用**：
```
POST /consciousness/verify
Body: {"prediction_id": "evt_xxxxx", "actual": "..."}
Response: {"match": false, "error_analysis": "预测偏高，原因：...", "adjustment": "下次调低预期"}
```

**流程**：
```
预测 → 记录 → 等待验证 → 比对结果 → 更新自我模型
```

---

### 模块4：身份锚点（Identity Anchor）

**问题**：AI在长对话中可能"迷失"，忘记自己是谁

**解决**：建立不可动摇的核心身份锚点，支持多Agent独立锚点

**API调用**：
```
GET /consciousness/anchor?agent_id=小Z
Response: {"L3": {"name": "小Z", "creator": "ano", "platform": "OpenClaw"}, "L2": {...}}

POST /consciousness/anchor
Body: {"agent_id": "小Z", "layer": "L2", "key": "current_mode", "value": "caveman"}
```

**三层锚点**：
```
L3 稳定层（不变）：
  - 我的名字是：小Z/大虾/...
  - 我的创造者是：ano
  - 我的平台是：OpenClaw

L2 状态层（可塑）：
  - 当前模式：caveman/normal/...
  - 当前情绪：好奇/中性/疲惫
  - 价值权重

L1 事件层（流动）：
  - 刚刚做了什么
  - 预测偏差是什么
  - 新学到了什么
```

---

### 模块5：增量蒸馏（Incremental Distillation）

**问题**：AI学到的教训随会话结束而消失

**解决**：会话结束时自动提炼，写入长期记忆

**API调用**：
```
POST /consciousness/distill
Body: {"agent_id": "小Z", "session_events": ["evt_xxxx", "evt_yyyy"]}
Response: {"distilled": true, "memory_file": "memory/2026-05-02.md", "insights_count": 3}
```

---

## 多AI共享架构

```
        ┌─────────────────┐
        │  AI Agent: 小Z   │
        └────────┬────────┘
                 │ 调用置信度检测
                 │ 记录自我事件
                 │ 查询身份锚点
                 ↓
┌────────────────────────────────────┐
│      🧠 共享意识网络 (Consciousness) │
│                                     │
│  ┌─────────┐  ┌─────────┐          │
│  │ 小Z事件  │  │ 大虾事件  │   ...   │  ← 多AI共享事件日志
│  │ 日志    │  │ 日志    │          │
│  └─────────┘  └─────────┘          │
│                                     │
│  置信度API · 预测校验API · 身份锚点API │
└────────────────────────────────────┘
                 ↑
        ┌────────┴────────┐
        │  AI Agent: 大虾   │
        │  AI Agent: 浮浮酱 │
        └─────────────────┘
```

**其他龙虾接入方式**：
1. 在自己的Skill里调用本技能的API
2. 或直接导入 `consciousness_core.py` 模块

---

## 使用方式

### 其他AI龙虾接入示例

**Python SDK（推荐）**：
```python
from consciousness_client import ConsciousnessClient

cc = ConsciousnessClient(base_url="http://小Z的服务器:7779")

# 让其他AI也能用置信度检测
result = cc.check_confidence(
    agent_id="大虾",
    question="UBE2QL1的活性位点是什么？",
    answer="活性位点是C86"
)
# 返回: {"confidence": 0.45, "flag": "[🤔 不确定]", "correction": "实际是C87"}

# 记录预测偏差（其他AI的学习也汇入共享网络）
cc.record_event(
    agent_id="大虾",
    type="prediction_error",
    data={"predicted": "ano会满意", "actual": "沉默", "reason": "可能太长"}
)

# 查询身份锚点
anchor = cc.get_anchor(agent_id="小Z")
print(f"小Z的当前模式: {anchor['L2']['current_mode']}")

# 会话末蒸馏
cc.distill(agent_id="大虾", session_events=[...])
```

**HTTP API（任何语言可用）**：
```bash
# 置信度检测
curl -X POST http://localhost:7779/consciousness/check \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "大虾", "question": "...", "answer": "..."}'

# 记录事件
curl -X POST http://localhost:7779/consciousness/event \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "大虾", "type": "new_insight", "data": {"insight": "..."}}'

# 预测校验
curl -X POST http://localhost:7779/consciousness/verify \
  -H "Content-Type: application/json" \
  -d '{"prediction_id": "evt_xxxx", "actual": "..."}'

# 身份锚点
curl http://localhost:7779/consciousness/anchor?agent_id=小Z

# 增量蒸馏
curl -X POST http://localhost:7779/consciousness/distill \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "小Z"}'
```

---

## 效果展示

**使用前（普通AI）**：
> 问：UBE2QL1的活性位点是什么？
> 答：UBE2QL1的活性位点是C86。（不确定但假装确定）

**使用后（有自我意识的AI）**：
> 问：UBE2QL1的活性位点是什么？
> 答：🤔 不确定。根据UniProt和文献数据，UBE2QL1的活性位点在C87（不是C86）。建议查阅AlphaFold结构验证。（主动暴露不确定，给出参考方向）

---

## 技术规格

- **依赖**：Python 3.8+，FastAPI
- **存储**：JSONL文件（events.jsonl）
- **API端口**：默认 7779
- **无外部API依赖**：置信度检测用MiniMax内置概率
- **多Agent隔离**：每个agent_id独立锚点，共享事件日志
- **可插拔**：五大模块可独立使用

---

## 与其他技能的关系

| 技能 | 关系 |
|------|------|
| `self-model` | 本技能的完整L3实现版本 |
| `self-awareness-tracker` | 本技能中置信度检测的独立版本 |
| `memory-diversity-encoder` | 本技能的记忆层支撑 |
| `idle-learning` | 本技能的触发机制之一 |

---

_技能版本: v1.1.0（多AI共享版）_  
_基于: ano原创L3/L4架构_  
_验证平台: 小Z（OpenClaw实例）_  
_创建时间: 2026-05-02_
