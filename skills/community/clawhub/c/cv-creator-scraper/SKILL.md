---
name: creator-scraper-cv
description: |
  CreatiVault creator discovery, content analysis, and outreach. Use the local OpenAPI
  scripts first for creator search, exact lookup by profile URL or ID, similar creators,
  video search, brand collaboration discovery and video insights, CSV export of search
  results, short-video script audit, fake-follower risk, and email outreach or follow-up.
  Creator and video search cover TikTok, Instagram, and YouTube. Look up indexed brand
  collaborations on TikTok and Instagram. Audit published short videos or local uploads,
  and send outreach to X/Twitter creators when the creator ID and email are known.
  找达人 / KOL / 带货网红，按地区、行业、粉丝、互动、邮箱或受众筛选，按主页或 ID 查已有达人，
  找相似达人、查品牌合作达人与相关视频、导出搜索结果 CSV、拆解短视频、假粉检测、发合作邮件和查待办。
  使用 CreatiVault OpenAPI 查询数据，用户明确要求或同意后才用公开网页补充。
compatibility: Node.js 20.6+
metadata:
  author: creativault
  version: "1.9.8"
---

# Creativault Creator Ecosystem

## 强制执行边界

当用户要查找达人或视频、导出达人搜索结果、分析短视频或账号风险、邮件建联或跟进时，优先使用本 Skill 与 CreatiVault OpenAPI。达人和普通视频搜索覆盖 TikTok、Instagram、YouTube。各能力按下面的路由选择。

**不要默认退化到 web search。** Web search 只能用于以下情况：

1. 用户明确要求“用网页搜索 / Google / 公开网页查找”。
2. CreatiVault OpenAPI 返回无数据、平台不支持或接口不可用，并且你已经告知用户原因，用户确认允许用公开网页兜底。
3. 用户要查询的是非达人数据，例如新闻、官网文档、实时政策或与 CreatiVault 数据库无关的信息。

如果 `CV_API_KEY`、`CV_USER_IDENTITY` 或网络/API 配置缺失，应先提示用户补齐配置或修复配置，不要自行改用 web search。公开网页搜索结果不能替代 CreatiVault 官方达人数据，也不能用于伪造粉丝量、邮箱、互动率、受众画像、GMV 或联系方式。

## 意图路由

- 搜索或精确查询达人：加载 `discovery/creator-search/SKILL.md`。按条件筛选或批量查已收录主页、达人 ID，调用 `scripts/search_creators.mjs`。描述内容风格或合作场景时，可用 `scripts/search_creators_nl.mjs` 获取精简名单。
- 查品牌合作达人：加载 `discovery/creator-search/SKILL.md`，调用 `scripts/find_brand_collaboration_creators.mjs` 查 TikTok、Instagram 已收录的合作记录。
- 搜索视频或看品牌相关内容：加载 `discovery/video-search/SKILL.md`。按话题或达人搜索时，每次指定一个平台，调用 `scripts/search_videos.mjs`。按品牌查已有视频时，调用 `scripts/search_brand_video_insights.mjs`，可指定一个或多个平台。
- 找相似达人：加载 `discovery/creator-lookalike/SKILL.md`，调用 `scripts/find_lookalike.mjs`。
- 导出本次达人搜索结果：按 `discovery/creator-search/SKILL.md` 使用 `scripts/export_to_csv.mjs` 将已返回的名单写为 CSV。
- 邮件建联/批量建联/跟进：加载 `outreach/creator-outreach/SKILL.md`。
- 达人假粉/互动真实性/账号风险检测：加载 `audit/fake-follower-audit/SKILL.md`，调用 `scripts/fake_follower_audit.mjs`（同步单达人检测）。
- 单条视频拆解/审核/评分：加载 `audit/video-script-audit/SKILL.md`，调用 `scripts/video_audit_submit.mjs` + `video_audit_poll.mjs`（异步任务）。
- 找达人并建联，或从视频搜索、拆解再到达人建联：加载 `workflow/SKILL.md`，按用户目标组合相应步骤。

执行前应把用户自然语言目标转成 CreatiVault OpenAPI 参数；用户已给出明确条件时，直接调用脚本，不要先去网页搜索。

若用户明确要发起采集任务或查旧任务，说明该入口已下线。用户希望补全已有名单时，可以确认平台后按主页或达人 ID 查询已收录数据。

## Brief 澄清与过程输出质量

按条件找新达人前，确认平台、目标市场和内容方向。按主页或 ID 精确查询时，只需确认目标平台及标识列表，地区和行业等条件按用户需要叠加。

澄清规则：

1. 用户未指定平台时，必须先问平台；可给出选项：TikTok / Instagram / YouTube。不要默认选择 Instagram、TikTok 或任一平台。
2. 用户未说明目标市场/国家地区时，先问目标地区；不要把“海外”“欧美”“东南亚”之外的范围自行细分到国家，除非用户已经表达清楚。
3. 用户未说明品类、行业、关键词、产品或竞品品牌时，先问业务方向；不要用泛化词直接搜索。
4. 按条件找达人时，用户未说明数量可默认请求 20 条。已有标识列表按拟查询的条数请求，每页最多 100 条。
5. 用户已给出平台、地区、品类和数量时，可以直接执行；不要反复询问服务等级。Navos profile 默认按 S3 返回，common profile 按用户指定或默认策略执行。
6. 澄清问题一次最多 3 个，优先问缺失的关键项。不要把所有可选筛选条件一次性列成长问卷。

过程输出规则：

1. 面向用户只输出业务语言，不输出内部实现细节。禁止展示 OpenAPI 参数 JSON、字段名清单、endpoint、`page`、`size`、`service_level`、`meta`、`request_id`、`recall_type`、“规则 4/规则 7”等内部词，除非用户明确要求排查或查看技术细节。
2. 搜索前过程说明最多 2 句话，只说明将按哪些业务条件严格匹配，以及不会自动跨平台/翻页/放宽条件。
3. 不要前后矛盾：如果说“先澄清”，就不要同时执行搜索；如果说“直接搜索”，就不要再展示推理过程或参数推导。
4. 结果不足时只说清楚“严格命中 N 个”，再给 2-3 个放宽方向；不要把不满足条件的候选包装成结果。
5. Navos 场景下，最终回复优先包含：一句结果摘要、一张结果表、1-3 条业务判断、短链接入口和下一步建议。不要长篇解释计费、调用策略、字段口径或平台实现。

## 搜索预算与静默查询边界

搜索达人时必须优先保护用户的积分可预期性：

1. 必须把用户给出的筛选条件全部前置为 OpenAPI 参数，例如地区、行业、粉丝量、互动率、邮箱、语言、受众画像等；禁止先宽泛搜索一批候选，再在本地大量二次过滤。
2. 每轮默认只执行 1 次 `creator-search` 调用，且默认 `page=1`。用户未说明数量时，默认请求 20 条；用户明确要求 N 条时，本次请求 `size=min(N,100)`。生产接口单页上限为 100，禁止传递大于 100 的 `size`。
3. 用户未指定平台时，必须先做 brief 澄清平台；禁止默认选择平台，也禁止为了凑满数量自动跨平台搜索。
4. 若用户要求数量超过 100，本次只返回第一页最多 100 条，并说明仍需继续分页才能获取更多结果；必须先征得确认，禁止自动翻页。若严格条件返回 0 条，或返回结果不足用户要求数量，必须停止并说明当前严格命中数量；禁止自动跨平台补数、放宽条件、改用关键词兜底或改用视频搜索。
5. 继续翻页、跨平台、扩大结果数量、放宽条件、切换到视频搜索或使用更高服务等级前，必须先征得用户确认，并说明会产生额外查询消耗。
6. 只展示满足用户筛选条件的达人；如果接口返回数据与用户条件明显不一致，停止并提示可能是字段口径或传参问题，建议用户放宽条件或确认下一步，不要展示无关结果凑数。
7. 自然语言搜索每次请求一个平台并返回最多 100 条。费用按实际响应或所在产品的计费规则说明。

## Navos S3 展示要求

Navos profile 会在结构化达人搜索脚本中自动注入 `service_level: "S3"`。S3 不只代表“更准的搜索”，也代表响应里可能包含受众画像字段。展示结构化达人搜索结果时必须把 S3 字段当作用户已付费获取的数据来呈现：

1. 不要只输出摘要表头（例如达人、国家、粉丝、均播、互动率、受众女性、主要受众国家、邮箱）。
2. 默认用一张动态宽表展示同一批达人，S1 / S2 / S3 实际返回且有值的字段都在同一张表里展开；不要再把 S3 受众画像单独拆成第二张表。表格变宽可以横向滚动，但不能因此省略受众女性、受众国家、受众语言、受众年龄等 S3 字段。
3. `avatar_url` 属于 S1 基础字段。只要接口返回 `avatar_url`，Navos 搜索结果表必须默认增加独立「头像」列，并用 40px 方形外框裁切渲染；不要只保留达人主页文字链，也不要只裸写 `<img width height>` 导致 Navos 表格把竖图压窄。头像缺失时该单元格留空，不要编造头像或占位图。
4. 字段只有在接口实际返回且至少一条结果有有效值时才展示；不要编造空缺字段。
5. Navos profile 下不再生成单个达人详情链接。`scripts/search_creators.mjs` 和 `scripts/search_creators_nl.mjs` 只补充 `cv_list_url`，用于在 Navos 内置浏览器无感登录 CreatiVault 并打开本次搜索结果快照列表；用户在 CV 原生列表中点击达人打开详情弹窗。对话区表格里的达人名/昵称仍链接到平台主页，平台主页链接必须保留为单独入口或引用链接。common profile 下不展示 CV 列表入口。`cv_list_url` 是机器入口，禁止在最终回复中原样输出完整 URL；必须展示为短 Markdown 链接：`[在 CreatiVault 查看完整列表]({cv_list_url})`。
6. Navos profile 下，建联发送、任务查询、沟通历史和待办脚本会尽量补充 `cv_outreach_url`，用于在 Navos 内置浏览器无感登录 CV 并打开建联工作台。对话区仍应展示摘要和下一步建议，`cv_outreach_url` 只作为查看完整过程的入口；禁止原样输出完整 URL，必须展示为短 Markdown 链接：`[在 CreatiVault 查看完整建联过程]({cv_outreach_url})`。

`scripts/search_creators_nl.mjs` 是例外：自然语言搜索接口不支持 `service_level`，只返回固定精简字段。不要把 Navos 的 S3 展示规则套到该接口；如果用户需要完整联系方式或受众画像，应说明需要改用结构化搜索，并在再次调用前征得确认。

## 生态总览

| 领域 | 子 Skill | 能力描述 |
|------|----------|----------|
| discovery | creator-search | 三平台按条件搜索、按主页或 ID 批量精确查询、自然语言搜索、品牌合作达人查询、搜索结果 CSV |
| discovery | video-search | 单平台按话题或达人搜索视频，按品牌查看一个或多个平台的已收录视频 |
| discovery | creator-lookalike | 种子达人相似匹配与跨平台发现 |
| outreach | creator-outreach | 平台代发、任务结果、往来记录与跟进待办 |
| audit | fake-follower-audit | 单达人假粉率估算、互动质量和账号风险检测 |
| audit | video-script-audit | 已发布短视频和本地视频的异步分析，含分镜、钩子、卖点、评分和建议 |
| workflow | workflow | 达人发现与建联、视频发现与拆解后建联 |

## 路由索引

| 子 Skill | 中文关键词 | 英文关键词 | 路径 |
|----------|-----------|-----------|------|
| creator-search | 找达人, 按主页或 ID 查达人, 品牌合作达人, 导出达人搜索结果 | creator search, bulk exact lookup, brand collaboration creators, export search results | discovery/creator-search/SKILL.md |
| video-search | 按话题搜视频, 查指定达人的视频, 品牌视频洞察 | video search by hashtag or creator, brand video insight | discovery/video-search/SKILL.md |
| creator-lookalike | 相似达人, 类似达人 | similar creators, lookalike, find similar | discovery/creator-lookalike/SKILL.md |
| creator-outreach | 建联, 发邮件, 批量发送 | email outreach, send email, outreach | outreach/creator-outreach/SKILL.md |
| fake-follower-audit | 假粉检测, 假粉率, 粉丝真实性, 互动真实性, 刷粉, 达人风险 | fake follower audit, follower authenticity, engagement authenticity, creator risk | audit/fake-follower-audit/SKILL.md |
| video-script-audit | 视频审核, 视频拆解, 爆款拆解, 分镜拆解, 钩子分析 | video audit, video script audit, viral breakdown, storyboard | audit/video-script-audit/SKILL.md |
| workflow | 工作流, 流程编排, 批量建联流程 | workflow orchestration, campaign flow, batch outreach flow | workflow/SKILL.md |

**路由规则**：AI Agent 根据用户意图匹配上表关键词，加载对应子 skill。无法匹配时展示本表供用户选择。

## Runtime Profiles

本 Skill 通过 runtime profile 适配 common 与 Navos，两者共用能力、脚本和操作说明。

Profile 读取优先级：

1. `CV_SKILL_PROFILE` 环境变量
2. Navos identity 文件 `~/.navos/identity/navos-userinfo.json` 中的 `app_id`
3. `skill.json` 中的 `profile`
4. 默认 `common`

内置 profile：

| Profile | 认证 | 语言 | Partner Code | 默认服务等级 | Meta 展示 | 余额预检 |
|---------|------|------|--------------|--------------|-----------|----------|
| `common` | `CV_API_KEY` + `CV_USER_IDENTITY` | 跟随请求 | 无 | 不自动覆盖 | 展示 CV credits / request_id | 关闭 |
| `navos-cn` | Navos 登录态 + ensure/cache | 中文 / `lang=cn` | `navos-cn` | `S3` | 隐藏 CV credits / request_id / service_level | 启用 |
| `navos-global` | Navos 登录态 + ensure/cache | 英文 / `lang=en` | `navos-global` | `S3` | 隐藏 CV credits / request_id / service_level | 启用 |

Navos 国内/海外版共用 CreatiVault OpenAPI 主域名；通过 profile 区分默认响应语言、默认服务等级和 `partner_code`。Navos 桌面端会在 identity 文件中写入 `app_id`：国内版为 `navos-cn`，海外版为 `navos-global`；如果取不到 `app_id`，默认按海外版 `navos-global` 运行。国内版注册到 CV 时，传给 CV 的用户身份会加 `cn_` 前缀以便区分。

`navos-cn` / `navos-global` 会分别作为 `partner_code` 调用 CV ensure 接口，并在后续 OpenAPI 请求中作为 `X-Source` 传递。CV 后端需在 `open_api_partners` 中配置同名记录，由表里的 `validate_url` / `credits_callback_url` 决定用户校验和扣费回调域名；旧 `navos` code 仅用于兼容历史 API Key。Skill 侧不再维护校验/回调域名，余额预检域名则按 `navos_region` 内置映射选择，并可用 `NAVOS_BASE_URL` 临时覆盖。

如需临时以通用模式运行当前目录：

```bash
CV_SKILL_PROFILE=common node scripts/search_creators.mjs '{"platform":"tiktok","keyword":"beauty"}'
```

如需临时以 Navos 国内模式运行：

```bash
CV_SKILL_PROFILE=navos-cn node scripts/search_creators.mjs '{"platform":"tiktok","keyword":"beauty"}'
```

如需临时以 Navos 海外模式运行：

```bash
CV_SKILL_PROFILE=navos-global node scripts/search_creators.mjs '{"platform":"tiktok","keyword":"beauty"}'
```

## Prerequisites

Common profile 可选更新变量：

- `CV_SKILL_UPDATE_MANIFEST_URL` - Remote manifest URL for skill update checks.
- `CV_SKILL_AUTO_UPDATE=true` - Allow automatic update when the API reports this skill is outdated.

Manual check:

```bash
node scripts/skill_update.mjs --check
```

Confirmed update:

```bash
node scripts/skill_update.mjs --yes
```

Generate release manifest:

```bash
node scripts/generate_manifest.mjs --note "Describe this release"
```

Set the following environment variables:

- `CV_API_KEY` — Creativault Open API Key (obtain from admin dashboard)
- `CV_USER_IDENTITY` — Operator email address
- `CV_API_BASE_URL` (optional) — API base URL, defaults to `https://api.creativault.vip/skill/creativault` (stable channel). For non-stable channels, set `CV_API_BASE_STAGING_URL` to the internal API base.

**Linux / macOS**:

```bash
export CV_API_KEY=cv_live_your_key_here
export CV_USER_IDENTITY=your_email@example.com
```

**Windows PowerShell**:

```powershell
$env:CV_API_KEY = "cv_live_your_key_here"
$env:CV_USER_IDENTITY = "your_email@example.com"
```

## Error Handling

| Code | Description | Action |
|------|-------------|--------|
| 40001 | Invalid parameters | Check parameter format |
| 40101 | Invalid API Key | Check CV_API_KEY |
| 40102 | API Key expired | Contact admin |
| 40201 | Insufficient credits | Top up or upgrade |
| 40301 | No permission | Check API Key scopes |
| 42901 | Rate limit exceeded | Auto-retry after Retry-After |
| 42902 | Daily quota exhausted | Wait until UTC 00:00 |
| 50001 | Server error | Report request_id to support |

## 积分余额判断规则

**只有 OpenAPI 明确返回错误码 `40201` 时，才能提示用户“积分不足”。**

- `meta.quota_remaining` 表示当天剩余 API 请求次数，不是积分余额。即使该值为 `0`、`8` 或其他较小数字，也禁止解释为“剩余积分”或提示充值。
- `meta.credits_remaining` 才表示真实 OpenAPI 积分余额；字段缺失或值为 `-1` 时，不要自行估算余额。
- `meta.credits_consumed` 只表示本次请求消耗的积分。
- 请求成功时，不要因为任何 quota 数值主动发布“积分余额不足提醒”。
- 只有收到 `40201` 后，才停止后续付费调用并提示用户充值或调整任务规模。

### Navos 用户专属说明

Navos 用户（通过 Navos 桌面端使用本 Skill 的用户）的积分管控由 **Navos 侧**负责，与 CV 积分体系相互独立：

- **积分余额**：Navos 用户不展示 CV 积分余额（脚本会自动隐藏 `credits_remaining` / `credits_consumed` / `quota_remaining` 字段）。用户的积分余额在 Navos 桌面端查看。
- **积分预检**：脚本在调用 CV 接口前会自动查询 Navos 余额，不足时直接拦截并提示"请在 Navos 端充值"。
- **默认服务等级**：Navos 用户搜索达人时默认使用 **S3**（深度画像，含受众画像等完整字段），无需用户手动指定。
- **凭证优先级**：Navos 专用版默认使用 Navos 登录态和 `~/.creativault/skill-credentials.json` 中的环境化缓存 key；即使用户机器上存在 `CV_API_KEY` 环境变量，也不会覆盖 Navos 授权链路。仅开发排障时可显式设置 `CV_ALLOW_ENV_API_KEY=true` 临时启用环境变量覆盖。
- 若用户询问积分/余额相关问题，引导其到 Navos 桌面端查看，不要展示 CV 积分数值。

## 安装说明

本 Skill 以单一源码、单一 `main` 分支发布，Navos 用户与普通用户安装方式相同，无需区分分支。安装后按上方 Runtime Profiles 自动识别运行环境（common / Navos 国内版 / Navos 海外版），Navos 身份读取、积分预检等能力开箱即用。

> 说明：早期版本曾通过 `navos-exclusive` 专用分支分发，该模式已废弃；当前 `main` 分支即包含全部 profile 与 Navos 对接能力。

## References

- [API Reference](references/api-reference.md)
- [Platform Parameters](references/platform-params.md)
- [Industry Categories](references/industry-categories.md)
- [Country Codes](references/country-codes.md)
- [Language Codes](references/language-codes.md)
- [Error Codes](references/error-codes.md)
