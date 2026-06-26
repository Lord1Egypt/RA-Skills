# 财经新闻分析器 - 个性化配置

创建此文件来自定义默认配置。

**位置**: `.baoyu-skills/finance-news-analyzer/EXTEND.md`

---

## 配置示例

```yaml
# ==================== 默认设置 ====================

# 默认新闻源
default_sources:
  - wallstreetcn      # 华尔街见闻
  - 36kr              # 36 氪
  - hackernews        # Hacker News
  - github            # GitHub Trending

# 每源默认新闻数量
default_limit: 15

# 默认输出格式
# 可选：brief（快速简报）, full（深度报告）, industry（行业报告）, stock（个股追踪）
default_output: brief

# 默认语言
# 可选：zh（中文）, en（英文）
default_language: zh

# 默认时间周期
# 可选：daily（日报）, weekly（周报）, monthly（月报）
default_period: daily


# ==================== 关注列表 ====================

# 关注的股票（用于优先分析）
watchlist:
  # 美股
  - NVDA    # 英伟达
  - TSLA    # 特斯拉
  - AAPL    # 苹果
  - MSFT    # 微软
  
  # A 股
  - 600519.SS   # 贵州茅台
  - 300750.SZ   # 宁德时代
  
  # 港股
  - 00700.HK    # 腾讯
  - 09988.HK    # 阿里

# 关注的行业
watchlist_industries:
  - 半导体
  - 新能源车
  - AI/人工智能
  - 互联网


# ==================== 情感分析配置 ====================

# 情感分析模型
# OpenAI: gpt-4o-mini, gpt-4o, gpt-4-turbo
# Anthropic: claude-3-5-sonnet-20241022, claude-3-opus-20240229
sentiment_model: gpt-4o-mini

# 置信度阈值
confidence_threshold:
  high: 0.8      # 高置信度：>80%
  medium: 0.5    # 中置信度：50-80%
  low: 0.5       # 低置信度：<50%

# 情感打分权重
sentiment_weights:
  title: 0.4     # 标题权重
  summary: 0.4   # 摘要权重
  content: 0.2   # 全文权重（如果有）


# ==================== 简报配置 ====================

# 简报中最多显示的新闻数量
brief_max_items:
  positive: 5    # 利好最多 5 条
  negative: 5    # 利空最多 5 条
  neutral: 5     # 中性最多 5 条

# 是否显示相关股票
show_related_stocks: true

# 是否显示置信度
show_confidence: true

# 是否显示投资提示
show_investment_tips: true


# ==================== 通知配置 ====================

# 重要新闻通知（仅当发现强烈利好/利空时）
enable_alerts: false

# 通知阈值
alert_threshold:
  sentiment_score_min: 80    # 强烈利好：>80 分
  sentiment_score_max: 20    # 强烈利空：<20 分

# 通知方式（未来支持）
# notification_channels:
#   - email
#   - wechat
#   - telegram


# ==================== 数据源配置 ====================

# 新闻源优先级（数字越小优先级越高）
source_priority:
  wallstreetcn: 1
  36kr: 1
  bloomberg: 2
  reuters: 2
  hackernews: 3
  github: 3

# 是否启用额外数据源
enable_premium_sources: false  # 需要付费 API


# ==================== 输出配置 ====================

# 输出目录
output_directory: reports

# 文件名格式
# 可用变量：{date}, {time}, {period}, {output_type}
filename_pattern: "finance_{output_type}_{date}.md"

# 是否生成图表
generate_charts: false  # 需要 matplotlib

# 是否保存原始数据
save_raw_data: true


# ==================== API 配置 ====================

# LLM API 配置
llm_api:
  provider: openai  # openai 或 anthropic
  timeout: 30       # 超时时间（秒）
  max_retries: 3    # 最大重试次数
  rate_limit: 10    # 每分钟最大请求数

# 新闻 API 配置（如果使用付费服务）
news_api:
  provider: newsapi  # newsapi, alphavantage, 等
  api_key: ""        # 留空使用免费抓取


# ==================== 自定义规则 ====================

# 自定义情感分析规则
custom_sentiment_rules:
  # 特定关键词的情感权重
  keywords:
    "革命性突破": 95    # 强烈利好
    "重大失败": 10      # 强烈利空
    "符合预期": 50      # 中性
    "超预期": 75        # 利好
    "不及预期": 25      # 利空
  
  # 特定公司的敏感度
  company_sensitivity:
    NVDA: 1.2    # 英伟达新闻影响放大 20%
    TSLA: 1.3    # 特斯拉新闻影响放大 30%


# ==================== 报告模板 ====================

# 自定义简报模板
# 留空使用默认模板
custom_brief_template: ""
custom_full_template: ""


# ==================== 其他配置 ====================

# 是否启用调试模式
debug: false

# 日志级别
# 可选：DEBUG, INFO, WARNING, ERROR
log_level: INFO

# 是否显示进度条
show_progress: true
```

---

## 使用说明

### 1. 创建配置文件

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:APPDATA\baoyu-skills\finance-news-analyzer"
notepad "$env:APPDATA\baoyu-skills\finance-news-analyzer\EXTEND.md"

# macOS/Linux
mkdir -p ~/.baoyu-skills/finance-news-analyzer
nano ~/.baoyu-skills/finance-news-analyzer/EXTEND.md
```

### 2. 修改配置

复制上面的示例配置，根据需要修改。

### 3. 使用配置

配置文件会自动被脚本加载，无需额外操作。

```bash
# 使用配置的默认值
python scripts/main.py

# 命令行参数会覆盖配置
python scripts/main.py --source wallstreetcn --limit 30
```

---

## 配置优先级

**优先级从高到低**:

1. 命令行参数（最高优先级）
2. EXTEND.md 配置文件
3. 脚本默认值（最低优先级）

---

## 常见问题

### Q: 如何更改默认新闻源？

修改 `default_sources` 列表：

```yaml
default_sources:
  - wallstreetcn
  - 36kr
  - bloomberg
```

### Q: 如何只分析特定股票？

在 `watchlist` 中添加股票代码：

```yaml
watchlist:
  - NVDA
  - TSLA
```

然后运行：
```bash
python scripts/main.py --ticker NVDA,TSLA
```

### Q: 如何生成周报？

修改默认周期：
```yaml
default_period: weekly
default_output: industry
```

或直接命令行：
```bash
python scripts/main.py --period weekly --output industry
```

---

## 更新记录

- 2026-03-09: 初始版本
