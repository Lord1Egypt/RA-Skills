# 八字全方位算命 Skill

> 八字排盘与全方位命理解读工具集

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-bazi--full--fortune-blue.svg)](https://clawhub.com/skills/bazi-full-fortune)

---

## 中文文档

### 简介

八字全方位算命 Skill 是一个完整的八字命理工作流工具集，基于 [cantian-tymext](https://www.npmjs.com/package/cantian-tymext) 构建，涵盖从排盘到全方位解读的完整链路：

- 排盘层 — CLI 脚本，支持阳历/农历输入，输出完整四柱、十神、神煞、大运、刑冲合会
- 分析层 — 全方位命理解读模板，覆盖家庭、健康、事业、财富、感情、人际、学业、精神八大维度
- 参考层 — 家庭背景命理模式速查清单，用于校准分析准确性
- 反推层 — 从已知八字四柱反查阳历日期
- 交叉验证层（可选）— 紫微斗数排盘参考文档与安星校验脚本，支持可选的紫微斗数交叉验证以提升结论稳定性

### 安装

方式一：通过 ClawHub 安装（推荐，适用于 Hermes / OpenClaw 用户）

```bash
clawhub install bazi-full-fortune
cd skills/bazi-full-fortune
npm install
```

方式二：通过 Git 克隆

```bash
git clone https://github.com/Laurc2004/bazi-full-fortune.git
cd bazi-full-fortune
npm install
```

### 环境要求

- Node.js ≥ 18（推荐 24，可直接运行 TypeScript）
- 兼容方案：若 Node 版本较低，需额外安装 `tsx`（`npm install -D tsx`）

### 使用

#### 1. CLI 脚本直接调用

阳历排盘：

```bash
node scripts/buildBaziFromSolar.ts "2004-04-05T12:00:00" 1 2
```

| 参数 | 说明 | 必填 | 取值 |
|------|------|------|------|
| solarTime | 阳历出生时间（ISO 8601，不带时区） | 是 | `2004-04-05T12:00:00` |
| gender | 性别 | 否 | `1`=男，`0`=女（默认 1） |
| sect | 早晚子时配置 | 否 | `1`=23:00-23:59 算次日，`2`=算当日（默认 2） |

农历排盘：

```bash
node scripts/buildBaziFromLunar.ts "2004-03-16T12:00:00" 1 2
```

参数格式与阳历一致，时间传入农历日期。注意：不支持农历闰月，闰月需先手动转换为阳历再调用阳历排盘。

黄历查询：

```bash
# 查询今天
node scripts/getChineseCalendar.ts

# 查询指定日期
node scripts/getChineseCalendar.ts 2024-02-10
```

反推扫描（从已知八字四柱反查阳历出生日期）：

```bash
# 完整四柱匹配
node scripts/scan_year.ts 2004 1 \
  --year-pillar 甲申 \
  --month-pillar 戊辰 \
  --day-pillar 甲寅 \
  --hour-pillar 庚午 \
  --hour 12:00:00

# 部分匹配（只知道年月日柱，时柱不确定）
node scripts/scan_year.ts 2004 1 \
  --year-pillar 甲申 \
  --month-pillar 戊辰 \
  --day-pillar 甲寅

# 跨年份扫描（同一八字每 60 年重复出现）
for y in 1944 2004; do node scripts/scan_year.ts $y 1 --day-pillar 甲寅; done
```

| 参数 | 说明 |
|------|------|
| year | 要扫描的年份（必填） |
| gender | 0=女，1=男（必填） |
| --year-pillar | 年柱过滤（如 甲申） |
| --month-pillar | 月柱过滤（如 戊辰） |
| --day-pillar | 日柱过滤（如 甲寅） |
| --hour-pillar | 时柱过滤（如 庚午） |
| --hour | 扫描用的时间，默认 15:30:00（申时） |

#### 2. npm scripts 快捷方式

不想记完整路径可以用 npm scripts：

```bash
npm run bazi:solar -- "2004-04-05T12:00:00" 1 2
npm run bazi:lunar -- "2004-03-16T12:00:00" 1 2
npm run calendar
npm run calendar -- 2024-02-10
npm run scan -- 2004 1 --day-pillar 甲寅 --hour 12:00:00
```

#### 3. 作为 AI Agent 技能使用（Hermes / OpenClaw）

安装后，AI Agent 会自动加载此技能。直接对 Agent 说话即可触发：

排盘：

```
帮我排一下八字：2004年4月5日中午12点，男
```

全方位分析：

```
甲申 戊辰 甲寅 庚午 男 2004年生人，帮我全方位分析
```

Agent 会自动：
1. 先确认命造信息（出生日期公历/农历与是否闰月、出生时间、性别、出生地、是否已有现成排盘结果）
2. 调用排盘脚本获取完整数据（四柱、十神、神煞、大运、刑冲合会），并自检年干阴阳与大运顺逆、月支节气、起运岁数、十神推算
3. 向你提出 5 个家庭校准问题（父母关系、父亲驻地、母亲角色、家庭经济、自身状态）
4. 用近一两年实际顺逆与 2-3 个已发生关键事件做回测校验，校准身强身弱与喜用假设
5. 询问是否需要紫微斗数交叉验证（默认不启用；如需要，按 references/ziwei/ 规则排紫微盘并交叉验证）
6. 按八大维度模板输出完整解读报告，并附温馨提示

反推阳历：

```
甲申 戊辰 甲寅 庚午，男命，帮我反推一下阳历出生日期
```

查黄历：

```
帮我查一下今天的黄历
帮我查一下 2024-02-10 的农历和宜忌
```

#### 4. 完整分析工作流（给开发者/高阶用户）

如果你想手动走完整流程，步骤如下：

第一步：确认命造信息（先访谈，再排盘）

1. 出生日期是公历还是农历？农历需问清是否闰月
2. 出生时间精确到分钟，或至少到时辰
3. 性别（影响大运顺逆）
4. 出生地（涉及时辰边界校正时可能需要）
5. 是否已有现成排盘结果（有的话优先校盘）

访谈问题库见 references/interview.md

第二步：排盘

```bash
node scripts/buildBaziFromSolar.ts "2004-04-05T12:00:00" 1 2
```

输出包含：四柱天干地支、十神、纳音、星运、自坐、藏干、宫位、神煞、大运、刑冲合会。

排盘自检：年干阴阳与大运顺逆一致、月支对应正确节气、起运岁数取自脚本输出（严禁手估）、十神推算无误。

第三步：校准（向用户确认 5 个事实）

1. 父母是否在一起？
2. 父亲做什么工作？常驻地在哪里？
3. 母亲在带你吗？还是由其他长辈带大？
4. 家里做什么的？（开店/体制内/务农/外出务工）
5. 你目前在做什么？（学业/工作/哪个阶段）

第四步：回测校验——先给身强身弱与喜用假设，请用户用近一两年实际顺逆（忌神年是否难受、喜用月是否得财）及 2-3 个已发生关键事件反校验，校准后再输出完整报告。

第五步（可选）：紫微斗数交叉验证——询问用户是否需要，默认不启用。如启用，按 references/ziwei/calculation.md 规则排紫微盘（命宫身宫十二宫、五行局、十四主星、四化、大限），排盘前声明口径（默认三合派；闰月归属默认「闰月按下月」并明确告知，用户有既定口径优先沿用）；两体系各自独立分析、不混用术语，按性格、事业、财运、感情、健康五维度逐项比对，结论一致标注「双体系一致，结论稳定性提升」，不一致则回查各自排盘口径（重点查闰月与子时换日），不强行调和；安紫微星可用 python3 scripts/ziwei_verify.py 校验。

第六步：根据排盘数据 + 校准信息，按 SKILL.md 中的八大维度模板填充分析报告。

第七步：输出为 txt 文件，文件名格式 `八字全解_日主X_生肖X.txt`，文末附温馨提示。

### 核心特性

六亲十神对应规则（男女命不同，搞错则全盘皆错）：

| 六亲 | 男命 | 女命 |
|------|------|------|
| 父亲 | 偏财 | 正财 |
| 母亲 | 正印 | 偏印（枭神） |
| 配偶 | 正财（妻） | 正官（夫） |
| 儿子 | 七杀 | 伤官 |
| 女儿 | 正官 | 食神 |
| 兄弟 | 比肩 | 劫财 |
| 姐妹 | 劫财 | 比肩 |

八大维度分析模板：家庭、健康、外貌身材、事业、财富、感情婚姻、人际关系、学业、精神世界

校准工作流：排盘后先问 5 个关键事实（父母关系、父亲驻地、母亲是否带大、家庭经济来源、自己当前状态），再做完整解读，避免"第一轮分析全错"。

### 推荐 LLM 模型

本项目依赖 LLM 进行命理分析和解读，以下模型按实测效果从高到低排名：

| 排名 | 模型 | 推荐理由 |
|------|------|----------|
| 1 | Qwen3.8 Max | 当前效果最佳，中文理解力与八字术语把握最强，逻辑严密，支持超长上下文，性价比高 |
| 2 | Kimi K3 | 长文分析能力强，推理出色，对命理术语和文化背景理解到位 |
| 3 | GLM-5 | 推理与 Agent 能力突出，中文命理语境把握准确，开源且性价比高 |
| 4 | GPT-5.6 | 综合能力全面，分析严谨，中文命理术语理解稍逊于国产旗舰 |
| 5 | DeepSeek V4 | 推理链条清晰，适合复杂命盘拆解，价格低廉 |
| 6 | Claude Opus 5 | 分析深度强，长文输出稳定，对命理术语理解精准 |

此外，MiniMax M3、MiMo v2.5 Pro 也可正常使用，可作为备选。

### 项目结构

```
bazi-full-fortune/
├── SKILL.md                        完整命理工作流文档
├── README.md                       本文件
├── package.json
├── LICENSE                         MIT
├── scripts/
│   ├── buildBaziFromSolar.ts       阳历排盘
│   ├── buildBaziFromLunar.ts       农历排盘
│   ├── getChineseCalendar.ts       黄历查询
│   ├── scan_year.ts                反推扫描
│   ├── ziwei_verify.py             紫微安星校验（可选交叉验证用）
│   └── util.ts                     公共工具
└── references/
    ├── family-patterns.md          家庭背景命理模式参考
    └── ziwei/                      紫微斗数参考（可选交叉验证用）
        ├── calculation.md          紫微排盘计算
        ├── stars.md                星曜解读
        ├── sihua.md                四化
        └── patterns.md             格局
```

### 文档

完整命理工作流文档（含排盘用法、六亲规则、分析模板、常见陷阱）请参阅 [SKILL.md](./SKILL.md)

家庭背景命理模式参考（8 种模式：命理信号 → 现实推断 → 校准问题）请参阅 [references/family-patterns.md](./references/family-patterns.md)

访谈问题库（第一轮核心问题、第二轮条件追问、家庭校准 5 问、回测校验问题、可选服务询问、不要这样问）请参阅 [references/interview.md](./references/interview.md)

完整八字分析请求提示词模板（可直接复制使用，输出要求对齐八大维度模板）请参阅 [references/prompt-template.md](./references/prompt-template.md)

紫微斗数交叉验证参考（可选）——排盘计算请参阅 [references/ziwei/calculation.md](./references/ziwei/calculation.md)，星曜解读请参阅 [references/ziwei/stars.md](./references/ziwei/stars.md)，四化请参阅 [references/ziwei/sihua.md](./references/ziwei/sihua.md)，格局请参阅 [references/ziwei/patterns.md](./references/ziwei/patterns.md)，安紫微星校验脚本为 `scripts/ziwei_verify.py`（Python 3 运行：`python3 scripts/ziwei_verify.py`）

### 依赖

- [cantian-tymext](https://www.npmjs.com/package/cantian-tymext) — 底层排盘引擎
- [tyme4ts](https://github.com/6tail/tyme4ts) — 农历/阳历转换

### 许可证

[MIT](./LICENSE) © 2026

### 致谢

底层算法基于 [cantian-tymext](https://www.npmjs.com/package/cantian-tymext) 和 [tyme4ts](https://github.com/6tail/tyme4ts)，命理分析框架融合了传统子平术与现代校准工作流。

---

## English Documentation

### Introduction

Bazi Full Fortune Telling Skill is a complete Bazi (Four Pillars of Destiny) workflow toolkit, built on [cantian-tymext](https://www.npmjs.com/package/cantian-tymext). It covers the full pipeline from chart generation to comprehensive destiny analysis:

- Charting Layer — CLI scripts supporting solar/lunar calendar input, outputting complete Four Pillars, Ten Gods, Auspicious Stars, Luck Cycles, and Interactions (clashes, combinations, punishments, harms)
- Analysis Layer — Full destiny interpretation template covering 8 dimensions: Family, Health, Appearance, Career, Wealth, Love & Marriage, Social Relations, Education, and Spiritual World
- Reference Layer — Family background pattern lookup table for calibrating analysis accuracy
- Reverse Lookup — Find the solar date matching known Bazi four pillars
- Cross-Validation Layer (optional) — Zi Wei Dou Shu (Purple Star Astrology) charting references and a star-placement verification script, supporting optional cross-validation to improve conclusion stability

### Installation

Option 1: Install via ClawHub (recommended for Hermes / OpenClaw users)

```bash
clawhub install bazi-full-fortune
cd skills/bazi-full-fortune
npm install
```

Option 2: Clone from Git

```bash
git clone https://github.com/Laurc2004/bazi-full-fortune.git
cd bazi-full-fortune
npm install
```

### Prerequisites

- Node.js ≥ 18 (Node 24 recommended for native TypeScript execution)
- Fallback: install `tsx` for older Node versions (`npm install -D tsx`)

### Usage

#### 1. CLI Scripts

Solar calendar chart:

```bash
node scripts/buildBaziFromSolar.ts "2004-04-05T12:00:00" 1 2
```

| Parameter | Description | Required | Values |
|-----------|-------------|----------|--------|
| solarTime | Solar birth datetime (ISO 8601, no timezone) | Yes | `2004-04-05T12:00:00` |
| gender | Gender | No | `1`=male, `0`=female (default: 1) |
| sect | Late-zi-hour config | No | `1`=23:00-23:59 counts as next day, `2`=same day (default: 2) |

Lunar calendar chart:

```bash
node scripts/buildBaziFromLunar.ts "2004-03-16T12:00:00" 1 2
```

Same parameter format as solar. Note: intercalary (leap) lunar months are not supported — convert to solar date first.

Chinese almanac query:

```bash
# Query today
node scripts/getChineseCalendar.ts

# Query a specific date
node scripts/getChineseCalendar.ts 2024-02-10
```

Reverse lookup (find solar date from known four pillars):

```bash
# Full four-pillar match
node scripts/scan_year.ts 2004 1 \
  --year-pillar 甲申 \
  --month-pillar 戊辰 \
  --day-pillar 甲寅 \
  --hour-pillar 庚午 \
  --hour 12:00:00

# Partial match (only year + month + day pillars known)
node scripts/scan_year.ts 2004 1 \
  --year-pillar 甲申 \
  --month-pillar 戊辰 \
  --day-pillar 甲寅

# Cross-year scan (same Bazi repeats every 60 years)
for y in 1944 2004; do node scripts/scan_year.ts $y 1 --day-pillar 甲寅; done
```

| Parameter | Description |
|-----------|-------------|
| year | Year to scan (required) |
| gender | 0=female, 1=male (required) |
| --year-pillar | Filter by year pillar (e.g. 甲申) |
| --month-pillar | Filter by month pillar (e.g. 戊辰) |
| --day-pillar | Filter by day pillar (e.g. 甲寅) |
| --hour-pillar | Filter by hour pillar (e.g. 庚午) |
| --hour | Time to use for scanning, default 15:30:00 (申时) |

#### 2. npm Scripts Shortcut

```bash
npm run bazi:solar -- "2004-04-05T12:00:00" 1 2
npm run bazi:lunar -- "2004-03-16T12:00:00" 1 2
npm run calendar
npm run calendar -- 2024-02-10
npm run scan -- 2004 1 --day-pillar 甲寅 --hour 12:00:00
```

#### 3. As an AI Agent Skill (Hermes / OpenClaw)

After installation, the AI Agent automatically loads this skill. Just talk to the Agent naturally:

Chart generation:

```
Chart my Bazi: April 5, 2004 at 12:00 PM, male
```

Full analysis:

```
甲申 戊辰 甲寅 庚午, male born 2004, give me a full analysis
```

The Agent will automatically:
1. Confirm your birth data first (solar/lunar date + leap month, birth time, gender, birthplace, any existing chart)
2. Run the charting script to get complete data (Four Pillars, Ten Gods, Auspicious Stars, Luck Cycles, Interactions), then self-check year-stem polarity vs. luck-cycle direction, month branch vs. solar term, luck-cycle start age, and Ten Gods
3. Ask you 5 family calibration questions (parents' relationship, father's location, mother's role, family economy, your current status)
4. Backtest the strong/weak day-master and favorable-element hypotheses against the last 1-2 years of actual outcomes and 2-3 key past events
5. Ask whether you want Zi Wei Dou Shu cross-validation (disabled by default; if enabled, chart the Zi Wei chart per references/ziwei/ rules and cross-validate)
6. Output a full interpretation report across 8 dimensions, with a closing reminder

Reverse lookup:

```
甲申 戊辰 甲寅 庚午, male — reverse-lookup the solar birth date
```

Almanac query:

```
Check today's Chinese almanac
Look up the lunar date and auspicious/inauspicious activities for 2024-02-10
```

#### 4. Full Analysis Workflow (for Developers / Advanced Users)

Step 1: Confirm birth data (interview before charting)

1. Solar or lunar birth date? If lunar, confirm whether it falls in an intercalary (leap) month
2. Birth time — precise to the minute if possible, at least to the 2-hour shichen
3. Gender (determines luck-cycle direction)
4. Birthplace (needed for boundary-hour corrections)
5. Whether an existing chart from another tool is available (if so, verify it first)

Interview question bank: references/interview.md

Step 2: Chart generation

```bash
node scripts/buildBaziFromSolar.ts "2004-04-05T12:00:00" 1 2
```

Output includes: Four Pillars (Heavenly Stems + Earthly Branches), Ten Gods, Nayin, Star Phase, Self-Position, Hidden Stems, Palaces, Auspicious Stars, Luck Cycles, and Interactions (clashes, combinations, punishments, harms).

Post-chart self-check: year-stem polarity matches luck-cycle direction; month branch matches the correct solar term; luck-cycle start age taken from script output (never estimated by hand); Ten Gods derived correctly.

Step 3: Calibration (confirm 5 key facts with the user)

1. Are the parents together?
2. What does the father do for work? Where is he based?
3. Did the mother raise you? Or were you raised by other elders?
4. What does the family do? (business / government / farming / migrant work)
5. What are you currently doing? (education / career / which life stage)

Step 4: Backtest verification — first present the strong/weak day-master and favorable-element hypotheses, then ask the user to verify against the last 1-2 years of actual ups and downs and 2-3 key past events; recalibrate before the full report.

Step 5 (optional): Zi Wei Dou Shu cross-validation — ask the user whether it is needed; disabled by default. If enabled, chart the Zi Wei chart per references/ziwei/calculation.md (Life/Body palace + 12 palaces, Five-Element Bureau, 14 major stars, Four Transformations, decade limits), declaring the conventions first (default San He school; leap-month convention defaults to "leap month counts as the next month" and must be stated explicitly — the user's established convention takes priority; this is separate from the Bazi leap-month conversion). The two systems are analyzed independently without mixing terminology; compare personality, career, wealth, relationships, and health dimension by dimension. Matching conclusions are labeled "consistent across both systems, conclusion stability improved"; mismatches trigger a re-check of each system's charting conventions (leap month and late-zi-hour day boundary first), never forced reconciliation. Star placement can be verified with `python3 scripts/ziwei_verify.py`.

Step 6: Fill in the 8-dimension analysis template (from SKILL.md) using chart data + calibration answers.

Step 7: Output as a txt file, named `八字全解_{DayMaster}_{Zodiac}.txt`, with the closing reminder appended.

### Key Features

Six Relations & Ten Gods mapping (varies by gender — getting it wrong invalidates the entire analysis):

| Relation | Male | Female |
|----------|------|--------|
| Father | Indirect Wealth | Direct Wealth |
| Mother | Direct Seal | Indirect Seal (Owl) |
| Spouse | Direct Wealth (Wife) | Direct Officer (Husband) |
| Son | Seven Killings | Indirect Officer |
| Daughter | Direct Officer | Eating God |
| Brother | Friend | Rob Wealth |
| Sister | Rob Wealth | Friend |

8-Dimension analysis template: Family, Health, Appearance, Career, Wealth, Love & Marriage, Social Relations, Education, Spiritual World

Calibration workflow: Ask 5 key questions after charting (parents' relationship, father's location, mother's role, family economy, current life stage) before full analysis — avoids the "first-round analysis all wrong, second rewrite" trap.

### Recommended LLMs

This project relies on LLMs for destiny analysis and interpretation. Models below are ranked by real-world performance (best first):

| Rank | Model | Why Recommended |
|------|-------|----------------|
| 1 | Qwen3.8 Max | Best overall performance: strongest Chinese comprehension and Bazi terminology grasp, rigorous logic, ultra-long context support, great value |
| 2 | Kimi K3 | Excellent long-form analysis and reasoning, solid grasp of metaphysics terms and cultural context |
| 3 | GLM-5 | Outstanding reasoning and agent capabilities, accurate Chinese metaphysics context, open-source and cost-effective |
| 4 | GPT-5.6 | Well-rounded and rigorous analysis, slightly behind top Chinese models on Bazi terminology |
| 5 | DeepSeek V4 | Clear reasoning chains for complex charts, very affordable |
| 6 | Claude Opus 5 | Deep analysis, stable long-form output, precise understanding of Bazi terminology |

MiniMax M3 and MiMo v2.5 Pro are also viable alternatives.

### Project Structure

```
bazi-full-fortune/
├── SKILL.md                        Full workflow documentation
├── README.md                       This file
├── package.json
├── LICENSE                         MIT
├── scripts/
│   ├── buildBaziFromSolar.ts       Solar calendar chart
│   ├── buildBaziFromLunar.ts       Lunar calendar chart
│   ├── getChineseCalendar.ts       Almanac query
│   ├── scan_year.ts                Reverse lookup
│   ├── ziwei_verify.py             Zi Wei star-placement verification (optional cross-validation)
│   └── util.ts                     Shared utilities
└── references/
    ├── family-patterns.md          Family pattern reference
    └── ziwei/                      Zi Wei Dou Shu references (optional cross-validation)
        ├── calculation.md          Zi Wei charting calculations
        ├── stars.md                Star interpretations
        ├── sihua.md                Four Transformations
        └── patterns.md             Chart patterns
```

### Documentation

Full workflow documentation (charting usage, six-relations rules, analysis templates, common pitfalls): [SKILL.md](./SKILL.md)

Family background pattern reference (8 patterns: signal → real-world inference → calibration questions): [references/family-patterns.md](./references/family-patterns.md)

Interview question bank (round-1 core questions, round-2 conditional follow-ups, 5 family calibration questions, backtest verification questions, optional service inquiry): [references/interview.md](./references/interview.md)

Ready-to-use full analysis prompt template (output requirements aligned with the 8-dimension template): [references/prompt-template.md](./references/prompt-template.md)

Zi Wei Dou Shu cross-validation references (optional) — charting: [references/ziwei/calculation.md](./references/ziwei/calculation.md), stars: [references/ziwei/stars.md](./references/ziwei/stars.md), four transformations: [references/ziwei/sihua.md](./references/ziwei/sihua.md), patterns: [references/ziwei/patterns.md](./references/ziwei/patterns.md); star-placement verification script: `scripts/ziwei_verify.py` (run with Python 3: `python3 scripts/ziwei_verify.py`)

### Dependencies

- [cantian-tymext](https://www.npmjs.com/package/cantian-tymext) — Core charting engine
- [tyme4ts](https://github.com/6tail/tyme4ts) — Lunar-Solar conversion

### License

[MIT](./LICENSE) © 2026

### Acknowledgments

Core algorithms powered by [cantian-tymext](https://www.npmjs.com/package/cantian-tymext) and [tyme4ts](https://github.com/6tail/tyme4ts). Analysis framework integrates traditional Ziping method with modern calibration workflow.
