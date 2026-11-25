# Principled Simplicity — Prompt Decompose / Prompt 解构

> **何时加载 / Load this when:** Prompt 越来越长、规则堆叠，或你在判断一条逻辑到底应该放在 prompt、code、memory 还是 skill。

**核心前提：** 不停增长的系统 Prompt，通常不是 Prompt 写法问题，而是一个**架构分配问题**。

## 五个桶 / Five Buckets

| Bucket | 定义 | 正确归宿 |
|---|---|---|
| **A. Stable knowledge** | 稳定事实、定义、产品信息 | Wiki / Memory / RAG |
| **B. Reusable procedure** | 可复用、有输入输出的方法 | Skill / Subflow |
| **C. Deterministic constraint** | 权限、Schema、格式、安全边界 | Code / Validator |
| **D. Semantic task** | 语言理解、判断、生成、歧义推理 | Prompt |
| **E. Architecture debt** | 未决产品逻辑、缺失模块、上游绕路 | Product / Architecture issue |

健康 Prompt 应尽量让模型只承担真正需要语义推理的 D 类任务。

## Procedure

1. 获取完整 Prompt。
2. 逐句标注 A/B/C/D/E。
3. 统计分布，识别膨胀来源。
4. 按 C → A → B → E → D 的顺序迁移和处理。
5. 只保留模型真正该做的语义任务，并跑回归。

## Standard Output

```text
## Bloat Diagnosis
Total length: ...
A. Stable knowledge: ...
B. Reusable methods: ...
C. Deterministic rules: ...
D. Semantic tasks: ...
E. Architecture debt: ...

## Migration Plan
1. ...

## Cleaned Prompt Draft
...

## Eval
- regression
- negative cases
- boundary cases
```

## Example — Routing prompt full of BUT rules

```text
Use web search for current facts, BUT use file search if...
Use CRM for customer data, BUT use email if...
Use calculator for numbers, BUT...
```

这通常不是 Prompt 写法问题，而是缺少独立的 routing / arbitration mechanism。

## Final Principle

Prompt 应该描述模型独有的工作：语义理解、判断、生成。

精简不是删规则，而是把规则**迁回正确层级**。
