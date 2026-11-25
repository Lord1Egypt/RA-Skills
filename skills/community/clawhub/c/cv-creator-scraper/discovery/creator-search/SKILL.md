---
name: creator-search
description: |
  使用 CreatiVault OpenAPI 搜索 TikTok、YouTube 和 Instagram 已收录达人。支持自然语言搜索、按地区/行业/粉丝/互动率/邮箱/受众筛选、按达人 ID 或主页链接批量精确查询、将本次结果导出 CSV，以及查 TikTok 和 Instagram 已收录的品牌合作达人。适用于找达人、带货达人、达人筛选、合作名单、品牌合作达人、creator search、influencer discovery。
compatibility: Node.js 20.6+
metadata:
  layer: discovery
  parent: creator-scraper-cv
---

# Creator Search（达人搜索）

## 概述

在 CreatiVault 已收录的 TikTok、YouTube 和 Instagram 达人中搜索。自然语言搜索适合描述内容方向和合作场景，结构化搜索适合硬性条件或批量查询已知账号。以 CreatiVault OpenAPI 为数据来源。除非用户明确要求公开网页搜索，或在 OpenAPI 未命中后确认使用公开来源，否则使用 CreatiVault OpenAPI。

## 脚本引用

| 脚本 | 相对路径 | 状态 |
|------|----------|------|
| search_creators_nl.mjs | `../../scripts/search_creators_nl.mjs` | ✅ 可用 |
| search_creators.mjs | `../../scripts/search_creators.mjs` | ✅ 可用 |
| find_brand_collaboration_creators.mjs | `../../scripts/find_brand_collaboration_creators.mjs` | ✅ 可用 |
| export_to_csv.mjs | `../../scripts/export_to_csv.mjs` | 将已返回的搜索结果转换为 CSV |

自然语言搜索调用格式：

```bash
node {baseDir}/scripts/search_creators_nl.mjs '{"platform":"instagram","query":"找欧美5万粉以上的跑步和马拉松训练达人，内容专业、真实，适合推广跑鞋","limit":20}'
```

结构化搜索调用格式：

```bash
node {baseDir}/scripts/search_creators.mjs '{"platform":"tiktok","country_code":"US","gender":"0","followers_cnt_gte":100000,"service_level":"S2"}'
```

## 竞品品牌找达人

当用户要找已与某个竞品或品牌合作过的达人时，使用品牌合作达人查询。只想看该品牌相关视频时，使用 `video-search` 的品牌视频洞察。

离线合作达人查询：

```bash
node {baseDir}/scripts/find_brand_collaboration_creators.mjs '{"brand_name":"Fenty Beauty","platforms":["tiktok","instagram"],"limit":20}'
```

- 查询 TikTok、Instagram 已收录的合作记录，可按地区、行业、粉丝量、互动率下限或邮箱可用性筛选达人。
- `items[].creator` 为合作达人，`items[].brand_account` 为匹配的品牌账号，`items[].collaboration_count` 为记录中的合作次数。`evidence_videos` 有值时可展示佐证视频。
- 无结果时说明当前未找到已收录的品牌合作记录。用户若需要品牌相关视频，可确认后使用品牌视频洞察查询已收录视频。

## 搜索前 Brief 规则

按已有主页链接或达人 ID 精确查询时，只需明确标识所属平台及标识列表，可按用户要求叠加筛选条件。筛选新候选名单时，按以下规则确认需求。

1. 用户未指定平台时，必须先问平台，给出 TikTok / Instagram / YouTube 选项；不要默认选一个平台，也不要同时搜多个平台。
2. 用户未指定目标市场/地区时，必须先问目标地区；“东南亚”“欧美”“美国”等明确范围可以直接使用。
3. 用户未指定品类、行业、关键词、产品、品牌或内容方向时，必须先问业务方向。
4. 用户未指定数量时，默认先找 20 个。
5. 用户已经给出平台、地区、品类和数量时，不要继续问服务等级或技术参数，直接按当前条件严格搜索。
6. 澄清问题必须短，一次最多 3 个，只问当前真正缺失的信息。示例：“可以，我先确认 2 点：你想优先搜哪个平台？目标地区是哪些国家或区域？”

不要用“基于规则”“参数如下”“size=min(...)”“Navos profile 自动 S3”“召回类型”等内部表达作为过程内容。内部规则只用于指导执行，不展示给用户。

## 搜索方式选择

每次用户请求只选择一种搜索方式，不要同时调用两个脚本：

1. 用户重点描述内容方向、达人画像、内容风格、真实场景、品牌或产品适配等难以稳定映射为类目/关键词的需求时，优先调用 `search_creators_nl.mjs`。Instagram 会使用语义向量召回；TikTok 和 YouTube 当前使用自然语言解析后的标量召回。
2. 用户要求按主页链接或达人 ID 查询，或要求精确邮箱/WhatsApp、更新时间、指定行业 ID、排序字段、S1/S2/S3 字段、GMV/GPM 等明确结构化条件时，调用 `search_creators.mjs`。
3. 用户既有复杂语义又有 Instagram 向量检索暂不支持的强约束（当前包括是否有邮箱、更新时间）时，不要假设自然语言接口会严格执行这些条件；优先使用结构化搜索，或先向用户说明限制并确认取舍。
4. 用户未指定平台时，先按「搜索前 Brief 规则」澄清平台；自然语言接口虽然有默认平台，但面向用户执行时不得依赖默认平台直接搜索。
5. 多平台需求必须拆成多次请求，并在调用第二个平台前告知用户会增加查询消耗。

### 自然语言搜索协议

- Endpoint：`POST /openapi/v1/creators/nl-search`
- 请求体只允许 `query`、`platform`、`limit`。不要传 `lang`、`service_level`、`debug`、`route_top_k` 等内部实现字段。
- `query` 必填，长度 1~1000；`platform` 支持 Instagram/TikTok/YouTube 及常用别名；`limit` 默认 20，范围 1~100。
- 一次请求只搜索一个平台。结果不足或为 0 时遵守本 Skill 的静默查询边界，不自动换平台、追加结构化搜索或放宽条件。
- 该脚本预估 15 credits 用于 Navos 余额预检。实际消耗以服务端计费配置和接口响应为准。
- 多平台需要分别调用。追加平台或切换检索方式前，说明会增加查询并征得用户确认。
- `meta.recall_type=vector` 表示 Instagram 语义向量召回；`scalar_fallback` 表示 Instagram 因语义不足自动使用结构化筛选；`scalar` 表示 TikTok/YouTube 标量召回。
- Instagram 服务端 fallback 在同一次请求内完成，不需要客户端再次调用，也不要把它算成一次新的补充搜索。
- 该接口返回固定精简字段，不返回 S3 受众画像或完整联系方式；需要丰富字段时应改用结构化搜索，并先征得用户确认。
- 该接口当前不支持 `lang`。按原始 `country_code` 等返回值展示，不要自行声称服务端已做中英文翻译。
- API Key 需要 `creator:nl_search` 或 `creator:*` 权限；收到 `40301` 时提示检查 scope，不要自动退回结构化搜索或网页搜索。

### 自然语言搜索结果展示

- 只展示接口实际返回的 `uid`、`username`、`nickname`、`avatar_url`、`profile_url`、`country_code`、`followers_count`、`avg_views`、`engagement_rate`、`match_score`。
- 只要返回 `avatar_url`，表格必须增加独立「头像」首列，用 40px 等比例缩略图渲染；不要只展示达人名文字链。`avatar_url` 为空时该格留空，不要编造头像或占位图。
- `engagement_rate` 是小数比例，展示时乘以 100 并加 `%`，例如 `0.0432` 展示为 `4.32%`。
- `match_score` 仅用于同一次请求内比较，不要跨请求、跨平台比较，也不要解释成百分制绝对质量分。
- 结果为 0 或不足 `limit` 时停止，不要自动发起第二次搜索；不要主动说明 `meta.recall_type` 等内部召回信息，除非用户明确要求排查。

## 参数提取强制规则

1. `platform` 必须转换为小写：`tiktok` / `youtube` / `instagram`。
2. 达人性别必须映射为编码：女性/女/female → `"0"`，男性/男/male → `"1"`。禁止传 `"女性"`、`"男性"`、`"female"`、`"male"`。
3. 所有比例筛选参数使用 **0~100 的百分比数值**：用户说“互动率至少 3%”时传 `3`，不能传 `0.03`；“女性受众至少 70%”传 `70`。
4. boolean 参数必须传 JSON boolean：`true` / `false`，不能传 `"true"` / `"false"`、`1` / `0`。`has_email`、`has_whatsapp`、`is_ai_creator`、`is_product_kol` 等均属于 boolean。
5. 国家和语言必须转换为代码；多选使用英文逗号连接，例如 `country_code: "US,CA"`、`language_code: "en,fr"`。
6. 日期筛选统一传 `YYYY-MM-DD`。
7. `lang` 只控制响应码值翻译，不用于筛选达人，默认 `en`。筛选达人内容语言使用 `language_code`。
8. 只传目标平台支持的字段。三平台播放量、互动率、受众语言等字段名并不完全相同。
9. **TikTok 带货指标**：可按近 30 天 GMV、GPM、客单价和佣金率区间筛选。S2 和 S3 有数据时可返回对应展示值与销售商品数，按接口实际提供的字符串展示，不用筛选区间补全缺失值。YouTube 和 Instagram 的达人搜索使用各自平台字段。
10. 不要发送旧字段名。HTTP Open API 请求模型会忽略未声明字段，旧字段可能请求成功但实际没有产生筛选效果。
11. **行业与关键词选择**：
    - **用户明确指定**"行业"或"关键词"时，按用户意图走,不要替换。例如用户说"关键词搜 funny"就用 `keyword`，说"行业选美妆"就用 `industry`。
    - **用户未明确区分**时（如"找搞笑达人"、"美妆博主"），优先映射为 `industry`。常见映射：搞笑/funny → Comedy & Humor, 美妆/beauty → Skincare 或 Beauty, 科技/tech → Technology, 宠物/pet → Pet Supplies, 美食/food → Food & Beverage。
    - **行业搜索结果为空时**（返回 0 条），不要自动用同义词降级为 `keyword` 重新搜索。应停止并告知用户"当前严格行业筛选无结果"，提供 2-3 个可选放宽方向，等待用户确认后再搜索。
    - `keyword` 仅用于：搜索具体用户名/昵称、精确主题词、或行业降级兜底。

## 搜索执行边界

为避免静默查询和不可预期扣费，达人搜索必须遵守以下边界：

1. 所有用户筛选条件必须进入 OpenAPI 请求体。包括但不限于 `country_code`、`industry`、`followers_cnt_gte/_lte`、`last10_avg_video_interaction_rate_gte/_lte`、`has_email`、`language_code`、受众字段。禁止先只传少量条件拿候选，再本地过滤大量结果。
2. 默认只调用一次搜索脚本，且只查 `page=1`。不得为了凑满用户要求的数量自动翻到 page 2、page 10 等。
3. 用户未说明数量时，默认 `size=20`。用户明确要求 N 条时，当前页 `size=min(N,100)`。只查询第 1 页，单页最多 100 条。批量精确查找时可按提供的标识数量（去重后）设置本页目标数量，仍遵守单页上限和翻页规则。
4. 用户未指定平台时，必须先澄清平台。不得自动选择平台，也不得自动并行或串行搜索 TikTok、Instagram、YouTube 来凑结果。
5. 严格条件返回 0 条时，不再发起任何补充搜索；直接说明没有命中，并询问是否放宽条件，例如降低互动率、扩大地区、换平台或改用关键词。
6. 严格条件返回数量少于用户要求时，只展示严格命中的结果。若用户要求超过 100 条，明确说明当前仅返回第 1 页、继续获取还需分页；任何继续翻页或跨平台搜索都必须先让用户确认。
7. 如果接口返回结果与用户筛选条件明显不一致，不展示不合格结果凑数；停止并说明可能是字段口径或传参问题，建议用户确认是否放宽条件或继续排查。
8. 视频搜索不是达人搜索兜底。只有用户明确要求"找视频 / 爆款视频 / 参考视频 / 话题视频 / 内容案例"时，才能切换到 `video-search`。

## 面向用户的回复口径

搜索过程和最终回复必须像业务助手，而不是接口调试日志。

### 搜索前

- 信息足够时，只用 1-2 句话确认业务口径，例如：“我会按 TikTok / 美国 / 美妆 / 粉丝 10-50 万 / 互动率 ≥3% / 有邮箱做严格匹配，不自动跨平台或放宽条件。”
- 信息不足时，只问缺失项，不展示参数、不解释规则、不输出 JSON。
- 不要输出“参数：”“规则：”“size/page/service_level/endpoint/meta/request_id/recall_type”等技术内容。

### 搜索后

按以下顺序输出：

1. 一句话结果摘要：严格命中了多少个、是否满足用户数量。
2. 一张达人表：展示真实返回字段，Navos S3 场景按宽表展示。
3. 1-3 条业务判断：谁最优先、为什么适合、潜在风险是什么。
4. 如果有 `cv_list_url`，只展示短链接 `[在 CreatiVault 查看完整列表]({cv_list_url})`，不要原样输出长 URL。
5. 下一步建议只给最相关的 1-3 条，优先围绕用户原始目标，例如建联、导出、继续放宽条件或找相似达人。

禁止：

- 不要解释“我选择了哪个接口”“用了哪个脚本”“Navos profile 自动 S3”“自然语言接口/结构化接口差异”等内部实现，除非用户明确问技术原因。
- 不要说“共匹配 5000+”同时又只展示 20 条而不说明这是本次返回结果；Navos 快照页和对话区都应以本次实际返回数量为主。
- 不要一边说“不会自动跨平台/翻页”，一边继续发起跨平台或翻页搜索。

## 服务等级

`service_level` 控制结构化搜索返回的数据范围。实际消耗以服务端计费配置和接口响应为准。

本节仅适用于 `search_creators.mjs` 结构化搜索。`search_creators_nl.mjs` 不接受 `service_level`，也不返回 S3 受众画像。

- 用户明确指定等级时按其选择；需要邮箱等详细信息时用 `S2`，需要受众画像时用 `S3`。未指定时，常规调用缺省 `S2`，Navos 默认注入 `S3`。

| 等级 | 返回范围 |
|------|----------|
| S1 | 基础身份、主页、粉丝或订阅数、联系方式可用性等 |
| S2 | 增加地区、内容表现、行业及已有的邮箱等信息。TikTok 有数据时可返回带货指标 |
| S3 | 增加受众性别、国家或地区、语言和年龄等画像 |

> **Navos 用户**：脚本会自动使用 S3（深度画像），无需手动指定。Navos 用户搜索结果可能不展示积分消耗信息（积分由 Navos 侧管控）。

服务等级不得作为静默补救手段。用户没有要求受众画像、年龄、性别、国家分布等 S3 字段时，不要为了"可能更准"而主动升高服务等级；如果当前运行 profile 自动注入更高等级，仍必须遵守上方的页数、平台和结果数量边界。

## 通用请求参数

除 `platform` 为脚本路由参数外，其余字段会作为 JSON Body 发送到对应平台搜索接口。

| 参数 | 类型 | 说明 |
|------|------|------|
| `platform` | string | 必填：`tiktok` / `youtube` / `instagram` |
| `union_user_ids` | string[] | 可选：达人 `union_user_id` 批量精确查询，最多 200 条；可与 `profile_urls` 同传，两者取并集 |
| `profile_urls` | string[] | 可选：达人主页链接批量精确查询，最多 200 条；可与其他筛选条件叠加 |
| `keyword` | string | 搜索关键词 |
| `country_code` | string | 国家代码，多选逗号分隔 |
| `gender` | string | `"0"`=女性，`"1"`=男性 |
| `has_email` | boolean | 是否有邮箱 |
| `language_code` | string | 达人内容语言代码，多选逗号分隔 |
| `followers_cnt_gte` / `followers_cnt_lte` | integer | 粉丝数/订阅数范围 |
| `industry` | string | 行业类目；脚本支持类目 ID、中文/英文名称和常用别名 |
| `audience_country_code_list` | string | 受众国家代码，多选逗号分隔 |
| `audience_age_list` | string | 受众年龄，多选逗号分隔 |
| `audience_female_rate_gte` / `audience_female_rate_lte` | number | TikTok 和 YouTube 的受众女性比例，传 0~100 百分比数值。Instagram 用 `female_ratio_gte` / `female_ratio_lte` |
| `page` | integer | 页码，默认 1 |
| `size` | integer | 每页 1~100，Skill 在用户未指定时取 20 |
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

批量查找已收录的账号，主页链接和达人 ID 可合用，两类各最多 200 条，按并集筛选：

```json
{"platform":"tiktok","profile_urls":["https://www.tiktok.com/@creator_a"],"union_user_ids":["123456789"],"has_email":true,"size":20}
```

## 导出搜索结果

将已经取得的结构化或自然语言搜索响应传给 `export_to_csv.mjs`。为本次结果选一个尚未使用的输出路径，脚本会生成本地 CSV，便于用户继续筛选。脚本默认追加到已有文件，复用路径前先确认用户是要合并还是覆盖。

```bash
node {baseDir}/scripts/export_to_csv.mjs '{"output":"creators-current-search.csv"}' < search-result.json
```

## 输出格式

### 表格设计原则（展示层优化）

达人名单表格必须遵循以下原则，提升可读性与交互效率：

**Markdown 表格安全清洗（防止 Navos 展示错位）**：
- 输出任何 Markdown 表格前，必须先清洗所有单元格文本，尤其是昵称、bio、标签、行业、内容方向、受众国家/语言等开放文本字段。
- 单元格内禁止出现原始竖线 `|`，也不要用 `\|` 转义；统一替换为 `／` 或 `/`。例如 `Gabe | Tech & Lifestyle` 展示为 `Gabe／Tech & Lifestyle`。
- 单元格内禁止出现换行、`\r`、`\n`、`<br>`；统一压成一个空格。
- 单元格内不要放会破坏表格结构的 Markdown 片段；长 URL 不进表格，链接只放在达人名或单独短入口里。
- 每一行的列数必须和表头完全一致；输出前检查每行 `|` 分隔数量一致。多个值用 `、` 或 `/` 连接，不要用 `|`。

1. **Navos 链接与入口规则**：Navos profile 下不再生成单个达人详情链接。`scripts/search_creators.mjs` 和 `scripts/search_creators_nl.mjs` 只补充 `cv_list_url`，用于在 Navos 内置浏览器无感登录 CreatiVault 并打开本次搜索结果快照列表；用户在 CV 原生列表中点击达人打开详情弹窗。对话区表格里的达人名/昵称仍链接到平台主页，平台主页链接必须保留为单独入口或引用链接。common profile 下不展示 CV 列表入口。
2. **动态展示返回字段，不要固定表头**：表格列必须基于本次接口实际返回字段动态生成，尤其 Navos 用户默认 S3，必须覆盖 S1 + S2 + S3 的所有可读字段。禁止只展示固定的少数列（如粉丝数、平均播放、互动率、国家、粉丝层级、认证、邮箱、带货、AI），也禁止因为表格变宽就省略 S3 受众画像字段。

   **固定语义列只保留这些：**
   - `#`：序号
   - `头像`：由 `avatar_url` 渲染
   - `用户名`：由 `username` 渲染为主页链接
   - `昵称` / `频道名`：由 `nickname` 渲染为主页链接

   **其余列必须按实际返回字段展开**：
   - 字段在接口响应里存在且至少一条结果有有效值，就展示为独立列
   - 字段在所有结果中都为空、`null`、空数组或空字符串时，可以省略该列
   - Boolean 字段不要只放空白图标；展示为 `是/否` 或带文字的 `✅ 是`、`—`
   - `avatar_url` 已通过头像承载，无需重复放原始 URL
   - `uid` 属于可追踪字段，S3 结果中如果返回必须展示，或至少在每行详情中展示，便于后续精确查询、建联、排障

   **S3 字段强制覆盖**：当 `service_level=S3`（Navos 默认）时，以下字段只要返回就必须展示，不得漏掉：
   - 受众女性比例：`audience_female_rate`
   - 受众国家分布：`audience_country_code_list`
   - 受众语言分布：TikTok/Instagram 用 `audience_language_code_list`，YouTube 用 `audience_language_list`
   - 受众年龄分布：TikTok/Instagram 用 `audience_age_id_list`，YouTube 用 `audience_age_list`
   - S2 核心指标也必须保留：粉丝/订阅数、视频/帖子数、平均播放、互动率、播放粉丝比、中位播放、行业、hashtags、bio、email/WhatsApp/Line/Zalo/MCN 等实际返回字段

   Navos 用户默认 S3，因此不要把 S3 结果压缩成少字段摘要表，也不要把同一批达人拆成“基础表 + 受众画像表”两张表。只要本次是 Navos profile、请求体包含 `service_level=S3`，或响应中出现任何 `audience_*` 字段，就必须默认输出**一张动态宽表**：
   - 同一张表内同时展示头像、用户名、昵称/频道名、uid、粉丝/订阅、视频数、点赞/总观看、均播、互动率、播放粉丝比、中位播放、国家、语言、性别、认证、联系方式、带货/类目、bio/hashtags，以及受众女性比例、受众国家、受众语言、受众年龄等 S3 字段。
   - 表格可以横向滚动，列名可以适当压缩，但不得因此省略实际返回且有值的 S1 / S2 / S3 字段。
   - 如果某个字段在所有结果里都是空、`null`、空数组或空字符串，可以省略该列；但不得把“字段过多”作为省略原因。

3. **达人属性列只在有真实字段时展示**：不要再输出单个「状态」列；如确实需要摘要属性，可拆成「粉丝层级」「认证」「邮箱」「带货」「AI」等独立列，但这些列必须满足“字段存在且至少一条结果有有效值”才出现。图标后必须带文字说明，方便用户直接读懂含义：

   **粉丝星级**（按粉丝量绝对值分 5 档，粉丝越多星越多）：
   - ⭐⭐⭐⭐⭐ 超头部（粉丝 > 200 万）
   - ⭐⭐⭐⭐ 头部（粉丝 50 万 - 200 万）
   - ⭐⭐⭐ 腰部（粉丝 10 万 - 50 万）
   - ⭐⭐ 初级（粉丝 1 万 - 10 万）
   - ⭐ 素人/起步（粉丝 < 1 万）

   **属性列**（图标+文字组合，根据返回字段显示，缺失则留空，不要凭空补）：
   - ✅ 已认证（`is_verified=true`）
   - ✉ 有邮箱（`has_email=true` 或 `email` 非空）
   - 🛒 带货（`product_categories` 非空，或 `has_showcase=true`）
   - 🤖 AI 达人（`is_ai_creator=true`，平台返回该字段时）

   **列值格式**：
   - 粉丝层级列必须输出完整文字，例如 `⭐⭐⭐⭐⭐ 超头部`，不要只放星星
   - 认证列输出 `✅ 已认证`，邮箱列输出 `✉ 有邮箱`，带货列输出 `🛒 带货`，AI 列输出 `🤖 AI达人`
   - 字段缺失或全量为空的属性列不要输出整列；粉丝数为 0 或缺失时粉丝层级列留空或省略
   - **不要把 `AI` 作为固定末列**。只有平台支持并实际返回 `is_ai_creator=true` 等有效值时才展示 AI 列；TikTok 结果通常不返回 `is_ai_creator`，不得凭空加 AI 列
4. **用户名与昵称保持两列**：不合并，保留独立列。
5. **核心指标列保留**：平均播放（avg_views）、互动率（engagement_rate）、粉丝数必须展示（S2/S3 场景），见「通用格式规则」。

### TikTok

- **头像列**：用固定方形外框承载头像，避免 Navos 表格列压缩竖图。推荐格式：`<span style="display:inline-flex;width:40px;height:40px;overflow:hidden;border-radius:4px;vertical-align:middle;"><img src="{avatar_url}" width="40" height="40" style="width:40px;height:40px;max-width:40px;min-width:40px;object-fit:cover;object-position:center;display:block;"></span>`；`avatar_url` 来自 S1 字段，缺失时该格留空，禁止放占位图或编造 URL。不要用 Markdown `![]()`，也不要只裸写 `<img src="{avatar_url}" width="36" height="36">`
- TikTok S3 动态列应覆盖实际返回的这些字段：`uid`、`followers_count`、`likes_count`、`video_count`、`has_showcase`、`has_email`、`has_mcn`、`has_line`、`has_zalo`、`last_video_publish_date`、`country_code`、`gender`、`avg_views`、`engagement_rate`、`views_per_follower`、`is_verified`、`last10_video_views_per_sub`、`last10_med_video_views_cnt`、`last10_med_video_views_per_sub`、`product_categories`、`industry_categories`、`bio`、`hashtags`、`language`、`email`、`link_whatsapp`、`link_line`、`link_zalo`、`mcn`、`audience_female_rate`、`audience_country_code_list`、`audience_language_code_list`、`audience_age_id_list`
- TikTok 不要固定输出 `AI` 列；除非响应里真实存在 AI 相关字段且有有效值

### YouTube

- **头像列**：用固定方形外框承载头像，避免 Navos 表格列压缩竖图。推荐格式：`<span style="display:inline-flex;width:40px;height:40px;overflow:hidden;border-radius:4px;vertical-align:middle;"><img src="{avatar_url}" width="40" height="40" style="width:40px;height:40px;max-width:40px;min-width:40px;object-fit:cover;object-position:center;display:block;"></span>`；`avatar_url` 来自 S1 字段，缺失时该格留空，禁止放占位图或编造 URL。不要用 Markdown `![]()`，也不要只裸写 `<img src="{avatar_url}" width="36" height="36">`
- YouTube S3 动态列应覆盖实际返回的这些字段：`uid`、`has_email`、`has_whatsapp`、`last_video_publish_time`、`country_code`、`language`、`gender`、`bio`、`followers_count`、`video_count`、`view_count`、`avg_views`、`avg_views_short`、`avg_views_long`、`engagement_rate`、`engagement_rate_short`、`engagement_rate_long`、`is_verified`、`last10_video_views_per_sub`、`last10_video_views_per_sub_short`、`last10_video_views_per_sub_long`、`last10_med_video_views_cnt`、`last10_med_video_views_cnt_short`、`last10_med_video_views_cnt_long`、`last10_med_video_views_per_sub`、`last10_med_video_views_per_sub_short`、`last10_med_video_views_per_sub_long`、`industry_categories`、`hashtags`、`email`、`whatsapp`、`audience_female_rate`、`audience_country_code_list`、`audience_language_list`、`audience_age_list`
- `is_ai_creator` 只在响应真实返回且有有效值时展示，不要固定输出空白 AI 列

### Fuzzy Industry Guidance

- High confidence terms can be searched directly. Examples: `skincare`, `skin care`, `funny`, `home cleaning`, `pet supplies`, `kids toys`, `phone accessories`.
- If the user gives a broad business phrase, map it to the closest supported category and briefly state the interpretation before searching. Example: "cleaning creators" -> `Home Cleaning`; "funny creators" -> `Comedy & Humor`.
- If the phrase is ambiguous, do not silently guess. Show 2-3 likely categories and ask the user to confirm. Examples: "toy" may mean `Children's Toys`, `Pet Toys`, `Model Toys`, or `Adult Art Toys`; "home" may mean `Home Cleaning`, `Home Decoration`, `Home Appliances`, or `Kitchen & Tableware`.
- When the script returns `suggestions`, present those category names to the user and ask which one to use instead of sending a request with an unknown industry value.

### Instagram

- **头像列**：用固定方形外框承载头像，避免 Navos 表格列压缩竖图。推荐格式：`<span style="display:inline-flex;width:40px;height:40px;overflow:hidden;border-radius:4px;vertical-align:middle;"><img src="{avatar_url}" width="40" height="40" style="width:40px;height:40px;max-width:40px;min-width:40px;object-fit:cover;object-position:center;display:block;"></span>`；`avatar_url` 来自 S1 字段，缺失时该格留空，禁止放占位图或编造 URL。不要用 Markdown `![]()`，也不要只裸写 `<img src="{avatar_url}" width="36" height="36">`
- Instagram S3 动态列应覆盖实际返回的这些字段：`uid`、`has_email`、`has_whatsapp`、`last_video_publish_time`、`country_code`、`language`、`gender`、`bio`、`followers_count`、`video_count`、`avg_views`、`engagement_rate`、`is_verified`、`last10_video_views_per_sub`、`last10_med_video_views_cnt`、`last10_med_video_views_per_sub`、`industry_categories`、`hashtags`、`email`、`link_whatsapp`、`audience_female_rate`、`audience_country_code_list`、`audience_language_code_list`、`audience_age_id_list`
- `is_product_kol` / `is_ai_creator` 只在响应真实返回且有有效值时展示，不要固定输出空白带货或 AI 列

### 通用格式规则

- 仅展示实际返回的字段，不能假设低服务等级包含其不具备的字段
- **等级字段范围（必须正确理解，避免漏展示核心指标）**：S1 ⊂ S2 ⊂ S3，高等级向下兼容低等级的全部字段
  - S1：基础身份、主页、粉丝或订阅数、联系方式存在性、最近发布时间
  - S2：在 S1 基础上增加平均播放量（avg_views）、互动率（engagement_rate）、行业、邮箱等，TikTok 有数据时可提供带货指标
  - S3：在 S2 基础上再增加受众画像（audience_female_rate / audience_country_code_list / audience_language_code_list / audience_age_id_list 等）
  - 因此 **S3 必须展示 S1 + S2 + S3 的全部实际返回字段**，它们是 S3 的子集，不可因"高等级"、"表格太宽"、"已有摘要列"而漏掉
  - Navos 用户默认走 S3，展示表格必须包含平均播放量、互动率、粉丝数/订阅数、联系方式、行业/标签、bio、最近发布时间、受众画像等全部实际返回字段
- **平台主页跳转必须保留（S1 起即返回，所有等级必须保留）**：`profile_url`（TikTok/Instagram）/ `channel_url`（YouTube）属于 S1 字段，S2/S3 同样返回
  - common profile 下，用户名、昵称列必须渲染为 `[名称][linkN]` 链接，指向该达人平台主页 URL，**不再单独设置末列"主页链接"**
  - 表格下方统一定义各 `[linkN]` 对应的完整 URL
  - **S3 场景同样必须保留可点击链接**——不可因增加了受众画像字段而挤掉或省略
- 统计信息单独列出：总匹配数、消耗积分、剩余配额、请求 ID（Navos 用户由脚本自动隐藏 service_level/credits/request_id，无需展示）
- `meta.total` 为 null 时不展示总匹配数
- **头像列渲染规则（S1 起即返回，所有等级适用）**：`avatar_url` 属于 S1 字段，全平台全等级返回
  - 表格新增独立的「头像」首列（紧随序号 # 之后），用固定方形外框承载头像：`<span style="display:inline-flex;width:40px;height:40px;overflow:hidden;border-radius:4px;vertical-align:middle;"><img src="{avatar_url}" width="40" height="40" style="width:40px;height:40px;max-width:40px;min-width:40px;object-fit:cover;object-position:center;display:block;"></span>`（外框固定、图片居中裁切，避免 Navos 表格列宽把竖图压窄）
  - 禁止裸写 `<img src="{avatar_url}" width="36" height="36">` 这类同时固定宽高但未设置 `object-fit` / 外层裁切框的格式，避免把竖图、横图头像压扁
  - 头像通过 `<img src>` 内联 avatar_url，无需单独定义引用链接；达人名链接（`[linkN]`）在表格下方列出完整 URL
  - `avatar_url` 为空或缺失时，该格留空，**禁止编造头像 URL 或放占位图**

### 达人分析润色（AI 即兴生成 + 真实数据对照）

**[必须]** 展示搜索结果表格后，不要只丢出原始数据就结束。基于返回的数据，对头部达人（前 3-5 个）给出**简短的专业分析**，帮助用户快速理解匹配价值。

润色维度参考（根据返回字段灵活组织，不必逐条罗列）：

- **推荐理由**：粉丝量/播放量/互动率等核心指标为什么值得合作
- **受众匹配**：受众国家、性别、语言分布与目标市场的契合度
- **潜在风险**：如"可能是场景号/品牌号而非个人达人"、"粉丝偏娱乐向转化弱"等
- **合作建议**：适合的内容形式（开箱/测评/植入/种草）、是否适合寄样、是否适合挂车

示例（输入数据 → 润色输出）：

```
原始数据：
  rumah.cafe | 平均播放 52,686 | MY 受众 82.4% | 女性受众 62.94% | 主语言 en 90.2% | home cafe/coffee

润色输出：
  🏆 [rumah.cafe][link1] — 最强推荐
  真实数据：粉丝 320K | 平均播放 52,686 | 互动率 6.2% | MY 受众 82.4% | 女性受众 62.94% | 主语言 en 90.2%
  推荐理由：平均播放 52,686，远高于其他账号；MY 受众 82.4%，本地转化潜力强
  受众画像：女性受众 62.94%（适合女性向产品）；主语言 en 90.2%，适合英文沟通
  内容匹配：home cafe / coffee 场景，与咖啡杯/杯具产品高度契合
  ⚠️ 风险：像 home cafe 场景号，不一定是个人达人，合作方式建议：场景植入 / 咖啡杯种草 / home cafe setup
```

注意：
- 分析必须**基于真实返回数据**，禁止编造数字或字段
- 指标缺失时不要硬编分析（如没有受众字段就说"受众数据待 S3 等级获取"）
- 语气专业简洁，不要过度营销化

### 下一步建议（搜索后主动提示）

**[必须]** 搜索结果展示完毕 + 达人分析润色后，主动给出 1-3 条下一步建议。建联建议必须按下面的确定性规则生成，不要只凭语感选择：

#### 建联建议判定规则

1. **用户表达合作/联系意图时必须给建联建议**：只要用户请求里出现或语义包含“合作 / 建联 / 联系 / 邮箱 / 发邮件 / outreach / contact / email”等意图，下一步建议里必须包含建联相关建议。
2. **邮箱数量 ≥ 2 时必须给批量建联建议**：如果搜索结果中 `email` 非空或 `has_email=true` 的达人数量大于等于 2，必须建议“批量建联这些有邮箱达人”，并说明可以先确认产品信息后生成个性化邮件。
3. **只有 1 个有邮箱时给单独建联建议**：如果只有 1 个达人 `email` 非空或 `has_email=true`，不要说“批量建联”；建议“先单独建联这个达人”，同时可建议“继续筛一批有邮箱达人后再批量建联”。
4. **没有邮箱时不要说批量建联**：如果所有结果都没有 `email` 且 `has_email` 不为 true，不要建议批量建联；改为建议“继续筛有邮箱达人 / 导出当前候选 / 基于优质账号找相似达人 lookalike”。
5. **产品信息不足时也不要省略建联**：如果满足建联条件但产品信息不足，不要跳过建联建议；应提示“补充产品名称、卖点、寄样/佣金、目标合作形式后，可以生成建联话术或批量邮件”。
6. **建联建议优先级高于导出和 lookalike**：当用户明确要合作/联系，或结果中有邮箱达人时，建联建议必须排在导出、lookalike、继续搜索之前。

#### 可选建议池

- "我可以基于这批达人做**更详细的匹配和数据解释**，比如分析哪个达人的受众最契合你的产品"
- "可以一键**批量建联**这些达人，我帮你起草个性化邮件（需要先确认你的产品信息）"
- "可以**将本次搜索结果导出为 CSV**，方便团队协作筛选"
- "可以**搜索相似达人**（lookalike），基于表现最好的账号扩大候选池"
- "可以**查找这批达人已收录的视频**，再拆解选定的视频"

先按“建联建议判定规则”决定是否建议建联，再按用户目标选取最相关的 CSV 导出、相似达人或进一步分析建议。

## Navos Output Link Rules

- If `cv_list_url` exists, never print the raw full URL in the final answer. Show it as `[在 CreatiVault 查看完整列表]({cv_list_url})`.
- These link rules only govern how links are presented; they do not relax the wide-table requirement above — the chat table must still cover every actually returned S1/S2/S3 field. Creator names in the chat table may still link to platform profiles; the CV list link must be a separate short entry after the summary.
