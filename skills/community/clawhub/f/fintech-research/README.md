# CC Fintech Research Toolkits

> **100% free, self-hosted, Claude Code native equity research agent for global markets (US, HK, CN)**

[English](#english) | [简体中文](#simplified-chinese)

---

## <a name="english"></a>English

## About

**CC Fintech Research Toolkits** transforms Claude Code into a professional equity research agent for **global equity markets**. It combines 24 analysis skills, a free data MCP server, and a personalization layer — all 100% self-hosted with **zero subscriptions**.

Works seamlessly across **US equities** (AAPL, NVDA, TSLA via yfinance + SEC EDGAR), **Hong Kong equities** (0700.HK, 9988.HK via yfinance + HKEX News), and **A-share Connect** (AH spread analysis) — all through a single unified interface.

## Three Components

| Component | What It Does |
|-----------|-------------|
| **Skill Library** | 24 reusable analysis skills organized across 4 command families (`/probe`, `/dive`, `/track`, `/landscape`) |
| **Accessible Interface** | Claude Code native commands with configurable depth, tone, and market coverage |
| **Free Data MCP** | Local MCP server connecting to yfinance (global), SEC EDGAR (US), HKEX (HK), FRED (macro), NewsAPI + RSS (news) — all free |

## Quick Start

1. Install Claude Code: `npm install -g @anthropics/claude-code`
2. `git clone https://github.com/fredtai/Fintech-research.git`
3. `cd Fintech-research`
4. `pip install -r requirements.txt`
5. `claude`
6. In Claude Code, run `/mcp` to verify local server is connected
7. Use `/probe`, `/dive`, `/track`, `/landscape` directly

## Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/probe` | Thematic discovery, screening, idea generation | "Find EV supply chain plays" or "Screen US semiconductor stocks" |
| `/dive` | Deep fundamental analysis on a single ticker | "Dive into AAPL" or "Analyze 0700.HK business model" |
| `/track` | Ongoing monitoring, thesis check, watchlist | "Track my portfolio" or "Check NVDA thesis" |
| `/landscape` | Macro analysis across CN-HK-US | "Show CN-HK-US yield curves" or "Compare US vs HK tech valuations" |

## Market Coverage

### US Equities
- **yfinance**: Real-time quotes, fundamentals, historical prices for all US tickers (AAPL, MSFT, GOOGL, NVDA, TSLA, META, etc.)
- **SEC EDGAR**: Free official filings (10-K, 10-Q, 8-K) with full-text search
- **FRED**: US macro data — Treasury yields, Fed Funds, CPI, unemployment, DXY
- **NewsAPI**: US market news with sentiment scoring

### Hong Kong Equities
- **yfinance**: Real-time quotes, fundamentals, historical prices for all `.HK` tickers
- **HKEX News**: Regulatory announcements and filings scraping from HKEX disclosure platform
- **65 Pre-configured tickers**: Hang Seng Top 50 + tech leaders (0700.HK, 9988.HK, 3690.HK, 1810.HK, 1211.HK, etc.)
- **AH Spread Analysis**: A-share vs H-share premium/discount calculation
- **Stock Connect**: Northbound/southbound flow context

### A-Share Equities (via Connect)
- **AH Spread**: Cross-market price comparison for dual-listed stocks
- **yfinance**: Limited A-share coverage via `.SS` / `.SZ` suffixes

## Free Data Sources

| Priority | Source | Cost | Coverage |
|----------|--------|------|----------|
| P0 Core | yfinance | Free | **Global** equities (US, HK, CN) |
| P0 Core | SEC EDGAR | Free | **US** filings (10-K, 10-Q, 8-K) |
| P0 Core | HKEX News | Free | **HK** announcements |
| P1 Macro | FRED | Free | **US** rates, FX, macro indicators |
| P1 Macro | HKMA | Free | **HK** monetary data |
| P2 News | NewsAPI | Free tier (100/day) | **Global** news |
| P2 News | RSS Feeds | Free | **Global** financial news |

All data sources are **100% free** with **zero subscription** required.

## Configuration

### Modes (`.claude/mode.md`)
- `new` — Claude presents orientation and capability map at session start
- `experienced` — Claude skips orientation, commands execute directly

### Style (`.claude/style.md`)
- **Experience**: `beginner` / `intermediate` / `advanced`
- **Depth**: `quick` (≤500 chars) / `balanced` (≤1500) / `deep` (unlimited)
- **Tone**: `professional` / `conversational`
- **Coverage**: `global` (US+HK+CN) / `us-only` / `hk-only`

## Contributing

Contributions are welcome! Please ensure:
- All data sources used are free with public documentation
- Multi-market support (US, HK, CN) is preserved or enhanced
- No external project dependencies are introduced
- Code passes `python -m py_compile` on all Python files

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

## <a name="simplified-chinese"></a>简体中文

## 关于

**CC Fintech Research Toolkits** 将 Claude Code 转变为面向**全球股票市场**的专业股票研究 Agent。它包含 24 个分析技能、免费数据 MCP 服务器和个性化层 —— 全部 100% 自托管，**零订阅费用**。

无缝覆盖**美股**（AAPL, NVDA, TSLA，通过 yfinance + SEC EDGAR）、**港股**（0700.HK, 9988.HK，通过 yfinance + 港交所披露易）和**A股通**（AH 价差分析）—— 全部通过统一界面操作。

## 三大组件

| 组件 | 说明 |
|------|------|
| **技能库** | 24 个可复用分析技能，按 4 个命令族组织（`/probe`, `/dive`, `/track`, `/landscape`） |
| **交互界面** | Claude Code 原生命令，支持可配置的深度、语气与市场覆盖范围 |
| **免费数据 MCP** | 本地 MCP 服务器：yfinance（全球）、SEC EDGAR（美股）、港交所（港股）、FRED（宏观）、NewsAPI + RSS（新闻）—— 全部免费 |

## 快速开始

1. 安装 Claude Code: `npm install -g @anthropics/claude-code`
2. `git clone https://github.com/fredtai/Fintech-research.git`
3. `cd Fintech-research`
4. `pip install -r requirements.txt`
5. `claude`
6. 在 Claude Code 中运行 `/mcp` 验证本地服务器已连接
7. 直接使用 `/probe`, `/dive`, `/track`, `/landscape`

## 命令说明

| 命令 | 用途 | 示例 |
|------|------|------|
| `/probe` | 主题发现、筛选、创意生成 | "Find EV supply chain plays" 或 "Screen US semiconductor stocks" |
| `/dive` | 单只股票的深度基本面分析 | "Dive into AAPL" 或 "Analyze 0700.HK business model" |
| `/track` | 持续监控、论点验证、观察名单 | "Track my portfolio" 或 "Check NVDA thesis" |
| `/landscape` | 中港美三地宏观分析 | "Show CN-HK-US yield curves" 或 "Compare US vs HK tech valuations" |

## 市场覆盖

### 美股
- **yfinance**: 全美股的实时报价、基本面、历史价格（AAPL, MSFT, GOOGL, NVDA, TSLA, META 等）
- **SEC EDGAR**: 免费官方备案文件（10-K, 10-Q, 8-K）全文搜索
- **FRED**: 美国宏观数据 — 国债收益率、联储利率、CPI、失业率、美元指数
- **NewsAPI**: 美股新闻 + 情绪评分

### 港股
- **yfinance**: 全部 `.HK` 股票的实时报价、基本面、历史价格
- **港交所披露易**: 监管公告和通函抓取
- **65 个预配置代码**: 恒指前50 + 科技龙头（0700.HK, 9988.HK, 3690.HK, 1810.HK, 1211.HK 等）
- **AH 价差分析**: A 股 vs H 股溢价/折价计算
- **互联互通**: 北水/南流资金流向

### A 股（通过互联互通）
- **AH 价差**: 两地上市股票的跨市场价格比较
- **yfinance**: 通过 `.SS` / `.SZ` 后缀有限覆盖

## 免费数据源

| 优先级 | 来源 | 费用 | 覆盖范围 |
|--------|------|------|----------|
| P0 核心 | yfinance | 免费 | **全球** 股票（美股、港股、A股） |
| P0 核心 | SEC EDGAR | 免费 | **美股** 备案文件（10-K, 10-Q, 8-K） |
| P0 核心 | 港交所披露易 | 免费 | **港股** 公告 |
| P1 宏观 | FRED | 免费 | **美国** 利率、汇率、宏观指标 |
| P1 宏观 | 香港金管局 | 免费 | **香港** 货币数据 |
| P2 新闻 | NewsAPI | 免费版 (100次/天) | **全球** 新闻 |
| P2 新闻 | RSS 订阅 | 免费 | **全球** 财经新闻 |

所有数据源均 **100% 免费**，**无需任何订阅**。

## 配置

### 模式 (`.claude/mode.md`)
- `new` — Claude 在会话开始时展示功能和导览
- `experienced` — Claude 跳过导览，命令直接执行

### 风格 (`.claude/style.md`)
- **经验水平**: `beginner` / `intermediate` / `advanced`
- **深度**: `quick` (≤500字) / `balanced` (≤1500字) / `deep` (无限制)
- **语气**: `professional` / `conversational`
- **覆盖范围**: `global` (美股+港股+A股) / `us-only` / `hk-only`

## 贡献

欢迎贡献！请确保：
- 使用的所有数据源都是免费的，并有公开文档
- 保持或增强多市场支持（美股、港股、A股）
- 不引入外部项目依赖
- 所有 Python 文件通过 `python -m py_compile` 编译检查

## 许可证

Apache License 2.0 — 详见 [LICENSE](LICENSE)。
