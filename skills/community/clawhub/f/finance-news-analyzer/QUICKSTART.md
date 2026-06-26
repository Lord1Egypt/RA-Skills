# 财经新闻分析器 - 快速参考

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install requests beautifulsoup4 jinja2 pyyaml
```

### 2. 选择并配置模型

#### OpenAI (推荐：gpt-4o-mini)
```bash
export OPENAI_API_KEY=sk-xxx
python scripts/main.py --model gpt-4o-mini
```

#### 通义千问 (推荐：qwen-plus)
```bash
export DASHSCOPE_API_KEY=sk-xxx
python scripts/main.py --model qwen-plus
```

#### 本地 Ollama (免费)
```bash
ollama pull llama3.1
python scripts/main.py --model ollama/llama3.1
```

### 3. 运行
```bash
python scripts/main.py --source wallstreetcn --limit 10
```

---

## 📊 常用命令

### 基础用法
```bash
# 分析今日新闻
python scripts/main.py

# 指定新闻源
python scripts/main.py --source wallstreetcn,36kr,hackernews

# 关键词过滤
python scripts/main.py --keyword "AI，芯片，半导体"

# 指定股票代码
python scripts/main.py --ticker NVDA,TSLA,AAPL
```

### 高级用法
```bash
# 指定输出格式
python scripts/main.py --output brief     # 快速简报
python scripts/main.py --output full      # 深度报告
python scripts/main.py --output industry  # 行业报告

# 指定时间周期
python scripts/main.py --period daily    # 日报
python scripts/main.py --period weekly   # 周报

# 批量分析
python scripts/analyze_sentiment.py --input news.json --output analyzed.json
```

---

## 🤖 模型选择指南

| 需求 | 推荐模型 | 命令 |
|------|---------|------|
| **最佳性价比** | GPT-4o Mini | `--model gpt-4o-mini` |
| **最高质量** | GPT-4o / Claude 3.5 | `--model gpt-4o` |
| **国产最佳** | 通义千问 Plus | `--model qwen-plus` |
| **完全免费** | Ollama + Llama 3.1 | `--model ollama/llama3.1` |
| **中文内容** | 通义千问 Max | `--model qwen-max` |
| **快速分析** | GPT-3.5 Turbo | `--model gpt-3.5-turbo` |

---

## 🔑 API Key 获取

| 厂商 | 获取链接 |
|------|---------|
| OpenAI | https://platform.openai.com/api-keys |
| Anthropic | https://console.anthropic.com/settings/keys |
| 阿里通义 | https://dashscope.console.aliyun.com/apiKey |
| 百度文心 | https://console.bce.baidu.com/qianfan/ |
| 智谱 AI | https://open.bigmodel.cn/usercenter/apikeys |
| Ollama | https://ollama.com (本地运行) |

---

## 📁 输出目录结构

```
reports/
├── finance_briefing_20260310_120000.md      # 快速简报
├── finance_full_20260310_120000.md          # 深度报告
├── finance_industry_20260310_120000.md      # 行业报告
└── analyzed_news_20260310_120000.json       # 原始分析数据
```

---

## ⚙️ 配置文件

创建 `~/.baoyu-skills/finance-news-analyzer/EXTEND.md`：

```yaml
# 默认设置
default_sources:
  - wallstreetcn
  - 36kr
  - hackernews

default_model: gpt-4o-mini
default_output: brief
default_language: zh

# 关注列表
watchlist:
  - NVDA
  - TSLA
  - 00700.HK
  - 600519.SS

# 情感分析配置
sentiment_model: gpt-4o-mini
confidence_threshold:
  high: 0.8
  medium: 0.5
```

---

## 🐛 常见问题

### Q: 提示 API Key 错误？
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 重新设置
export OPENAI_API_KEY=sk-xxx
```

### Q: 如何切换模型？
```bash
# 使用通义千问
export DASHSCOPE_API_KEY=sk-xxx
python scripts/main.py --model qwen-plus
```

### Q: 本地模型怎么安装？
```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 下载模型
ollama pull llama3.1

# 3. 使用
python scripts/main.py --model ollama/llama3.1
```

### Q: 如何分析特定股票？
```bash
python scripts/main.py --ticker NVDA,TSLA --sentiment positive
```

### Q: 如何生成周报？
```bash
python scripts/main.py --period weekly --output industry
```

---

## 📚 完整文档

- [SKILL.md](SKILL.md) - 完整技能说明
- [references/supported-models.md](references/supported-models.md) - 支持的模型列表
- [references/config-example.md](references/config-example.md) - 配置文件示例
- [references/ticker-map.md](references/ticker-map.md) - 股票代码映射
- [references/industry-map.md](references/industry-map.md) - 行业分类
- [references/sentiment-rules.md](references/sentiment-rules.md) - 情感分析规则

---

## 💡 使用技巧

1. **晨间简报**：每天早上运行一次，快速了解隔夜新闻
   ```bash
   python scripts/main.py --source all --limit 20 --output brief
   ```

2. **个股追踪**：设置 watchlist，自动追踪关注股票
   ```bash
   python scripts/main.py --ticker NVDA,TSLA --period weekly
   ```

3. **行业研究**：按行业分析新闻趋势
   ```bash
   python scripts/main.py --industry 半导体 --period weekly --output industry
   ```

4. **实时预警**：设置高置信度阈值，只关注重要新闻
   ```bash
   python scripts/main.py --sentiment positive --confidence high
   ```

---

**版本**: 1.0  
**最后更新**: 2026-03-10
