# AI Web API Extract 静态参数契约

- 接口：`POST https://aiwebapi.dataify.com/extract`（可用 `AI_WEB_API_BASE_URL` 覆盖）
- 鉴权：`Authorization: Bearer <DATAIFY_API_TOKEN>`
- unique_id：`extract`

| 参数名 | key | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| URL | `url` | string | 是 | -- | 公开 HTTP(S) 页面地址 |
| 结果格式 | `formats` | array<string> | 否 | markdown | markdown、raw_html、clean_html、links |
| 采集策略 | `advanced_mode` | boolean | 否 | true | 是否启用自动解锁链路 |
| 结果来源国家 | `country` | string | 否 | US | 两位大写国家码 |
| 保留标签 | `include_tags` | array<string> | 否 | -- | 最多 50 项 |
| 排除标签 | `exclude_tags` | array<string> | 否 | -- | 最多 50 项 |
| 是否只保留主体 | `only_main_content` | boolean | 否 | true | 是否只保留正文 |
| 请求标头 | `headers` | object | 否 | -- | 不得包含 Host 或 hop-by-hop 头 |
| 页面请求限制 | `timeout_ms` | integer | 否 | 60000 | 1000～120000 毫秒 |
| 页面加载限制 | `wait_for_ms` | integer | 否 | 0 | 0～30000 毫秒 |
| 页面缓存限制 | `max_age_ms` | integer | 否 | 172800000 | 0～172800000 毫秒 |