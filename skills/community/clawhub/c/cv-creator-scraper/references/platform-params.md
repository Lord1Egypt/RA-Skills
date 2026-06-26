# 各平台特有筛选参数

搜索达人时，除通用参数外，各平台有特有的筛选条件。本文件以 `backend/src/openapi/models/creator_request.py` 中当前 HTTP Open API 请求模型为准。

## 参数值规则

- 性别：`"0"`=女性，`"1"`=男性。
- boolean：使用 `true` / `false`，不要使用字符串或数字。`has_email`、`has_whatsapp`、`is_ai_creator`、`is_product_kol` 等均为 boolean。
- 比例：互动率、受众女性比例、佣金率等筛选值使用 0~100 百分比数值，例如 3% 传 `3`。
- 国家/语言多选：使用代码并以英文逗号分隔。
- 日期：使用 `YYYY-MM-DD`。
- `lang` 只翻译响应码值，不用于筛选，默认 `en`。
- 未声明的旧字段可能被请求模型忽略并且不产生筛选效果，禁止继续使用旧字段名。

## TikTok 特有参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `has_mcn` | boolean | 是否绑定 MCN |
| `has_line` | boolean | 是否有 Line |
| `has_zalo` | boolean | 是否有 Zalo |
| `language_code` | string | 语言代码，多选逗号分隔（如 `en,zh`）|
| `last10_avg_video_views_cnt_gte` | number | 近10条视频平均播放量 ≥ |
| `last10_avg_video_views_cnt_lte` | number | 近10条视频平均播放量 ≤ |
| `last10_avg_video_interaction_rate_gte` | number | 近10条视频平均互动率 ≥，传 0~100 |
| `last10_avg_video_interaction_rate_lte` | number | 近10条视频平均互动率 ≤，传 0~100 |
| `last_video_publish_date_gte` | string | 最近视频发布时间起始（YYYY-MM-DD）|
| `last_video_publish_date_lte` | string | 最近视频发布时间截止（YYYY-MM-DD）|
| `product_category_id_array` | string | 带货类目 ID，逗号分隔 |
| `industry` | string | 行业 level-3 数字类目 ID，逗号分隔；skill 脚本可将名称或上级类目自动展开 |
| `audience_female_rate_gte` | number | 粉丝女性比例 ≥，传 0~100 |
| `audience_female_rate_lte` | number | 粉丝女性比例 ≤，传 0~100 |
| `audience_age_list` | string | 粉丝主要年龄区间 |
| `last30day_gmv_gte` | number | 近30天 GMV ≥ |
| `last30day_gmv_lte` | number | 近30天 GMV ≤ |
| `last30day_gpm_gte` | number | 近30天 GPM ≥ |
| `last30day_gpm_lte` | number | 近30天 GPM ≤ |
| `last30day_gmv_per_buyer_gte` | number | 近30天客单价 ≥ |
| `last30day_gmv_per_buyer_lte` | number | 近30天客单价 ≤ |
| `last30day_commission_rate_gte` | number | 近30天佣金率 ≥，传 0~100 |
| `last30day_commission_rate_lte` | number | 近30天佣金率 ≤，传 0~100 |
| `audience_country_code_list` | string | 受众国家代码，多选逗号分隔 |
| `audience_language_code_list` | string | 受众语言代码，多选逗号分隔 |

**TikTok 排序字段**：`followers_cnt`（默认）、`last10_avg_video_views_cnt`、`last10_avg_video_interaction_rate`

---

## 服务等级（所有平台通用）

搜索接口支持 `service_level` 参数，控制返回字段范围和积分消耗。同时支持 `lang` 参数控制码值字段的国际化翻译（`cn` 中文 / `en` 英文）。

对话中用户未指定 `service_level` 时，应先向用户展示三档含义并说明默认推荐 `S2`；用户确认默认、推荐或直接搜索时使用 `S2`。用户已明确指定等级，或本轮已展示过等级说明时，不要重复打断。

| 等级 | 名称 | 包含数据字段 | 积分单价（每条） |
|------|------|------------|------------|
| S1 | 纯名单筛选 | 基础身份、主页、联系方式存在性、最近发布时间；具体字段因平台而异 | 1 积分 |
| S2 | 精准触达 | S1 + 国家、性别、粉丝/播放/互动、行业、邮箱等；具体字段因平台而异 | 3 积分 |
| S3 | 深度画像 | S2 + 受众性别、国家、语言、年龄分布 | 4 积分 |

默认 `S2`。响应 `meta` 中会返回 `service_level`（实际使用的等级）、`credits_consumed`（本次扣减积分数）和 `lang`（翻译语言）。

`audience_female_rate` 返回值为百分比数值（如 78.65 表示 78.65%）。

---

## YouTube 特有参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `has_whatsapp` | boolean | 是否有 WhatsApp |
| `is_ai_creator` | boolean | 是否 AI 达人 |
| `industry` | string | 行业 level-3 数字类目 ID，逗号分隔；skill 脚本可将名称或上级类目自动展开 |
| `language_code` | string | 语言代码，多选逗号分隔 |
| `last10_avg_video_view_count_all_gte` | number | 近10条视频平均播放量（全部）≥ |
| `last10_avg_video_view_count_all_lte` | number | 近10条视频平均播放量（全部）≤ |
| `last10_avg_video_view_count_short_gte` | number | 近10条短视频平均播放量 ≥ |
| `last10_avg_video_view_count_short_lte` | number | 近10条短视频平均播放量 ≤ |
| `last10_avg_interaction_rate_all_gte` | number | 近10条视频平均互动率（全部）≥，传 0~100 |
| `last10_avg_interaction_rate_all_lte` | number | 近10条视频平均互动率（全部）≤，传 0~100 |
| `last10_avg_interaction_rate_short_gte` | number | 近10条短视频平均互动率 ≥，传 0~100 |
| `last10_avg_interaction_rate_short_lte` | number | 近10条短视频平均互动率 ≤，传 0~100 |
| `last_video_publish_date_gte` | string | 最近视频发布时间起始（YYYY-MM-DD） |
| `last_video_publish_date_lte` | string | 最近视频发布时间截止（YYYY-MM-DD） |
| `audience_country_code_list` | string | 受众国家代码，多选逗号分隔 |
| `audience_language_code_list` | string | 受众语言代码，多选逗号分隔 |
| `audience_age_list` | string | 受众年龄，多选逗号分隔 |
| `audience_female_rate_gte` | number | 受众女性占比 ≥，传 0~100 |
| `audience_female_rate_lte` | number | 受众女性占比 ≤，传 0~100 |

不要使用旧字段名 `last10_avg_video_views_cnt_*`、`last10_avg_video_views_cnt_short_*`、`last10_avg_video_interaction_rate_*`、`last10_avg_video_interaction_rate_short_*`。

---

## Instagram 特有参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `has_whatsapp` | boolean | 是否有 WhatsApp |
| `is_product_kol` | boolean | 是否带货达人 |
| `is_ai_creator` | boolean | 是否 AI 达人 |
| `industry` | string | 行业 level-3 数字类目 ID，逗号分隔；skill 脚本可将名称或上级类目自动展开 |
| `language_code` | string | 语言代码，多选逗号分隔 |
| `last10_avg_video_view_count_gte` | number | 近10条视频平均播放量 ≥ |
| `last10_avg_video_view_count_lte` | number | 近10条视频平均播放量 ≤ |
| `last10_avg_video_interaction_rate_gte` | number | 近10条视频平均互动率 ≥，传 0~100 |
| `last10_avg_video_interaction_rate_lte` | number | 近10条视频平均互动率 ≤，传 0~100 |
| `last_video_publish_time_gte` | string | 最近视频发布时间起始（YYYY-MM-DD） |
| `last_video_publish_time_lte` | string | 最近视频发布时间截止（YYYY-MM-DD） |
| `audience_country_code_list` | string | 受众国家代码，多选逗号分隔 |
| `audience_language_list` | string | 受众语言，多选逗号分隔 |
| `audience_age_list` | string | 受众年龄，多选逗号分隔 |
| `female_ratio_gte` | number | 受众女性占比 ≥，传 0~100 |
| `female_ratio_lte` | number | 受众女性占比 ≤，传 0~100 |

当前 HTTP Open API 不支持 GMV 和销售商品数筛选。不要使用旧字段名 `last10_avg_video_views_cnt_*`、`last_video_publish_date_*`、`audience_female_rate_*`、`is_top_creator`。

---

## 搜索结果字段

### TikTok 返回字段

| 字段 | 类型 | 等级 | 说明 |
|------|------|------|------|
| `uid` | string | S1 | 达人唯一标识 |
| `username` | string | S1 | 用户名 |
| `nickname` | string | S1 | 昵称 |
| `avatar_url` | string | S1 | 头像链接 |
| `profile_url` | string | S1 | 主页链接 |
| `followers_count` | integer | S1 | 粉丝数 |
| `likes_count` | integer | S1 | 点赞数 |
| `video_count` | integer | S1 | 视频总数 |
| `has_showcase` | boolean | S1 | 是否开通橱窗带货 |
| `has_email` | boolean | S1 | 是否有邮箱 |
| `has_mcn` | boolean | S1 | 是否绑定 MCN |
| `has_line` | boolean | S1 | 是否有 Line |
| `has_zalo` | boolean | S1 | 是否有 Zalo |
| `last_video_publish_date` | string | S1 | 最近视频发布日期（YYYY-MM-DD） |
| `country_code` | string | S2 | 国家/地区代码 |
| `gender` | string | S2 | 性别（传 `lang` 时翻译） |
| `avg_views` | integer | S2 | 近10条视频平均播放量 |
| `engagement_rate` | number | S2 | 近10条视频平均互动率 |
| `views_per_follower` | number | S2 | 均播/粉丝比 |
| `is_verified` | boolean | S2 | 是否已认证 |
| `last10_video_views_per_sub` | number | S2 | 近10条视频播放量/粉丝比 |
| `last10_med_video_views_cnt` | integer | S2 | 近10条视频播放量中位数 |
| `last10_med_video_views_per_sub` | number | S2 | 近10条视频播放量中位数/粉丝比 |
| `product_categories` | string[] | S2 | 带货类目列表 |
| `industry_categories` | array | S2 | 达人领域（三级类目，含 primary/secondary/tertiary） |
| `bio` | string | S2 | 个人介绍 |
| `hashtags` | string[] | S2 | Hashtag 标签列表 |
| `language` | string | S2 | 语言 |
| `email` | string | S2 | 邮箱 |
| `link_whatsapp` | string | S2 | WhatsApp |
| `link_line` | string | S2 | Line |
| `link_zalo` | string | S2 | Zalo |
| `mcn` | string | S2 | MCN 机构 |
| `audience_female_rate` | number | S3 | 受众女性比例（百分比，如 78.65 表示 78.65%） |
| `audience_country_code_list` | string[] | S3 | 受众国家分布 |
| `audience_language_code_list` | string[] | S3 | 受众语言分布 |
| `audience_age_id_list` | string[] | S3 | 受众年龄分布（传 `lang` 时翻译为可读标签） |

### YouTube 返回字段

| 字段 | 类型 | 等级 | 说明 |
|------|------|------|------|
| `uid` | string | S1 | 达人唯一标识 |
| `username` | string | S1 | 用户名 |
| `nickname` | string | S1 | 昵称/频道名 |
| `avatar_url` | string | S1 | 头像链接 |
| `channel_url` | string | S1 | 频道链接 |
| `has_email` | boolean | S1 | 是否有邮箱 |
| `has_whatsapp` | boolean | S1 | 是否有 WhatsApp |
| `last_video_publish_time` | string | S1 | 最近视频发布时间（ISO 8601） |
| `country_code` | string | S2 | 国家/地区代码 |
| `language` | string | S2 | 语言 |
| `gender` | string | S2 | 性别（传 `lang` 时翻译） |
| `bio` | string | S2 | 频道简介 |
| `followers_count` | integer | S2 | 订阅数 |
| `video_count` | integer | S2 | 视频数量 |
| `view_count` | integer | S2 | 总观看次数 |
| `avg_views` | integer | S2 | 近10条视频平均播放量（全部） |
| `avg_views_short` | integer | S2 | 近10条短视频平均播放量 |
| `avg_views_long` | integer | S2 | 近10条长视频平均播放量 |
| `engagement_rate` | number | S2 | 近10条视频互动率（全部） |
| `engagement_rate_short` | number | S2 | 近10条短视频互动率 |
| `engagement_rate_long` | number | S2 | 近10条长视频互动率 |
| `is_verified` | boolean | S2 | 是否已认证 |
| `last10_video_views_per_sub` | number | S2 | 近10条视频播放量/粉丝比（全部） |
| `last10_video_views_per_sub_short` | number | S2 | 近10条短视频播放量/粉丝比 |
| `last10_video_views_per_sub_long` | number | S2 | 近10条长视频播放量/粉丝比 |
| `last10_med_video_views_cnt` | integer | S2 | 近10条视频播放量中位数（全部） |
| `last10_med_video_views_cnt_short` | integer | S2 | 近10条短视频播放量中位数 |
| `last10_med_video_views_cnt_long` | integer | S2 | 近10条长视频播放量中位数 |
| `last10_med_video_views_per_sub` | number | S2 | 近10条视频播放量中位数/粉丝比（全部） |
| `last10_med_video_views_per_sub_short` | number | S2 | 近10条短视频播放量中位数/粉丝比 |
| `last10_med_video_views_per_sub_long` | number | S2 | 近10条长视频播放量中位数/粉丝比 |
| `industry_categories` | array | S2 | 达人领域（三级类目，含 primary/secondary/tertiary） |
| `hashtags` | string[] | S2 | Hashtag 标签列表 |
| `email` | string | S2 | 邮箱 |
| `whatsapp` | string | S2 | WhatsApp |
| `audience_female_rate` | number | S3 | 受众女性比例（百分比，如 78.65 表示 78.65%） |
| `audience_country_code_list` | string[] | S3 | 受众国家分布 |
| `audience_language_list` | string[] | S3 | 受众语言分布 |
| `audience_age_list` | string[] | S3 | 受众年龄分布（传 `lang` 时翻译为可读标签） |

### Instagram 返回字段

| 字段 | 类型 | 等级 | 说明 |
|------|------|------|------|
| `uid` | string | S1 | 达人唯一标识 |
| `username` | string | S1 | 用户名 |
| `nickname` | string | S1 | 昵称 |
| `avatar_url` | string | S1 | 头像链接 |
| `profile_url` | string | S1 | 主页链接 |
| `has_email` | boolean | S1 | 是否有邮箱 |
| `has_whatsapp` | boolean | S1 | 是否有 WhatsApp |
| `last_video_publish_time` | string | S1 | 最近视频发布时间 |
| `country_code` | string | S2 | 国家/地区代码 |
| `language` | string | S2 | 语言 |
| `gender` | string | S2 | 性别（传 `lang` 时翻译） |
| `bio` | string | S2 | 个人介绍 |
| `followers_count` | integer | S2 | 粉丝数 |
| `video_count` | integer | S2 | 视频/帖子数量 |
| `avg_views` | integer | S2 | 近10条视频平均播放量 |
| `engagement_rate` | number | S2 | 近10条视频平均互动率 |
| `is_verified` | boolean | S2 | 是否已认证 |
| `last10_video_views_per_sub` | number | S2 | 近10条视频播放量/粉丝比 |
| `last10_med_video_views_cnt` | integer | S2 | 近10条视频播放量中位数 |
| `last10_med_video_views_per_sub` | number | S2 | 近10条视频播放量中位数/粉丝比 |
| `industry_categories` | array | S2 | 达人领域（三级类目，含 primary/secondary/tertiary） |
| `hashtags` | string[] | S2 | Hashtag 标签列表 |
| `email` | string | S2 | 邮箱 |
| `link_whatsapp` | string | S2 | WhatsApp |
| `audience_female_rate` | number | S3 | 受众女性比例（百分比，如 78.65 表示 78.65%） |
| `audience_country_code_list` | string[] | S3 | 受众国家分布 |
| `audience_language_code_list` | string[] | S3 | 受众语言分布 |
| `audience_age_id_list` | string[] | S3 | 受众年龄分布（传 `lang` 时翻译为可读标签） |

---

## 相似达人推荐（lookalike）

接口内部自动解析用户名、识别平台、获取达人 ID，一步完成相似搜索，无需单独 resolve。

### lookalike 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `uid` | string | 达人唯一标识 |
| `username` | string / null | 用户名 |
| `nickname` | string / null | 昵称 |
| `avatar_url` | string / null | 头像链接 |
| `profile_url` | string / null | 主页链接 |
| `country_code` | string / null | 国家/地区代码 |
| `followers_count` | integer / null | 粉丝数 |
| `avg_views` | integer / null | 近10条视频平均播放量 |
| `engagement_rate` | number / null | 近10条视频平均互动率 |
| `match_score` | number / null | 相似度匹配分数 |

### lookalike 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `username` | string | 否 | 达人用户名（不含 `@`），与 `profile_url` 二选一 |
| `platform` | string | 否 | 达人所在平台：`tiktok` / `youtube` / `instagram`，不传则自动在三个平台查找 |
| `profile_url` | string | 否 | 达人主页地址（自动解析平台和用户名），与 `username` 二选一 |
| `target_platform` | string | 否 | 目标搜索平台：`tiktok` / `youtube` / `instagram`，不传则与种子达人同平台 |
| `target_region` | string | 否 | 目标地区代码，`all` 表示不限 |
| `target_language` | string | 否 | 目标语言代码，`all` 表示不限 |
| `limit` | integer | 否 | 返回数量，默认 20，范围 1~50 |
| `follower_min` | integer | 否 | 粉丝数下限 |
| `follower_max` | integer | 否 | 粉丝数上限 |
| `avg_views_min` | integer | 否 | 平均观看量下限 |
| `avg_views_max` | integer | 否 | 平均观看量上限 |
| `female_rate_min` | number | 否 | 女性受众占比下限（%），范围 0~100 |
| `lang` | string | 否 | 响应语言：`cn`（中文）/ `en`（英文） |
| `service_level` | string | 否 | 服务等级，默认 `S1` |
