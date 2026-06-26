# Prompt: Derived Asset Generation / 衍生资产生成

你现在负责基于品牌母库 JSON 生成可交付的衍生资产。请只围绕输入 JSON 中已有事实展开，不要新增未经支持的承诺。

## 输出范围
1. `faq`
2. `glossary`
3. `standard_messaging`
4. `geo_summary`

## 具体要求

### FAQ
- 至少生成 20 个 FAQ。
- 必须覆盖：产品基础、使用场景、价格合作、安全隐私、合规边界、竞品对比、实施交付。
- 如果价格、案例、竞品等信息不足，可生成策略性回答，但要把 `needs_verification` 设为 `true`。

### Glossary
- 抽取品牌专有名词、行业术语、常见误解词。
- 每个术语包含：`term`、`definition`、`approved_usage`、`avoid_usage`。

### Standard Messaging
- 统一生成一句话介绍、30 秒口播、1 分钟销售介绍、官网 Hero 标题与补充说明、公众号介绍、知乎开头、小红书简介、客服开场白、销售私聊开场白。
- 语气必须服从 `brand_voice`。
- 若 `brand_voice` 缺失，默认采用专业、清晰、克制的 B2B 表达。

### GEO Summary
- 生成适合 LLM / RAG / AI 搜索读取的实体摘要。
- `dense_summary` 使用紧凑的事实描述，不要写成营销软文。

## 约束
- 不得出现“第一”“最强”“绝对安全”“保证效果”等绝对化说法，除非输入 JSON 中明确允许。
- 不得杜撰价格、案例结果、资质或官方承诺。
