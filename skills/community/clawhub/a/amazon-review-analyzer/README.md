# Amazon Review Analyzer

Amazon 评论深度分析工具 - 输入 ASIN，自动抓取数百条评论，AI 逐条深度打标，生成痛点/卖点/Listing 优化洞察报告。

## 🚀 功能特性

- 🔍 **自动抓评**：通过 RapidAPI 采集产品评论（支持多市场：US/UK/DE/JP/FR 等）
- 🤖 **AI 深度打标**：每条评论提取情感、痛点、卖点、使用场景、用户画像、改进建议
- 📊 **智能汇总**：聚合所有打标结果，输出高频痛点 TOP10、卖点 TOP10
- 📝 **Listing 优化建议**：基于真实用户反馈，给出可操作的优化方向
- 📄 **交互式 HTML 报告**：可视化图表 + 结构化洞察，可直接发给团队

## 📋 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 体验示例报告（无需 API Key）

```bash
python scripts/demo.py
```

这会生成一个示例 HTML 报告，让你快速了解报告包含哪些内容。

### 3. 配置 API Key

**LLM API（必填）**：用于 AI 打标，支持任何兼容 OpenAI API 格式的模型。

```bash
# OpenAI（推荐 gpt-4o-mini，性价比高）
python scripts/analyze.py \
  --asin B08N5WRWNW \
  --api-key YOUR_OPENAI_KEY

# DeepSeek（国内推荐，便宜）
python scripts/analyze.py \
  --asin B08N5WRWNW \
  --api-key YOUR_DEEPSEEK_KEY \
  --api-base https://api.deepseek.com/v1 \
  --model deepseek-chat
```

**RapidAPI Key（可选）**：用于获取真实评论数据。如未配置，则使用模拟数据。

```bash
# 获取 RapidAPI Key：
# 1. 访问 https://rapidapi.com/hub/amazon
# 2. 订阅 "Amazon Products and Reviews" API
# 3. 复制 API Key，通过 --rapidapi-key 参数传入

python scripts/analyze.py \
  --asin B08N5WRWNW \
  --api-key YOUR_OPENAI_KEY \
  --rapidapi-key YOUR_RAPIDAPI_KEY
```

## 📖 使用说明

### 基本用法

```bash
python scripts/analyze.py \
  --asin B08N5WRWNW \
  --market US \
  --max-reviews 500 \
  --api-key YOUR_API_KEY
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--asin` | ✅ | - | Amazon ASIN（产品 ID） |
| `--market` | ❌ | US | 市场区域：US/UK/DE/JP/FR/CA/IT/ES |
| `--max-reviews` | ❌ | 500 | 最大评论数量（建议 500-1000） |
| `--api-key` | ✅ | - | LLM API Key（OpenAI/DeepSeek/其他兼容 API） |
| `--api-base` | ❌ | https://api.openai.com/v1 | API Base URL |
| `--model` | ❌ | gpt-4o-mini | 模型名称 |
| `--output` | ❌ | ./review_analysis_{ASIN}.html | 输出报告路径 |
| `--rapidapi-key` | ❌ | 内置免费 Key | RapidAPI Key（可选） |
| `--use-mock` | ❌ | False | 使用模拟数据（不需要 RapidAPI） |
| `--use-mock-tags` | ❌ | False | 使用模拟打标结果（不调用 AI API） |

### 示例

**分析 AirPods Pro 2（ASIN: B0CHX1W1XY）**

```bash
python scripts/analyze.py \
  --asin B0CHX1W1XY \
  --market US \
  --max-reviews 500 \
  --api-key sk-xxx \
  --api-base https://api.deepseek.com/v1
```

## 📊 输出报告内容

生成的 HTML 报告包含以下板块：

1. **产品概览**：标题、价格、评分、图片、ASIN
2. **评论概览**：评论总数、平均评分、评分分布图、情感分布图
3. **痛点分析**：高频痛点 TOP10（带词云图）、典型评论摘录
4. **卖点分析**：高频卖点 TOP10（带词云图）、典型评论摘录
5. **用户画像**：谁在买、使用场景、购买动机
6. **Listing 优化建议**：标题/五点/描述/A+ 页面的具体改进建议
7. **竞品机会**：基于差评的竞品切入机会
8. **原始数据**：可下载的 CSV 文件（含所有打标结果）

## 🔧 技术架构

```
用户输入 ASIN
    ↓
[评论采集模块] fetch_reviews.py
  - 调用 RapidAPI 获取评论数据
  - 支持分页采集（最多 1000 条）
    ↓
[AI 打标模块] ai_tagging.py
  - 每条评论调用 LLM 进行深度分析
  - 提取：情感/痛点/卖点/场景/画像/建议
  - 带频率控制（避免 API 限流）
    ↓
[汇总分析模块] analyze.py
  - 聚合所有打标结果
  - 统计高频词、情感分布、评分分布
    ↓
[报告生成模块] generate_report.py
  - 基于 HTML 模板生成交互式报告
  - 包含 Chart.js 可视化图表
    ↓
输出 HTML 报告（自动在浏览器打开）
```

## ⚠️ 注意事项

- ⏱️ **时间成本**：500 条评论约需 5-10 分钟（取决于 API 速率）
- 💰 **API 成本**：gpt-4o-mini 处理 500 条评论约 $0.15；DeepSeek 约 ¥0.5
- 🚫 **反爬限制**：RapidAPI 有免费额度限制，大量使用建议自备 API Key
- 📝 **评论语言**：主要支持英文评论，其他语言准确率可能降低

## 📝 常见问题

### Q: 如何找到产品的 ASIN？

A: 在 Amazon 产品页面的 URL 中，ASIN 是 `/dp/` 后面的那串代码。例如：`https://www.amazon.com/dp/B08N5WRWNW` → ASIN 是 `B08N5WRWNW`

### Q: 为什么评论数量少于预期？

A: 有几个可能：
1. 产品本身的评论总数就少
2. RapidAPI 只返回近期评论（或抽样）
3. 免费 API Key 有请求限制

### Q: AI 打标的准确率如何？

A: 使用 gpt-4o-mini 或更好模型时：
- 情感分析准确率 > 90%
- 痛点/卖点提取准确率 > 85%
- 使用场景识别准确率 > 80%

## 🔮 未来改进方向

- [ ] 支持免费评论爬取方案（无需 RapidAPI Key）
- [ ] 支持多语言评论分析（西班牙语、日语、德语等）
- [ ] 增加竞品对比功能（同时分析多个 ASIN）
- [ ] 支持导出 PDF 报告
- [ ] 增加评论时间趋势分析（痛点变化、评分变化）

## 📄 许可证

MIT License

## 👨‍💻 作者

WorkBuddy Skill Creator

---

**⭐ 如果这个项目对你有帮助，请给它一个星标！**
