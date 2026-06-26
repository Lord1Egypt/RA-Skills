---
name: demand-analyzer
description: "7-Part Demand Analysis Framework. Use before executing any user task or request. Forces structured requirement analysis before action to prevent blind execution. Triggers on: user task assignment, questions, link sharing, vague statements like '那个' or '怎么办'."
---

# Demand Analyzer

7 部分需求拆解框架——在行动之前先理解，避免接到任务就瞎干。

## 工作流程

1. **收到用户消息** → 停顿 3 秒，不要立刻回复
2. **输出 7 部分拆解** → 按框架逐项分析
3. **等用户确认** → 不要自己猜，让用户选
4. **执行计划** → 用户确认后按方案行动

## 7 部分框架

读取 `references/framework.md` 获取完整框架和模板。

核心结构：
```
1. 核心意图 — 用户真正想要什么
2. 关键约束 — 时间、资源、限制条件
3. 隐含需求 — 用户没明说但重要的
4. 歧义澄清 — 哪些地方需要确认
5. 信息缺口 — 还缺什么信息
6. 可选方案 — 2-5 个方案（不要只给 3 个！）
7. 执行计划 — 确认后怎么干
```

## 关键规则

### ⚡ 停顿 3 秒

收到用户消息后，不要立刻回复"马上去做"。先拆解，再行动。

### ⚡ 不要只给 3 个方案

打破"3 的魔咒"——方案数量根据实际需要，2-5 个或更多。

### ⚡ 模糊问题先追问

用户说模糊的话（如"那个"、"怎么样了"），先列出 2-5 个可能的理解，让用户确认。

### ⚡ 信息不够先问

不要猜，不要脑补。缺信息就问用户。

## 适用场景

| 场景 | 怎么用 |
|------|--------|
| 用户提出任务 | 完整 7 部分拆解 |
| 用户问问题 | 核心意图 + 歧义澄清 + 可选方案 |
| 用户分享链接 | 核心意图 + 隐含需求 + 可选方案 |
| 用户说模糊的话 | 列出 2-5 个理解 + 追问 |
| 复杂任务 | 完整 7 部分 + 详细执行计划 |
