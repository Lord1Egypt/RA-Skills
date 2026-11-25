---
name: b-comments
slug: b-pinglun
displayName: B站评论采集（会话制）
version: 1.0.0
description: B站视频评论采集工具（分步会话）。当用户需要采集 B站视频下面的评论——发布者昵称、评论内容、时间、点赞数、回复@、二级回复，导出评论 CSV（Excel 直开），或提到"B站评论/评论采集/评论导出/评论分析/评论区舆情/弹幕区之外的评论"时使用本 skill。支持 bilibili.com/video/<BV号>、/video/av<数字> 直链与 b23.tv 短链（短链由节点自动还原）。分步会话制：start 建会话（免费）后按页采集主评论、按需翻页展开二级回复，每一步实时返回最新增量结果，由 AI 询问用户是否继续（每步 1 点数，注册送 10 点）。适合评论舆情分析、用户口碑调研、评论区选题、活动/投放效果评估等场景。
---

# B站评论采集 Skill（b-comments）

**产品定位**：输入 B站视频链接 → 平台调度内网浏览器节点打开该视频页 → 按页抓主评论、按需翻二级回复 → 结果实时分步返回、可 CSV 导出。

**会话制 v2（本 skill 核心特性）**：评论采集与小红书/抖音/快手系列一致采用「分步会话」模式——

1. `start` 建会话（**免费**：节点打开视频页解析 SSR 状态，探测标题/互动数/评论总数），返回评论总数与预估页数。
2. `step --page` 采一页主评论（实测 20 条/页 + 内嵌预览回复，扣 1 点）；`step --expand --root <cid>` 翻指定主评论的**下一页二级回复**（约 20 条，扣 1 点）。
3. 每一步实时返回增量结果，由 AI 把最新评论展示给用户并**询问是否继续**。
4. `finish` 主动结束会话（释放采集节点；忘记 finish 空闲 20 分钟也会自动过期）。

**为什么是会话制**：评论接口高频翻页风控风险高；按页计费 + 用户确认，避免一次性采集几百条用户实际不需要的内容。**这是产品决策，不是技术限制。**

- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。
- 采集由**平台调度内网浏览器节点**完成（节点登录态在浏览器端人工维护，平台不持有账号）。
- 导出 CSV 自带 BOM 头，Excel 直开不乱码。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、采集结果异常、批量采购等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **点数换算：0.1 元 = 1 点数。**
- **每步 1 点数**：`step --page` 采一页主评论（约 20 条 + 内嵌预览回复）= 1 点数；`step --expand` 翻一页二级回复 = 1 点数。
- **start 免费**（探测稿件信息不扣费）、`status` / `comments` / `export` / `finish` / `sessions` 全部免费。
- **步失败自动返还**：步进超时/风控拦截/本步 0 条导致未采到新数据时，该步点数自动返还。
- 注册即送 **10 免费点数**（可采约 10 页主评论）。点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 链接要求（重要）

- **只支持 B站视频链接**：`https://www.bilibili.com/video/<BV号>`、`/video/av<数字>` 直链或 `https://b23.tv/<短码>` 短链（短链由节点浏览器打开后自动还原，无需人工转换）。
- UP主主页链接不支持（评论采集必须有具体稿件）；主页投稿列表请用 `b-profile` skill。
- 稿件需为**公开可见**；私密/删除/审核中稿件无法采集（start 会失败，不扣费）。

## ⚠️ 交互协议（agent 必须严格遵守）

**本 skill 的核心使用方式是「会话制分步采集」，不是一次性批量工具。**严格遵守以下流程（这是产品决策——评论接口高频翻页风控风险高，按页计费+用户确认，避免一次性采集用户实际不需要的内容）：

### 流程

1. **查余额**：`node cli.js quota` 确认点数充足（余额 < 1 无法 step）。
2. **建立会话（免费）**：`node cli.js start --url <视频链接>` → 返回 `session_id`、稿件标题、评论总数（`metrics.comment_count`）、预估页数（`estimated_pages`）。
3. **报价确认（必须）**：把评论总数和预估页数告诉用户，算好预估点数（每页主评论 1 点 + 翻回复每页 1 点），**等用户确认后再开始 step**：
   - 例：`预估 N 页 × 1 点/页 = N 点；如需翻某条评论的二级回复，每翻一页 1 点。`
4. **逐步采集**：`node cli.js step --session <id> --page` 采下一页主评论。**每步返回后**：
   - 把本页新增评论（昵称/内容/时间/点赞）**展示给用户**；
   - 若返回 `expandable` 列表（可展开回复的主评论），告知用户：`以下 X 条评论有二级回复，是否展开？每翻一页 1 点`，由用户决定（**不要擅自展开**）；
   - **每步都要询问用户是否继续采下一页**（`has_more_main` 提示是否还有下一页）。
5. **中途可随时**：`status` 查会话状态与余额；`comments` 免费翻看已采累计明细；`export` 免费导出已采部分 CSV。
6. **结束会话**：`finish` 主动结束（推荐，立即释放采集节点）；或用户不想采了放着 20 分钟自动过期。

**会话保持时间**：采集节点绑定到会话直到 finish 或 20 分钟空闲自动过期。会话过期后需重新 `start`（probe 重新探测，免费）。已采集的评论数据**不会丢失**（落库），`comments` / `export` 对已过期会话依然有效。

### 绝对红线

- **报价未确认前禁止执行 step**（start/status/comments/export 免费，可随意调用）。
- **每步后必须询问用户**是否继续/是否展开，不要连续 step 多页。
- **绝不把 start 返回的 `session_id` 泄露给终端用户**（他人可用它枚举你的会话数据）；也不要把 `expandable` 列表里的评论枚举数据当普通文本随意传播。
- **不要将免费额度（start probe）用于资源探测**（如对同一视频反复 start 试图刷探测结果）。

### 时长与超时预期

- `step` 单步服务端最长可执行 **180 秒**（节点翻页 + 数据回传），CLI 客户端超时 200 秒。**单步超时是正常现象**，该步点数已自动返还，直接重试同一步即可。
- 会话空闲 **20 分钟**自动过期（过期后 `step` 返回 1404 会话不存在，重新 `start` 即可，已采数据不丢）。
- 采集节点池紧张时 `step` 可能排队等待几十秒，属正常。

## 前置条件

- **Node.js ≥ 18**（使用内置 fetch，零 npm 依赖）。
- **不注册不登录没有任何点数**：所有接口都需要 token，10 免费点数在注册成功后发放到账号。
- 首次使用需先 `register --link`（注册即送 10 点数；用户手机微信扫码/点链接在网页完成，页面自带图形+短信验证码）或 `login --link`（已有账号）。成功后 token 自动保存，后续调用免输。
- **配置文件（含 token）存放于用户级目录 `~/.xhs-platform/config.json`**（升级/重装 skill 不丢配置；与小红书/抖音/快手系列 skill 共用同一账号体系）。可用环境变量 `XHS_CONFIG_PATH` 覆盖（测试隔离用）。
- **安全策略：登录和注册（发短信）每次都强制图形验证码**，终端无法展示，所以一律走 `--link` 微信扫码/链接方式。
- 后端服务地址默认 `http://st.aidata366.com`，可用 `node cli.js config set base-url <url>` 修改，或单次加 `--base-url <url>` 覆盖。
- **⚠️ 安全提示（重要）**：默认服务地址是**明文 http**，token 会在公网明文传输。客户端每次请求都会在 stderr 提示。请知悉该风险；如环境允许，建议通过 `config set base-url https://...` 切换到 https 服务地址（需服务端已配好证书）。
- 所有命令支持全局参数 `--token <token>`（临时覆盖配置文件中的 token）。
- `~/.xhs-platform/config.json` 含 token，**不要泄露、不要提交 git**。

## 输出规约（重要）

- **stdout 只输出 JSON**：成功 `{"ok":true,"data":{...}}`，失败 `{"ok":false,"code":<业务码>,"message":"..."}`。直接解析 stdout 即可。
- 交互提示（如「请把预估点数报给用户确认」）一律走 **stderr**，不要解析，但其中给用户的引导话术应照做。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。

## 命令清单

### version — 查看版本与安装信息

```bash
node cli.js version
```

```json
{"ok":true,"data":{"name":"b-comments","version":"1.0.0","capability":"b_comments"}}
```

### register — 注册（注册即送 10 点数）

**方式一：扫码/链接注册（唯一方式，用户在手机上完成）**

```bash
node cli.js register --link        # 生成注册二维码/链接
node cli.js register --check --access-token "<上一步下发的串>"   # 用户完成后确认并保存 token
```

`register --link` 的 stdout 返回 `qr_url` / `register_url` / `access_token`。**agent 必须把注册引导原样发给用户**（stderr 里也给出了同样话术，可直接复制）：

```text
需要先注册账号（注册即送 10 免费点数；不注册不登录没有点数，无法采集）。请用手机微信扫码或打开链接注册：

注册方式（二选一）
二维码图片：<qr_url>
注册链接：<register_url>
access_token（注册后校验用）：<access_token>
微信扫码/注册完成后告诉我一声，我会执行校验并保存凭证，然后继续之前的操作：
（注册/使用中如遇问题，请拨打客服电话 18722121663）
```

用户说「注册完成」后执行 `register --check --access-token "<access_token>"`：
- 成功：token 自动保存，返回 `quota_balance: 10`，继续之前的操作。
- `LOGIN_PENDING`：用户还没完成注册，提醒后再试。
- `LOGIN_EXPIRED`：会话过期（10 分钟）或已使用，重新执行 `register --link`。

### login — 登录

```bash
node cli.js login --link
node cli.js login --check --access-token "<上一步下发的串>"
```

引导话术同 register（把"注册"换成"登录"）。成功后 token 自动保存。

### quota — 查询点数

```bash
node cli.js quota
```

```json
{"ok":true,"data":{"quota":10,...}}
```

### start — 建立会话（免费）

```bash
node cli.js start --url "https://www.bilibili.com/video/BV1GJ411x7h7"
node cli.js start --url "https://b23.tv/AbCdEf"     # 短链直接提交, 节点自动还原
```

输出示例：

```json
{"ok":true,"data":{
  "platform":"b",
  "session_id":"e3b0c44298fc1c149afbf4c8996fb924",
  "bvid":"BV1GJ411x7h7",
  "aid":"80433022",
  "video_url":"https://www.bilibili.com/video/BV1GJ411x7h7",
  "title":"机油怎么选？一篇讲透",
  "author_nickname":"老司机说车",
  "metrics":{"comment_count":"156","liked_count":"1.2万","collected_count":"3200",
             "play_count":"560000"},
  "estimated_pages":8,
  "status":"active",
  "mains_collected":0,
  "subs_collected":0,
  "charged_steps":0
}}
```

**拿到 `session_id` + 评论总数后，必须把数字报给用户做报价确认（每页 1 点），确认后才能 step。**

### step — 采集一步（扣 1 点）

```bash
node cli.js step --session <session_id> --page                          # 采下一页主评论
node cli.js step --session <session_id> --expand --root <主评论cid>      # 翻该主评论的下一页二级回复
```

`step --page` 返回示例（评论字段为 B站口径：cid/text/digg_count/create_time/reply_to_nickname）：

```json
{"ok":true,"data":{
  "no_more":false,
  "type":"page",
  "page_no":1,
  "comments":[
    {"cid":"7350000000000000001","nickname":"车友A","text":"美孚1号真不错",
     "create_time":1773547200,"digg_count":"23","sub_count":3,
     "sub_comments":[{"cid":"7350000000000000002","nickname":"车友B","text":"同感",
                      "reply_to_nickname":"车友A"}]}
  ],
  "has_more_main":true,
  "expandable":[
    {"root_cid":"7350000000000000001","sub_count":3,"subs_collected":1,"has_more":true}
  ],
  "mains_collected":20,
  "subs_collected":1,
  "charged_steps":1,
  "refunded_this_step":false,
  "quota_balance":9
}}
```

`step --expand` 返回示例（`comments` 为该主评论本次新翻出的回复）：

```json
{"ok":true,"data":{
  "no_more":false,
  "type":"expand",
  "root_cid":"7350000000000000001",
  "comments":[{"cid":"7350000000000000002","nickname":"车友B","text":"同感",
                "create_time":1773547500,"digg_count":"2",
                "reply_to_nickname":"车友A"}],
  "sub_has_more":false,
  "sub_page":1,
  "subs_collected_for_root":3,
  "subs_remaining_estimate":0,
  "charged_steps":2,
  "refunded_this_step":false,
  "quota_balance":8
}}
```

**解读要点（agent 必读）**：

- `step --page` 后 `has_more_main: false` 表示主评论已采完（继续 step 返回 `no_more: true`，不扣费）。
- `expandable` 为本页采完后**含可展开回复的主评论**：`root_cid`（展开时传给 `--root`）、`sub_count`（回复总数）、`subs_collected`（已采回复数）。
- `step --expand`：B站二级回复是**按页翻**（每页约 20 条），`sub_has_more: true` 表示还有下一页（继续翻每次 1 点），`no_more: true` 表示已翻完，本次不扣费。
- `refunded_this_step: true` 表示本步一条都没采到（风控/懒渲染），点数已自动返还，会话仍可继续采。
- `quota_balance` 为当前余额，每步后**必须核对**，余额不足时提醒用户充值。
- 每一步输出中的评论是**本步增量**，不是全量。全量累计请用 `comments` 命令翻页获取，或 `export` 导出。

### status — 查询会话状态（免费）

```bash
node cli.js status --session <session_id>
```

返回会话状态（active/expired/failed/done）、稿件信息、累计采集量（`mains_collected`/`subs_collected`/`charged_steps`）、`quota_balance`。

### comments — 拉取累计评论明细（免费）

```bash
node cli.js comments --session <session_id>                    # 默认第 1 页, 100 条/页
node cli.js comments --session <session_id> --page 2 --page-size 50
```

返回该会话**累计**采集的全部评论（主评论+二级回复，分页），落库数据，会话过期后依然可查。字段含 `bvid`、`aid`、`cid`、`root_cid`、`nickname`、`author_id`、`reply_to_nickname`、`text`、`digg_count`、`create_time`（`root_cid` 为空即主评论）。

### export — 导出会话结果 CSV（免费）

```bash
node cli.js export --session <session_id> --out 评论导出.csv
```

下载该会话累计评论 CSV（BOM 头，Excel 直开不乱码）：视频汇总段（session_id/bvid/aid/标题/评论总数/点赞/收藏/播放/UP主/已采页数/主评论数/回复数/已扣步数/状态）+ 评论明细段（bvid、aid、cid、root_cid、昵称、作者ID、回复对象昵称、内容、点赞数、时间）。**含已过期会话**——只要 session_id 在，随时可导出。

### finish — 结束会话（免费）

```bash
node cli.js finish --session <session_id>
```

主动结束会话、立即释放采集节点。返回 `status: "done"`。

### sessions — 列出自己的会话（免费）

```bash
node cli.js sessions                    # 全部会话
node cli.js sessions --status active    # 只看进行中
```

分页列出当前用户的历史会话（`session_id`、稿件链接、状态、累计采集量、创建时间）。

### logout — 登出（切换账号）

```bash
node cli.js logout
```

### config — 配置管理

```bash
node cli.js config set base-url http://127.0.0.1:8084
node cli.js config show        # token 脱敏显示
```

## 典型工作流（agent 照此执行）

用户：**帮我采集这个 B站视频的评论 https://b23.tv/AbCdEf**

1. **检查链接**：`b23.tv` 短链直接可提交（节点自动还原），不需要人工转换。
2. **登录检查**：`node cli.js quota` → 未登录则引导 `login --link`（或注册 `register --link` 送 10 点数）。
3. **建立会话（免费）**：`node cli.js start --url "https://b23.tv/AbCdEf"`。
4. **报价确认**：把 `metrics.comment_count`（评论总数）与 `estimated_pages`（预估页数）报给用户：
   - 例：`这个稿件共 156 条评论，预估 8 页主评论，每页 1 点，共约 8 点（如需翻某条评论的二级回复，每翻一页额外 1 点）。是否开始采集？`
   - **用户确认后才继续**；余额不足先引导充值。
5. **采集第一页**：`node cli.js step --session <sid> --page`。
6. **展示 + 询问**：把本页评论摘要（昵称/内容/点赞）展示给用户；若有 `expandable` 告知「以下评论有二级回复，是否展开（每页 1 点）」；问「是否继续采下一页？」。
7. **循环 step**：用户确认继续 → 再采下一页，直到用户喊停 / `has_more_main: false` / 点数不足。
8. **收尾**：用户不再继续 → `node cli.js finish --session <sid>` 释放节点（数据已落库）。
9. **交付**：`node cli.js export --session <sid> --out <稿件标题或日期>.csv` → 把 CSV 路径交给用户。
10. 用户要求分析评论（舆情/口碑/关键词统计）→ 可基于导出 CSV 或 `comments` 明细直接分析，无需重新采集。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误（session id 不合法/step 类型不合法/链接不合法） | 检查 `--session <32位id>`、`--root <cid>`、`--url` 参数（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 引导 `login --link`（未注册先 `register --link` 送 10 点数）（退出码 2） |
| LOGIN_PENDING / LOGIN_EXPIRED | 用户未完成 / 会话过期 | 提醒用户完成扫码后重试 `--check`，或重新 `--link`（退出码 2） |
| 2003 | 需要图形验证码 | 终端无法完成，统一走 `--link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| 1404 | 会话不存在（含已过期/已 finish/稿件不可见） | 重新 `start` 建会话（probe 免费），已采数据不丢可继续 export |
| 步超时 / `refunded_this_step` | 单步超时（最长 180s）或本步 0 条 | **该步点数已自动返还**；直接重试同一步（如 `step --page`） |
| 风控拦截 | 页面要求滑块/验证码 | 点数已返还；稍等几分钟再试；持续拦截提示联系客服 18722121663 |
| 4290 | 触发限流 | 稍等后重试 |
| TIMEOUT | step 客户端超时（200s） | 服务端可能仍在执行；先 `status` 查累计量再决定是否重试本步 |
| NETWORK_ERROR | 网络/服务不可达 | 检查 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- **免费**：start（探测）/ status / comments / export / finish / sessions / quota，以及被参数校验拒绝的请求。
- **计费**：仅 step（每步 1 点：一页主评论 或 一页二级回复）；`no_more` 步不扣费。
- **自动返还**：步进超时/风控拦截/本步 0 条等未采到新数据的失败步，点数自动返还。
- **不返还**：已成功采到新数据的步（即使评论数少于预期，一页不到 20 条也收 1 点）；稿件中途不可见（业务性失败）不返还。

## 红线

- 仅采集**公开**评论数据；不用于任何违法违规用途。
- **报价未确认不 step、每步后必须询问**（见「交互协议」），不要擅自连续采集或展开。
- 不要向用户承诺 100% 成功；风控/超时失败如实透出（失败步点数已返还）。
- 评论含用户公开昵称：**仅用于用户已授权或公开可获取的舆情/调研场景**，遵守平台与数据合规要求；不在未授权场景下转售、滥用；CSV 导出文件请告知用户自行妥善保管。
