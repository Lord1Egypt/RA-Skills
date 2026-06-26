# Digest Spec

## 建议字段

- `item_id`
- `cluster_id`
- `title`
- `source`
- `published_at`
- `raw_url`
- `normalized_url`
- `summary`
- `summary_zh`
- `topic_tags`
- `risk_tags`
- `actionability`
- `public_importance`
- `personal_relevance`
- `ranking_reason`
- `origin_system`
- `origin_feed`
- `freshrss_categories`

## 噪音过滤规则

优先过滤：

- 无法访问正文且无可靠替代来源
- 标题与正文明显不符
- 纯营销宣传
- 重复转载但无新增信息
- 与当前主题体系长期无关的低价值内容

## 严格去重规则

### URL 去重

- 去除常见追踪参数后的归一化 URL 相同，视为同一条目。
- 同一正文被多个短链接或跳转链接指向时，只保留最终正文源。

### 事件去重

- 不同来源报道同一事件时，只保留信息增量最高的一条作为主条目。
- 其他来源只记录在参考来源列表中，不再生成独立摘要段。

### 摘要去重

- 若两条摘要的核心事实、结论、价值判断高度重合，必须合并或重写。
- Digest 中每条摘要都必须能回答“它和上一条有什么本质不同”。

## 摘要要求

- 说明发生了什么。
- 说明为什么值得关注。
- 说明是否有动作价值或风险信号。
- 用简洁中文表达，避免空泛形容。
- 英文文章也必须输出中文摘要。
- 摘要不能只是标题改写，必须包含正文关键信息。

## 链接规范

- 最终输出中的链接统一使用 Markdown：`[标题文本](链接)`
- 标题文本应优先使用人工可识别的短标题，而不是完整 URL

## 聚类要求

- 同一事件多来源时，保留信息增量高的来源为主。
- 其他来源作为补充引用，不重复占位。

## FreshRSS 原始映射建议

若上游来自 FreshRSS：

- `item_id` 对应 FreshRSS / Google Reader item id
- `origin_system` 固定为 `freshrss`
- `origin_feed` 保存订阅源标题或 feed id
- `summary` 可先用 API 返回的 `summary.content` 或正文片段兜底
- `summary_zh` 作为最终对外摘要字段，尤其用于英文文章的中文摘要

