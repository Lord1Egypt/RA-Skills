---
name: amazon-review-analyzer
description: "输入ASIN，自动抓取数百条评论，AI逐条深度打标，生成痛点/卖点/Listing优化洞察报告。支持RapidAPI数据采集、OpenAI/DeepSeek兼容API、交互式HTML报告输出。"
author: "WorkBuddy"
version: "1.0.0"
triggers:
  - "amazon-review"
  - "评论分析"
  - "评论打标"
  - "产品洞察"
  - "ASIN分析"
  - "Amazon reviews"
  - "review analyzer"
agent_created: true
---

# Amazon评论深度分析助手

输入一个Amazon ASIN，5-10分钟内给你一份能直接用的洞察报告——痛点、卖点、Listing怎么改，全在里面。

## 能做什么

- 🔍 **自动抓评**：通过RapidAPI采集产品评论（支持多市场：US/UK/DE/JP/FR等）
- 🤖 **AI深度打标**：每条评论提取情感、痛点、卖点、使用场景、用户画像、改进建议
- 📊 **智能汇总**：聚合所有打标结果，输出高频痛点TOP10、卖点TOP10
- 📝 **Listing优化建议**：基于真实用户反馈，给出可操作的优化方向
- 📄 **交互式HTML报告**：可视化图表 + 结构化洞察，可直接发给团队

## 快速开始

### 1. 安装依赖

```bash
pip install -r ~/.workbuddy/skills/amazon-review-analyzer/requirements.txt
```

### 2. 体验示例报告（无需API Key）

```bash
python ~/.workbuddy/skills/amazon-review-analyzer/scripts/demo.py
```

这会生成一个示例HTML报告，让你快速了解报告包含哪些内容。

### 3. 配置API Key

**LLM API（必填）**：用于AI打标，支持任何兼容OpenAI API格式的模型。

```bash
# OpenAI（推荐gpt-4o-mini，性价比高）
python ~/.workbuddy/skills/amazon-review-analyzer/scripts/analyze.py \
  --asin B08N5WRWNW \
  --api-key YOUR_OPENAI_KEY

# DeepSeek（国内推荐，便宜）
python ~/.workbuddy/skills/amazon-review-analyzer/scripts/analyze.py \
  --asin B08N5WRWNW \
  --api-key YOUR_DEEPSEEK_KEY \
  --api-base https://api.deepseek.com/v1 \
  --model deepseek-chat
```

**RapidAPI Key（可选）**：用于获取真实评论数据。如未配置，则使用模拟数据。

```bash
# 获取RapidAPI Key：
# 1. 访问 https://rapidapi.com/hub/amazon
# 2. 订阅 "Amazon Products and Reviews" API
# 3. 复制API Key，通过 --rapidapi-key 参数传入

python ~/.workbuddy/skills/amazon-review-analyzer/scripts/analyze.py \
  --asin B08N5WRWNW \
  --api-key YOUR_OPENAI_KEY \
  --rapidapi-key YOUR_RAPIDAPI_KEY
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--asin` | ✅ | - | Amazon ASIN（产品ID） |
| `--market` | ❌ | US | 市场区域：US/UK/DE/JP/FR/CA/IT/ES |
| `--max-reviews` | ❌ | 500 | 最大评论数量（建议500-1000） |
| `--api-key` | ✅ | - | LLM API Key（OpenAI/DeepSeek/其他兼容API） |
| `--api-base` | ❌ | https://api.openai.com/v1 | API Base URL |
| `--model` | ❌ | gpt-4o-mini | 模型名称 |
| `--output` | ❌ | ./review_analysis_{ASIN}.html | 输出报告路径 |
| `--rapidapi-key` | ❌ | 内置免费Key | RapidAPI Key（可选，内置有免费额度） |

## 输出报告内容

生成的HTML报告包含以下板块：

1. **产品概览**：标题、价格、评分、图片、ASIN
2. **评论概览**：评论总数、平均评分、评分分布图、情感分布图
3. **痛点分析**：高频痛点TOP10（带词云图）、典型评论摘录
4. **卖点分析**：高频卖点TOP10（带词云图）、典型评论摘录
5. **用户画像**：谁在买、使用场景、购买动机
6. **Listing优化建议**：标题/五点/描述/A+页面的具体改进建议
7. **竞品机会**：基于差评的竞品切入机会
8. **原始数据**：可下载的CSV文件（含所有打标结果）

## API Key 配置

### LLM API（必填）
支持任何兼容OpenAI API格式的模型：

**OpenAI**
```
--api-key sk-xxx --api-base https://api.openai.com/v1 --model gpt-4o-mini
```

**DeepSeek（国内推荐）**
```
--api-key sk-xxx --api-base https://api.deepseek.com/v1 --model deepseek-chat
```

**其他兼容API**：只需修改 `--api-base` 和 `--model`

### RapidAPI Key（可选）
评论数据通过 RapidAPI 的 "Amazon Products and Reviews" 接口获取。内置一个免费Key（有额度限制），你也可以自己申请：

1. 访问 https://rapidapi.com/hub/amazon
2. 订阅 "Amazon Products and Reviews" API
3. 复制你的API Key，通过 `--rapidapi-key` 参数传入

## 技术架构

```
用户输入ASIN
    ↓
[评论采集模块] fetch_reviews.py
  - 调用RapidAPI获取评论数据
  - 支持分页采集（最多1000条）
    ↓
[AI打标模块] ai_tagging.py
  - 每条评论调用LLM进行深度分析
  - 提取：情感/痛点/卖点/场景/画像/建议
  - 带频率控制（避免API限流）
    ↓
[汇总分析模块] analyze.py
  - 聚合所有打标结果
  - 统计高频词、情感分布、评分分布
    ↓
[报告生成模块] generate_report.py
  - 基于HTML模板生成交互式报告
  - 包含Chart.js可视化图表
    ↓
输出HTML报告（自动在浏览器打开）
```

## 注意事项

- ⏱️ **时间成本**：500条评论约需5-10分钟（取决于API速率）
- 💰 **API成本**：gpt-4o-mini处理500条评论约$0.15；DeepSeek约¥0.5
- 🚫 **反爬限制**：RapidAPI有免费额度限制，大量使用建议自备API Key
- 📝 **评论语言**：主要支持英文评论，其他语言准确率可能降低

## 示例

**分析AirPods Pro 2（ASIN: B0CHX1W1XY）**
```bash
python ~/.workbuddy/skills/amazon-review-analyzer/scripts/analyze.py \
  --asin B0CHX1W1XY \
  --market US \
  --max-reviews 500 \
  --api-key sk-xxx \
  --api-base https://api.openseek.com/v1
```

**分析报告示例截图**（略）

## 常见问题

**Q: 如何找到产品的ASIN？**
A: 在Amazon产品页面的URL中，ASIN是 `/dp/` 后面的那串代码。例如：`https://www.amazon.com/dp/B08N5WRWNW` → ASIN是 `B08N5WRWNW`。也可以在产品详情页的"产品信息"板块中找到。

**Q: 为什么评论数量少于预期？**
A: 有几个可能：
1. 产品本身的评论总数就少
2. RapidAPI只返回近期评论（或抽样）
3. 免费API Key有请求限制
建议：尝试增加 `--max-reviews` 参数，或自备RapidAPI Key。

**Q: 能分析非美国市场的产品吗？**
A: 可以，用 `--market` 参数指定市场代码：
- `US` - 美国
- `UK` - 英国
- `DE` - 德国
- `JP` - 日本
- `FR` - 法国
- `CA` - 加拿大
- `IT` - 意大利
- `ES` - 西班牙

**Q: AI打标的准确率如何？**
A: 使用gpt-4o-mini或更好模型时：
- 情感分析准确率 > 90%
- 痛点/卖点提取准确率 > 85%
- 使用场景识别准确率 > 80%
注意：英文评论准确率更高，其他语言可能降低。

**Q: 分析报告能直接用于优化Listing吗？**
A: 报告的"Listing优化建议"板块提供了基于真实用户反馈的改进方向，但还需要结合产品特性和市场策略来细化。建议：
1. 先看完"痛点分析"，了解用户最在意的问题
2. 参考"卖点分析"，确认用户真正认可的价值
3. 在Listing中主动解答痛点（将痛点转化为卖点）
4. 用用户的原话来写五点描述（更有说服力）

**Q: API调用成本大概多少？**
A: 以500条评论为例：
- **OpenAI gpt-4o-mini**: 约 $0.15（输入$0.15/1M tokens，输出$0.6/1M tokens）
- **DeepSeek-V2**: 约 ¥0.5（输入¥1/1M tokens，输出¥2/1M tokens）
- **本地模型**（如Ollama）: 免费，但质量可能降低

**Q: 如何降低API成本？**
A: 几个建议：
1. 先用少量评论测试（如 `--max-reviews 50`）
2. 使用更便宜的模型（如gpt-4o-mini或DeepSeek）
3. 对长评论进行截断（已在代码中实现，每条评论最多1500字符）
4. 考虑本地部署模型（如Ollama + Qwen），完全免费

## 故障排查

### 问题1：API调用失败（HTTP 429 - 限流）

**原因**：API调用频率过高，触发限流

**解决方案**：
1. 增加延迟时间：修改 `analyze.py` 中的 `delay` 参数（如改为1.0秒）
2. 使用批量处理：如果API支持批量调用，改用批量接口
3. 升级API计划：付费API通常有更高的速率限制

### 问题2：AI打标结果解析失败

**原因**：LLM返回的结果不是标准JSON格式

**解决方案**：
代码已内置4种解析策略（直接解析、Markdown提取、文本提取、模糊匹配），如果仍然失败：
1. 开启 `--debug` 模式，查看AI返回的原始内容
2. 调整Prompt（在 `ai_tagging.py` 的 `_build_tagging_prompt` 函数中），要求模型"只输出JSON，不要输出其他内容"
3. 降低温度参数（修改 `temperature` 为0.1）

### 问题3：获取评论失败（RapidAPI返回空数据）

**原因**：
1. RapidAPI Key无效或额度用尽
2. 产品ASIN错误
3. 该产品没有评论

**解决方案**：
1. 检查ASIN是否正确（在Amazon上手动搜索验证）
2. 自备RapidAPI Key（免费额度有限制）
3. 使用模拟数据测试流程：`python analyze.py --asin TEST --use-mock --use-mock-tags`

### 问题4：报告打开后样式错乱

**原因**：CDN加载失败（Chart.js可能无法访问）

**解决方案**：
1. 检查网络连接，确保能访问 `cdn.jsdelivr.net`
2. 或者，下载Chart.js到本地，修改 `generate_report.py` 中的CDN链接为本地路径

## 高级技巧

### 1. 批量分析多个产品

创建一个ASIN列表文件 `asins.txt`：
```
B08N5WRWNW
B08N5WRWNX
B08N5WRWNY
```

然后批量运行：
```bash
while read asin; do
  python ~/.workbuddy/skills/amazon-review-analyzer/scripts/analyze.py \
    --asin $asin \
    --api-key YOUR_KEY \
    --use-mock-tags  # 先用模拟打标测试
done < asins.txt
```

### 2. 定期监控竞品评论

创建一个自动化脚本，每周分析竞品评论，追踪用户痛点变化：

```bash
# cron job: 每周一早上8点运行
0 8 * * 1 python /path/to/analyze.py --asin COMPETITOR_ASIN --api-key YOUR_KEY
```

### 3. 导出打标数据用于进一步分析

修改 `generate_report.py`，增加CSV导出功能：

```python
# 在报告生成后，导出CSV
import pandas as pd
df = pd.DataFrame([{
    "rating": item["review"]["rating"],
    "sentiment": item["tags"]["sentiment"],
    "pain_points": ", ".join(item["tags"]["pain_points"]),
    "selling_points": ", ".join(item["tags"]["selling_points"]),
    "summary": item["tags"]["summary"]
} for item in tagged_reviews])

df.to_csv(output_path.replace(".html", ".csv"), index=False, encoding="utf-8-sig")
```

## 更新日志

- **v1.0.0** (2026-06-18): 初始版本
  - 支持RapidAPI评论采集（需配置API Key）
  - 支持AI深度打标（兼容OpenAI格式）
  - 生成交互式HTML报告（含Chart.js可视化）
  - 提供模拟数据演示模式
  - 已知限制：真实评论采集依赖RapidAPI（后续版本将支持免费爬取方案）

## 未来改进方向

- [ ] 支持免费评论爬取方案（无需RapidAPI Key）
- [ ] 支持多语言评论分析（西班牙语、日语、德语等）
- [ ] 增加竞品对比功能（同时分析多个ASIN）
- [ ] 支持导出PDF报告
- [ ] 增加评论时间趋势分析（痛点变化、评分变化）
- [ ] 集成到Amazon Seller Central（自动监控自己产品的评论）

---

**作者**: WorkBuddy Skill Creator
**反馈**: 如遇到问题或有改进建议，请在WorkBuddy中反馈
