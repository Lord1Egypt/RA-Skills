---
name: creator-search
description: |
  三平台达人搜索能力，支持 TikTok、YouTube、Instagram 多维度筛选（关键词、国家、粉丝数、互动率、类目等）。
  Use when: 达人搜索, KOL搜索, 找达人, creator search, influencer discovery, search creators
compatibility: Node.js 20.6+
metadata:
  layer: discovery
  parent: creator-scraper-cv
---

# Creator Search（达人搜索）

## 概述

三平台（TikTok、YouTube、Instagram）达人实时搜索，支持关键词、国家、粉丝数、互动率、行业等多维度筛选，结果即时返回。

## 脚本引用

| 脚本 | 相对路径 | 状态 |
|------|----------|------|
| search_creators.mjs | `../../scripts/search_creators.mjs` | ✅ 可用 |

调用格式：

```bash
node {baseDir}/scripts/search_creators.mjs '{"platform":"tiktok","country_code":"US","gender":"0","followers_cnt_gte":100000,"service_level":"S2"}'
```

## 参数提取强制规则

1. `platform` 必须转换为小写：`tiktok` / `youtube` / `instagram`。
2. 达人性别必须映射为编码：女性/女/female → `"0"`，男性/男/male → `"1"`。禁止传 `"女性"`、`"男性"`、`"female"`、`"male"`。
3. 所有比例筛选参数使用 **0~100 的百分比数值**：用户说“互动率至少 3%”时传 `3`，不能传 `0.03`；“女性受众至少 70%”传 `70`。
4. boolean 参数必须传 JSON boolean：`true` / `false`，不能传 `"true"` / `"false"`、`1` / `0`。`has_email`、`has_whatsapp`、`is_ai_creator`、`is_product_kol` 等均属于 boolean。
5. 国家和语言必须转换为代码；多选使用英文逗号连接，例如 `country_code: "US,CA"`、`language_code: "en,fr"`。
6. 日期筛选统一传 `YYYY-MM-DD`。
7. `lang` 只控制响应码值翻译，不用于筛选达人，默认 `en`。筛选达人内容语言使用 `language_code`。
8. 只传目标平台支持的字段。三平台播放量、互动率、受众语言等字段名并不完全相同。
9. 当前 HTTP Open API 不支持 Instagram 的 GMV、销售商品数筛选，不要发送这些字段。
10. 不要发送旧字段名。HTTP Open API 请求模型会忽略未声明字段，旧字段可能请求成功但实际没有产生筛选效果。
11. **行业 vs 关键词的决策逻辑**：
    - **用户明确指定**"行业"或"关键词"时，按用户意图走,不要替换。例如用户说"关键词搜 funny"就用 `keyword`，说"行业选美妆"就用 `industry`。
    - **用户未明确区分**时（如"找搞笑达人"、"美妆博主"），优先映射为 `industry`。常见映射：搞笑/funny → Comedy & Humor, 美妆/beauty → Skincare 或 Beauty, 科技/tech → Technology, 宠物/pet → Pet Supplies, 美食/food → Food & Beverage。
    - **行业搜索结果为空时**（返回 0 条），自动用同义词降级为 `keyword` 重新搜索,并告知用户"行业筛选无结果,已改用关键词搜索"。例如 `industry: "Comedy & Humor"` 返回空 → 用 `keyword: "funny"` 重搜。
    - `keyword` 仅用于：搜索具体用户名/昵称、精确主题词、或行业降级兜底。

## 服务等级

`service_level` 控制返回字段与积分消耗。面向用户发起搜索前，必须让用户清楚三档含义：

- 用户未指定等级时，先展示下方简短表格，并说明默认推荐 `S2`。
- 用户确认“默认/推荐/直接搜”时，使用 `S2`。
- 用户明确指定 `S1` / `S2` / `S3`，或本轮对话已展示过等级说明时，可直接执行，避免重复打断。

| 等级 | 名称 | 积分/条 | 返回范围 |
|------|------|---------|----------|
| S1 | 纯名单筛选 | 1 | 基础身份、主页、联系方式存在性、最近发布时间；具体字段因平台而异 |
| S2 | 精准触达 | 3 | S1 + 国家、性别、粉丝/播放/互动、行业、邮箱等；具体字段因平台而异 |
| S3 | 深度画像 | 4 | S2 + 受众性别、国家、语言、年龄分布 |

## 通用请求参数

除 `platform` 为脚本路由参数外，其余字段会作为 JSON Body 发送到对应平台搜索接口。

| 参数 | 类型 | 说明 |
|------|------|------|
| `platform` | string | 必填：`tiktok` / `youtube` / `instagram` |
| `keyword` | string | 搜索关键词 |
| `country_code` | string | 国家代码，多选逗号分隔 |
| `gender` | string | `"0"`=女性，`"1"`=男性 |
| `has_email` | boolean | 是否有邮箱 |
| `language_code` | string | 达人内容语言代码，多选逗号分隔 |
| `followers_cnt_gte` / `followers_cnt_lte` | integer | 粉丝数/订阅数范围 |
| `industry` | string | 行业类目；脚本支持类目 ID、中文/英文名称和常用别名 |
| `audience_country_code_list` | string | 受众国家代码，多选逗号分隔 |
| `audience_age_list` | string | 受众年龄，多选逗号分隔 |
| `audience_female_rate_gte` / `audience_female_rate_lte` | number | 受众女性比例，传 0~100 百分比数值 |
| `page` | integer | 页码，默认 1 |
| `size` | integer | 每页数量，默认 50；普通 Open API 调用最大 100 |
| `sort_field` | string | 排序字段，必须使用目标平台支持的字段 |
| `sort_order` | string | `asc` / `desc`，默认 `desc` |
| `service_level` | string | `S1` / `S2` / `S3`，默认 `S2` |
| `lang` | string | 响应显示语言：`cn` / `en`，默认 `en`，不参与筛选 |

## TikTok 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `has_mcn` / `has_line` / `has_zalo` | boolean | 是否绑定 MCN / 有 Line / 有 Zalo |
| `last10_avg_video_views_cnt_gte` / `_lte` | number | 近 10 条视频平均播放量范围 |
| `last10_avg_video_interaction_rate_gte` / `_lte` | number | 近 10 条视频平均互动率范围，传 0~100 |
| `last_video_publish_date_gte` / `_lte` | string | 最近视频发布日期范围，`YYYY-MM-DD` |
| `product_category_id_array` | string | 带货类目 ID，多选逗号分隔 |
| `audience_language_code_list` | string | 受众语言代码，多选逗号分隔 |
| `last30day_gmv_gte` / `_lte` | number | 近 30 天 GMV 范围 |
| `last30day_gpm_gte` / `_lte` | number | 近 30 天 GPM 范围 |
| `last30day_gmv_per_buyer_gte` / `_lte` | number | 近 30 天客单价范围 |
| `last30day_commission_rate_gte` / `_lte` | number | 近 30 天佣金率范围，传 0~100 |

TikTok `sort_field`：`followers_cnt` / `last10_avg_video_views_cnt` / `last10_avg_video_interaction_rate`。

## YouTube 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `has_whatsapp` / `is_ai_creator` | boolean | 是否有 WhatsApp / 是否 AI 达人 |
| `last10_avg_video_view_count_all_gte` / `_lte` | number | 近 10 条全部视频平均播放量范围 |
| `last10_avg_video_view_count_short_gte` / `_lte` | number | 近 10 条短视频平均播放量范围 |
| `last10_avg_interaction_rate_all_gte` / `_lte` | number | 近 10 条全部视频平均互动率范围，传 0~100 |
| `last10_avg_interaction_rate_short_gte` / `_lte` | number | 近 10 条短视频平均互动率范围，传 0~100 |
| `last_video_publish_date_gte` / `_lte` | string | 最近视频发布日期范围，`YYYY-MM-DD` |
| `audience_language_code_list` | string | 受众语言代码，多选逗号分隔 |

YouTube 不要使用旧字段名 `last10_avg_video_views_cnt_*`、`last10_avg_video_views_cnt_short_*`、`last10_avg_video_interaction_rate_*`、`last10_avg_video_interaction_rate_short_*`。

## Instagram 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `has_whatsapp` / `is_product_kol` / `is_ai_creator` | boolean | 是否有 WhatsApp / 带货达人 / AI 达人 |
| `last10_avg_video_view_count_gte` / `_lte` | number | 近 10 条视频平均播放量范围 |
| `last10_avg_video_interaction_rate_gte` / `_lte` | number | 近 10 条视频平均互动率范围，传 0~100 |
| `last_video_publish_time_gte` / `_lte` | string | 最近视频发布日期范围，`YYYY-MM-DD` |
| `female_ratio_gte` / `_lte` | number | 受众女性占比范围，传 0~100（Instagram 专用，替代通用 `audience_female_rate_*`） |
| `audience_language_list` | string | 受众语言，多选逗号分隔 |

Instagram 不要使用旧字段名 `last10_avg_video_views_cnt_*`、`last_video_publish_date_*`、`audience_female_rate_*`、`is_top_creator`。

## Category Input（industry 参数说明）

`industry` 参数在 HTTP Open API 中要求传 level-3 数字类目 ID。通过本 skill 的脚本调用时，脚本支持以下输入并自动转换为 level-3 类目 ID：

- **三级类目 ID**：`5001001,25009001,24001001`（真实 ID 可能为 7 位或 8 位）
- **一级类目 ID**：`5,25`（真实 ID 可能为 1 位或 2 位，自动展开为所有三级子类目）
- **中文类目名**：`美妆,科技数码`
- **英文类目名**：`Skincare,Mobile Phones`
- **常用英文别名**：`Fashion`, `Beauty`, `Sports`, `Tech`, `Food`, `Gaming`, `Travel`
- **混合输入**：`Fashion,Beauty`（逐项解析）

脚本会校验每个行业值是否存在于完整行业树中。只要有一项无法识别，搜索会在发送 HTTP 请求前失败，不会发送名称、未知数字 ID 或部分转换结果。

## 示例

```json
{"platform":"tiktok","country_code":"US","gender":"0","has_email":true,"followers_cnt_gte":100000,"last10_avg_video_interaction_rate_gte":3,"service_level":"S2"}
```

```json
{"platform":"youtube","country_code":"US","last10_avg_video_view_count_short_gte":50000,"audience_female_rate_gte":70,"service_level":"S3"}
```

```json
{"platform":"instagram","industry":"Beauty","is_product_kol":true,"audience_language_list":"en","service_level":"S2"}
```

## 输出格式

### TikTok

```
| # | 用户名 | 昵称 | 粉丝数 | 获赞数 | 平均播放 | 互动率 | 国家 | 主页链接 |
```

### YouTube

```
| # | 用户名 | 频道名 | 订阅数 | 总观看 | 平均播放 | 互动率 | 国家 | 频道链接 |
```

### Fuzzy Industry Guidance

- High confidence terms can be searched directly. Examples: `skincare`, `skin care`, `funny`, `home cleaning`, `pet supplies`, `kids toys`, `phone accessories`.
- If the user gives a broad business phrase, map it to the closest supported category and briefly state the interpretation before searching. Example: "cleaning creators" -> `Home Cleaning`; "funny creators" -> `Comedy & Humor`.
- If the phrase is ambiguous, do not silently guess. Show 2-3 likely categories and ask the user to confirm. Examples: "toy" may mean `Children's Toys`, `Pet Toys`, `Model Toys`, or `Adult Art Toys`; "home" may mean `Home Cleaning`, `Home Decoration`, `Home Appliances`, or `Kitchen & Tableware`.
- When the script returns `suggestions`, present those category names to the user and ask which one to use instead of sending a request with an unknown industry value.

### Instagram

```
| # | 用户名 | 昵称 | 粉丝数 | 帖子数 | 平均播放 | 互动率 | 国家 | 主页链接 |
```

### 通用格式规则

- 仅展示实际返回的字段，不能假设低服务等级包含 S2/S3 字段
- 表格内链接用 `[查看][linkN]` 引用式，表格下方定义完整 URL
- 统计信息单独列出：总匹配数、服务等级、消耗积分、剩余配额、请求 ID
- `meta.total` 为 null 时不展示总匹配数
- 默认展示 5~10 条，超过时询问用户
- 展示后主动询问是否需要导出 CSV/Excel
