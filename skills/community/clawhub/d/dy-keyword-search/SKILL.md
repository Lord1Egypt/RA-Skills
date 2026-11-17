---
name: dy-search
slug: dy-keyword-search
displayName: 抖音关键词搜索采集
version: 1.0.0
summary: 按关键词搜索抖音视频并批量采集结果列表（文案、五项互动数、作者、发布时间、直链），导出 CSV，用于内容选题调研、竞品监测与达人初筛（20 条 = 5 点数）。
description: 抖音搜索视频采集工具（关键词搜索）。当用户需要按关键词搜索抖音视频并采集结果列表——视频文案、点赞/评论/收藏/分享/播放数、作者昵称、发布时间、封面图、视频链接，批量获取竞品视频、选题调研、KOL 初筛、导出搜索结果 CSV（Excel 直开），或提到"抖音搜索/搜视频/关键词采集/搜索结果导出/选题/竞品视频列表"时使用本 skill。适合内容选题调研、竞品监测、达人初筛、品类视频盘点等场景。**一次接口返回（约 20 条）= 5 点数；预扣按请求量、结算按实采量退差；零结果或失败全额返还（注册送 10 点）。**
---

# 抖音搜索视频采集 Skill（dy-search）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用。输入**关键词 + 条数**，平台调度内网浏览器节点以真人滚动方式打开抖音搜索页（`/search/<关键词>?type=video`），拦截官方搜索接口响应，采集视频列表。

- **能采什么**：搜索结果页的视频明细（`title` 视频文案、`digg_count` 点赞、`comment_count` 评论数、`collect_count` 收藏、`share_count` 分享数、`play_count` 播放量、`recommend_count` 推荐数、`author_nickname` 作者昵称、`author_sec_uid` / `author_uid`、`topics` 话题、`create_time` 发布时间、`duration_ms` 时长、`cover_url` 封面图、`url` 视频链接）。
- **适用场景**：内容选题调研、竞品视频监测、达人/KOL 初筛、品类视频盘点、关键词热度摸底。
- **采集方式**：内网浏览器节点拟人滚动搜索页 + 拦截官方接口（不调签名 API，风控风险由平台侧承担）。
- **限制**：单任务 1 个关键词、1~500 条；节点滚动约 3-5 分钟（500 条约 5 分钟）。
- 采集由**平台调度内网浏览器节点**完成（节点登录态在浏览器端人工维护，平台不持有账号）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、采集结果异常、批量采购等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **一次接口返回（约 20 条）= 5 点数**（1 点数 = 1 元以下优惠价请联系客服）。
- **预扣**：`ceil(请求条数/20) × 5`（如 50 条预扣 15 点）；**结算按实采量**：`ceil(实采条数/20) × 5`，差值自动返还（如实采 45 条只收 15 点——不满 20 条的零头按一次计）。
- **零结果或失败全额返还**：关键词无结果、节点离线超时、风控拦截等，预扣点数全额退还。
- 注册即送 **10 免费点数**。点数不足时提示用户充值；充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 交互协议（agent 必须严格遵守）

本 skill 是**确认制一次性任务**，不是跑完就完。请按下面的流程驱动对话：

1. **查余额**：`node cli.js quota` 确认点数充足（余额 < 预扣点数会被 3001 拒绝）。
2. **报价确认（必须）**：向用户明确以下信息并**等用户确认后**再提交：
   - 搜索关键词、采集数量（1~500）、排序（默认综合排序）、发布时间（默认不限）
   - 预估点数：`ceil(数量/20) × 5`（例：50 条 → 15 点；120 条 → 30 点）
   - 计费规则：**预扣 ceil(N/20)×5，按实采 ceil(M/20)×5 结算退差，零头按一次计，零结果或失败全退**
   - **未经用户确认不要执行 submit。**
3. **提交并等待**：`node cli.js submit --keyword "<词>" --count <N> --wait --timeout 600`。节点滚动约 3-5 分钟属正常，不要中途重试。
4. **如实汇报结算**：结果里的 `collected_count`（实采条数）、`settle_charged`（实收点数）、`refunded_diff`（退还差值）必须如实告知用户（例：「实采 45 条，实收 15 点，退 0 点」）。
5. **需要文件时导出**：`node cli.js export <task_id> --wait --out 搜索结果.csv`，把 CSV 路径交给用户。

**筛选说明**：`--sort` 0=综合排序 / 1=最多点赞 / 2=最新发布（默认 0）；`--publish-time` 0=不限 / 1=一天内 / 7=一周内 / 180=半年内（默认 0）。

## 前置条件

- **Node.js ≥ 18**（使用内置 fetch，零 npm 依赖）。
- **不注册不登录没有任何点数**：所有接口都需要 token，10 免费点数在注册成功后发放到账号。
- 首次使用需先 `register --link`（注册即送 10 点数；用户手机微信扫码/点链接在网页完成，页面自带图形+短信验证码）或 `login --link`（已有账号）。成功后 token 自动保存，后续调用免输。
- **配置文件（含 token）存放于用户级目录 `~/.xhs-platform/config.json`**（升级/重装 skill 不丢配置；与小红书系列 skill 共用同一账号体系）。可用环境变量 `XHS_CONFIG_PATH` 覆盖（测试隔离用）。
- **安全策略：登录和注册（发短信）每次都强制图形验证码**，终端无法展示，所以一律走 `--link` 微信扫码/链接方式。
- 后端服务地址默认 `http://st.aidata366.com`，可用 `node cli.js config set base-url <url>` 修改，或单次加 `--base-url <url>` 覆盖。
- **⚠️ 安全提示（重要）**：默认服务地址是**明文 http**，token 会在公网明文传输。客户端每次请求都会在 stderr 提示。请知悉该风险；如环境允许，建议通过 `config set base-url https://...` 切换到 https 服务地址（需服务端已配好证书）。
- 所有命令支持全局参数 `--token <token>`（临时覆盖配置文件中的 token）。
- `~/.xhs-platform/config.json` 含 token，**不要泄露、不要提交 git**。

## 输出规约（重要）

- **stdout 只输出 JSON**：成功 `{"ok":true,"data":{...}}`，失败 `{"ok":false,"code":<业务码>,"message":"..."}`。直接解析 stdout 即可。
- 交互提示（如「请把预估点数报给用户确认」）一律走 **stderr**，不要解析，但其中给用户的引导话术应照做。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。
- `submit --wait` 单次最长 10 分钟（默认 600s 超时，节点滚动 3-5 分钟），属正常现象，不要中途重试。

## 命令清单

### version — 查看版本与安装信息

```bash
node cli.js version
```

```json
{"ok":true,"data":{"name":"dy-search","version":"1.0.0","capability":"dy_search"}}
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

### submit — 提交搜索采集任务

```bash
node cli.js submit --keyword "机油"                          # 默认 50 条, 综合排序, 发布时间不限
node cli.js submit --keyword "机油" --count 120              # 120 条 (预扣 30 点)
node cli.js submit --keyword "美孚" --count 40 --sort 2 --publish-time 7
node cli.js submit --keyword "机油" --count 50 --wait        # 提交并等待结果 (约 3-5 分钟)
node cli.js submit --keyword "机油" --count 50 --wait --timeout 600 --force
```

- `--keyword`：搜索关键词（≤64 字符；填视频链接会被拒绝，单篇互动数请用 dy-collect skill）。
- `--count`：采集条数 1~500（默认 50）。
- `--sort`：0=综合排序 1=最多点赞 2=最新发布（默认 0）。
- `--publish-time`：0=不限 1=一天内 7=一周内 180=半年内（默认 0）。
- `--wait`：等待任务终态再返回（推荐）；`--timeout` 轮询超时（默认 600s）；`--interval` 轮询间隔（默认 5s）。
- `--force`：跳过 24h 相同内容去重强制重提（幂等键混入时间戳）。

`--wait` 完成后的输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261015_ab12cd34","capability":"dy_search","status":"done",
 "success_count":1,"fail_count":0,"charged_quota":15,"refunded_quota":0,
 "items":[{"id":"1","payload":{"keyword":"机油","count":50,"sort":"0","publish_time":"0"},
   "result":{"keyword":"机油","requested_count":50,"collected_count":45,
             "settle_charged":15,"refunded_diff":0,
             "videos":[{"aweme_id":"7312...","title":"机油怎么选？一篇讲透","media_type":"4",
                        "digg_count":"1.2万","comment_count":"156","collect_count":"890",
                        "share_count":"45","play_count":"56万","recommend_count":"0",
                        "author_nickname":"老司机说车","author_sec_uid":"MS4w...",
                        "topics":"机油,养车","create_time":"03-15","duration_ms":"253000",
                        "cover_url":"https://p3-pc.douyinpic.com/...",
                        "url":"https://www.douyin.com/video/7312..."}]},
   "status":"success"}]}}
```

**拿到结果后必须把 `collected_count` / `settle_charged` / `refunded_diff` 如实汇报给用户（见「交互协议」）。**

### query — 查询任务状态与结果

```bash
node cli.js query <task_id>            # 单次查询
node cli.js query <task_id> --wait     # 轮询到终态 (默认 600s 超时)
```

### export — 导出结果 CSV

```bash
node cli.js export <task_id> --wait --out 搜索结果.csv
```

下载任务结果 CSV（BOM 头，Excel 直开不乱码）：任务汇总（关键词/状态/实采数/实收点数/退差点数）+ 视频明细（文案/互动数/作者/发布时间/封面/链接）。导出文件保留 7 天。

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

1. 用户说「帮我搜一下 XX 的抖音视频」→ `node cli.js quota` 确认余额。
2. 和用户确认关键词、数量、排序、发布时间；算出预估点数 `ceil(N/20)×5`；**明确告知计费规则（预扣/结算退差/零头按一次计/零结果失败全退）并等确认**。
3. `node cli.js submit --keyword "<词>" --count <N> --wait --timeout 600`（3-5 分钟，不重试）。
4. 如实汇报：实采条数、实收点数、退差点数；简要展示视频列表（文案/互动数/作者）。
5. 用户要文件 → `node cli.js export <task_id> --wait --out <文件>.csv`，交付路径。
6. 用户要继续分析 → 可基于视频链接用 dy-collect 采单篇互动数或 dy-comments 采评论。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 / 关键词无效 / 超 500 条 | 检查参数；链接型输入引导用 dy-collect（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册走 `register --link`（送 10 点数），已有账号走 `login --link`；完成后 `--check`（退出码 2） |
| LOGIN_PENDING / LOGIN_EXPIRED | 用户未完成 / 会话过期 | 提醒用户完成扫码后重试 `--check`，或重新 `--link`（退出码 2） |
| 2003 | 需要图形验证码 | 终端无法完成，统一走 `--link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| TIMEOUT | 等待超时（任务仍在跑） | 任务未丢：稍后 `query <task_id>` 查终态；预扣仍在，终态后按实采结算 |
| 5001 | 采集服务暂不可用（无在线抖音节点/超时/风控） | 点数已全额返还；稍后重试；持续不可用提示联系客服 18722121663 |
| 4290 | 触发限流 | 稍等后重试（Retry-After） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- **免费**：quota / query / export / config，以及 submit 被参数校验拒绝的请求。
- **预扣**：`ceil(请求条数/20) × 5`，提交成功立即扣除。
- **结算退差**：任务成功后按 `ceil(实采条数/20) × 5` 实收，差值自动返还（`refunded_diff`）；实采多于请求量时不多收（封顶预扣额）。
- **全额返还**：零结果（关键词无结果）、节点离线/超时、风控/登录拦截等服务侧失败。
- **不返还**：已成功采集的部分（结果不足请求量时按实采结算，本身就是退差逻辑）。

## 红线

- 仅采集**公开**搜索结果数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功或具体条数；风控/结果不足时如实透出（点数按实采结算，用户不损失）。
- 视频列表含作者公开昵称、发布时间等信息：**仅用于用户已授权或公开可获取的调研/分析场景**，遵守平台与数据合规要求；不在未授权场景下转售、滥用；CSV 导出文件请告知用户自行妥善保管。
