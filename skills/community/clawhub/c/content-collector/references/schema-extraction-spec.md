# Schema.org 提取规范

**目标**:自动从网页结构化数据中获取更准确的元数据,减少人工补充。

## 提取方法
1. 如果已用 `browser` 打开页面,`evaluate` 执行:
   ```javascript
   JSON.parse(document.querySelector('script[type="application/ld+json"]')?.textContent || 'null')
   ```
2. 如果只用了 `web_fetch`,用正则从 HTML 中提取 `<script type="application/ld+json">` 内容
3. 页面可能有多个 JSON-LD 块,取 `@type` 最相关的一个(优先 Article > NewsArticle > BlogPosting > WebPage)

## 字段映射

| Schema.org 字段 | → frontmatter 字段 | 覆盖规则 |
|---|---|---|
| `headline` / `name` | `title` | 仅当现有 title 为空或明显是 URL slug 时覆盖 |
| `author.name` / `author[0].name` | `author` | 仅当现有 author 为空时填充 |
| `datePublished` | `date_published` | 优先使用(比 meta tag 更准确) |
| `description` | `summary` | 仅当现有 summary 为空时填充 |
| `aggregateRating.ratingValue` | `schema_data.rating` | 直接写入 |
| `aggregateRating.reviewCount` | `schema_data.reviewCount` | 直接写入 |
| `@type` | `schema_type` | 直接写入 |
| 其他有价值字段 | `schema_data.*` | 按需写入,总共不超过 10 个 key-value |

## 注意
- **静默降级**:提取失败(无 JSON-LD、解析报错、字段为空)→ 跳过,不阻塞收藏流程
- **不覆盖已有**:已有明确值的字段不被 Schema.org 数据覆盖(Schema.org 是补充,不是权威源)
- **schema_data 精简**:只保留有信息量的字段(rating/price/duration/keywords 等),忽略 @context、publisher logo URL 等噪音
