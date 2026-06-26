# AI Daily Brief Skill

一个专为Claude Code和OpenClaw设计的AI新闻聚合技能，每日自动从数十个高质量数据源采集AI领域最新动态，生成结构化的新闻简报。

## 项目概述

AI Daily Brief Skill 是一个高效的信息聚合工具，专门用于收集和整理人工智能领域的最新动态。它从多个可靠数据源（包括技术媒体、学术平台、社区论坛和社交媒体）抓取内容，通过智能过滤，生成易于阅读的每日简报。

## 主要特性

### 📊 多源数据采集
- **RSS订阅**: 支持主流科技媒体和博客的RSS/Atom订阅
- **社交媒体**: X/Twitter关键账号
- **学术平台**: arXiv、OpenAI Blog、Hugging Face Blog等
- **网页爬虫**: 使用Playwright抓取动态网页内容
- **API接口**: Hacker News API等开放接口

### 🎯 智能内容处理
- **关键词过滤**: 基于配置的关键词包含/排除过滤
- **时效性过滤**: 自动过滤过时内容（默认72小时内）
- **去重处理**: 基于URL自动去重
- **智能排序**: 按发布时间降序排列新闻

### 📈 多格式输出
- **详细报告**: 完整的Markdown格式报告，包含所有新闻条目
- **简洁摘要**: 重点突出热门新闻的摘要报告
- **结构化数据**: JSON格式数据，便于进一步处理

### ⚡ 高性能架构
- **异步并发**: 使用asyncio并发抓取多个数据源
- **模块化设计**: 易于扩展新的抓取器类型
- **可配置性强**: 通过YAML文件灵活配置所有参数

## 快速开始

### 环境要求
- Python 3.8+
- 依赖包（见requirements.txt）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd daily-ai-brief-skill
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **安装Playwright浏览器**（如需网页爬虫）
```bash
playwright install
```

4. **运行技能**
```bash
python src/main.py
```

### 配置说明

主要配置文件为 `src/data_sources.yaml`，包含以下部分：

#### 数据源配置
```yaml
rss_sources:
  - name: "36氪 AI科技"
    url: "https://www.36kr.com/feed"
    enabled: true
    priority: 1
    num_items: 10
    filters:
      include_keywords: ["AI", "人工智能", "OpenAI"]
```

#### 抓取配置
```yaml
fetch_config:
  max_items_per_source: 15
  timeout_seconds: 30
  user_agent: "Mozilla/5.0 ..."
  max_retries: 2
  max_age_hours: 72
```

## 项目结构

```
daily-ai-brief-skill/
├── src/                    # 源码目录
│   ├── modules/           # 功能模块
│   │   ├── base_fetcher.py    # 抽象抓取器基类
│   │   ├── rss_fetcher.py     # RSS抓取器
│   │   ├── x_fetcher.py       # X/Twitter抓取器
│   │   ├── web_scraper.py     # 网页爬虫
│   │   ├── api_fetcher.py     # API抓取器
│   │   ├── fetcher_factory.py # 抓取器工厂
│   │   ├── orchestrator.py    # 抓取协调器
│   │   ├── report_generator.py # 报告生成器
│   │   └── config.py          # 配置加载器
│   ├── test/              # 测试脚本
│   └── main.py           # 运行入口
├── reports/              # 报告文件目录
├── src/data_sources.yaml # 数据源配置
├── requirements.txt      # Python依赖
├── SKILL.md             # 技能描述文件
└── README.md            # 项目说明
```

## 使用示例

### 基本使用
```bash
# 运行完整抓取流程
python src/main.py

# 查看生成的报告
ls -la reports/
cat reports/ai_news_summary_*.md
```

### 自定义配置
1. 编辑 `src/data_sources.yaml` 文件
2. 启用/禁用特定数据源
3. 调整关键词过滤规则
4. 修改抓取数量限制

### 扩展开发
如需添加新的数据源类型：
1. 在 `src/modules/` 下创建新的抓取器类
2. 继承 `BaseFetcher` 基类
3. 实现 `fetch()` 方法
4. 在 `fetcher_factory.py` 中注册


## 常见问题

### Q: 抓取速度太慢怎么办？
A: 调整 `fetch_config` 中的 `timeout_seconds` 参数，或减少每个源的 `num_items` 数量。

### Q: 如何添加新的RSS源？
A: 在 `data_sources.yaml` 的 `rss_sources` 部分添加新的配置项。

### Q: 报告生成在哪里？
A: 所有报告生成在 `reports/` 目录下，按时间戳命名。

### Q: 如何过滤特定内容？
A: 在数据源配置中添加 `filters` 部分，设置 `include_keywords` 或 `exclude_keywords`。

## 许可证

本项目采用 MIT 许可证。

## 贡献指南

欢迎提交Issue和Pull Request！在提交代码前，请确保：
1. 通过现有测试 `python run_tests.py`
2. 添加新功能的测试用例
3. 更新相关文档

## 联系方式

如有问题或建议，请通过项目仓库的Issue功能联系我们。