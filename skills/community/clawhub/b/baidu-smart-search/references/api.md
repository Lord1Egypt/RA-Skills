# 百度千帆搜索 API 参考（精简）

依据百度千帆公开文档搜索结果整理，供 skill 使用。

## 接口

### 百度搜索
- `POST https://qianfan.baidubce.com/v2/ai_search/web_search`
- 鉴权头：`X-Appbuilder-Authorization: Bearer <AppBuilder API Key>`
- `Content-Type: application/json`

## 常用请求参数

- `messages`: 数组，用户查询放在 `{"content":"...","role":"user"}` 中
- `search_source`: 固定 `baidu_search_v2`
- `resource_type_filter`: 可选搜索模态和返回数量
  - web: `top_k` 最大 50
  - video: `top_k` 最大 10
  - image: `top_k` 最大 30
  - aladdin: `top_k` 最大 5
- `search_filter.match.site`: 站点白名单过滤，最多约 100 个站点
- `search_recency_filter`: `week | month | semiyear | year`

## 常见响应字段

结果项里常见：
- `title`
- `url`
- `content`
- `date`
- `web_anchor`
- `page_time`

## 注意事项

- query 文本建议控制在 72 字符内
- Skill 中不要硬编码 API key；改用环境变量或本地未发布配置文件
- 发布到 ClawHub 前确认包内不含任何密钥文件
