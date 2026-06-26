---
name: deep-stock
description: "Professional stock analysis framework — 6-step deep dive from macro to valuation, powered by Charlie V3.0 methodology."
---

# Deep Stock 🎯
## 一套框架，穿透噪音

> 大多数股票分析工具告诉你一只股票*过去*发生了什么。  
> Deep Stock 告诉你它*现在*值多少钱——以及现在是不是该行动的时机。

---

**Charlie 是谁？** → Charlie 致敬 **查理·芒格（Charlie Munger）**——他的多元思维模型和人类误判心理学是这个框架的底层基因。

## 你用它会得到什么

- ✅ **专业级分析**（以前得找卖方分析师才能拿到的东西）
- ✅ **6步系统框架**（宏观→行业→公司→估值→概率→决策）
- ✅ **贝叶斯概率更新**（不是拍脑袋猜）
- ✅ **内置反面论证**（防止确认偏误）

这不是又一个股票筛选器。这是**一套思考框架**——每一步都强制你严谨。

---

## 怎么用

就一句话：

> **"分析 [股票名/代码]"**

然后 Deep Stock 自动跑完整 6 步流程：

```
① 数据采集     → 股价、财报、新闻、股东数据
② 宏观过滤     → 国际 → 国内 → 行业 → 公司（4层）
③ 估值分析     → PE-TTM / PEG / DCF / SOTP + 可信度评级
④ 贝叶斯更新   → 概率加权情景推演，告别主观猜测
⑤ 反面论证     → 强制找反面证据（芒格25种误判）
⑥ 决策矩阵     → 综合评分 → 买入/持有/减仓/观望
```

每一步的完整方法论在 **Charlie V3.0 框架**（12章，随 Skill 附送）。

---

## 一份典型报告长什么样

分析一只股票后，你会得到这样的深度报告：

```
┌─────────────────────────────────────────────┐
│ Deep Stock · 分析报告                       │
│ 目标：小米集团 (01810.HK)                     │
│ 日期：2026-05-26（一季报后）                   │
└─────────────────────────────────────────────┘

📊 第一层：宏观过滤
  国际形势 → [分析]
  国内政策 → [分析]
  行业发展 → [分析]
  公司层面 → [分析]

📈 第二层：估值分析
  PE-TTM:   22.5x (行业均值 28x)  → ⭐⭐⭐⭐
  PEG:      0.8x                  → ⭐⭐⭐
  DCF:      HK$48.2/股            → ⭐⭐⭐
  SOTP:     HK$52-58/股           → ⭐⭐⭐⭐

🎯 最终结论：买入（65%置信度，±8%）
```

---

## 适合谁用

| 你是... | Deep Stock 帮你... |
|---------|-------------------|
| 个人投资者 | 用结构化流程做买卖决策 |
| 长线持仓者 | 季度复盘持仓逻辑是否依然成立 |
| 学习型投资者 | 理解一只股票*为什么*值这个价 |
| 厌倦拍脑袋交易的人 | 用概率加权逻辑取代情绪 |

---

## 快速开始

```bash
# 1. 安装
clawhub install deep-stock

# 2. 开始分析
#    直接说：
#    "分析比亚迪"
#    "分析 002594.SZ"
#    "用 Deep Stock 分析小米"
```

---

## ⚠️ 使用须知

### 1. 数据深度靠你追问

AI 的默认行为是够用就停。你第一句说"分析比亚迪"，它可能只拉 2-3 个数据源就出报告了。

**建议用法：**
- 先问："分析比亚迪"
- 觉得不够深 → "财报数据再详细点"
- 想查更多 → "搜一下最近的负面新闻"
- 不够 → "More! More! More!" 🤣

这不是 bug，是 AI 的工作方式——它倾向于简洁，你倾向于深度。**你追问越狠，报告越硬。**

### 2. 数据不准怎么办——让 AI 互相质疑

AI 可能编造数字、记错增长率、用错币种。解决方式是让**多个 AI 互相质疑数据**，谁编的谁露馅。

**建议用法：**
- 先跑一轮 Deep Stock 出报告
- 换一个 AI 说："检查这份报告的数据，找出所有可疑的数字"
- 冲突的地方自然浮出水面

**这不是作弊，这叫"对抗式验证"**——比你手动核对 100 个数字靠谱多了。

---

## 为什么选 Deep Stock

| 对比项 | Deep Stock | 普通分析 |
|--------|-------------|---------|
| 4层宏观过滤 | ✅ 系统化 | ❌ 通常缺失 |
| 4种估值方法 | ✅ 带可信度评级 | ❌ 通常只用1种 |
| 贝叶斯概率 | ✅ 动态更新 | ❌ 主观猜测 |
| 强制反面论证 | ✅ 内置 | ❌ 确认偏误 |
| 数据来源标注 | ✅ 每个数字有来源+时间+币种 | ❌ "据报道" |
| 决策矩阵 | ✅ 0-10分量表 | ❌ "我感觉要涨" |

---

## 附送框架

完整的 **Charlie V3.0 分析框架**（12章，32,000+字）包含在此 Skill 中：

📄 `charlie-v3.0.md`

| 章节 | 内容 |
|------|------|
| 一 | 核心方法论 |
| 二 | 专业报告搜索 |
| 三 | 数据来源标注规范 |
| 四 | 评分量表 |
| 五 | 四层过滤框架（国际→国内→行业→公司）|
| 六 | 估值分析模块（PE/PEG/DCF/SOTP）|
| 七 | 因果回路图（系统动力学）|
| 八 | 贝叶斯概率（动态更新机制）|
| 九 | 反面论证（芒格25种误判）|
| 十 | 决策矩阵（综合评分）|
| 十一 | 分析流程（标准SOP）|
| 十二 | 配套文件说明 |

---

## License

MIT-0 — 自由使用、修改、分发，无需署名。

---

## 英文版 / English

### Deep Stock 🎯
**One framework to cut through the noise.**

Most stock analysis tools tell you what a stock *did*. Deep Stock tells you what it's *worth* — and whether now is the time to act.

**Charlie** = inspired by **Charlie Munger** — his multidisciplinary mental models and human misjudgment psychology are the DNA of this framework.

### What You Get
- Professional-grade analysis (used to require a sell-side analyst)
- 6-step systematic framework (macro → industry → company → valuation → probability → decision)
- Bayesian probability updates (not subjective guesses)
- Built-in contradiction checker (avoids confirmation bias)

### Notes
- **Data depth:** AI defaults to "good enough." Push for more data — the framework is designed for depth.
- **Data accuracy:** Use adversarial verification — have one AI check the report, another re-verify key numbers from different sources. Cross-agent questioning catches fabricated data better than manual checking.

### Quick Start
```bash
clawhub install deep-stock
# Then ask: "Analyze Xiaomi" or "Run Deep Stock on 002594.SZ"
```

---

*Built with Charlie V3.0 · 经实战检验*
