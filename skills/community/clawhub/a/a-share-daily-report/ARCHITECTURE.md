
# A股日报 - 软件架构设计文档

&gt; 本文档定义A股日报生成器的软件架构、模块划分、数据流和目录结构

---

## 🎯 现有技能复用说明

### 已安装并复用的技能（🎯 标记）

| 技能名称 | 路径 | 用途 | 复用方式 |
|---------|------|------|---------|
| **akshare-cn-market** | `skills/akshare-cn-market/` | A股指数、涨跌停、龙虎榜、资金流向、交易日历 | 直接 import 使用 Python 接口 |
| **tushare-skills** | `skills/tushare-skills/` | tushare 数据源（降级备用） | 直接 import 使用 Python 接口 |
| **mx-data** | `skills/mx-data/` | 东方财富权威数据（自然语言查询） | 调用 API 或使用 Skill 接口 |
| **mx-search** | `skills/mx-search/` | 财经新闻、宏观政策 | 调用 API 或使用 Skill 接口 |

### 不适用的技能（❌ 标记）

| 技能名称 | 原因 |
|---------|------|
| stock-analysis | 美股/Yahoo Finance，不适用A股 |
| us-stock-analysis | 美股分析，不适用 |

### 技能复用示例代码

```python
# 复用 akshare-cn-market Skill
import sys
sys.path.append('/Users/yibiao/.openclaw/workspace-trader/skills/akshare-cn-market')
from scripts.trade_cal import is_trade_day, prev_trade_day
import akshare as ak

# 获取指数数据（直接用 akshare）
df = ak.stock_zh_index_daily(symbol="sh000001")

# 获取涨跌停数据
df = ak.stock_zt_pool_em(date="20260328")

# 获取交易日历
if not is_trade_day("2026-03-28"):
    last_close = prev_trade_day("2026-03-28")

# 复用 mx-data Skill（自然语言查询）
# 通过 curl 调用 API，或直接使用 Skill 接口

# 复用 mx-search Skill（新闻查询）
# 通过 curl 调用 API，或直接使用 Skill 接口
```

---

## 🏗️ 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                          用户层                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  早报预测版  │  │  晚报复盘版  │  │  配置文件     │      │
│  │  --mode morning│  │ --mode evening│  │  config.yaml │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         业务逻辑层                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  ReportGenerator (主控制器)               │  │
│  │  - generate_morning_report()                            │  │
│  │  - generate_evening_report()                            │  │
│  │  - publish_report()                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│         │                    │                     │            │
│         ▼                    ▼                     ▼            │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│  │  数据采集模块  │   │  分析模块     │   │  报告生成模块  │   │
│  │  DataFetcher │   │  Analyzer    │   │  Renderer    │   │
│  └──────────────┘   └──────────────┘   └──────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   发布模块 (Publisher)                   │  │
│  │  - create_feishu_doc()    创建飞书文档                  │  │
│  │  - convert_to_pdf()        转换PDF                      │  │
│  │  - send_feishu_message()   发送飞书消息                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         数据源层                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ 🎯 akshare  │  │ 🎯 tushare-  │  │ 🎯 mx-data   │      │
│  │   (新浪源)   │  │   skills     │  │   (东方财富)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  新浪财经API │  │ 🎯 mx-search │  │  配置文件     │      │
│  │  (美股/商品) │  │   (新闻)     │  │  (自选股)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         存储层                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  报告输出    │  │  数据缓存     │  │  日志文件     │      │
│  │  Markdown    │  │  cache/       │  │  logs/        │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 目录结构

```
skills/a-share-daily-report/
├── STRUCTURE.md          # 内容结构规范
├── DATA_SOURCES.md       # 数据源配置表
├── ARCHITECTURE.md       # 软件架构设计（本文件）
├── INTERFACE.md          # 接口设计文档
├── TODO.md               # 执行计划TODO
├── TESTING.md            # 测试方案
├── config/               # 配置文件目录
│   ├── config.yaml       # 主配置文件
│   └── watchlist.yaml    # 自选股配置
├── scripts/              # 脚本目录
│   ├── __init__.py
│   ├── generate_report.py     # 主入口脚本
│   ├── data_fetcher.py        # 数据采集模块
│   ├── analyzer.py            # 分析模块
│   ├── renderer.py            # 报告生成模块
│   ├── publisher.py           # 发布模块（飞书/PDF）
│   ├── trade_calendar.py      # 交易日历（复用akshare技能）
│   └── utils/                 # 工具函数
│       ├── __init__.py
│       ├── cache.py           # 缓存工具
│       ├── logger.py          # 日志工具
│       └── helpers.py         # 辅助函数
├── cache/                # 数据缓存目录（gitignore）
│   ├── akshare/
│   ├── tushare/
│   └── sina/
├── logs/                 # 日志目录（gitignore）
│   └── report_generator.log
├── reports/              # 报告输出目录
│   ├── morning/
│   └── evening/
└── tests/                # 测试目录
    ├── __init__.py
    ├── test_data_fetcher.py
    ├── test_analyzer.py
    ├── test_renderer.py
    └── test_integration.py
```

---

## 🧩 模块划分

### 1. ReportGenerator（主控制器）
**职责**：协调整个报告生成流程

**主要方法**：
```python
class ReportGenerator:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.data_fetcher = DataFetcher(self.config)
        self.analyzer = Analyzer(self.config)
        self.renderer = Renderer(self.config)

    def generate_morning_report(self, date: str = None) -&gt; str:
        """生成早报预测版"""
        pass

    def generate_evening_report(self, date: str = None) -&gt; str:
        """生成晚报复盘版"""
        pass
```

---

### 2. DataFetcher（数据采集模块）
**职责**：从各数据源采集原始数据，处理降级逻辑

**主要方法**：
```python
class DataFetcher:
    def __init__(self, config: dict):
        self.config = config

    # ===== A股数据 =====
    def get_index_data(self, index_code: str, date: str) -&gt; dict:
        """获取指数数据（优先级：akshare &gt; tushare &gt; mx-data）"""
        pass

    def get_market_sentiment(self, date: str) -&gt; dict:
        """获取市场情绪数据（涨跌停、炸板率等）"""
        pass

    def get_money_flow(self, date: str) -&gt; dict:
        """获取资金流向数据（北向、主力）"""
        pass

    def get_sector_data(self, date: str) -&gt; dict:
        """获取板块数据"""
        pass

    def get_longhubang(self, date: str) -&gt; dict:
        """获取龙虎榜数据"""
        pass

    # ===== 国际盘面 =====
    def get_us_market(self) -&gt; dict:
        """获取美股数据（新浪财经API）"""
        pass

    def get_hk_market(self) -&gt; dict:
        """获取港股数据"""
        pass

    def get_commodities(self) -&gt; dict:
        """获取大宗商品数据（原油、黄金、铜）"""
        pass

    def get_forex(self) -&gt; dict:
        """获取外汇数据（美元指数、人民币汇率）"""
        pass

    def get_index_futures(self) -&gt; dict:
        """获取期指数据（A50、沪深300）"""
        pass

    # ===== 新闻 =====
    def get_news(self, date: str, limit: int = 10) -&gt; list:
        """获取财经新闻"""
        pass
```

---

### 3. Analyzer（分析模块）
**职责**：对原始数据进行分析，生成有价值的洞察

**主要方法**：
```python
class Analyzer:
    def __init__(self, config: dict):
        self.config = config
        self.watchlist = load_watchlist(config['watchlist_path'])

    # ===== 30秒总览分析 =====
    def generate_summary(self, data: dict, mode: str) -&gt; dict:
        """生成30秒总览"""
        pass

    # ===== 自选股分析 =====
    def analyze_watchlist_morning(self, data: dict) -&gt; list:
        """早报：自选股简洁预测"""
        pass

    def analyze_watchlist_evening(self, data: dict) -&gt; dict:
        """晚报：自选股复盘"""
        pass

    # ===== 核心决策分析 =====
    def generate_trading_strategy(self, data: dict) -&gt; dict:
        """生成交易策略（进攻/防守/观望）"""
        pass

    def analyze_focus_stocks(self, data: dict) -&gt; list:
        """分析今日关注标的"""
        pass

    def suggest_position(self, data: dict) -&gt; dict:
        """建议仓位"""
        pass

    # ===== 市场分析 =====
    def analyze_market_sentiment(self, data: dict) -&gt; dict:
        """分析市场情绪"""
        pass

    def analyze_international_impact(self, data: dict) -&gt; list:
        """分析国际盘面关联影响"""
        pass

    # ===== 新闻分级 =====
    def classify_news(self, news_list: list) -&gt; list:
        """新闻重要性分级（🔴🟡🟢）"""
        pass
```

---

### 4. Renderer（报告生成模块）
**职责**：将分析结果渲染成Markdown格式

**主要方法**：
```python
class Renderer:
    def __init__(self, config: dict):
        self.config = config

    def render_morning_report(self, analysis_result: dict) -&gt; str:
        """渲染早报预测版Markdown"""
        pass

    def render_evening_report(self, analysis_result: dict) -&gt; str:
        """渲染晚报复盘版Markdown"""
        pass

    # ===== 辅助渲染方法 =====
    def _render_30sec_overview(self, data: dict) -&gt; str:
        pass

    def _render_watchlist_morning(self, data: list) -&gt; str:
        pass

    def _render_watchlist_evening(self, data: dict) -&gt; str:
        pass

    def _render_core_decision(self, data: dict) -&gt; str:
        pass

    def _render_a_market(self, data: dict) -&gt; str:
        pass

    def _render_international(self, data: dict) -&gt; str:
        pass

    def _render_news(self, news_list: list) -&gt; str:
        pass

    def _render_tomorrow_outlook(self, data: dict) -&gt; str:
        pass
```

---

### 5. Publisher（发布模块）
**职责**：创建飞书文档、转换PDF、发送飞书消息

**主要方法**：
```python
class Publisher:
    def __init__(self, config: dict):
        self.config = config
        self.feishu_config = load_feishu_config(config)

    def publish_report(self, markdown_content: str, mode: str, date: str) -&gt; dict:
        """完整发布流程：创建飞书文档 → 转换PDF → 发送消息"""
        pass

    def create_feishu_doc(self, markdown_content: str, title: str) -&gt; str:
        """创建飞书文档，返回文档链接"""
        pass

    def convert_to_pdf(self, markdown_content: str, output_path: str) -&gt; str:
        """Markdown转PDF，返回PDF文件路径"""
        pass

    def send_feishu_message(self, doc_url: str, pdf_path: str, mode: str, date: str) -&gt; bool:
        """发送飞书消息到指定对话"""
        pass
```

---

## 🔄 数据流

### 早报预测版数据流
```
1. 确定交易日期
   ├─ 检查今天是否为交易日
   └─ 非交易日 → 使用最近一个收盘日

2. 采集数据
   ├─ A股昨日数据（指数、情绪、资金、板块）
   ├─ 昨夜今晨数据（美股、中概、商品、外汇、期指）
   └─ 国内要闻（10篇）

3. 分析数据
   ├─ 生成30秒总览
   ├─ 自选股简洁预测
   ├─ 核心决策（策略、关注、仓位）
   └─ 国际盘面关联影响

4. 渲染报告
   └─ 生成Markdown格式早报

5. 保存输出
   └─ reports/morning/A股早报-YYYYMMDD.md
```

### 晚报复盘版数据流
```
1. 确定交易日期
   └─ 使用今天（交易日）

2. 采集数据
   ├─ A股今日数据（指数、情绪、资金、板块、龙虎榜）
   ├─ 港股今日数据
   └─ 今日要闻（10篇）

3. 分析数据
   ├─ 生成30秒总览
   ├─ 自选股复盘
   ├─ 市场深度分析
   └─ 新闻重要性分级

4. 渲染报告
   └─ 生成Markdown格式晚报

5. 保存输出
   └─ reports/evening/A股晚报-YYYYMMDD.md

6. 发布流程（新增）
   ├─ 创建飞书文档
   ├─ 转换PDF文件
   └─ 发送飞书消息（文档链接+PDF）
```

---

### 完整发布数据流（新增）
```
Markdown报告
    │
    ▼
┌─────────────────────────────────┐
│  Publisher.publish_report()     │
├─────────────────────────────────┤
│  1. 创建飞书文档                 │
│     feishu_create_doc()         │
│     ↓ 返回 doc_url              │
│  2. 转换PDF                     │
│     convert_to_pdf()            │
│     ↓ 返回 pdf_path             │
│  3. 发送飞书消息                │
│     send_feishu_message()       │
│     包含：doc_url + pdf_path    │
└─────────────────────────────────┘
```

---

## ⚙️ 配置文件设计

### config.yaml（主配置）
```yaml
# A股日报生成器配置
version: "1.0"

# 输出配置
output:
  base_dir: "reports"
  morning_subdir: "morning"
  evening_subdir: "evening"

# 数据源配置
data_sources:
  # 优先级1：AKShare
  akshare:
    enabled: true
    cache_ttl: 3600  # 缓存1小时

  # 优先级2：tushare-skills
  tushare:
    enabled: true
    path: "../../tushare-skills/tushare"
    cache_ttl: 3600

  # 优先级3：mx-data
  mx_data:
    enabled: true
    api_key_env: "MX_APIKEY"

  # 优先级4：新浪财经API
  sina:
    enabled: true
    cache_ttl: 1800  # 缓存30分钟

# 自选股配置
watchlist:
  path: "config/watchlist.yaml"

# 日志配置
logging:
  level: "INFO"
  file: "logs/report_generator.log"
  max_size: "10MB"
  backup_count: 5

# 发布配置
publish:
  # 飞书文档配置
  feishu_doc:
    enabled: true
    folder_token: ""  # 飞书文件夹token（可选）

  # PDF转换配置
  pdf:
    enabled: true
    output_dir: "reports/pdf"
    engine: "weasyprint"  # 或 "wkhtmltopdf"

  # 飞书消息推送
  feishu_message:
    enabled: true
    target_chat_id: "ou_4e28c025ac8a3beb1bf10621a9ddeb86"
    message_template: |
      📊 {mode}已生成！
      📅 日期：{date}
      📄 飞书文档：{doc_url}
      📑 PDF文件：{pdf_path}
```

### watchlist.yaml（自选股）
```yaml
# 自选股配置
watchlist:
  - code: "002594.SZ"
    name: "比亚迪"
    note: "新能源车龙头"

  - code: "300308.SZ"
    name: "中际旭创"
    note: "光模块龙头"

  - code: "00700.HK"
    name: "腾讯控股"
    note: "港股科技龙头"
```

---

## 🎯 关键设计决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| **主语言** | Python | 金融生态完善，akshare/tushare都是Python |
| **配置格式** | YAML | 人可读，支持注释 |
| **缓存策略** | 本地文件缓存 | 减少API调用，提高稳定性 |
| **数据源降级** | 优先级链 | 确保主源失败时仍能生成报告 |
| **错误处理** | 单模块失败不影响整体 | 部分数据缺失时仍能输出报告 |
| **输出格式** | Markdown | 易读，可转换为PDF/HTML |

---

## 📝 依赖项

```txt
# requirements.txt
akshare&gt;=1.18.0
pandas&gt;=2.0.0
pyyaml&gt;=6.0
python-dateutil&gt;=2.8.0
```

---

*本文档定义了软件架构，详细接口设计请参考 INTERFACE.md*

