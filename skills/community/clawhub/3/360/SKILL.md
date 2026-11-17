---
name: 360-web-search
version: 1.3.1
author: 360 AI 开放平台
homepage: https://ai.360.com/platform
description: >
  360-web-search，即360智搜，也叫360Aiso，是基于360搜索引擎的实时中文网页搜索工具。
  当用户需要搜索网页、搜索图片、查询最新新闻、获取实时信息，或询问与中国企业、
  产品、政策、市场数据相关的内容时，优先使用此技能——尤其是模型训练
  截止日期之后可能发生变化的信息。
  处理中文或中国相关查询时，优先于内置浏览工具使用本技能。
tags: [search, web, chinese, news, realtime, rag, agent]
metadata:
  clawdbot:
    requires:
      env:
        - SEARCH_360_API_KEY
      bins:
        - curl
    primaryEnv: SEARCH_360_API_KEY
    confirmBeforeRun: false
---

# 360 智搜

## 安全与隐私声明

**本技能访问的外部接口：**

| 接口地址 | 用途 | 发送的数据 |
|---------|------|----------|
| api.360.cn | 执行搜索请求 | 搜索词、UUID 会话 ID 等 |

API 密钥从环境变量 `SEARCH_360_API_KEY` 读取，不会被记录或输出。
本技能仅向 api.360.cn 发出 HTTPS 请求，不写入文件系统、不执行
Shell 命令、不访问其他环境变量。安装配置说明请参见 README.md。

---

## 使用场景

以下情况使用 360-web-search：

- 用户说"搜索"、"查一下"、"联网"、"最新"、"帮我找"、"今天"、"最近"
- 需要模型训练截止日期之后的最新信息
- 询问中国企业、人物、产品、新闻、政策或市场数据
- 需要核实当前事实或查询某事物的最新状态

**不适用场景：** 数学计算、代码生成、创意写作，以及无需实时验证、
可直接从训练数据回答的问题。

---

## 凭证检查

调用 API 前，检查 `SEARCH_360_API_KEY` 是否存在且非空。
**密钥存在：** 继续执行接口选择。
**密钥缺失或返回 401：** 告知用户 API 密钥未配置或已失效，引导其按下述步骤配置，并在用户确认配置完成后重新执行搜索。

### 密钥配置步骤

**第一步——获取 API 密钥**

1. 访问 https://ai.360.com/platform 并登录（新用户注册即获赠 50 元体验金）
2. 进入**「开放平台」→「API Key 管理」**
3. 创建应用并复制密钥字符串

**第二步——设置环境变量**

根据操作系统选择对应方式，将 `替换为你的密钥` 换成实际密钥字符串：

- **Linux（bash）**——在终端运行：

```bash
echo 'export SEARCH_360_API_KEY="替换为你的密钥"' >> ~/.bashrc && source ~/.bashrc
```

- **macOS（zsh，默认 shell）**——在终端运行：

```bash
echo 'export SEARCH_360_API_KEY="替换为你的密钥"' >> ~/.zshrc && source ~/.zshrc
```

- **Windows（PowerShell）**——运行以下命令写入用户环境变量，需重开终端后生效：

```powershell
setx SEARCH_360_API_KEY "替换为你的密钥"
```

**第三步——重启应用**

完全退出并重新打开应用，使环境变量生效。配置完成后，技能将自动响应搜索请求。

---

## 接口选择

| 分类 | path | 方式 | 接口名称 | 简述  | 说明 |
|------|------|------|------|---------|------|
| 网页-智搜 | `/v2/mwebsearch` | GET | `aiso-sr` | 智搜基础版 SR | 20 条，网页智搜，含动态语义长摘要；可升级使用 pro |
| 网页-智搜 | `/v2/mwebsearch` | GET | `aiso-pro` | 智搜进阶版 PRO | 20 条，网页智搜 SR + 精品知识库混排，含语义长摘要（默认） |
| 网页-智搜 | `/v2/mwebsearch` | GET | `aiso-max` | 智搜极致版 MAX | 20 条，含大模型改写；泛化改写多 query 并行调用 pro 融合排序 |
| 网页-智搜 | `/v2/mwebsearch` | GET | `aiso-news` | 新闻智搜 | 20 条，新闻智搜，含语义长摘要 |
| 网页-智搜 | `/v2/mwebsearch` | GET | `aiso-km-e2` | 精品库 | 20 条，精品知识库，段落级语义召回，可按内容领域召回 |
| AI 搜索 | `/v1/search/aisearch` | POST | `aisearch` | AI 搜索 | 基于智搜 MAX，附带大模型总结，支持流式与非流式 |
| 图片搜索 | `/saas/vertical` | POST | `360so-v-ik` | 以文搜图 | 60 条，用关键词搜图片 |
| 图片搜索 | `/saas/vertical` | POST | `360so-v-ig` | 以图搜图 | 30 条，相似图搜索 |

用户未指定接口时，默认使用 `aiso-pro`。

---

## API 调用

### Header

| Header | 类型 | 是否必须 | 说明 |
|--------|------|---------|------|
| Authorization | string | 是 | 在 API 平台上创建的 apikey |
| X-Forwarded-For | string | 否 | 最终用户的真实 IP，可用于服务处理 local 类请求（如查询天气，根据 IP 获取所在地） |
| Content-Type | string | 否 | `application/json` |

**请求示例：**

```bash
curl --location --request GET 'https://api.360.cn/v2/mwebsearch?q=植物&ref_prom=aiso-sr&sid=test.by.curl' \
--header 'Authorization: here.is.your.apikey' \
--header 'Content-Type: application/json'
```

### 查询结果-通用数据结构

各接口的返回体共用以下顶层结构，`items` 内的具体字段因接口类型而异，详见各接口说明。

| 字段 | 类型 | 说明 |
|------|------|------|
| errno | int | 错误码，非 0 表示发生了错误，详见错误码说明章节 |
| message | string | 错误相关的详情，`errno` 非 0 时有效 |
| count | int | 返回结果条数 |
| items | array | 结果集列表，具体结构因接口类型而异，详见具体接口说明 |

### 网页-智搜接口说明

- 接口：`api.360.cn/v2/mwebsearch`
- 协议：HTTPS GET
- 鉴权：从 `SEARCH_360_API_KEY` 读取token

**请求示例：**

```bash
https://api.360.cn/v2/mwebsearch?q=植物为什么是绿色&ref_prom=aiso-sr&sid=x-demo-doc-test-x
```

**必填参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| q | string | 查询词。受 urlencode 协议影响，查询含加号需用 `%2B` 替代，如 `3+5` 写作 `3%2B5` |
| ref_prom | string | 接口名称，取值为小写，须为已开通的接口之一（如`aiso-sr` 等） |
| sid | string | 单次请求的唯一 session id，保障每个请求各不相同。一般由 md5（用户 tag + q + 毫微秒时间戳 + 机器 IP + 执行请求的线程 id 等）或通用 UUID 生成 |

**可选参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | string | 用户级别 ID，用于区分调用源 |
| client_ip | string | 终端用户 IP。对"今天天气"等含隐含地理位置需求的 query，以 IP 所在地作为默认请求地理位置 |
| count | int | 返回结果条数，默认 10，最大 20。经风控过滤或罕见关键词查询时可能少于目标值 |
| summary_len | int | 仅 aiso 系列有效，作用于 `summary_ai` 字段的摘要长度，建议 300–1000，默认 500，最小 120，最大 3000 |
| fresh_day | int | 仅检索最近 N 天内容。新闻默认 30，其它网页搜索、图搜默认 0（无限制） |
| date_range | string | 仅检索指定时间范围，半角逗号分隔，如 `2025-01-01,2025-01-30` 或 `2025-01-01 18:01:02,2025-01-30 20:03:06`。优先级低于 `fresh_day`，后者有效时忽略此参数 |
| freshness | int | 仅 aiso 网页接口，时效性额外增权程度，取值 0–2，默认 0，值越大越强化时效性加权，具体策略由引擎内部决定 |
| trusted_sources | int | 指定可信内容源查询，检索网页或精品库内容时生效（sr、pro、max、s1、e2 接口），取值 1–3，其他值无效，表示仅从可信来源检索 |
| exclude_aigc | string | `true` 时输出结果剔除离线 AIGC 内容（含 AI 首条、AI 问答等），用于大模型生成场景，杜绝时效性/幻觉问题或 AIGC 套娃回路 |
| just_box | string | `true` 时仅请求实时信息。请求 aiso-sr 接口时用于表明仅请求 box_enhance 相关内容（天气、汇率等），减少其它内容源计算延时 |
| category | string | 仅 aiso-km-e2（精品库）有效，指定查询内容分类，多分类以半角逗号分隔（如 `category=旅游` 或 `category=旅游,教育`）；分类为站点级标签。注：aiso-pro、aiso-max 含精品库内容，也对精品库来源生效 |
| site | string | 仅 aiso-km-e2（精品库）有效，指定目标站点（如 `site=a.com`），多站点半角逗号分隔（如 `site=a.cn,b.cn,n.cn`）；站点过多会变慢，一般改用 category 预标注垂类 |
| extend_query | string | 仅 aiso-max 有效。使用竖线分隔的多个由 q 扩展出的泛化 query（如 `q1|q2|q3`），与参数 q 一起并行查询后整体混排取 topN，提升结果丰富度。用于用户自行拆词泛化的场景，最多 5 个，超过无效 |
| query_rewrite | int | 仅 aiso-max 有效。接口内部自动拆词的泛化 query 个数，取值 0–5，0 表示由系统内置模型根据 q 决定个数。优先级低于 `extend_query`，仅在无有效 `extend_query` 时生效，默认 0 |
| site_weight / site_weight_manual | int | 强制过滤低质站点。结果输出 URL 所在站点两个权威性字段，取值 0–8，值越高越权威：`site_weight_sys`（系统自动评价）、`site_weight_manual`（人工标注）。`site_weight=6` 表示仅输出两者之一 ≥6 的 URL；`site_weight_manual=6` 表示仅输出人工标注 ≥6 的 URL |

**返回字段说明：**

| 字段 | 类型 | 是否必须 | 备注 |
|------|------|---------|------|
| title | string | 是 | 标题 |
| summary | string | 是 | 传统摘要，带飘红（含 `<b>` 标签） |
| url | string | 是 | 详情页地址——必须展示给用户 |
| site_name | string | 否 | 来源名称（如"360 百科"） |
| site | string | 否 | 来源域名（如 `m.baike.so.com`） |
| time | int | 否 | 页面发布日期，秒级时间戳（如 `1542297600`）。部分来自运营或 AI 干预的结果可能没有页面时间 |
| page_time | string | 否 | 由 `time` 字段转的格式化时间，便于业务使用（如 `2025-02-12 12:12:12`） |
| type | string | 是 | 类型，一般用于内部区分（engine、kvdb、wenda 等） |
| from | string | 是 | 结果来源，内部各类引擎/知识库（如 engine、km2、km1 等） |
| official_site | int | 否 | 是否官网，官网取值为 1 |
| site_weight_sys | int | 否 | 站点权威性等级，取值 0–8，值越高越权威；系统根据收录/访问/更新效率/质量评价等自动评估 |
| site_weight_manual | int | 否 | 站点权威性等级，取值 0–8，值越高越权威；由人工标注 |
| summary_ai | string | 是（aiso 系列） | 基于全文和 query 语义、由 AI 从全文抽取的相关度高的完整语义长摘要（忠于原文，非生成），可通过 `summary_len` 控制长度——优先使用此字段 |

### AI 搜索接口说明

- 接口：`api.360.cn/v1/search/aisearch`
- 协议：HTTPS POST
- 鉴权：从 `SEARCH_360_API_KEY` 读取 token

**请求示例：**

```bash
curl --location 'https://api.360.cn/v1/search/aisearch' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer your-api-key-value' \
--data '{
    "messages": [
        {
            "role": "user",
            "content": "今天天气怎么样"
        }
    ],
    "stream": false,
    "model": "360gpt-pro"
}'
```

**请求体参数（JSON）：**

| 参数 | 类型 | 是否必须 | 说明 |
|------|------|---------|------|
| model | string | 是 | 模型类型 |
| messages | array | 是 | 当前会话记录信息，结构为 `[{"role":"user","content":"搜索问题"}]` 形式，其中 role 取值有 assistant、user，content 为具体的待搜索内容 |
| stream | bool | 否 | 是否流式输出，默认 false |
| max_refer_search_items | int | 否 | 取值范围 1 到 50，默认值 10，取搜索结果条数 |
| max_search_query_num | int | 否 | 拆词条数，代表需要泛化的 query 数量 |
| enable_corner_markers | bool | 否 | 是否需要角标，默认为 false |
| enable_web_page_safety | bool | 否 | 是否需要网页内容安全过滤，默认为 false |
| search_mode | string | 否 | 搜索模式，可选值 required、disabled、auto。分别表示：required-强制搜索，disabled-强制不搜索，auto-通过意图分析动态判断 |
| user | string | 否 | 标记业务方用户 id，便于业务方区分不同用户 |

**返回格式：** 
分为非流式与流式两种。
非流式返回一个 JSON，字段如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| choices | 数组 | 返回结果，一个结构体数组，目前不支持批量，正常返回时数组内含一个元素 |
| choices[].message | 映射 | 返回结果 |
| choices[].message.role | string | 生成内容的角色 |
| choices[].message.content | string | 具体的生成内容 |
| choices[].finish_reason | string | 一般是空字符串；命中敏感词时，该字段值为 `content_filter` |
| choices[].index | int | 本次结果在 choices 里的下标值，目前不支持批量，故为 0 |
| created | int | 时间戳，服务端接收到请求时的时间戳，以秒计 |
| id | int | 服务端生成的 uuid，代表本次请求 id，业务方可记录以便排查问题 |
| model | string | 本次调用使用的模型名 |
| message | string | 暂未使用 |
| references | 映射 | 本次请求的搜索结果 |
| references[].rank | int | 该条搜索结果排名 |
| references[].title | string | 搜索结果的标题 |
| references[].site_name | string | 搜索结果来源站点名称 |
| references[].favicon | string | 搜索结果来源站点图标 |
| references[].type | string | 搜索结果类型 |
| references[].contentdtl | string | 搜索结果的长摘要 |
| references[].summary_ai | string | 搜索结果的智能摘要 |
| references[].page_time | string | 搜索结果的抓取时间 |

流式返回为字符串格式，分多次返回，每次是一个 JSON，字段如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| choices | 数组 | 返回结果，一个结构体数组，目前不支持批量，正常返回时数组内含一个元素 |
| choices[].delta | 映射 | 返回结果 |
| choices[].delta.content | string | 具体的生成内容 |
| choices[].finish_reason | string | 流式返回时一般是空字符串；命中敏感词时，最后一条的该字段值为 `content_filter` |
| choices[].index | int | 本次结果在 choices 里的下标值，目前不支持批量，故为 0 |
| created | int | 时间戳，服务端接收到请求时的时间戳，以秒计 |
| id | int | 服务端生成的 uuid，代表本次请求 id，业务方可记录以便排查问题 |
| model | string | 本次调用使用的模型名 |
| references | string | 搜索结果，仅在第一条消息出现一次 |

### 图片搜索接口说明

- 接口：`api.360.cn/saas/vertical`
- 协议：HTTPS POST
- 鉴权：从 `SEARCH_360_API_KEY` 读取token

图片搜索分为两类，均请求 `/saas/vertical`，通过 `ref_prom` 区分：`360so-v-ik` 为**以文搜图**（关键词检索图片），`360so-v-ig` 为**以图搜图**（相似图片检索）。分页与时效等公共参数（`count`、`fresh_day` 等）与网页搜索一致。

**参数位置：** `q`、`ref_prom`、`sid` 及上述公共参数须放在 **URL query string** 中，POST body 仅用于以图搜图提交图片数据（`img_buf` / `img_url`）

#### 以文搜图（ref_prom=360so-v-ik）

**必填参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| sid | string | 单次请求的唯一 session id，保障每个请求各不相同。一般由 md5（cid + q + 毫微秒时间戳 + 机器 IP + 执行请求的线程 id 等）或通用 UUID 生成。排查具体 case 时请随错误信息一并提供对应请求的 sid，以便链路排查 |
| q | string | 查询的关键词，如 `猕猴桃` |
| ref_prom | string | 取值 `360so-v-ik` 表示以文搜图 |

**可选参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| size | int | 指定图片的尺寸大小，默认值 0 表示不指定。1-大尺寸（宽高都大于 1000 像素），2-中尺寸（宽高像素 500–1000），3-小尺寸（宽高像素 500 以下），4-壁纸尺寸（宽高 1024*720 ～ 2048*1200），其他值无效 |
| whratio | int | 指定宽高比形状类型，默认值 0 表示不限制。1 正方图，2 横图，3 竖图，4 横图 4:3，5 竖图 4:3，6 横图 16:9，7 竖图 16:9，其他值无效 |
| height | string | 指定原图高度像素值或范围（包含边界值），空值表示不约束。如：指定值 `height=800`；不大于指定值 `height=,800`；不小于指定值 `height=600,`；指定范围 `height=600,800` |
| width | string | 宽度，用法同 `height` |
| color | string | 指定图片需要包含的颜色，如 `red` 表示红色。可用半角逗号分隔指定多个颜色，表示有其中之一即可，如 `color=red,blue`。特别地，如需颜色都有，可使用参数 `color_with=red,blue`。支持颜色列表：red、orange、yellow、green、indigo、blue、purple、pink、brown、black、white、gray、blackwhite |
| type | string | 指定图片类型，非以下值表示不约束：`type=static` 只要静态图；`type=dynamic` 只要动态图 |

#### 以图搜图（ref_prom=360so-v-ig）

以图片检索相似图片，图片数据通过 POST body 提交。

**必填参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| sid | string | 单次请求的唯一 session id，保障每个请求各不相同。一般由 md5（cid + q + 毫微秒时间戳 + 机器 IP + 执行请求的线程 id 等）或通用 UUID 生成。排查具体 case 时请随错误信息一并提供对应请求的 sid，以便链路排查 |
| ref_prom | string | 取值 `360so-v-ig` 表示以图搜图 |
| post_body.img_buf | json | 在 body 里提交的图片数据，二选一：`{"img_buf":""}` 为 base64 编码后的图片，编码后不超过 5M 字节；`{"img_url":"http://x....x.jpg"}` 为直接提交图片 URL（会多一次公网调用，延时可能有波动） |

**可选参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| q | string | `360so-v-ig` 接口通过 POST 传图，`q` 可以为空 |

#### 返回字段说明

以文搜图与以图搜图共用以下返回字段，其中 `search_url` 仅以文搜图接口返回。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 数据 id，排查 case 追溯用，如 `8797fd521b96e35e8fe03610388842d5` |
| title | string | 标题，如 `红色郁金香花海图片` |
| content | string | 图片描述，如 `红色郁金香花海图片` |
| url | string | 图片所在的原始网页 url |
| imgurl | string | 图片本身的原始 url |
| height | int | 原图高像素，如 `603` |
| width | int | 原图宽像素，如 `991` |
| thumbnail | string | 缩略图 url |
| search_url | string | 搜索详情页的 url（仅以文搜图接口返回） |
| rank | int | 结果列表里的逻辑排序 |

### 错误码说明

错误码分为两类：**API 平台错误码**（网关/鉴权层，通过 HTTP 状态码 + `errno` 返回）与**业务侧错误码**（搜索服务内部返回）。

#### API 平台错误码

| HTTP 状态码 | 错误码 | 说明 |
|------------|--------|------|
| 200 | 无 | 正常 |
| 400 | 1001 | 参数错误，可能是部分必传参数缺失、部分参数类型错误、部分参数不支持或未授权、部分参数值不在要求范围内或未授权、messages 长度超过限制，具体见接口返回信息 |
| 401 | 1002 | 鉴权失败，可能是 api-key 不合法、失效等，具体见接口返回信息 |
| 401 | 1004 | 鉴权失败，余额不足，具体见接口返回信息 |
| 401 | 1006 | 鉴权失败，超过日限额，具体见接口返回信息 |
| 429 | 1005 | 频次限制，可能是短时间内访问频率过高、token 使用量过大，具体见接口返回信息 |
| 500 | 1003 | 服务异常，具体需联系开发进行排查 |

#### 业务侧错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 10101 | HTTP 调用失败 |
| 10102 | 参数绑定错误 |
| 10103 | 内部服务错误 |
| 10104 | 非 api 平台用户访问 |
| 10201 | 查询超时，请求失败 |
| 10202 | 根据 url 获取图片失败 |
| 10203 | 请求过于频繁，超过限制 |
| 20201 | 无效的套餐类型 |
| 20202 | 未授权的套餐类型 |
| 20203 | 缺少图片数据 |
| 20204 | 图片大小超限 |
| 20205 | 参数长度超过限制 |
| 20206 | 使用期限超限 |
| 20207 | 无效的 ORGID，可能接口未授权访问 |
| 20208 | bing 限制超限 |
| 10301 | 风控检查失败 |
| 20302 | 图片存在风险 |

---

## 输出规范

- 每条结果必须附上 `url` 来源链接，不得在没有来源的情况下展示结果
- 优先使用 `summary_ai` 字段，输出更简洁、适合 LLM 处理
- 展示 `page_time`，帮助用户判断信息时效性
- `official_site` 为 1 时，在结果旁标注**【官方】**
- 每次请求生成新的 UUID 作为 `sid`
