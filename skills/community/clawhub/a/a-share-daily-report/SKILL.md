
# A股日报生成器 - Skill 使用说明

> **Skill ID**: `a-share-daily-report`
> **版本**: v1.0
> **维护者**: 阿宽
> **最后更新**: 2026-04-02

---

## 概述

本 Skill 提供 **A 股日报自动生成**能力，通过 OpenClaw 平台一键生成专业的市场早报和晚报。

**适用场景**：
- 每日交易前的市场预判（早报，建议 6:00-9:00 生成）
- 收盘后的复盘总结（晚报，建议 15:30-18:00 生成）
- 量化策略的辅助决策支持

---

## 核心能力

### 1. 生成早报（盘前预测）

```bash
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report \
  --mode morning \
  [--date YYYY-MM-DD] \
  [--publish]
```

**输出**：`reports/morning/A股早报-YYYYMMDD.md`

**内容**：
- 30 秒总览（一句话总结 + 核心机会 + 风险提示）
- 自选股预测（基于昨日行情 + 均线/量比技术分析）
- 核心决策（交易策略 + 关注标的含介入区间/止损 + 凯利公式仓位）
- 主要指数行情
- 美股市场 + 期指数据
- 行业资金流向
- 国内要闻（分级新闻）

### 2. 生成晚报（盘后复盘）

```bash
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report \
  --mode evening \
  [--date YYYY-MM-DD] \
  [--publish]
```

**输出**：`reports/evening/A股晚报-YYYYMMDD.md`

**内容**：
- 30 秒总览（市场走势 + 情绪 + 资金一句话总结 + 明日展望）
- 自选股复盘（涨跌统计 + 最佳/最差表现 + 明日策略）
- 市场全景（情绪评分 0-100）
- 盘面深度（炸板率、涨跌幅统计）
- 主要指数 + 全球资产
- 技术面分析（RSI、MACD、支撑阻力）
- 综合分析（大盘走势、量能、风格分化）
- 主题投资追踪（算力/半导体/新能源等 8 大主题）
- 板块全景 + 龙虎榜
- 今日要闻

### 3. 飞书发布（可选）

```bash
--publish  # 启用发布到飞书
```

**前置配置**：

在项目根目录 `.env` 中配置：
```bash
FEISHU_NOTIFY_OPEN_ID=ou_xxxxxxxxxxxx   # 飞书用户 open_id
MX_APIKEY=mkt_xxxxxxxx                   # mx-data API 密钥（可选）
```

或在 `config/config.yaml` 中配置：
```yaml
publish:
  feishu_doc:
    enabled: true
    folder_token: ""          # 文件夹 token（可选）
  feishu_message:
    enabled: true
    target_chat_id: "ou_xxxxxxxxxxxx"
```

**发布结果**：
- 自动创建飞书云文档
- 发送消息通知（含文档链接）
- OpenClaw 环境自动使用真实 API，其他环境使用模拟实现

---

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--mode` | str | 是 | `morning` | `morning`（早报）或 `evening`（晚报） |
| `--date` | str | 否 | 今天 | 报告日期，格式 `YYYY-MM-DD` |
| `--publish` | flag | 否 | False | 是否发布到飞书 |
| `--config` | str | 否 | 默认路径 | 自定义配置文件路径 |
| `--outdir` | str | 否 | 配置值 | 覆盖输出目录 |

---

## 配置文件

### config/config.yaml

```yaml
# 数据源配置
data_sources:
  akshare:          # 主数据源：A 股指数/板块/情绪/龙虎榜
    enabled: true
    cache_ttl: 3600
  tushare:          # 备用：资金流向
    enabled: true
  mx_data:          # 期指数据（A50、沪深300）
    enabled: true
    api_key_env: "MX_APIKEY"
  sina:             # 新浪财经
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
    folder_token: ""
  feishu_message:
    enabled: false
    target_chat_id: ""
  pdf:
    enabled: false
    engine: "wkhtmltopdf"
```

### config/watchlist.yaml

```yaml
watchlist:
  - code: "002594.SZ"
    name: "比亚迪"
    note: "新能源车龙头"
  - code: "300308.SZ"
    name: "中际旭创"
    note: "光模块龙头"
```

**格式**：`xxxxxx.SZ`（深市）、`xxxxxx.SH`（沪市）。建议 3-5 只核心持仓。

---

## 测试

```bash
# 全部测试
./venv/bin/python3 -m pytest skills/a-share-daily-report/tests/ -v

# 分析模块（10 用例）
./venv/bin/python3 -m pytest skills/a-share-daily-report/tests/test_analyzer.py -v

# 渲染模块（5 用例）
./venv/bin/python3 -m pytest skills/a-share-daily-report/tests/test_renderer.py -v
```

---

## 架构

```
generate_report.py (主控制器)
  ├── DataFetcher (数据采集, 1600+ 行)
  │   ├── get_index_data()             # 指数行情
  │   ├── get_market_sentiment()       # 市场情绪
  │   ├── get_money_flow()             # 资金流向
  │   ├── get_sector_data()            # 板块数据
  │   ├── get_lhb_data()               # 龙虎榜
  │   ├── get_us_market()              # 美股市场
  │   ├── get_futures_data()           # 期指数据
  │   ├── get_news()                   # 新闻
  │   ├── get_market_overview()        # 市场全景
  │   ├── get_market_depth()           # 盘面深度
  │   ├── get_major_indices()          # 主要指数
  │   ├── get_global_assets()          # 全球资产
  │   ├── get_industry_fund_flow()     # 行业资金流
  │   └── get_watchlist_performance()  # 自选股行情
  │
  ├── Analyzer (分析引擎, 978 行)
  │   ├── generate_summary()           # 30 秒总览
  │   ├── analyze_watchlist_*()        # 自选股分析
  │   ├── generate_trading_strategy()  # 交易策略
  │   ├── analyze_focus_stocks()       # 关注标的
  │   ├── suggest_position()           # 凯利公式仓位
  │   ├── analyze_market_overview()    # 市场全景
  │   ├── analyze_technical_analysis() # 技术面分析
  │   ├── analyze_comprehensive()      # 综合分析
  │   ├── analyze_theme_tracking()     # 主题投资追踪
  │   └── classify_news()             # 新闻分级
  │
  ├── Renderer (报告渲染, 878 行)
  │   ├── render_morning_report()
  │   └── render_evening_report()
  │
  └── Publisher (发布器)
      ├── publish_morning_report()
      └── publish_evening_report()
```

**数据流**：采集 → 分析 → 渲染 → 保存 →（可选）发布

**降级策略**：主源失败 → 备用源 → Mock 数据。所有源失败时仍可生成报告。

---

## 数据源

| 数据项 | 主源 | 备用源 | 说明 |
|--------|------|--------|------|
| 指数数据 | akshare | yfinance | 实时行情含成交额 |
| 市场情绪 | akshare (涨停/连板) | Mock | 涨停家数、连板高度 |
| 资金流向 | akshare (北向资金) | Mock | 北向/主力净流入 |
| 行业板块 | akshare | Mock | 行业/概念板块涨跌 |
| 龙虎榜 | akshare | Mock | 机构游资买卖 |
| 美股数据 | yfinance | Mock | 纳指/标普/道指 |
| 期指数据 | mx-data API | Mock | A50/沪深300 期指 |
| 新闻 | mx-search API | Mock | 财经新闻 + 分级 |
| 全球资产 | mx-data API | Mock | 美元/黄金/原油 |

---

## 调试

```bash
# 启用详细日志
export LOG_LEVEL=DEBUG
./venv/bin/python3 -m skills.a-share-daily-report.scripts.generate_report --mode morning

# 验证数据源连通性
./venv/bin/python3 -m skills.a-share-daily-report.scripts.verify_data_sources

# 验证数据真实性
./venv/bin/python3 -m skills.a-share-daily-report.scripts.verify_data_truth
```

---

## 已知限制

1. **akshare SSL**：当前环境可能存在 SSL 限制，系统自动降级到备用源
2. **数据延迟**：早报基于昨日收盘数据，晚报使用当日数据
3. **飞书发布**：需要用户配置 `FEISHU_NOTIFY_OPEN_ID` 或 `target_chat_id`
4. **自选股数量**：建议不超过 5 只

---

## 扩展开发

### 添加新数据源

在 `data_fetcher.py` 中添加方法，返回统一格式：
```python
def get_your_data(self, dt):
    return {"success": True, "data": ..., "source": "your_source"}
```

### 添加新分析维度

在 `analyzer.py` 中添加方法，输入 `data` 字典，返回统一格式。

### 添加新报告章节

在 `renderer.py` 中修改对应的 `render_*_report` 方法。

---

**状态**：生产就绪
**最后更新**：2026-04-02
