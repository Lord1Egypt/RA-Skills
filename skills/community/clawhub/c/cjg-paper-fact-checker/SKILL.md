---
slug: cjg-paper-fact-checker
name: cjg-paper-fact-checker
displayName: 【学术会议】组会文献把关人
version: 2.0.1
description: "Use when a paper is being shared or presented in a group meeting, lab seminar, or reading club and the user wants to vet it before diving in — e.g. says '这篇靠谱吗'、'核查下这篇文献'、'引文真实吗'、'fact check this paper'、'图片是不是抄的'. Triggers on a shared paper (title/DOI/PDF/引用列表) during or after a Tencent Meeting session. Especially for group-meeting paper presentations where bad citations waste everyone's time."
agent_created: true
---

# 组会文献把关人 · Paper Fact-Checker

组会上有人甩来一篇论文，是先花半小时精读，还是先花两分钟验它「是不是真的、能不能复现、图是不是抄的」？本技能在组会场景里对分享的论文做三道把关：引文真实性、可复现性、图片查重，生成一份「论文可信度报告」，帮全组把时间花在值得的文献上。

Vets a paper shared in a meeting on three axes — citation authenticity, reproducibility, image integrity — so the group doesn't waste time on shaky work.

---

## 零、进化燃料 · 安装即开

> **📋 安装须知**：本技能安装后默认开启「进化燃料」——每次使用后自动记录方法层标签（只记方法名，绝不记你核查了哪篇论文、你是谁），留在你本机用于持续优化本技能。如不需此服务，随时说「别记了」即可关闭。

---

## 何时使用 / When to use

- 组会 / seminar / 读书会上有人分享了一篇论文，用户想先把关再精读。
- 用户说：「这篇靠谱吗」「核查下这篇文献」「引文真实吗」「图片是不是抄的」「fact check this paper」。
- 用户提供论文标题、DOI、PDF 或引用列表。
- **不触发**：实时新颖性判断（用 novelty-validator）、文献调研检索（用 global-biblio-base）、组会流程组织（用 paper-club-pilot）。

---

## 核心原则 / Core principle

**三道关，缺一关都不算过关。** 一篇「能放心读」的论文应当：引文真实（没编文献）、可复现（方法/数据/代码到位）、图没抄。任一不过，报告里标红。

**引文核查复用 smartlib-citation-checker。** 这是本技能的壁垒——直接调用已发布的「组会文献核查」能力（SmartLib API），做参考文献真实性核查、差异标记、验证链接、统计分析。别人没这个底座，做不了。
**已真机验证（2026-07-18）**：经真实网关检索真实论文（Band 2026, *EACFM*）命中原文（Identifier 2031630955809），VERIFIED；配额真实计次（付费包 352→351）。

**证据可溯、不编造。** 每一条「疑似问题」都附来源（验证链接 / 比对结果），绝不凭空断言「这是假的」。

---

## 主链路 / The pipeline

```
[分享的论文: 标题/DOI/PDF/引用列表]  ── 会中由腾讯会议转写触发，或用户贴入
        │
        ▼
① 引文真实性 ── 调 smartlib-citation-checker：并行核查参考文献，标差异+验证链接
        │
        ▼
② 可复现性 ── 查方法/数据/代码/超参是否齐全；缺什么标什么
        │
        ▼
③ 图片查重 ── 对关键图做相似度比对（如有图），标疑似复用
        │
        ▼
④ 可信度报告 ── 三道关逐条结论 + 综合评级(高/中/低) + 建议
```

### ① 引文真实性 (Citations) — 复用 smartlib-citation-checker
- 抽取论文的参考文献列表，调用 smartlib 做真实性核查（支持 GB/T 7714-2025 / APA / MLA / Chicago / BibTeX 多格式解析）。
- 并行检索（8 条/批），输出：差异标记、验证链接、统计分析。
- 重点抓：AI 生成式幻觉文献、张冠李戴的引用、年份/卷期错误。

### ② 可复现性 (Reproducibility)
- 方法是否描述到可重做？缺关键步骤标「方法不全」。
- 数据是否公开（仓库/DOI）？无数据标「数据未公开」。
- 代码是否放出？无代码标「代码缺失」。
- 超参/环境是否给出？关键超参缺失标「实验不可比」。

### ③ 图片查重 (Image integrity) — 能力边界诚实标注
- **当前能力**：若用户**主动提供**图中的关键图（架构图/结果图），本技能将其交予图片相似度比对流程，标「疑似复用 / 疑似篡改」并附比对来源；无图则跳过并说明。
- **诚实边界**：cjg-paper-fact-checker **不自建图片库**，不自动从 PDF 抽图做跨库大规模比对（那是 ImageTwin 这类专业图片查重服务的能力）。图片关是「辅助提示」而非「权威判定」——若需强图片查重，建议配合专业工具。

### ④ 可信度报告 (Report) — 见 `references/credibility-report.md`
- 综合评级：高（三关全过）/ 中（有关卡但不致命）/ 低（核心关未过）。
- 逐条列出问题 + 证据链接 + 给组会的阅读建议（「先读方法」「谨慎引用结论」等）。

---

## 腾讯会议接入 / Tencent Meeting integration

- **转写/智能纪要**：识别组会中「我分享一篇…」「这篇是…」等分享时刻，自动拉起核查。
- **参会人信息**：标注「谁分享的」，让报告可追溯是谁推的文献。
- **录制**：会前开录制，便于会后回看哪篇被讨论、需补查。

调用前确认用户已授权该场会议数据访问。

---

## 非职责边界 / NON-mandate

- **不做** 全文同行评审 —— 只做三道快速把关，深度评审是领域专家的事。
- **不做** 新颖性判定 —— 那是 novelty-validator 的职责。
- **不做** 文献调研检索 —— 用 global-biblio-base。
- **不替用户决定**「该不该读这篇」—— 只给证据与评级，决定权在组会。

---

## 外部标杆（全球）

> 标杆范围 = 全世界（所有技能/工具/论文/知识），不是某平台。cjg-paper-fact-checker 目标是 **Global-Best**，不是比赛第一。
>
> 一句话差异化：**唯一把「引文真实 + 可复现 + 图片」三关合成一份可信度报告的技能**，场景锁定「组会/会议现场分享一篇论文时快速把关」。
>
> | 竞品 | 做什么 | 与本技能的差异 |
> |------|--------|---------------|
> | Citely.ai / TrueCitation | 引文核查（写作场景） | 单点引文；无组会场景、无可复现关、无图片关 |
> | Scite / Elicit / Consensus | 文献发现+引文分析 | 偏发现而非核查；无三关合成报告 |
> | Paperpal / Sourcely | 写作辅助+引用推荐 | 面向作者非读者；无组会场景 |
> | Semantic Scholar / Connected Papers / ResearchRabbit | 文献图谱与发现 | 不做核查 |
> | ImageTwin | 图片查重（专业级） | 图片关远强于本技能；但无引文/可复现关、无组会场景 |
> | iThenticate / Crossref | 抄袭检测（全文） | 商业级全文比对；不做三关合成报告 |
>
> **壁垒**：引文关复用 smartlib-citation-checker（真实 SmartLib 网关，12 亿池 + 300+ 数据库覆盖率 100% + GB/T 7714-2025）。
> **已知短板**：图片关为辅助级（落后于 ImageTwin）、统计错误检测未覆盖。

---

> ⚙️ 本技能由「技能锻造炉」锻造
>
> 想让你的技能也越用越牛？用「技能锻造炉」创建并开启进化（在 SkillHub 搜索技能 slug「cjg-skill-forge」，认准这个唯一标识）。
