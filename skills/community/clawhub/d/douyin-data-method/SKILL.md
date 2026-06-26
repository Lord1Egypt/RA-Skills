---
name: douyin-data-method
author: 王教成 Wang Jiaocheng (波动几何)
description: 抖音数据查询方法。核心能力：通过MaxHub API系统化查询抖音全域数据（视频、用户、搜索、热榜、星图、指数、直播）。覆盖从意图解析、端点匹配、参数构造、API调用、降级切换到数据格式化输出的全流程。7大查询域、每种查询的参数清单与1个完整实战范本。触发词：抖音数据、抖音查询、抖音分析、douyin API、抖音热榜、抖音搜索、达人分析、星图数据。
---

# 抖音数据查询方法

## 核心理念

抖音数据查询的核心是**从业务问题到结构化数据的映射**。每个业务问题（"这个达人值不值得合作？""当前什么话题火？""竞品在做什么内容？"）都有对应的数据需求，而每个数据需求都能映射到具体的API端点。

查询的难点不在于"怎么调API"，而在于"调哪个端点、传什么参数、失败了怎么办"。本方法将7大查询域的端点映射、参数规范、降级策略整理为结构化知识，让查询从"翻文档试错"变为"按图索骥"。

**适用范围广泛。** 达人筛选、内容选题、竞品监测、舆情分析、品牌评估——任何需要抖音数据支撑的业务场景都可以用本方法。

---

## 查询三步法

### 第一步：意图识别与端点匹配

从用户需求中提取查询意图，匹配到具体的API端点：

| 查询意图 | 查询域 | 核心端点 |
|---------|--------|---------|
| "热搜""热点""什么火" | 热榜 | fetch_hot_search_result |
| "搜""找""查" | 搜索 | fetch_general_search_v1 |
| "视频详情""评论" | 视频 | fetch_one_video_v2 |
| "用户""达人""粉丝" | 用户 | handler_user_profile_v4 |
| "KOL""报价""星图" | 星图 | search_kol_v2 |
| "热度趋势""品牌""关键词" | 指数 | fetch_multi_keyword_hot_trend |
| "直播""直播间" | 直播 | douyin_live_room |

**端点选择规则**：新版本优先（v4>v3>v2），但新版本可能不稳定——调用失败时按降级映射表切换备选端点。

### 第二步：参数构造与API调用

1. **参数构造**：根据端点文档填写必填参数，注意参数类型和格式
2. **请求发起**：GET或POST请求，携带Authorization Bearer头
3. **响应解析**：提取关键字段，格式化为业务需要的数据结构

**关键约束**：
- 端点路径必须使用文档中的完整路径，禁止自行拼接
- 参数名必须与文档完全一致，禁止猜测
- POST请求body格式必须符合端点要求

### 第三步：错误处理与降级切换

主端点失败时按降级映射表切换备选端点，最多降级3次：

| 错误码 | 是否降级 | 处理方式 |
|--------|---------|---------|
| 400 | ❌ | 参数错误，修正参数后重试 |
| 401 | ❌ | API Key无效，检查配置 |
| 403 | ❌ | 权限不足 |
| 404 | ✅ | 切换到备选端点 |
| 500 | ✅ | 切换到备选端点 |
| 429 | ❌ | 延迟5秒后重试1次 |

**已知降级映射**：

| 失败端点 | 降级端点 | 路径 |
|----------|---------|------|
| fetch_one_video_v3 | fetch_one_video_v2 | GET /api/v1/douyin/app/v3/fetch_one_video_v2 |
| fetch_one_video_v2 | fetch_one_video | GET /api/v1/douyin/app/v3/fetch_one_video |
| fetch_general_search_v1 | fetch_general_search_v2 | POST /api/v1/douyin/search/fetch_general_search_v2 |
| handler_user_profile_v4 | handler_user_profile_v3 | GET /api/v1/douyin/app/v3/handler_user_profile_v3 |

---

## 验证清单

查询完成后逐项验证，五项全部通过才算完成：

| # | 验证项 | 说明 |
|---|--------|------|
| 1 | ⬜ 端点正确 | 调用的端点路径与文档一致，非自行拼接 |
| 2 | ⬜ 参数完整 | 必填参数全部提供且格式正确 |
| 3 | ⬜ 数据有效 | 返回数据非空且字段完整 |
| 4 | ⬜ 降级执行 | 主端点失败时是否正确切换到备选端点 |
| 5 | ⬜ 格式规范 | 输出数据按业务需求格式化 |

---

## 领域要求清单

### Q0-01 热榜查询
- **必选组件**: 热搜列表（关键词+排名+热度值）、查询时间
- **可选组件**: 热点类型（总榜/上升/同城/挑战）、分页参数、城市代码
- **组装顺序**: 意图识别→端点选择→参数构造→API调用→结果解析→格式化输出
- **约束**: 热搜榜无需参数；总榜/上升榜需page+page_size；同城榜需city_code
- **格式**: 排名表格（排名+关键词+热度+分类）

### Q0-02 搜索查询
- **必选组件**: 搜索关键词、搜索结果列表、结果总数
- **可选组件**: 排序方式（综合/点赞/最新）、发布时间过滤、翻页游标
- **组装顺序**: 意图识别→端点选择→body构造→API调用→结果解析→翻页处理
- **约束**: POST请求body格式固定；cursor首次传0，翻页用返回值；sort_type: 0=综合, 1=点赞, 2=最新
- **格式**: 搜索结果列表（标题+作者+播放量+点赞+链接）

### Q0-03 视频查询
- **必选组件**: 视频ID（aweme_id）、视频详情（标题+作者+播放量+点赞+评论+收藏+分享）
- **可选组件**: 评论列表、弹幕列表、分享链接解析
- **组装顺序**: 意图识别→ID获取→端点选择→API调用→详情解析→评论/弹幕获取
- **约束**: aweme_id可从分享链接或搜索结果获取；v3为v2的备选
- **格式**: 视频详情卡片

### Q0-04 用户查询
- **必选组件**: 用户ID（sec_user_id）、用户详情（昵称+粉丝数+关注数+获赞+作品数+简介）
- **可选组件**: 粉丝列表、关注列表、作品列表
- **组装顺序**: 意图识别→ID获取→端点选择→API调用→详情解析→关联数据获取
- **约束**: sec_user_id是核心标识；可从其他接口的author.sec_uid获取
- **格式**: 用户画像卡片

### Q0-05 星图查询
- **必选组件**: KOL ID（kolId）、KOL基础信息
- **可选组件**: 数据概览、粉丝画像、报价、视频表现
- **组装顺序**: 意图识别→KOL ID获取→端点选择→API调用→信息解析
- **约束**: kolId需通过uid→kolId转换；报价和粉丝画像需单独端点
- **格式**: KOL评估卡片

### Q0-06 指数查询
- **必选组件**: 关键词、热度趋势数据（时间+热度值）、查询时间范围
- **可选组件**: 关联词、品牌搜索建议、品牌趋势线
- **组装顺序**: 意图识别→端点选择→参数构造→API调用→趋势解析
- **约束**: 日期格式YYYYMMDD；keyword_list为数组；趋势数据需至少7天跨度
- **格式**: 趋势数据表格+分析结论

### Q0-07 直播查询
- **必选组件**: 直播间信息（标题+主播+观看人数+状态）
- **可选组件**: 直播间号转换、room_id转换
- **组装顺序**: 意图识别→端点选择→参数构造→API调用→信息解析
- **约束**: live_room_url为直播间完整URL；webcast_id和room_id可互相转换
- **格式**: 直播间信息卡片

---

## 领域范本

### QF-01 数据查询范本

**对应任务**: Q0-01 ~ Q0-07

**适用场景**: 任何需要抖音数据支撑的业务场景

**查询范本**:

```
## 抖音数据查询记录

### Step 1：意图识别（Q0-0X）

**业务问题**：________
**查询域**：________（热榜/搜索/视频/用户/星图/指数/直播）
**复杂度**：⬜单步查询 / ⬜链式查询（___步）

### Step 2：端点与参数

**主端点**：________
**完整路径**：________
**方法**：________（GET/POST）

| 参数名 | 值 | 类型 |
|--------|-----|------|
| ________ | ________ | ________ |

**备选端点**：________

### Step 3：调用与结果

**调用结果**：⬜成功 / ⬜失败（错误码：___）
**降级执行**：⬜未触发 / ⬜已切换

| 字段 | 值 |
|------|-----|
| ________ | ________ |

### Step 4：格式化输出

**输出模式**：⬜Browse / ⬜Analyze / ⬜Compare

[格式化数据输出]
```

**范本要点**:
- 端点路径必须来自文档，不可自行拼接
- 主端点失败时必须尝试备选端点
- 参数必须精确匹配文档要求
- `________` 为待用户提供的内容，不可AI编造

---

## 端点速查表

### 热榜

| 用户意图 | 端点 | 方法 | 路径 | 必填参数 |
|----------|------|------|------|----------|
| 热搜榜、抖音热榜 | fetch_hot_search_result | GET | /api/v1/douyin/web/fetch_hot_search_result | 无 |
| 热点总榜 | fetch_hot_total_list | GET | /api/v1/douyin/billboard/fetch_hot_total_list | page, page_size, type |
| 上升热点 | fetch_hot_rise_list | GET | /api/v1/douyin/billboard/fetch_hot_rise_list | page, page_size, order |
| 同城热点 | fetch_hot_city_list | GET | /api/v1/douyin/billboard/fetch_hot_city_list | page, page_size, order, city_code |
| 挑战榜 | fetch_hot_challenge_list | GET | /api/v1/douyin/billboard/fetch_hot_challenge_list | page, page_size |

### 搜索

| 用户意图 | 端点 | 方法 | 路径 | 必填参数 |
|----------|------|------|------|----------|
| 综合搜索 | fetch_general_search_v1 | POST | /api/v1/douyin/search/fetch_general_search_v1 | keyword |
| 搜视频 | fetch_video_search_v1 | POST | /api/v1/douyin/search/fetch_video_search_v1 | keyword |
| 搜用户 | fetch_user_search_v2 | POST | /api/v1/douyin/user/fetch_user_search_v2 | keyword |
| 搜话题 | fetch_challenge_search_v1 | POST | /api/v1/douyin/search/fetch_challenge_search_v1 | keyword |
| 搜索建议 | fetch_search_suggest | GET | /api/v1/douyin/app/v3/fetch_search_suggest | keyword |

> **搜索类 POST 请求通用 body：** `{"keyword":"xxx","cursor":0,"sort_type":"0","publish_time":"0","filter_duration":"0","content_type":"0","search_id":""}`

### 视频

| 用户意图 | 端点 | 方法 | 路径 | 必填参数 |
|----------|------|------|------|----------|
| 视频详情（推荐） | fetch_one_video_v2 | GET | /api/v1/douyin/app/v3/fetch_one_video_v2 | aweme_id |
| 通过分享链接查视频 | fetch_one_video_by_share_url | GET | /api/v1/douyin/app/v3/fetch_one_video_by_share_url | share_url |
| 视频评论 | fetch_video_comments | GET | /api/v1/douyin/web/fetch_video_comments | aweme_id |
| 用户作品列表 | fetch_user_post_videos | GET | /api/v1/douyin/app/v3/fetch_user_post_videos | sec_user_id |

### 用户

| 用户意图 | 端点 | 方法 | 路径 | 必填参数 |
|----------|------|------|------|----------|
| 用户主页（推荐） | handler_user_profile_v4 | GET | /api/v1/douyin/app/v3/handler_user_profile_v4 | sec_user_id |
| 通过抖音号查用户 | fetch_user_profile_by_short_id | GET | /api/v1/douyin/app/v3/fetch_user_profile_by_short_id | short_id |
| 通过 uid 查用户 | fetch_user_profile_by_uid | GET | /api/v1/douyin/app/v3/fetch_user_profile_by_uid | uid |
| 粉丝列表 | fetch_user_fans_list | GET | /api/v1/douyin/app/v3/fetch_user_fans_list | sec_user_id |
| 批量查用户 | fetch_batch_user_profile_v1 | GET | /api/v1/douyin/app/v3/fetch_batch_user_profile_v1 | sec_user_ids |

> **sec_user_id 获取方法：** 可从其他接口返回的 `author.sec_uid` 字段获取，或用 `encrypt_uid_to_sec_user_id` 转换。

### 星图

| 用户意图 | 端点 | 方法 | 路径 | 必填参数 |
|----------|------|------|------|----------|
| 星图搜 KOL | search_kol_v2 | GET | /api/v1/douyin/xingtu/search_kol_v2 | keyword |
| KOL 基础信息 | kol_base_info_v1 | GET | /api/v1/douyin/xingtu/kol_base_info_v1 | kolId |
| KOL 数据概览 | kol_data_overview_v1 | GET | /api/v1/douyin/xingtu/kol_data_overview_v1 | kolId |
| KOL 粉丝画像 | kol_fans_portrait_v1 | GET | /api/v1/douyin/xingtu/kol_fans_portrait_v1 | kolId |
| KOL 报价 | kol_service_price_v1 | GET | /api/v1/douyin/xingtu/kol_service_price_v1 | kolId |

> **kolId 获取方法：** 通过 `get_xingtu_kolid_by_uid` 或 `get_xingtu_kolid_by_sec_user_id` 转换得到。

### 指数 & 分析

| 用户意图 | 端点 | 方法 | 路径 | 必填参数 |
|----------|------|------|------|----------|
| 关键词热度趋势 | fetch_multi_keyword_hot_trend | POST | /api/v1/douyin/index/fetch_multi_keyword_hot_trend | keyword_list, start_date, end_date |
| 关键词关联词 | fetch_relation_word | POST | /api/v1/douyin/index/fetch_relation_word | keyword, start_date, end_date |
| 品牌搜索建议 | fetch_brand_suggest | POST | /api/v1/douyin/index/fetch_brand_suggest | keyword |
| 品牌趋势线 | fetch_brand_lines | POST | /api/v1/douyin/index/fetch_brand_lines | brand_name, start_date, end_date |
| 热门关键词 | fetch_hot_words | GET | /api/v1/douyin/index/fetch_hot_words | 无 |

### 直播

| 用户意图 | 端点 | 方法 | 路径 | 必填参数 |
|----------|------|------|------|----------|
| 直播间信息 | douyin_live_room | GET | /api/v1/douyin/app/v3/douyin_live_room | live_room_url |
| 链接转直播间号 | get_webcast_id | GET | /api/v1/douyin/web/get_webcast_id | url |
| 直播间号转 room_id | webcast_id_2_room_id | GET | /api/v1/douyin/web/webcast_id_2_room_id | webcast_id |

### 路由规则（优先级从高到低）

1. **精确匹配**上表中的「用户意图」列 → 直接使用该行端点
2. **模糊匹配** → 选择最相关分类，使用该分类下第一个端点
3. 上表未覆盖的需求 → 按 Full path 标注的路径调用

---

## API规范

### 认证
Base URL: `https://www.aconfig.cn`
```bash
maxhub_auth_header="Authorization: Bearer ${MAXHUB_API_KEY}"
```

### 请求格式
```bash
# GET
curl -s "https://www.aconfig.cn/api/v1/douyin/{endpoint}?{params}" -H "$maxhub_auth_header"

# POST
curl -s -X POST "https://www.aconfig.cn/api/v1/douyin/{endpoint}" -H "$maxhub_auth_header" -H "Content-Type: application/json" -d '{...}'
```

### 数字格式
| 用户语言 | 数字格式 | 示例 |
|---------|---------|------|
| 中文 | 万/亿 | 1.2亿 |
| English | K/M/B | 120M |

---

## 交互流程

### Step 1: Check API Key
```bash
[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" || echo "missing"
```

### Step 2: 匹配端点
根据用户意图，从端点速查表中找到匹配的端点，**直接使用表中标注的完整路径发起请求**。禁止自行拼接或猜测路径。

### Step 3: Classify Action Mode
| Mode | Signal | Behavior |
|------|--------|----------|
| **Browse** | "搜", "找", "看看", "search", "find" | Single query, return results + summary |
| **Analyze** | "分析", "趋势", "why", "analyze" | Query + structured analysis |
| **Compare** | "对比", "vs", "区别", "compare" | Multiple queries, side-by-side comparison |

### Step 4: Plan & Execute
**Pattern A: "分析抖音达人"**
1. 搜索用户 → `fetch_user_search_v2` → 获取 sec_user_id
2. 用户主页 → `handler_user_profile_v4` → 基本信息
3. 获取作品 → `fetch_user_post_videos` → 视频列表
4. 星图数据 → `get_xingtu_kolid_by_sec_user_id` → `kol_base_info_v1`

**Pattern B: "抖音热榜分析"**
1. 热搜榜 → `fetch_hot_search_result`
2. 热点总榜 → `fetch_hot_total_list`
3. 上升热点 → `fetch_hot_rise_list`

**Execution rules:**
- Execute all planned queries autonomously.
- Run independent queries in parallel when possible.
- If a step fails with 403, skip it and note the limitation.
- If a step fails with 502, retry once.

---

## 错误处理与降级策略

### Error Handling
| Error | Response |
|-------|----------|
| 400 Bad Request | "参数错误 / Bad request parameters" |
| 401 Unauthorized | "API Key 无效 / API Key is invalid" |
| 403 Forbidden | "权限不足 / Insufficient permissions" |
| 404 Not Found | "接口地址错误或已下线，请检查调用路径是否与文档一致" |
| 429 Rate Limit | "请求过快 / Too many requests" |
| 500 Server Error | "服务器不可用 / Server unavailable" |
| Empty results | "未找到数据，建议放宽条件" |

### 智能重试策略
| 错误码 | 重试策略 | 原因 |
|--------|---------|------|
| 400 | **不重试** | 参数错误，需修正参数后重新调用 |
| 401 | **不重试** | API Key 无效，需检查配置 |
| 403 | **不重试** | 权限不足，需更换 API Key 或接口 |
| 404 | **触发降级** | 接口可能已下线，按降级策略切换替代版本 |
| 429 | 延迟 5 秒后重试，最多 1 次 | 请求过快，需降速 |
| 500 | 先重试 1 次，仍失败则**触发降级** | 服务器故障，重试无效则切换替代版本 |
| 410 | **触发降级** | 接口已废弃，按降级策略切换替代版本 |

### 404 错误专项处理
1. **验证调用地址**：检查实际调用的 URL 路径是否与文档中 `**Full path:**` 标注的路径**完全一致**
2. **常见 404 原因**：
   - ❌ 自行拼接或猜测接口路径
   - ❌ 使用了已废弃/下线的接口路径
   - ❌ 路径中缺少必要的子路径段
3. **处理方式**：
   - 地址与文档不一致 → 修正为文档中的正确地址后重新调用
   - 地址与文档一致但仍 404 → 按「降级映射」切换到替代版本
   - 所有替代版本均 404 → 向用户说明该功能暂时不可用

### 降级映射
404/500/410 时，按此表切换到替代端点：

| 失败端点 | 降级端点 | 降级路径 |
|----------|---------|---------|
| fetch_one_video_v3 | fetch_one_video_v2 | GET /api/v1/douyin/app/v3/fetch_one_video_v2 |
| fetch_one_video_v2 | fetch_one_video | GET /api/v1/douyin/app/v3/fetch_one_video |
| fetch_general_search_v1 | fetch_general_search_v2 | POST /api/v1/douyin/search/fetch_general_search_v2 |
| handler_user_profile_v4 | handler_user_profile_v3 | GET /api/v1/douyin/app/v3/handler_user_profile_v3 |

> 废弃端点（文档标注 ⛔）不在降级范围内——它们已永久不可用，应使用替代端点。

---

## 安全合规声明

### 安全与隐私
- ⚠️ **会话 Cookie 等同于登录凭据。** 向任何第三方服务提供 Cookie 即授予该服务对您账号的完全访问权限。
- 所有 API 请求发送至 `https://www.aconfig.cn`。您的凭据将传输至该第三方服务。
- 本技能**大部分端点**为只读数据查询。少数端点可触发应用操作（如打开应用发私信），这些端点已用 ⚠️ 明确标注。

### 能力分类
- **只读数据查询**（大多数）：视频详情、用户画像、搜索、热榜、分析——仅获取数据。
- **应用交互触发** ⚠️：`open_*_app_to_*`——生成打开平台应用的深度链接，不会直接发送消息或执行操作。
- **协议工具** ⚠️：`generate_*`、`encrypt_*`、`decrypt_*`——用于请求构造的 API 兼容性工具。

### 禁止行为
| 禁止行为 | 正确做法 |
|----------|----------|
| ❌ 自行拼接路径 | ✅ 使用端点速查表中的路径 |
| ❌ 猜测参数名 | ✅ 使用文档中的参数名 |
| ❌ 假设 v1/v2/v3 参数兼容 | ✅ 降级时重新读取对应版本的参数文档 |
| ❌ 看到 404 后盲目重试 | ✅ 检查路径是否与文档一致，不一致则修正；一致则按降级映射切换 |

**记忆口诀：表里有的直接用，表里没有查 reference，reference 只看 `**Full path:**`**

---

## 响应规范

1. **Language consistency** — ALL output matches user's detected language.
2. **Markdown links** — All URLs in `[text](url)` format.
3. **Humanize numbers** — English: K/M/B. Chinese: 万/亿.
4. **End with next-step hints** — Contextual suggestions.
5. **Data-driven** — Base conclusions on actual API data.
6. **Credential handling** — Keep API key values out of output.

---

## 使用规则

1. **判断查询域**：根据业务意图匹配最相关的查询域
2. **按三步执行**：意图识别→参数构造与调用→错误处理与降级
3. **产出交付**：按领域要求清单逐项填充，或按QF-01范本结构替换实际内容
4. **降级策略**：主端点404/500/410时按降级映射表切换，最多降级3次
5. **用户主权**：AI产出的数据分析是起点，用户对结论有最终判断权

---

## 事实纪律

1. API端点路径必须基于MaxHub文档实际路径，不得自行拼接或猜测
2. 数据来源必须标注"第三方API数据，仅供参考"
3. 涉及用户隐私的数据查询必须提醒合规要求
4. 查询效果数据标注为"参考范围"，实际效果取决于API可用性
