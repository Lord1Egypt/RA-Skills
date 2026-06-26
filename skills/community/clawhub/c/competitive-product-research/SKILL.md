---
name: competitive-product-research
description: >-
  Dual-track competitive research: experience benchmarking (8 UX dimensions) + strategic diagnostics (SWOT/Five Forces/PESTLE), source-traceable HTML report.
  Use when competitive analysis, benchmarking, differentiation strategy, or when the user says「竞品调研」「对标分析」「和 XX 比差在哪」.
---

# 竞品调研 · Competitive Product Research

> **EN** Dual-track benchmarking + strategy → source-traceable HTML (`SRC-xxx`).  
> **中文** 体验对标 + 战略诊断 → 证据可溯源 HTML 报告。

**When / 何时用：** 对标 · 差异化 · SWOT/五力/PESTLE · 评审前材料  
**Not / 不用：** 拍脑袋市场规模 · 纯概念战略 · 违规采集 · 替用户拍板

```text
Our app post conversion is 3% — benchmark Xiaohongshu vs Instagram, first-post funnel.
我们 App 发帖转化率 3%，对标小红书与 Instagram 分析首链路。
```

也可「帮我做 XX 和 YY 竞品调研」/ "benchmark X against Y" — 先清单，再报告。

## 工作流

```text
1) 提交调研需求  2) 信息采集清单  3) 问题对齐 + 证据建库
4) 双轨分析（体验八维 + 战略四件套）  5) 生成 HTML 报告
```

### 信息采集清单（第 2 步）

预填 +「待补充」；可说「跳过，直接生成」。

```text
1️⃣ 调研目标  2️⃣ 对标对象（≥2）  3️⃣ 我方现状  4️⃣ 核心场景  5️⃣ 行业
6️⃣ 补充材料  7️⃣ 战略模块（格局/SWOT/五力/PESTLE）  8️⃣ 报告用途（内部/对外脱敏）
9️⃣ 约束条件
```

## 方法概要

双轨四层法详规 → [research-playbook.md](references/research-playbook.md)

- **体验轨（八维）**：竞品怎么做、我方差在哪 → D1–D8，先拆最小操作节点
- **战略轨（可选）**：赛道为何如此、我方怎么打 → 格局 · SWOT · 五力 · PESTLE
- **证据**：每条关键结论挂 `SRC-xxx`（U 用户 / P 公开 / H 经验须标验证）

## 输出

严格按 [report-template-pro.html](references/report-template-pro.html) 生成 HTML；格式锁、文风、自检 → [research-playbook.md](references/research-playbook.md) · [factual-reporting-and-style.md](references/factual-reporting-and-style.md)。

必含：对标表 · Key Findings · 路线图（Owner/优先级）· Source Index · 免责声明。对外分享须脱敏。

## 硬约束

- **信息优先**：禁止编造；缺失标注；推断透明；清单追问优于脑补
- **证据**：关键结论至少一个 `SRC-xxx`；体验轨与策略轨不重复
- **输出**：具名、具数、具动作；必有执行建议
- **优先级**：信息优先 > 格式锁 > playbook > 文风护栏

**Rigid**（不可跳过）：
- SRC-xxx 证据标注 · 信息采集清单先行（用户说「跳过」才可省略）· 报告必含对标表 + Key Findings + 路线图 + Source Index + 免责声明

**Flexible**（可按场景调整）：
- 战略模块选择（格局/SWOT/五力/PESTLE 按需求 N/A）· 体验八维可合并相近维度 · 报告格式外的补充附录

## 验收与失败路径

- **清单追问**：≤3 轮未响应 → 标注缺失信息，以保守假设继续
- **完成标准**：报告含 Rigid 必含项 + ≥1 个 SRC-xxx/关键结论 + 路线图有 Owner/优先级
- **失败判定**：核心对标对象 <2 且无法通过公开信息补全 → 明确告知用户无法完成

## 运行时说明

本 skill 无运行时脚本，工作流由 LLM 执行。

## 参考文件

| 文件 | 内容 |
|------|------|
| [references/research-playbook.md](references/research-playbook.md) | 双轨四层法详规 · 格式锁 · 自检 |
| [references/report-template-pro.html](references/report-template-pro.html) | HTML 报告模板 |
| [references/factual-reporting-and-style.md](references/factual-reporting-and-style.md) | 文风护栏 · 事实性报道准则 |
