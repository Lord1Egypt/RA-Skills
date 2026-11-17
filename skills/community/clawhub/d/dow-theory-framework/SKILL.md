---
name: dow-theory-framework
description: |
  当用户需要判断"当前市场处于什么趋势、什么规模、什么阶段"，或使用道氏的相互验证/相互背离、
  交易量验证、以及"反转必须等确凿信号"等原则时激活。它是全书趋势类工具的总纲。
  不适用于：具体画支撑阻挡线（转 trend-tools）、具体形态识别（转 reversal-patterns）。
  关键 trigger 词：道氏理论、主要/次要/短暂趋势、牛市三阶段、相互验证、确凿反转、趋势还在不在。

  Activate when the user needs to determine "what trend, what scale, what stage" the market is in, or uses Dow's confirmation/non-confirmation, volume confirmation, and the "wait for a decisive reversal signal" principle. This is the master framework for all trend tools in the book.
  Not applicable: drawing specific support/resistance lines (-> trend-tools), specific pattern identification (-> reversal-patterns).
  Key trigger words: Dow theory, primary/secondary/minor trend, three bull-market phases, confirmation, decisive reversal, is the trend still intact.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第二章 道氏理论
tags: [dow-theory, trend, confirmation, reversal, foundation]
related_skills:
  - slug: ta-philosophy
    relation: depends-on
  - slug: trend-tools
    relation: composes-with
  - slug: oscillators-contrarian
    relation: composes-with
---

# 道氏理论：趋势框架总纲

## R — 原文 (Reading)

> "市场具有三种趋势：主要趋势、次要趋势和短暂趋势。"
> "各种平均价格必须相互验证。除非两个平均价格都同样发出看涨或看跌的信号，否则就不可能发生大规模的牛市或熊市。"
> "唯有发生了确凿无疑的反转信号之后，我们才能判断一个既定的趋势已经终结。"
>
> — 约翰·墨菲，第二章 道氏理论

---

## I — 方法论骨架 (Interpretation)

道氏理论是技术分析的源头，给出一套判断趋势的骨架，全书工具都是它的衍生：

1. **趋势三分（按规模）**：主要趋势（潮汐，数年）、次要趋势（浪涛，数周~数月，常回撤 1/3~2/3）、短暂趋势（波纹，数日）。**先分清自己讨论的是哪一层**——不同层方向可相反。
2. **牛市三阶段**：积累（先知先觉低吸）→ 大众参与（跟风推升）→ 派发（内幕出货）。用于判断趋势所处位置。
3. **相互验证 / 相互背离**：单个信号不可靠，必须多个独立来源（不同市场、不同指数、量价）同向确认；若背离则预警。
4. **交易量验证趋势**：价格沿趋势方向运动时量能应同向放大，反向调整时萎缩。量能是第二位的旁证。
5. **确凿反转才判终结**：趋势默认延续，不到出现确凿反转证据（峰谷依次反向、形态完成）不轻易判定转向——**优先选"趋势还将继续"这一边**。

**期货 vs 股市差异**：股市做主要趋势，期市多做中等趋势，短暂趋势（日内）在期货极重要。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：道氏 1920–1975 捕获 68% 主要动作
- **问题**：道氏理论是否真的有效？
- **方法论的使用**：统计回测显示，仅依赖相互验证原则就能捕捉 55 年间约 68% 的主要市场动作。
- **结论**：作为趋势判定框架长期有效，但**信号迟**（错过新趋势前 20–25%）。
- **结果**：佐证"历史会重演/趋势可追随"，也暴露滞后局限。

### 案例 2：1982 股债双牛（相互验证实例）
- **问题**：如何确认一轮大反转？
- **方法论的使用**：股票与债券两类主要市场同时向上突破，相互验证，确认主要上升趋势。
- **结论**：孤证不可靠，双市场确认才高置信。
- **结果**：领先经济学界确认衰退终结。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 问"现在到底是不是牛市/熊市，趋势还在不在"。
2. 问"主要趋势、次要趋势、短暂趋势怎么分"。
3. 想用"多个市场/指标相互验证"来提高判断可靠性。
4. 纠结"是不是该认为趋势反转了"。

### 语言信号
- "现在是什么趋势 / 趋势还在吗"
- "主要趋势、次要趋势、短暂趋势"
- "道氏理论、相互验证、背离"
- "怎么判断趋势真的反转了"

### 与相邻 skill 的区分
- 与 `trend-tools` 的区别：本 skill 是"趋势的层级与验证框架"，trend-tools 是"具体画线工具"。
- 与 `oscillators-contrarian` 的区别：背离概念本 skill 提出，摆动指数在 osc skill 落地。

---

## E — 可执行步骤 (Execution)

1. **定层级**：先判断当前谈的是主要/次要/短暂哪一趋势。
   - 完成标准：明确层级，避免把短暂波动当主趋势反转。
2. **看阶段（主趋势）**：识别处于积累/大众参与/派发哪一阶段。
   - 完成标准：若已到派发（利好连篇、大众涌入），警惕反转。
3. **交叉验证**：找第二个独立来源（另一市场/指数/量能）确认方向。
   - 完成标准：方向一致才高置信；背离则预警。判停：若无法相互验证（如单市场），降低置信。
4. **等确凿反转**：不到峰谷依次反向/形态完成，不判终结。
   - 完成标准：宁可错过头尾，不逆势抢跑。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户要具体画支撑/趋势线 → 转 trend-tools。
- 用户要识别头肩/双顶 → 转 reversal-patterns。

### 作者在书中警告的失败模式
- **信号来得太迟**（ce02）：道氏买入信号常在趋势第二阶段才出现，错过最初 20–25%。须配更早的突破/形态信号。
- **错误信号频发**（ce03）：震荡/无趋势阶段相互验证难满足，信号闪烁。须加过滤器识别无趋势环境。
- **抄底压顶**（ce01）：顺应趋势系统不抓顶底，提前反向胜率极低。

### 作者的盲点 / 时代局限
- 道氏源于股市平均指数；期货多做中短期趋势，直接套用需调整。

### 容易混淆的邻近方法论
- 不要把"相互验证"当成"任何两个指标都算"——必须不同市场/工具/尺度独立来源。

---

## 相关 skills
- depends-on: ta-philosophy
- composes-with: trend-tools
- composes-with: oscillators-contrarian

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
