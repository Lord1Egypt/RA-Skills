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
1. 调用排盘脚本获取完整数据（四柱、十神、神煞、大运、刑冲合会）
2. 向你提出 5 个校准问题（父母关系、父亲驻地、母亲角色、家庭经济、自身状态）
3. 根据你的回答校准分析
4. 按八大维度模板输出完整解读报告

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

第一步：排盘

```bash
node scripts/buildBaziFromSolar.ts "2004-04-05T12:00:00" 1 2
```

输出包含：四柱天干地支、十神、纳音、星运、自坐、藏干、宫位、神煞、大运、刑冲合会。

第二步：校准（向用户确认 5 个事实）

1. 父母是否在一起？
2. 父亲做什么工作？常驻地在哪里？
3. 母亲在带你吗？还是由其他长辈带大？
4. 家里做什么的？（开店/体制内/务农/外出务工）
5. 你目前在做什么？（学业/工作/哪个阶段）

第三步：根据排盘数据 + 校准信息，按 SKILL.md 中的八大维度模板填充分析报告。

第四步：输出为 txt 文件，文件名格式 `八字全解_日主X_生肖X.txt`。

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

本项目依赖 LLM 进行命理分析和解读，以下是实测后推荐的模型：

| 模型 | 推荐理由 |
|------|----------|
| Claude 4.* | Claude 系列越新越好，分析深度最强，逻辑严密，长文输出稳定，对命理术语理解精准 |
| Qwen 3.7 Max | 中文理解力极强，对八字术语和文化背景把握到位，性价比高 |
| MiniMax M3 | 中文输出流畅自然，分析有条理，响应速度快 |
| MiMo v2.5 Pro | 推理能力强，逻辑链条清晰，适合复杂命盘 |

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
│   └── util.ts                     公共工具
└── references/
    └── family-patterns.md          家庭背景命理模式参考
```

### 文档

完整命理工作流文档（含排盘用法、六亲规则、分析模板、常见陷阱）请参阅 [SKILL.md](./SKILL.md)

家庭背景命理模式参考（8 种模式：命理信号 → 现实推断 → 校准问题）请参阅 [references/family-patterns.md](./references/family-patterns.md)

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
1. Run the charting script to get complete data (Four Pillars, Ten Gods, Auspicious Stars, Luck Cycles, Interactions)
2. Ask you 5 calibration questions (parents' relationship, father's location, mother's role, family economy, your current status)
3. Calibrate the analysis based on your answers
4. Output a full interpretation report across 8 dimensions

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

Step 1: Chart generation

```bash
node scripts/buildBaziFromSolar.ts "2004-04-05T12:00:00" 1 2
```

Output includes: Four Pillars (Heavenly Stems + Earthly Branches), Ten Gods, Nayin, Star Phase, Self-Position, Hidden Stems, Palaces, Auspicious Stars, Luck Cycles, and Interactions (clashes, combinations, punishments, harms).

Step 2: Calibration (confirm 5 key facts with the user)

1. Are the parents together?
2. What does the father do for work? Where is he based?
3. Did the mother raise you? Or were you raised by other elders?
4. What does the family do? (business / government / farming / migrant work)
5. What are you currently doing? (education / career / which life stage)

Step 3: Fill in the 8-dimension analysis template (from SKILL.md) using chart data + calibration answers.

Step 4: Output as a txt file, named `八字全解_{DayMaster}_{Zodiac}.txt`.

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

This project relies on LLMs for destiny analysis and interpretation. Recommended models after real-world testing:

| Model | Why Recommended |
|-------|----------------|
| Claude 4.* | Claude series (newer is better), deepest analysis, rigorous logic, stable long-form output, precise understanding of Bazi terminology |
| Qwen 3.7 Max | Excellent Chinese comprehension, strong grasp of Bazi terms and cultural context, great value |
| MiniMax M3 | Fluent and natural Chinese output, well-structured analysis, fast response |
| MiMo v2.5 Pro | Strong reasoning capability, clear logical chains, ideal for complex charts |

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
│   └── util.ts                     Shared utilities
└── references/
    └── family-patterns.md          Family pattern reference
```

### Documentation

Full workflow documentation (charting usage, six-relations rules, analysis templates, common pitfalls): [SKILL.md](./SKILL.md)

Family background pattern reference (8 patterns: signal → real-world inference → calibration questions): [references/family-patterns.md](./references/family-patterns.md)

### Dependencies

- [cantian-tymext](https://www.npmjs.com/package/cantian-tymext) — Core charting engine
- [tyme4ts](https://github.com/6tail/tyme4ts) — Lunar-Solar conversion

### License

[MIT](./LICENSE) © 2026

### Acknowledgments

Core algorithms powered by [cantian-tymext](https://www.npmjs.com/package/cantian-tymext) and [tyme4ts](https://github.com/6tail/tyme4ts). Analysis framework integrates traditional Ziping method with modern calibration workflow.
