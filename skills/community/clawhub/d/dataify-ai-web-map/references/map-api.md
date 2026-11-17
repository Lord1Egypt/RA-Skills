# AI Web API Map 静态参数契约

- 接口：`POST https://aiwebapi.dataify.com/map`（可用 `AI_WEB_API_BASE_URL` 覆盖）
- 鉴权：`Authorization: Bearer <DATAIFY_API_TOKEN>`
- unique_id：`map`

| 参数名 | key | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| URL | `url` | string | 是 | -- | 公开 HTTP(S) 起始地址 |
| 结果来源国家 | `country` | string | 否 | US | 两位大写国家码 |
| 结果域名 | `domain_filter` | enum | 否 | all | all 或 domain |
| 结果数量 | `limit` | integer | 否 | 5000 | 1～100000 |
| 网站 Sitemap | `sitemap` | enum | 否 | include | skip、include、only；only 当前不稳定 |