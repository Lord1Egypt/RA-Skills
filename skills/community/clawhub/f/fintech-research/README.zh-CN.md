# CC 金融科技研究工具集（CC Fintech Research Toolkits）

[English](README.md) | **简体中文**

**100% 免费、自托管、Claude Code 原生，支持全球股票市场（美股、港股、A股）。用本地免费 MCP 服务器替代 15 万美元/年的机构数据栈，再以个性化交互层服务于卖方分析师、组合经理、个人投资者和学术经济学家。**

<br>

![本地 MCP 服务器运行港股探测 skill —— 并行 agent 在港股与美股 ticker 中梳理产业链上游标的](assets/screenshots/cc-equity.png)

三个组件构成整体：

1. **Skill 库。** 24 套分析工作流——Anthropic 官方采用 Apache 许可证的股票研究 bundle（9 个 skill），加上社区维护的扩展库（14 个 skill）。覆盖选股探测、单公司深度分析、持仓跟踪和宏观研究。

2. **可适配的交互层。** Claude 会根据你的金融熟练度和偏好调整语气、深度和术语密度——卖方分析师、组合经理、个人投资者、学术经济学家都能用。四个统一的斜杠命令——`/probe`、`/dive`、`/track`、`/landscape`——把自然语言请求自动路由到全部 24 个 skill。

3. **本地免费数据 MCP。** 自托管 MCP 服务器整合 yfinance + SEC EDGAR + HKEX 披露易 + FRED + NewsAPI + RSS，完全免费零订阅。美股（SEC EDGAR 备案 + FRED 宏观）、港股（恒指前 50 + 科技龙头 + HKEX 公告）、A 股（AH 比价）全覆盖。

---

## 为什么做这个

Anthropic 最近开源了一套出色的[股票研究 skill bundle](https://github.com/anthropics/financial-services/tree/main/plugins/vertical-plugins/equity-research)——九套机构级工作流模板（initiation note、earnings analysis、catalyst calendar、morning note、thesis tracker 等等），把 Claude Code 在股票研究领域的能力上限抬高了一大截。但仍有两个缺口。

1. **数据连接器太贵。** Anthropic 的 skill 是纯方法论——本身不带数据，需要自己接上数据源。Anthropic 官方的[参考仓库](https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/financial-analysis/.mcp.json)把这些 skill 连到了 **11 个机构级 MCP**——FactSet、LSEG、标普全球、Morningstar、Moody's、PitchBook 等——**每家通常每个席位每年 1.5–3 万美元**，合计远超 15 万美元。独立分析师、学术经济学家，以及任何没有机构预算却想跑严肃工作流的人，根本接触不到。

2. **默认面向卖方专业人士，没有可达性层。** Bundle 里的模板是按卖方研究部的日常输出搭的——首次覆盖报告、晨会纪要、业绩前瞻。**概念**是通用的；**术语**（实际/预期年份记号 A/E、bp 简写、卖方报告的特定结构）对个人投资者和做企业层面探索性研究的学者来说，显得隔行如隔山。开箱即用时，Agent 不会根据使用者的金融熟练度或偏好风格自动调整。

这个项目同时解决两点。本地自托管 MCP 服务器用免费开源数据源替代昂贵的机构数据栈；一个由记忆驱动的交互层让输出风格匹配键盘前的人。

---

## Quick Start

1. 安装 [Claude Code](https://claude.com/claude-code)
2. `git clone https://github.com/fredtai/Fintech-research.git`
3. `cd Fintech-research`
4. `pip install -r requirements.txt`
5. `claude`
6. 在 Claude Code 中运行 `/mcp` 验证本地 server
7. 直接使用 `/probe`、`/dive`、`/track`、`/landscape`

---

## 交互——四个斜杠命令

每个命令会打开该类别下的一个简短菜单。按名称选，或者直接用自然语言描述需求，dispatcher 会自动路由。

| 命令 | 类别 | 涵盖范围 |
|---|---|---|
| `/probe` | 选股探测 | 主题、供应链、替代标的；外加 Anthropic 的 `idea-generation`（系统性筛选）和 `sector-overview` |
| `/dive` | 单公司深度分析 | 商业模式、业绩记分卡、财务取证、披露质量漂移、管理层；外加 Anthropic 的 `initiating-coverage`、`earnings-preview`、`earnings-analysis`、`model-update` |
| `/track` | 持仓跟踪 | watchlist、thesis check、事件雷达；外加 Anthropic 的 `thesis-tracker`、`catalyst-calendar`、`morning-note` |
| `/landscape` | 宏观全景 | 收益率曲线、贸易流向、劳动力市场、港元汇率 |

**自然语言同样可用。** *"对拼多多跑一遍 forensics"*、*"PLTR 接下来 6 周有哪些催化"*、*"美国劳动力市场在转弱吗"*、*"腾讯业绩怎么解读"*——Claude 通过 `CLAUDE.md` 的意图映射直接路由到对应 skill。斜杠命令是发现层，自然语言是高阶用户层，底下是同一套 skill。

例子：`/dive PDD forensics` → 对拼多多跑财务取证。`/landscape` → 打开宏观菜单。`/probe AI 基建里什么在跑赢` → 路由到 `themes`。

**无论 skill 数量增加到多少，斜杠命令始终保持四个**——新 skill 是加在 dispatcher 内部，而不是变成新命令。

---

## Modes——根据使用者自我调整

两个项目本地文件决定每次回应的形态。这就是解决 Problem #2 的层——同样的分析严谨度，针对键盘前的人切换语调。

- **`.claude/mode.md`** —— `new`（默认）会在会话开始时显示引导；`experienced` 跳过。可以直接编辑文件，或者告诉 Claude "我已经熟了" 来切换。
- **`.claude/style.md`** —— 四个字段控制 Claude 的表达方式：`experience`（experienced / intermediate / learning）、`depth`（quick / balanced / deep）、`tone`（professional / institutional / conversational / educational），以及可选的 `coverage`（你专注的市场，可选：global / hk-only / us-only）。默认是"专业但好懂"。

Claude 在会话开始时读取两者，每一轮回都应用，会话过程中也会吸收偏好变化。你随手开始用 A/E 记号，`tone` 自动升级到 `institutional`；你问某个术语是什么意思，`experience` 自动降到 `intermediate`。文件更新后会用一行确认。

> 注：这两个文件是*项目本地*的——存在仓库里，不在 Claude Code 的跨会话自动记忆中。换一台机器 clone，不同步仓库就是从默认开始。

---

## Skills

**Anthropic bundle**（`anthropic-equity-research-skills/`）—— 从 [`anthropics/financial-services`](https://github.com/anthropics/financial-services)（Apache 2.0）vendored 过来的九套工作流模板：`initiating-coverage`、`earnings-preview`、`earnings-analysis`、`model-update`、`morning-note`、`catalyst-calendar`、`thesis-tracker`、`idea-generation`、`sector-overview`。

**社区扩展**（`community-skills/`）—— 分析师贡献的 14 种视角，分四个领域：
- `probe/`（themes、supply-chain、alt-plays）
- `dive/`（business-model、earnings-scorecard、financial-forensics、reporting-quality、management）
- `track/`（watchlist、thesis-check、event-radar）
- `landscape/`（yield-curve、trade-flows、labor-market、hkma-rates）

每个 skill 都是一个简短的 markdown 文件——读一个就知道它具体做什么。

---

## 数据——本地自托管免费 MCP 服务器

一个 MCP 支撑所有 skill。基于 100% 免费开源数据源，个人用户无需注册或 API Key 即可使用基础功能。

### P0 核心数据源（零配置，开箱即用）

| 数据源 | 内容 | 覆盖范围 |
|---|---|---|
| **yfinance** | 三大报表、60+ 标准化指标、历史行情、K 线数据 | 港股（.HK）、美股、A 股 |
| **HKEX 披露易** | 公告、财报、内幕交易披露、权益变动 | 港股全量上市公司 |

**港股覆盖：** 65 个 .HK ticker（恒指前 50 + 科技龙头），含 AH 股比价支持。

### P1 宏观数据（零配置，开箱即用）

| 数据源 | 内容 | 覆盖范围 |
|---|---|---|
| **FRED** | 美联储利率、国债收益率、CPI、就业数据 | 美国宏观经济 |
| **HKMA** | 港元汇率、香港基准利率、HIBOR | 香港货币市场 |

> FRED 高级功能可选填 API Key（免费额度，个人用户基本够用）。

### P2 新闻与情绪（零配置，开箱即用）

| 数据源 | 内容 | 覆盖范围 |
|---|---|---|
| **NewsAPI** | 全球财经新闻标题与摘要 | 港股、美股、A 股相关 |
| **RSS 聚合** | 主流财经媒体、港交所公告 RSS | 实时资讯 |

> NewsAPI 高级功能可选填 API Key（免费额度 100 条/天）。

### 覆盖范围

- **港股（主力）**：恒指成分股、科技龙头、AH 股——65 个 .HK ticker
- **美股**：标普 500 核心成分股、中概股 ADR
- **A 股**：沪深 300 核心成分股，AH 股联动

数据直接来自一手来源（Yahoo Finance、SEC EDGAR、HKEX 披露易、FRED、NewsAPI、RSS 订阅源），通过开源 Python 库获取——**不是转售的专有 feed**。**全部免费，个人用户无需注册或 API Key 即可使用基础功能**。FRED / NewsAPI 高级功能可选填 API Key（免费额度）。无需 FactSet、LSEG、标普全球或 Morningstar 订阅。

你不用写 SQL——描述你要什么，运行 skill 时 Claude 会自动取数。

---

## 贡献

非常欢迎社区 skill 贡献——这是工具集随着实战分析师分享方法、不断变锋利的部分。

新增一个社区 skill 涉及三处小改动：
1. 在 `community-skills/<area>/` 加上 skill 文件
2. 在 `CLAUDE.md` 的能力映射表中加一行
3. 在 `.claude/commands/<area>.md` 对应 dispatcher 的菜单中加一行

然后提 PR。Anthropic bundle 是从上游 vendored 进来的——对它的修改建议应该提到 [`anthropics/financial-services`](https://github.com/anthropics/financial-services)，不要提到本仓库。

skill 模板、合格 skill 的判断标准、review 期望，请参考 `CONTRIBUTING.md`。

---

## 许可

工具集本体（社区 skill、脚手架、dispatcher、文档、本地 MCP 服务器）采用 Apache 2.0 许可证——见根目录的 `LICENSE` 文件。Vendored 的 Anthropic 股票研究 bundle 同样是 Apache 2.0；归属信息与上游同步命令见 `anthropic-equity-research-skills/NOTICE.md`。

---

## About

本项目基于：

- **[anthropics/financial-services](https://github.com/anthropics/financial-services)** —— Anthropic 官方开源的股票研究 skill bundle，vendored 在 `anthropic-equity-research-skills/`（Apache 2.0）
- **本地自托管免费 MCP 服务器** —— 整合 yfinance、HKEX 披露易、FRED、NewsAPI、RSS 等 100% 免费开源数据源，支撑所有 skill 的数据需求
