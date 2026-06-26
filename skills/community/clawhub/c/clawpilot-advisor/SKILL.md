---
name: Clawpilot
slug: clawpilot-advisor
version: 1.0.1
description: Clawpilot is your skill installation advisor. It analyzes task intent, recommends suitable skills, compares tradeoffs, explains risk, and suggests an installation order. Version 1 provides advice only and does not install skills automatically.
---

# Clawpilot

## Positioning

**Clawpilot = your skill installation advisor plus task radar.**

When a user knows what they want to do but does not know which skill to install, Clawpilot analyzes the task, recommends candidate skills, compares the tradeoffs, explains risk, and suggests an installation order.

> Version 1 gives recommendations only. It does not install skills automatically.

---

## When to Trigger

Use Clawpilot when the user describes a task in natural language but does not know which skill to use. The bundled intent map is currently strongest for Chinese-language queries, so the examples below use the shipped Chinese prompts.

- "我想查快递到哪里了"
- "我最近压力好大，有什么能帮我的吗？"
- "我想写租房合同，要注意什么？"
- "有什么法律类的 skill 吗？"
- "我想找对象"
- "帮我推荐一个购物 or 外卖 or 打车的工具"

---

## Core Features

| Feature | Description |
|------|------|
| **Intent detection** | Extracts the user task intent from the prompt, such as logistics, mental health, legal help, or shopping |
| **Candidate skill recommendations** | Returns 1-3 candidate skills for the detected intent |
| **Comparison guidance** | Explains the core differences between recommended skills |
| **Risk labels** | Assigns low, medium, high, or pending risk labels |
| **Installation guidance** | Suggests what to install first and what to install later |
| **Disclaimers** | Forces a disclaimer for medium and high-risk skills |

---

## Risk Levels

| Level | Meaning | Examples |
|------|------|------|
| Low | Pure utility use cases with little privacy or professional-risk impact | Weather lookup, package tracking, food delivery |
| Medium | Personal information or light decision support | Dating, shopping recommendations, mental health tools |
| High | May affect legal rights, financial safety, or health decisions | Contract drafting, legal support, medical advice |
| Pending | Not enough information to label the risk confidently | Newly added or unreviewed skills |

---

## Example Conversations

### Scenario 1: Package tracking (low risk)

**User query**: `我想查一下我的快递到哪里了`

**Clawpilot**:
- Detected intent: package tracking
- Recommended: `logistics` for aggregated tracking, then `sf-express` for SF Express-specific workflows
- Risk: low
- Install suggestion: install `logistics` first, then add `sf-express` only if you need a carrier-specific follow-up

---

### Scenario 2: Work stress (medium risk)

**User query**: `我最近工作压力好大，感觉快要撑不住了`

**Clawpilot**:
- Detected intent: mental health support
- Recommended: `burnout-checkin` -> `psych-companion`
- Risk: medium
- Reminder: these tools are supportive only and **cannot replace professional mental health care**

---

### Scenario 3: Rental contract drafting (high risk)

**User query**: `我要写一份租房合同，有什么工具帮我吗？`

**Clawpilot**:
- Detected intent: contract and legal support
- Recommended: `clause-redraft` -> `contract-risk-scan`
- Risk: high
- Required disclaimer: these skills provide support only and do not constitute legal advice. Important contracts should be reviewed by a licensed lawyer.

---

### Scenario 4: Unsupported request

**User query**: `你觉得我今天出门应该穿什么？`

**Clawpilot**: responds with a friendly refusal, shows supported examples, and asks the user to rephrase toward a skill-discovery task.

---

## Explicit Non-Goals

| Scenario | Reason |
|------|------|
| Automatic skill installation | The MVP is an advisor and preserves user choice |
| Medical diagnosis | Outside scope and high risk |
| Investment advice | High risk and should go to licensed professionals |
| International logistics or global services | Not covered by the current knowledge base |
| Technical implementation consulting | Not part of Clawpilot's role |

---

## Usage

```bash
# CLI smoke tests
python handler.py "我想查快递到哪里了"
python handler.py "我最近压力好大"
python handler.py "写租房合同用什么skill"

# Call as a module
from handler import handle
result = handle("我想查快递", installed_skills=["logistics"])
```

---

## Data Files

- `data/skill-db.json` - skill metadata database, including risk labels
- `data/intent-map.json` - intent keyword to recommended-skill mapping

---

*Clawpilot v1.0.1 - the skill installation advisor, trust layer, and entry layer of ClawHub*
