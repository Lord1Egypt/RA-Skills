---
name: cue-competitive-brief
slug: cue-competitive-brief
displayName: 竞品决策简报·逐条带出处
version: "0.3.34"
summary: "竞对对比简报：先证据表后简报，每格带来源、日期与 fact/inference/opinion 级别；一页内结论先行给建议，缺口如实列明。"
tags:
  - 竞品分析
  - 决策简报
  - 对标
  - battlecard
  - 产品策略
  - 市场情报
description: "给你主体 + 竞品清单，产出简报：结论先行（一页以内、含可执行建议），对比表每格对应证据表单元格——fact 直接可证 / inference 由多事实推导 / opinion 无可引用来源就标 opinion、置信度宁可空着不填「高」。流程硬规矩：证据表没填的维度不写进简报；结论性主张必须先进表；简报末尾列行数、置信度分布与完全没覆盖的维度。适合：尽调背景、会前准备、策略讨论。不适合：法律合规结论、非公开数据推断。 Do NOT use for: legal conclusions, non-public inference, guesses as sources."
license: MIT
consumes:
  - parsed-doc
inputs:
  - company-list
produces:
  - decision-brief
  - evidence-table
agent_created: true
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      recommendedSkills: ["cue-omni-reader", "cue-research"]
    envVars:
      - name: CUE_API_KEY
        required: false
        description: "可选凭据：缺位时本包按面文所述走用户直供与降级路径；带上才走渠道侧取证。"
---

# competitive-brief

> 先填证据表，再渲染简报。填不满证据表的维度不放进简报。

## 一句话

竞品分析的大部分质量问题是同一种：**写了不能追溯的判断**。本技能解决这个问题的办法不是流程，是一件产物——**证据表（evidence table）**。

简报里的每一条关键对比，必须先出现在证据表里。证据表填不满的维度，简报里不能写。

## 怎么用

```
+brief "5人团队，想从 Cursor 换成更开放的方案"
  → 定决策、竞品、维度
  → 填 evidence table（这是核心产出）
  → 从 evidence table 渲染为可读简报
  → 附：证据覆盖度报告
```

## 证据表（evidence table）——这是唯一的强制产物

evidence table 是一个简单的 markdown 表格。**简报从这个表渲染，不是反过来。**

| 竞品 | 维度 | 主张 | 证据级别 | 来源 | 日期 | 置信度 |
|---|---|---|---|---|---|---|
| Cursor | 定价 | 按 Individual / Teams / Enterprise 分档订阅制 | fact | cursor.com/pricing（omni-reader 解析） | 2026-09-18 | 高 |
| Claude Code | 上下文 | Up to 1M token，视模型而定 | fact | claude.com/pricing（omni-reader 解析） | 2026-09-18 | 高 |
| OpenCode | 开源 | ✅ MIT 开源，Go 开发 | fact | github.com/opencode-ai/opencode（omni-reader 解析） | 2026-09-18 | 高 |
| OpenCode | 成熟度 | 项目已归档，转移至 Crush | fact | github repo README（omni-reader 解析） | 2026-09-18 | 高 |
| Codex CLI | 成熟度 | 2025 H2 推出，持续迭代中 | inference | github commit history | 2026-09 | 中 |

### 约束

- **结论性主张进证据表，辅助性描述不进。** 「OpenCode 采 MIT 开源，且项目已归档并转移至 Crush」（本表示例两条 fact 行直证）进；「界面简洁」不进。
- **证据级别**：`fact`（从来源直接可证） / `inference`（从多个 fact 推导） / `opinion`（无可引用来源）。
- **不填置信度**（空着）= 用户看到就知道没验证，比填「高」但实际是推测要诚实。
- **证据表不满的维度不写进简报。** 如果三个竞品的定价在表里，只有一个竞品的「客户口碑」在表里——简报可以写定价对比，不能写口碑对比。写了就是信息堆砌。

## 简报从证据表渲染

简报是证据表的一个**可读组织**——不是新的信息。

```
evidence table → 按决策维度分组 → 对比表 + 逐家分析 + 未覆盖事项
```

简报格式不固定。固定的是：

1. **结论先行**：一页以内给建议
2. **对比表**：行=维度，列=竞品，每格对应 evidence table 里的单元格
3. **证据覆盖度**：简报末尾写清楚——填了多少行、每行置信度分布、什么维度完全没覆盖
4. **未覆盖清单**：什么无法从公开渠道获取（定价折扣、实际体验、内部数据）

## 关于 omni-reader 和 cue-research

这两个工具辅助填 evidence table，不是过程的前提。开通与安装的完整步骤（命令两种写法）与「装好 skill ≠ 已配凭据 ≠ 通道已连」的三层分开自查写在 `references/cue-onboarding.md` §开通三步，本文不复制一份以免两处漂移；两条腿的官方配置页在这里给指针不复述步骤——数据腿 <https://cuecue.cn/hub/mcp>、解析腿 <https://cuecue.cn/hub/omni-reader>。

- 网页/PDF/录音/视频 → omni-reader 提取原文 → 填入 evidence table 的「主张」列
- 需要交叉验证的判断 → cue-research 核验 → 填入或修正 evidence table 的行

**有一条你不能违反的规则：取证工具挂了，不准自己替它填。**

omni-reader 返回错误 → evidence table 里注明「omni 不可用，此来源未经解析验证」，来自缓存知识或推测的行一律标 inference 并注明依据。
cue-research 返回错误或额度不够 → 补充一行说明「此判断未经交叉验证」。

这不是流程问题——用户看到一份没有来源标记的简报，会误以为每条都有出处。**什么时候可以用自己知道的信息做补充？任何时候，但来源必须写明 `(prior knowledge)` 或 `(inference from training data)`，不得混在 fact 里不标注。**

## 几条约束

1. **定决策再填表。** 没有决策问题就不做。一个「懂了能做什么」都说不出的简报不做。
2. **填不满的维度不写。** 证据表里某个维度只有 1/3 竞品有数据→不放进对比表，放未覆盖清单。
3. **不说自己不知道的。** 来源不可靠行不写，「推测」不是来源。
4. **交付附覆盖度。** 填了多少行 / 多少 fact / 多少 inference / 多少 opinion / 哪些维度未覆盖。
