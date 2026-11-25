---
name: video-search
description: |
  通过 CreatiVault OpenAPI 查找 TikTok、YouTube 或 Instagram 视频。普通视频搜索每次指定一个平台，按话题标签或发布达人查找，可附加标题、播放量、互动率和日期条件。品牌视频洞察按品牌名查已收录的视频，可选择多个平台。适用于视频搜索、短视频案例、话题爆款、品牌相关视频和竞品内容洞察。
compatibility: Node.js 20.6+
metadata:
  layer: discovery
  parent: creator-scraper-cv
---

# Video Search（视频搜索）

## 概述

普通视频搜索从 TikTok、YouTube 或 Instagram 中一次选择一个平台。按话题标签或发布达人查找已收录视频，可附加标题、播放量、互动率和发布日期条件。品牌视频洞察按品牌名检索已收录视频，可指定一个或多个平台。

如需进一步了解发布者，按视频结果的 `creator.uid` 和 `platform` 交给 `creator-search` 精确查询。除非用户明确要求公开网页搜索，或在 CreatiVault 未命中后确认可改用公开来源，否则使用 CreatiVault OpenAPI。

## 脚本引用

| 脚本 | 相对路径 | 状态 |
|------|----------|------|
| search_videos.mjs | `../../scripts/search_videos.mjs` | 可用 |
| search_brand_video_insights.mjs | `../../scripts/search_brand_video_insights.mjs` | 可用 |

调用格式：

```bash
node {baseDir}/scripts/search_videos.mjs '{"platform":"tiktok","hashtag":["beauty","skincare"],"video_views_cnt_gte":100000,"page":1,"size":10}'
```

### 品牌视频洞察

用户想看某品牌或竞品相关视频时，使用 `search_brand_video_insights.mjs`。`brand_name` 必填，`platforms` 可从 `tiktok`、`youtube`、`instagram` 中多选，缺省只查 TikTok。可通过 `hashtags` 提供 1~5 个品牌话题标签，否则系统按品牌名扩展。支持按播放量、互动率和发布日期继续筛选。

```bash
node {baseDir}/scripts/search_brand_video_insights.mjs '{"brand_name":"Fenty Beauty","platforms":["tiktok","instagram"],"limit":20}'
```

### 品牌视频洞察展示规则

当调用 `search_brand_video_insights.mjs` 时，不要直接把原始 JSON 丢给用户。必须按下面结构展示：

1. 说明检索范围是 CreatiVault 已收录的视频。
2. 展示 `keyword_expansion.used_hashtags`，让用户知道品牌名被扩展成了哪些检索词。
3. 展示 `summary` 中本次返回视频的数量、平台分布、热门标签与高频发布者。
4. 用视频表格展示 `items`，推荐字段为：`#`、平台、视频标题、匹配词、播放量、点赞、评论、互动率、达人、发布时间、视频链接。
5. 表格下方给 1-3 条业务判断，例如品牌内容集中在哪些场景、哪些标签更热、哪些达人值得继续看。
6. 如果 `items` 为空，说明当前查询未命中。用户要继续查已收录的视频时，可确认是否调整品牌标签或筛选条件。

推荐展示模板：

```md
已在 CreatiVault 已收录视频中检索 {brand_name} 相关内容。

扩展检索词：{used_hashtags}

命中概览：
- 命中视频：{video_count} 条
- 平台分布：{platform_distribution}
- 热门标签：{top_hashtags}
- 高频达人：{top_creators}

| # | 平台 | 视频标题 | 匹配词 | 播放量 | 点赞 | 评论 | 互动率 | 达人 | 发布时间 | 视频 |
|---|---|---|---|---:|---:|---:|---:|---|---|---|
```

## 普通视频搜索参数

`platform` 必填，`hashtag` 和 `union_user_ids` 至少提供一个，二者同时填写时按交集筛选。用户只给标题、播放量、互动率或日期时，先请其补充话题标签或发布达人。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `platform` | string | - | 每次一个平台，支持 `tiktok`、`youtube` 或 `instagram` |
| `hashtag` | array[string] | - | Hashtag 列表（精确匹配，最多 **5 个**，全部满足） |
| `video_title` | string | - | 视频标题关键词（模糊匹配，最长 200 字符） |
| `video_views_cnt_gte` | integer | - | 最小播放量 |
| `video_views_cnt_lte` | integer | - | 最大播放量 |
| `video_interaction_rate_gte` | number | - | 最小互动率（百分比，如 `5.5` 表示 5.5%） |
| `video_interaction_rate_lte` | number | - | 最大互动率（百分比，如 `20` 表示 20%） |
| `video_publish_date_gte` | string | 不限 | 发布日期起始（`YYYY-MM-DD`） |
| `video_publish_date_lte` | string | 不限 | 发布日期截止（`YYYY-MM-DD`） |
| `query_type` | string | `union_user_id` | 达人标识类型，支持 `union_user_id`（达人 ID）、`kol_page_url`（主页链接）、`user_name`（用户名） |
| `union_user_ids` | array[string] | - | 同一种达人标识的列表，具体类型由 `query_type` 指定，最多 100 个 |
| `page` | integer | `1` | 页码（1-10） |
| `size` | integer | `10` | 每页数量（1-10，固定上限 10） |

### 参数提取规则

1. `platform` 必须转换为小写：`tiktok` / `youtube` / `instagram`。
2. `hashtag` 按 JSON 字符串数组传裸话题名，例如 `["beauty"]`。
3. 互动率传 **0~100 的百分比数值**：用户说“互动率至少 5%”时传 `5`，不能传 `0.05`。
4. 日期格式统一传 `YYYY-MM-DD`。
5. 用户指定「最近 15 天」等时间段时，按实际日期计算并传入。省略日期时查询范围不限于近期。

### 参数传递强制规则（NOT Pass）

- **[NOT]** `service_level` 参数：视频搜索不使用分级计费。
- **[NOT]** `keyword` / `industry` / `gender` / `country_code` 等达人筛选参数：这些属于 `creator-search`。
- **[NOT]** `sort_field` / `sort_order`：视频搜索暂不支持自定义排序。

## 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `platform` | string | 平台：tiktok / youtube / instagram |
| `videoId` | string | 视频唯一标识 |
| `videoTitle` | string | 视频标题 |
| `videoUrl` | string | 视频页面 URL |
| `viewsCount` | string | 播放量（字符串，避免大数精度问题） |
| `likesCount` | string | 点赞数 |
| `commentsCount` | string | 评论数 |
| `sharesCount` | string | 分享数 |
| `interactionRate` | string | 互动率（百分比字符串，如 `"3.25"`） |
| `publishDate` | string | 发布日期 |
| `duration` | string | 视频时长 |
| `hashtags` | array[string] | Hashtag 列表 |
| `creator` | object | 发布达人信息 |
| `creator.uid` | string | 达人唯一标识 |
| `creator.username` | string | 用户名 |
| `creator.nickname` | string | 昵称 |

## 示例

### 按 Hashtag 搜索 TikTok 视频

```json
{"platform":"tiktok","hashtag":["beauty"],"page":1,"size":10}
```

### 按标签叠加标题关键词和互动率

```json
{"platform":"youtube","hashtag":["skincare"],"video_title":"skincare routine","video_interaction_rate_gte":5,"page":1,"size":10}
```

### 按达人 ID 搜索视频

```json
{"platform":"tiktok","query_type":"union_user_id","union_user_ids":["7480117868423119918","7158794701745964074"],"page":1,"size":10}
```

## 输出格式

```md
| # | 平台 | 视频标题 | 播放量 | 点赞 | 评论 | 互动率 | 达人 | 发布日期 | 视频链接 |
```

### 格式规则

- 仅展示实际返回的非空字段。
- 表格内链接用 `[查看][linkN]` 引用式，表格下方定义完整 URL。
- 统计信息单独列出：总匹配数、消耗积分、剩余配额、请求 ID。

## 积分消耗

计费以服务端当前配置与请求实际返回的 `meta.credits_consumed` 为准。

## 错误处理

| Code | 说明 | 处理方式 |
|------|------|----------|
| 40001 | 请求参数无效 | 检查平台、必填筛选条件及参数类型 |
| 40101 | API Key 无效 | 检查 CV_API_KEY |
| 50001 | 服务端错误 | 重试或联系支持，附带 request_id |
