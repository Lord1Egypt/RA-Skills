
# A股日报生成器

**自动生成A股市场每日早报/晚报，支持飞书发布**

基于 OpenClaw 平台的专业 A 股市场日报生成系统。自动采集多源市场数据、智能分析行情、生成结构化 Markdown 报告，并可一键发布到飞书文档。

---

## 核心特性

- **多源数据采集** - 集成 akshare、yfinance、tushare、mx-data/mx-search，支持多级降级策略
- **智能分析引擎** - 30 秒总览、自选股预测、交易策略、凯利公式仓位、新闻分级
- **双模式报告** - 早报预测版（盘前预判）+ 晚报复盘版（盘后总结）
- **飞书集成** - 自动创建飞书云文档 + 消息通知推送
- **主题投资追踪** - 算力、半导体、新能源等预定义主题板块表现追踪
- **技术面分析** - RSI、MACD、支撑阻力位估算
- **全球资产联动** - 美元、黄金、原油等全球资产数据

---

## 项目结构

```
a-share-daily-report/
├── config/
│   ├── config.yaml              # 主配置文件（数据源、输出、发布）
│   └── watchlist.yaml           # 自选股列表
├── scripts/
│   ├── __init__.py
│   ├── generate_report.py       # 主入口（ReportGenerator 类）
│   ├── data_fetcher.py          # 数据采集模块（1600+ 行，多源降级）
│   ├── analyzer.py              # 分析引擎（978 行，策略/仓位/主题）
│   ├── renderer.py              # Markdown 渲染（早报/晚报模板）
│   ├── publisher.py             # 飞书文档发布 + 消息通知
│   ├── trade_calendar.py        # 交易日历（节假日/周末判断）
│   ├── verify_data_sources.py   # 数据源连通性验证工具
│   ├── verify_data_truth.py     # 数据真实性验证工具
│   └── utils/
│       ├── __init__.py          # 包导出
│       ├── cache.py             # 基于文件的缓存层（TTL 控制）
│       ├── logger.py            # 日志配置
│       └── helpers.py           # 工具函数（日期/数值/格式化）
├── tests/
│   ├── test_analyzer.py         # 分析模块单元测试（10 用例）
│   ├── test_renderer.py         # 渲染模块单元测试（5 用例）
│   ├── test_data_fetcher.py     # 数据采集单元测试（9 用例）
│   └── test_integration.py      # 集成测试（6 用例）
├── reports/                     # 生成的报告（自动创建）
│   ├── morning/
│   └── evening/
├── validation/                  # 验证脚本
├── SKILL.md                     # 技能使用说明
├── TODO.md                      # 开发进度
├── README.md                    # 本文件
└── _meta.json                   # 技能元数据
```

---

## 快速开始

### 环境要求

- Python 3.10+
- 虚拟环境（推荐使用项目根目录的 `venv`）
- 依赖包：`akshare`、`pyyaml`、`pandas`、`python-dotenv`、`yfinance`

### 安装依赖

```bash
cd /Users/yibiao/.openclaw/workspace-trader
./venv/bin/pip install -r skills/a-share-daily-report/requirements.txt
```

### 配置自选股

编辑 `config/watchlist.yaml`：

```yaml
watchlist:
  - code: "002594.SZ"
    name: "比亚迪"
    note: "新能源车龙头"
  - code: "300308.SZ"
    name: "中际旭创"
    note: "光模块龙头"
```

格式说明：`xxxxxx.SZ`（深市）、`xxxxxx.SH`（沪市），建议 3-5 只核心持仓。

### 生成报告

```bash
# 生成早报（默认今日）
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report --mode morning

# 生成晚报
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report --mode evening

# 指定日期
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report --mode evening --date 2026-03-28

# 生成并发布到飞书
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report --mode morning --publish

# 自定义输出目录
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report --mode morning --outdir /tmp/reports
```

---

## 命令行参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--mode` | str | 是 | `morning` | `morning`（早报）或 `evening`（晚报） |
| `--date` | str | 否 | 今天 | 报告日期，格式 `YYYY-MM-DD` |
| `--config` | str | 否 | 默认路径 | 自定义配置文件路径 |
| `--publish` | flag | 否 | False | 是否发布到飞书 |
| `--outdir` | str | 否 | 配置值 | 覆盖输出目录 |

---

## 配置文件

### config/config.yaml

```yaml
# 数据源配置（按优先级排列）
data_sources:
  akshare:                    # 主数据源：A 股指数、板块、情绪、龙虎榜
    enabled: true
    cache_ttl: 3600
  tushare:                    # 备用数据源：资金流向
    enabled: true
    cache_ttl: 3600
  mx_data:                    # 期指数据（A50、沪深300）
    enabled: true
    api_key_env: "MX_APIKEY"
  sina:                       # 新浪财经 API
    enabled: true
    cache_ttl: 1800

# 输出配置
output:
  base_dir: "/Users/yibiao/Desktop/openclaw_doc/财经日报"
  morning_subdir: "morning"
  evening_subdir: "evening"

# 自选股路径
watchlist:
  path: "config/watchlist.yaml"

# 发布配置
publish:
  feishu_doc:
    enabled: true
    folder_token: ""          # 飞书文件夹 token（可选，留空到个人空间）
  feishu_message:
    enabled: false
    target_chat_id: ""        # 飞书用户 open_id
  pdf:
    enabled: false
    engine: "wkhtmltopdf"
```

### 环境变量（.env 文件）

在项目根目录 `/Users/yibiao/.openclaw/workspace-trader/.env` 中配置：

```bash
MX_APIKEY=mkt_xxxxxxxx               # mx-data/mx-search API 密钥
TUSHARE_TOKEN=xxxxxxxx               # tushare 令牌
FEISHU_NOTIFY_OPEN_ID=ou_xxxx        # 飞书用户 open_id
```

---

## 报告内容

### 早报预测版

| 章节 | 内容 |
|------|------|
| 30 秒总览 | 一句话总结、核心机会（关键词提取）、风险提示（三级） |
| 自选股简洁预测 | 基于昨日行情 + 技术面（均线/量比）生成看涨/偏多/震荡/偏空/看跌判断 |
| 核心决策 | 交易策略（进攻/中性/防守）、关注标的（介入区间+止损位）、仓位建议（凯利公式） |
| 主要指数 | 上证/深证/创业板等 10 个指数实时行情 |
| 美股市场 | 纳指/标普/道指涨跌 + 中概股表现 |
| 期指数据 | A50 期指、沪深 300 期指（mx-data API） |
| 行业资金流向 | 北向资金、主力资金流向 |
| 国内要闻 | 前 10 条新闻，按重要性分级（🔴重大/🟡中等/🟢一般） |

### 晚报复盘版

| 章节 | 内容 |
|------|------|
| 30 秒总览 | 市场走势、情绪、资金一句话总结 + 核心亮点 + 明日展望 |
| 自选股复盘 | 整体涨跌统计、最佳/最差表现股、明日策略 |
| 市场全景 | 情绪评分（0-100）、涨跌家数、涨停/跌停统计 |
| 盘面深度 | 炸板率、涨跌幅超 5% 统计 |
| 主要指数 | 10 个 A 股主要指数行情 |
| 全球资产 | 美元指数、黄金、原油价格 |
| 技术面分析 | RSI 估算、MACD 信号、支撑/阻力位 |
| 综合分析 | 大盘走势判断、量能分析、风格分化、后市展望 |
| 主题投资追踪 | 算力、半导体、新能源等主题板块表现 |
| 板块全景 | 行业/概念板块 Top 排行 |
| 龙虎榜 | 机构/游资买卖数据 |
| 今日要闻 | 分级新闻列表 |

---

## 数据源

| 数据项 | 主源 | 备用源 | 说明 |
|--------|------|--------|------|
| 指数数据 | akshare (stock_zh_index_spot_em) | yfinance | 实时行情含成交额 |
| 市场情绪 | akshare (涨停/连板 API) | Mock | 涨停家数、连板高度 |
| 资金流向 | akshare (北向资金) | Mock | 北向/主力净流入 |
| 行业板块 | akshare (stock_board_industry_name_em) | Mock | 行业/概念板块涨跌 |
| 龙虎榜 | akshare (stock_lhb_detail) | Mock | 机构游资买卖 |
| 美股数据 | yfinance | Mock | 纳指/标普/道指 |
| 期指数据 | mx-data API | Mock | A50/沪深300 期指 |
| 新闻 | mx-search API | Mock | 财经新闻 + 重要性分级 |
| 全球资产 | mx-data API | Mock | 美元/黄金/原油 |

**降级策略**：主源失败自动降级到备用源，所有源失败时使用 Mock 数据生成报告。

---

## 测试

```bash
# 运行全部测试
cd /Users/yibiao/.openclaw/workspace-trader
./venv/bin/python3 -m pytest skills/a-share-daily-report/tests/ -v

# 分析模块测试（10 用例）
./venv/bin/python3 -m pytest skills/a-share-daily-report/tests/test_analyzer.py -v

# 渲染模块测试（5 用例）
./venv/bin/python3 -m pytest skills/a-share-daily-report/tests/test_renderer.py -v

# 数据采集测试（9 用例，网络相关可能失败）
./venv/bin/python3 -m pytest skills/a-share-daily-report/tests/test_data_fetcher.py -v

# 集成测试（6 用例）
./venv/bin/python3 -m pytest skills/a-share-daily-report/tests/test_integration.py -v
```

**测试现状**：
- `test_analyzer.py`：10/10 通过
- `test_renderer.py`：3/5 通过（部分依赖实时数据的用例可能失败）
- `test_data_fetcher.py`：核心逻辑通过（网络/SSL 相关用例在受限环境可能失败）
- `test_integration.py`：核心流程通过（部分依赖外部 API 的用例可能失败）

---

## 飞书发布配置

### 方法 A：使用 .env 文件（推荐）

在项目根目录 `.env` 中设置：
```bash
FEISHU_NOTIFY_OPEN_ID=ou_xxxxxxxxxxxx
```

### 方法 B：使用 config.yaml

```yaml
publish:
  feishu_message:
    enabled: true
    target_chat_id: "ou_xxxxxxxxxxxx"
  feishu_doc:
    enabled: true
    folder_token: "fldcnXXXX"    # 可选
```

### 发布流程

1. `--publish` 参数启用发布
2. Publisher 检测是否在 OpenClaw 环境（自动使用真实飞书 API）
3. 创建飞书云文档（标题格式：`A股早报-20260328`）
4. 发送消息通知（包含文档链接）
5. 非 OpenClaw 环境使用模拟实现

---

## 架构

```
generate_report.py (主控制器)
  ├── DataFetcher (数据采集)
  │   ├── get_index_data()          # 指数行情
  │   ├── get_market_sentiment()    # 市场情绪
  │   ├── get_money_flow()          # 资金流向
  │   ├── get_sector_data()         # 板块数据
  │   ├── get_lhb_data()            # 龙虎榜
  │   ├── get_us_market()           # 美股市场
  │   ├── get_futures_data()        # 期指数据
  │   ├── get_news()                # 新闻
  │   ├── get_market_overview()     # 市场全景
  │   ├── get_market_depth()        # 盘面深度
  │   ├── get_major_indices()       # 主要指数
  │   ├── get_global_assets()       # 全球资产
  │   ├── get_industry_fund_flow()  # 行业资金流
  │   └── get_watchlist_performance() # 自选股行情
  │
  ├── Analyzer (分析引擎)
  │   ├── generate_summary()           # 30 秒总览
  │   ├── analyze_watchlist_morning()  # 早报自选股预测
  │   ├── analyze_watchlist_evening()  # 晚报自选股复盘
  │   ├── generate_trading_strategy()  # 交易策略
  │   ├── analyze_focus_stocks()       # 关注标的
  │   ├── suggest_position()           # 凯利公式仓位
  │   ├── analyze_market_overview()    # 市场全景
  │   ├── analyze_market_depth()       # 盘面深度
  │   ├── analyze_major_indices()      # 主要指数
  │   ├── analyze_global_assets()      # 全球资产
  │   ├── analyze_technical_analysis() # 技术面分析
  │   ├── analyze_comprehensive()      # 综合分析
  │   ├── analyze_theme_tracking()     # 主题投资追踪
  │   └── classify_news()             # 新闻分级
  │
  ├── Renderer (报告渲染)
  │   ├── render_morning_report()
  │   └── render_evening_report()
  │
  └── Publisher (发布器)
      ├── publish_morning_report()
      └── publish_evening_report()
```

**数据流**：采集 → 分析 → 渲染 → 保存 →（可选）发布

---

## 故障排除

### ModuleNotFoundError: No module named 'scripts'

使用 `-m` 模式运行：
```bash
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report --mode morning
```

### akshare SSL 错误

当前环境可能存在 SSL 限制，系统会自动降级到备用数据源或 Mock 数据。配置代理可解决。

### 报告数据全是模拟值

检查 `.env` 中的 `MX_APIKEY` 和 `TUSHARE_TOKEN` 是否正确配置。

### 飞书发布失败

确认 `FEISHU_NOTIFY_OPEN_ID` 或 `config.yaml` 中的 `target_chat_id` 已正确设置。

---

## 开发者

- **维护者**：阿宽 & Claude
- **版本**：v1.0
- **更新日期**：2026-04-02
- **许可证**：MIT
