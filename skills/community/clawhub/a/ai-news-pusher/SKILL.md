---
name: ai-news-pusher-v2
description: AI新闻自动获取与推送Skill v2.2。新增智能产品价值评分、高质量信源过滤、三级分类机制和人工反馈迭代。支持Tavily、Brave、RSS多新闻源聚合，无需API Key即可使用RSS源。当用户需要获取AI行业最新动态、自动化新闻推送、多源新闻聚合或智能内容过滤时触发此Skill。
optional_envs:
  - name: FEISHU_WEBHOOK_URL
    description: 飞书群聊自定义机器人的Webhook URL，用于推送新闻消息（需要此变量才能实际推送）
  - name: OPENAI_API_KEY
    description: OpenAI API Key，用于LLM评分功能（可选，无Key时使用规则评分）
  - name: ANTHROPIC_API_KEY
    description: Anthropic API Key，用于LLM评分功能（可选，与OpenAI二选一）
  - name: TAVILY_API_KEY
    description: Tavily API Key，用于Tavily新闻源（可选）
  - name: BRAVE_API_KEY
    description: Brave Search API Key，用于Brave新闻源（可选）
  - name: OPENCLAW_GATEWAY_URL
    description: OpenClaw网关地址（用于定时任务，可选）
  - name: OPENCLAW_GATEWAY_TOKEN
    description: OpenClaw网关令牌（用于定时任务，⚠️ 高度敏感：可允许调度/外部控制，仅在完全理解此功能并信任运行环境时使用）
---

# AI News Pusher v2.2 - AI新闻推送

## 🎉 v2.2 重大更新！

**v2.2 全新升级：**
- ✅ **产品价值评分系统** - 基于LLM的四维度智能评分
- ✅ **高质量信源过滤** - 新增Arxiv、OpenAI博客等权威信源
- ✅ **三级分类机制** - 自动推送、待阅池、彻底拦截
- ✅ **人工反馈迭代** - 通过标记持续优化评分系统
- ✅ **数据持久化** - 完整的历史记录和反馈管理
- ✅ **管理工具** - 交互式审核、分析和配置

## 概述

本Skill提供AI新闻的自动获取和智能推送功能，支持多新闻源聚合和价值评分：
- **多源聚合** - Tavily API、Brave Search API、RSS订阅源
- **智能评分** - 基于LLM的产品价值四维度评分
- **灵活分类** - 80分以上自动推送，60-80分待审核，60分以下拦截
- **持续优化** - 通过人工反馈和分析不断改进

## 🚀 快速开始

### 1. 仅使用RSS源（无需任何API Key）

```bash
# 获取AI新闻（仅RSS源）
python3 scripts/fetch_ai_news.py --source rss --limit 10
```

### 2. 启用智能评分（推荐）

```bash
# 设置OpenAI API Key（用于评分）
export OPENAI_API_KEY=your_api_key_here

# 获取新闻并启用评分
python3 scripts/fetch_ai_news.py --source all --limit 20 --enable-scoring
```

### 3. 审核待阅池

```bash
# 交互式审核待阅池内容
python3 scripts/news_manager.py review

# 查看统计数据
python3 scripts/news_manager.py stats
```

### 4. 推送到Feishu

```bash
# 设置Feishu Webhook
export FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx

# 推送新闻
python3 scripts/push_to_feishu.py --limit 8
```

## 📖 详细使用说明

### 获取AI新闻（带评分）

```bash
python3 scripts/fetch_ai_news.py [选项]

选项:
  --limit N           返回N条新闻 (默认10)
  --days N            搜索最近N天的新闻 (默认3)
  --source SOURCE     新闻源: tavily|brave|rss|all (默认all)
  --format FORMAT     输出格式: json|text|markdown (默认json)
  --output FILE       输出到文件
  --query QUERY       搜索关键词 (默认: AI artificial intelligence)
  --enable-scoring    启用智能价值评分
  --llm-provider      LLM提供商: openai|anthropic (默认openai)
```

### 多源新闻聚合

```python
from scripts.news_sources import get_default_aggregator

# 获取聚合器（自动检测可用的API Key）
aggregator = get_default_aggregator(
    include_tavily=True,
    include_brave=True,
    include_rss=True
)

# 获取新闻
news = aggregator.fetch_all(
    query="AI artificial intelligence",
    limit=10,
    days=3
)

print(f"共获取 {len(news)} 条新闻")
```

### 智能价值评分

```python
from scripts.news_scorer import NewsScorer
from scripts.data_storage import DataStorage

# 初始化评分器
scorer = NewsScorer(llm_provider="openai")

# 批量评分
categorized = scorer.score_batch(news_list)

print(f"自动推送: {len(categorized['auto_push'])}")
print(f"待阅池: {len(categorized['gray_zone'])}")
print(f"已过滤: {len(categorized['filtered'])}")

# 保存到存储
storage = DataStorage()
storage.batch_save_gray_zone(categorized['gray_zone'])
storage.save_pushed(categorized['auto_push'])
storage.save_filtered(categorized['filtered'])
```

### 新闻管理工具

```bash
# 查看所有可用命令
python3 scripts/news_manager.py --help

# 常用命令
python3 scripts/news_manager.py review      # 审核待阅池
python3 scripts/news_manager.py stats       # 查看统计
python3 scripts/news_manager.py filtered    # 查看被过滤内容
python3 scripts/news_manager.py feedback    # 查看反馈记录
python3 scripts/news_manager.py analyze     # 分析反馈数据
python3 scripts/news_manager.py config      # 更新配置
```

### 推送到Feishu

```bash
python3 scripts/push_to_feishu.py [选项]

选项:
  --limit N           推送新闻数量 (默认8)
  --input FILE        从文件加载新闻(JSON格式)
  --multi-source      使用多源聚合
  --channel CHANNEL   推送渠道 (默认feishu)
  --dry-run           仅格式化消息，不实际发送
  --use-webhook       使用Webhook发送
```

### 配置定时推送任务

```bash
# 创建每天9点推送任务
python3 scripts/schedule_push.py create --time "0 9 * * *" --limit 8

# 使用简写时间格式
python3 scripts/schedule_push.py create --time "09:00" --limit 10

# 测试推送
python3 scripts/schedule_push.py test --limit 5

# 列出所有任务
python3 scripts/schedule_push.py list

# 删除任务
python3 scripts/schedule_push.py delete --job-id <任务ID>
```

## 🔧 环境变量配置

### ⚠️ 安全提示
- **所有API Keys和Webhook URL都是敏感信息，请妥善保管，不要提交到代码仓库**
- **OPENCLAW_GATEWAY_TOKEN特别敏感：此令牌可能允许调度/外部控制，仅在完全理解此功能后使用**

### 新闻源API Key（可选）

```bash
# Tavily API Key（可选，推荐）
export TAVILY_API_KEY=your_tavily_api_key

# Brave Search API Key（可选）
export BRAVE_API_KEY=your_brave_api_key
```

### LLM评分配置（可选）

```bash
# OpenAI API Key（用于评分，推荐）
export OPENAI_API_KEY=your_openai_api_key

# 或使用 Anthropic
export ANTHROPIC_API_KEY=your_anthropic_api_key
```

### Feishu推送配置（可选，但需要设置才能推送）

```bash
# Feishu Webhook URL
export FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx
```

### OpenClaw Gateway配置（用于定时任务，可选）

```bash
# OpenClaw Gateway地址
export OPENCLAW_GATEWAY_URL=http://localhost:8080

# ⚠️ OpenClaw Gateway令牌（敏感：仅在理解此功能时使用）
export OPENCLAW_GATEWAY_TOKEN=your_gateway_token
```

## 📦 依赖项

- Python 3.8+
- tavily-python（可选）
- feedparser（必需）
- requests（必需）
- openai（可选，用于LLM评分）
- anthropic（可选，用于LLM评分）

安装依赖：

```bash
# 核心依赖
pip install feedparser requests

# 完整依赖（推荐）
pip install tavily-python feedparser requests openai anthropic
```

## 🎯 评分机制说明

### 四维度评分

1. **时效性 (25%)**
   - 6小时内：+25分
   - 12小时内：+20分
   - 24小时内：+15分
   - 48小时内：+10分
   - 72小时内：+5分

2. **源头权重 (25%)**
   - 官方/学术机构（权重≥9）：+25分
   - 高质量媒体（权重≥7）：+15分
   - 普通来源：+5分

3. **产业关联度 (25%)**
   - 底层技术突破：+25分
   - 应用层创新：+15分
   - 资讯八卦：+5分

4. **信息增量 (25%)**
   - 新技术参数/融资额/落地场景：+25分
   - 有新信息：+15分
   - 旧闻重发：+5分

### 三级分类

- **≥80分**：自动推送（auto_push）
- **60-80分**：待阅池（gray_zone）- 人工审核
- **<60分**：彻底拦截（filtered）

## 🔒 安全注意事项

1. **API Key安全**：不要将API Key硬编码在代码中，使用环境变量。所有API Keys和Webhook URL都是敏感信息，请妥善保管，不要提交到代码仓库。
2. **Feishu Webhook**：保护好Webhook URL，不要泄露给他人
3. **网络连接**：RSS源和API调用需要访问外网，请确保网络畅通
4. **定时任务**：使用OpenClaw Cron系统时需要配置Gateway URL。⚠️ OPENCLAW_GATEWAY_TOKEN特别敏感：此令牌可能允许调度/外部控制，仅在完全理解此功能后使用。
5. **数据存储**：data目录包含敏感信息，注意保密

## 🐛 故障排除

### Tavily API错误
- 检查 `TAVILY_API_KEY` 是否正确设置
- 确认API Key是否过期或额度用完
- 如果没有Tavily Key，使用 `--source rss` 仅使用RSS源

### LLM评分失败
- 检查 `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY` 是否设置
- 确认API Key额度充足
- 评分器会自动降级到规则评分模式

### RSS源获取失败
- 检查网络连接
- 确认RSS URL是否有效（可在浏览器中打开测试）
- 某些RSS源可能有访问频率限制

### Feishu推送失败
- 检查 `FEISHU_WEBHOOK_URL` 是否正确设置
- 确认Webhook URL是否有效
- 检查Feishu机器人是否有发送消息权限

## 📚 版本历史

### v2.2.0 (2026-03-07)
- **重大升级**：智能产品价值评分系统
- 新增Arxiv、OpenAI博客等高质量信源
- 实现三级分类机制（自动推送、待阅池、拦截）
- 新增人工反馈和迭代优化系统
- 新增数据持久化模块
- 新增管理工具脚本

### v2.1.0 (2026-03-02)
- 修复v2.0的所有问题
- Tavily API Key现在是可选的
- 新增Brave Search API支持
- RSS源无需API Key，始终可用
- 移除所有硬编码路径
- 支持真正的Feishu推送

### v1.0.0 (2026-03-02)
- 初始版本
- 支持Tavily API和RSS源
- 支持定时任务配置
- 支持推送到Feishu

## 📞 获取帮助

如果在使用过程中遇到问题，可以：

1. 查看故障排除指南
2. 检查环境变量配置
3. 查看脚本输出错误信息
4. 查看 `OPTIMIZATION_GUIDE.md` 获取详细优化指南
5. 联系Skill作者获取支持

---

**🎉 感谢使用 AI News Pusher v2.2！**
