---
name: continuation-patterns
description: |
  当用户在图中看到三角形、旗形、三角旗形、楔形、矩形等"价格中途歇脚"的图案，想判断趋势是否会延续时激活。
  持续形态与反转形态相反：它代表趋势暂停后**沿原方向突破**。也涵盖喇叭形（常是反转预警）与钻石形态。
  不适用于：头肩/双顶等反转图案（转 reversal-patterns）、通用支撑阻挡（转 trend-tools）。
  关键 trigger 词：三角形整理、旗形、楔形、矩形、箱体、持续形态、整理后继续涨、喇叭形。

  Activate when the user spots triangle, flag, pennant, wedge, rectangle, or similar "mid-trend resting" patterns and wants to judge whether the trend will continue.
  Continuation patterns are the opposite of reversal patterns: they represent a pause after which price **breaks out in the original direction**. Also covers broadening formations (often a reversal warning) and diamonds.
  Not applicable: head-and-shoulders / double-top reversal patterns (-> reversal-patterns), or generic support/resistance (-> trend-tools).
  Key trigger words: triangle consolidation, flag, wedge, rectangle, box range, continuation pattern, resume-after-consolidation, broadening formation.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第六章 持续形态
tags: [triangle, flag, wedge, rectangle, continuation, pattern]
related_skills:
  - slug: reversal-patterns
    relation: contrasts-with
  - slug: trend-tools
    relation: depends-on
---

# 持续形态：三角 / 旗形 / 楔形 / 矩形 / 喇叭 / 钻石

## R — 原文 (Reading)

> "价格形态具有两个类别：反转型和持续型。"
> "对称三角形、上升三角形、下降三角形……旗形和三角旗形……楔形……矩形。"
> "喇叭形中采用机械的突破信号入市，必受挫于一系列错误信号。"
>
> — 约翰·墨菲，第六章 持续形态

---

## I — 方法论骨架 (Interpretation)

持续形态是趋势的"中场休息"——形态完成后，价格**沿原趋势方向突破**继续走。识别要点：

1. **先定性反转还是持续**：同样一个图案，若出现在趋势中段多为持续，若出现在趋势末端多为反转。持续形态**规模通常小于**反转形态。
2. **三角形**：对称三角（等待突破方向）、上升三角（看涨，水平阻力+抬高底边）、下降三角（看跌）。突破伴随放量更可靠。
3. **旗形 / 三角旗形**：陡直的短暂回撤（旗杆后的小旗），**倾斜方向与主趋势相反**，完成后续涨/续跌，是强势中继。
4. **楔形**：倾斜的收敛通道，上升楔形多在下跌反弹中（偏空）、下降楔形多在上涨回调中（偏多）；注意它与三角形的区分。
5. **矩形**：水平箱体，突破方向延续原有趋势概率高。
6. **喇叭形（扩大三角）**：高点渐高、低点渐低、波幅放大、方向乱——**往往是反转预警而非跟随**，机械突破信号在此必受挫（ce14）。
7. **钻石形态**：由扩大三角+对称三角组成，常出现在顶部，偏反转。

**与反转的关键区别**：持续形态"歇脚后继续"，反转形态"到头了掉头"；且持续形态出现在趋势中途、规模较小。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：旗形作为强势中继
- **问题**：急速上涨后小幅回撤，是反转还是休息？
- **方法论的使用**：旗杆后的小旗形（倾斜与主趋势相反），完成后沿原方向突破继续涨。
- **结论**：旗形是中继，顺势续多而非反手。
- **结果**：区分"回调"与"反转"。

### 案例 2：喇叭形警示（ce14）
- **问题**：在喇叭形里反复跟突破会怎样？
- **方法论的使用**：喇叭形波幅无序扩大，机械突破信号连续出错。
- **结论**：喇叭形应视为反转预警，而非跟随突破。
- **结果**：避免在该形态中反复被扫。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 图上出现三角/旗形/楔形/矩形，问"这是整理还是反转、后面怎么走"。
2. 问"旗形/三角旗完成后是不是继续原趋势"。
3. 看到波幅不断扩大的喇叭形，问"还能不能跟突破"。

### 语言信号
- "三角形 / 旗形 / 楔形 / 矩形 整理"
- "这是持续形态还是反转"
- "整理完是不是继续涨/跌"
- "喇叭形"

### 与相邻 skill 的区分
- 与 `reversal-patterns` 的区别：本 skill 是"歇脚续行"，reversal 是"掉头"。
- 与 `trend-tools` 的区别：本 skill 是完整图案，trend-tools 是通用线/位。

---

## E — 可执行步骤 (Execution)

1. **定位趋势阶段**：确认形态处在趋势中段（持续）还是末端（可能反转）。
   - 完成标准：结合 trend-tools 判断主趋势方向。
2. **识别图案类型**：三角/旗形/楔形/矩形/喇叭。
   - 完成标准：对照各图案构件。
3. **等突破方向**：持续形态沿原趋势突破；喇叭形则预警反转。
   - 完成标准：放量突破确认。判停：喇叭形不机械跟突破。
4. **量度目标**：旗形用旗杆高度投影；矩形用箱体高度。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户看头肩/双顶（末端掉头）→ 转 reversal-patterns。
- 用户只问某条支撑线 → 转 trend-tools。

### 作者在书中警告的失败模式
- **喇叭形机械突破受挫**（ce14）：波幅无序扩大，突破多假，应视反转预警。
- **误把持续当反转**：同一图案位置不同性质不同，须先看趋势阶段。

### 作者的盲点 / 时代局限
- 形态主观；现代可用形态识别算法辅助，但"持续vs反转"的定性仍需结合趋势层级。

### 容易混淆的邻近方法论
- 上升三角形（持续·看涨）vs 头肩底（反转·看涨）：方向预期可能相同，但完成机制不同，勿混。

---

## 相关 skills
- contrasts-with: reversal-patterns
- depends-on: trend-tools

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
