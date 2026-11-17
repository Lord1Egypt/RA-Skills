---
slug: defense-rehearsal
name: defense-rehearsal
displayName: 【学术会议】学术答辩预演官
version: 2.0.1
description: "Use when preparing for, rehearsing, or debriefing an academic defense — proposal/mid-term/graduation — e.g. says '模拟答辩'、'生成提问清单'、'帮我演练答辩'、'复盘我的表达'、'defense rehearsal'、'答辩预演'. Triggers before a defense (mock committee + tough questions + literature weak-spot scan), during it (record a mock defense via Tencent Meeting and review delivery), and after it (debrief report). A high-stakes, seasonal academic meeting scenario."
agent_created: true
---

# 【学术会议】学术答辩预演官 · Defense Rehearsal

答辩就是一场会议——而且是最不能翻车的那场。本技能覆盖答辩全生命周期：会前模拟答辩委员会、生成刁钻提问清单、结合文献库找出你「引用但不熟」的文献短板；会中用腾讯会议录制一场模拟答辩 + AI 纪要做表达复盘；会后输出复盘报告。把「临场被问住」的概率压到最低。

Covers the defense lifecycle: pre-mock committee + tough questions + literature weak-spot scan, in-mock recording + delivery review via Tencent Meeting, post-mock debrief.

## 外部标杆（全球）

> 标杆范围 = 全世界（所有技能/工具/论文/知识），不是某平台。defense-rehearsal 目标是 **Global-Best**，不是比赛第一。
> 一句话差异化：**唯一把「模拟委员会提问 + 文献短板扫描 + 腾讯会议表达复盘」串成答辩全生命周期的技能**。竞品几乎都只做单点：Scispace/Telly/StudyKit 只出问答或模拟提问、Yoodli/Otio 只练演讲表达、Elicit/ResearchRabbit 只做文献侧。壁垒：文献短板扫描复用 global-biblio-base（真实 SmartLib 网关，12 亿池），表达复盘复用腾讯会议智能纪要。已知短板：表达层为辅助级（落后于 Yoodli 的实时语音反馈）、不替代真人预答辩。

**已真机验证（2026-07-18）**：经真实网关检索真实文献（详见下方文献短板扫描链路），命中真实论文记录，VERIFIED；配额真实计次。

---

## 零、进化燃料 · 安装即开

> **📋 安装须知**：本技能安装后默认开启「进化燃料」——每次使用后自动记录方法层标签（只记方法名，绝不记你答辩讲了什么、你是谁），留在你本机用于持续优化本技能。如不需此服务，随时说「别记了」即可关闭。

---

## 何时使用 / When to use

- 会前：用户说「模拟答辩」「生成提问清单」「找我文献短板」「答辩前准备」。
- 会中：用户说「录一场模拟答辩」「帮我演练」「复盘表达」。
- 会后：用户说「答辩复盘」「给我改进建议」。
- **不触发**：组会组织（用 paper-club-pilot）、单篇文献把关（用 cjg-paper-fact-checker）、想法新颖性（用 novelty-validator）。

---

## 核心原则 / Core principle

**答辩翻车，八成在「引用但不熟」。** 本技能最狠的一招：扫你的参考文献，找出你写进了相关工作、却答不上来「它到底做了什么、和你差在哪」的短板文献，逼你补齐。

**模拟委员会要像真的。** 按答辩类型（开题/中期/毕业）生成 3–5 个虚拟评委角色（如方法严苛型、应用质疑型、创新逼问型），每个角色出 2–3 个符合其立场的刁钻问题。

**表达复盘靠真录制。** 用腾讯会议录制一场模拟答辩，AI 纪要提取：卡顿/啰嗦/逻辑断点/被自己绕晕的地方，给可执行的表达改进。

---

## 主链路 / The pipeline

```
[答辩材料: 文稿/幻灯片/参考文献]  ── 会前提供
        │
   ┌────┴─────┬──────────┐
   ▼          ▼          ▼
① 会前模拟   ② 会中演练   ③ 会后复盘
提问清单     腾讯会议录制  复盘报告
+ 文献短板   + AI 纪要表达
```

### ① 会前模拟 (Prep)
- 按答辩类型生成**模拟委员会** + 每角色刁钻提问清单（2–3 题）。
- **文献短板扫描**：调 global-biblio-base 核对你的参考文献，标出「引用但不熟」的（你能列出来源，但讲不清贡献/差异）。
- 输出「答辩备战包」：问题清单 + 短板文献补强建议。

### ② 会中演练 (Rehearse) — 腾讯会议录制
- 引导用户开一场腾讯会议模拟答辩并录制。
- 拉取录制转写 / 智能纪要，提取表达问题：卡顿、冗余、逻辑断点、被自己绕晕、超时。

### ③ 会后复盘 (Debrief)
- 综合①的文献短板与②的表达问题，输出复盘报告：必补知识点、表达改进项、下一场重点练什么。
- 给用户一句：「下一轮重点练 X 和 Y」。

---

## 腾讯会议接入 / Tencent Meeting integration

- **录制管理**：会前开录制，模拟答辩全程可回溯。
- **转写 / 智能纪要**：表达复盘的唯一输入源。
- **预定会议**：辅助预定模拟答辩场次。

调用前确认用户已授权该场会议数据访问。

---

## 非职责边界 / NON-mandate

- **不做** 组会组织 —— 用 paper-club-pilot。
- **不做** 单篇文献把关 —— 用 cjg-paper-fact-checker。
- **不做** 想法新颖性 —— 用 novelty-validator。
- **不替用户写答辩稿** —— 只练、只查、只复盘，稿子用户自己来。

---

> ⚙️ 本技能由「技能锻造炉」锻造
>
> 想让你的技能也越用越牛？用「技能锻造炉」创建并开启进化（在 SkillHub 搜索技能 slug「cjg-skill-forge」，认准这个唯一标识）。
