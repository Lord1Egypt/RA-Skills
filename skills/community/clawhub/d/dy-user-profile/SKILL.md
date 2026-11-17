---
name: dy-profile
slug: dy-user-profile
displayName: 抖音用户主页采集
version: 1.0.0
summary: 输入抖音博主主页链接，采集其视频作品列表（文案、五项互动数、发布时间、封面图、直链）并导出 CSV，用于达人筛选、竞品账号监测与 KOL 背调（每页约 20 条 = 5 点数）。
description: 抖音用户主页视频采集工具。当用户提供抖音博主主页链接，需要采集该博主发布的视频作品列表——视频文案、点赞/评论/收藏/分享/播放数、作者昵称、发布时间、封面图、视频链接，导出结果 CSV（Excel 直开），或提到"抖音主页/博主作品/达人视频列表/抖音账号视频采集"时使用本 skill。适合达人筛选、博主内容盘点、竞品账号监测、KOL 背调等场景。支持 douyin.com/user/<sec_uid> 直链与 v.douyin.com 短链。**一页（约 20 条）= 5 点数；预扣按页数、结算按实采量退差；零结果或失败全额返还（注册送 10 点）。**
---

# 抖音用户主页视频采集 Skill（dy-profile）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用。输入**抖音用户主页链接 + 页数**，平台调度内网浏览器节点以真人滚动方式打开博主主页，拦截官方作品接口（`/aweme/v1/web/aweme/post/`，max_cursor 翻页）采集该用户的视频列表。

- **能采什么**：主页作品列表的视频明细（`title` 视频文案、`digg_count` 点赞、`comment_count` 评论数、`collect_count` 收藏、`share_count` 分享数、`play_count` 播放量、`author_nickname` 作者昵称、`topics` 话题、`create_time` 发布时间、`duration_ms` 时长、`cover_url` 封面图、`url` 视频链接），以及博主 `sec_uid` / `blogger_nickname`。
- **适用场景**：达人筛选、博主内容盘点、竞品账号监测、KOL 背调、账号作品全量导出。
- **采集方式**：内网浏览器节点拟人滚动主页 + 拦截官方接口；每页约 18-20 条。
- **限制**：单任务 1 个博主、1~10 页（约 20 条/页）；`v.douyin.com` 短链由节点浏览器打开后自动还原。
- 采集由**平台调度内网浏览器节点**完成（节点登录态在浏览器端人工维护，平台不持有账号）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、采集结果异常、批量采购等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **一页（约 20 条）= 5 点数**（1 点数 = 1 元以下优惠价请联系客服）。
- **预扣**：`页数 × 5`（如 3 页预扣 15 点）；**结算按实采量**：`ceil(实采条数/20) × 5`，差值自动返还（零头按一页计）。
- **零结果/采集失败/主页不可见全额返还**：博主无作品、节点离线超时、风控拦截、账号被封等，预扣点数全额退还。
- 注册即送 **10 免费点数**。点数不足时提示用户充值；充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 交互协议（agent 必须严格遵守）

本 skill 是**确认制一次性任务**。请按下面的流程驱动对话：

1. **查余额**：`node cli.js quota` 确认点数充足（余额 < 预扣点数会被 3001 拒绝）。
2. **报价确认（必须）**：向用户明确以下信息并**等用户确认后**再提交：
   - 主页链接、采集页数（1~10，每页约 20 条）
   - 预估点数：`页数 × 5`（例：3 页 → 15 点）
   - 计费规则：**预扣 页数×5，按实采 ceil(M/20)×5 结算退差，零头按一页计，零结果/失败/主页不可见全退**
   - **未经用户确认不要执行 collect。**
3. **提交并等待**：`node cli.js collect --url <主页链接> --pages <N> --wait --timeout 600`。每页滚动约 5-10 秒，属正常，不要中途重试。
4. **如实汇报结算**：结果里的 `collected_count`（实采条数）、`settle_charged`（实收点数）、`refunded_diff`（退还差值）必须如实告知用户。
5. **需要文件时导出**：`node cli.js export <task_id> --wait --out 主页视频.csv`，把 CSV 路径交给用户。

**链接说明**：支持 `douyin.com/user/<sec_uid>` 直链与 `v.douyin.com` 短链（短链直接提交，节点浏览器打开后自动还原）；**视频链接不要提交本 skill**（单篇互动数请用 dy-collect，评论请用 dy-comments）。

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
- 交互提示一律走 **stderr**，不要解析，但其中给用户的引导话术应照做。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。
- `collect --wait` 默认 600s 超时，属正常现象，不要中途重试。

## 命令清单

### version — 查看版本与安装信息

```bash
node cli.js version
```

```json
{"ok":true,"data":{"name":"dy-profile","version":"1.0.0","capability":"dy_profile"}}
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

### collect — 提交主页采集任务

```bash
node cli.js collect --url "https://www.douyin.com/user/MS4wLjABAAAA..." --pages 3 --wait
node cli.js collect --url "https://v.douyin.com/iAbCdEf/" --pages 1     # 短链直接提交
node cli.js collect --url <主页链接> --pages 5 --wait --timeout 600 --force
```

- `--url`：抖音用户主页链接（`douyin.com/user/<sec_uid>` 或 `v.douyin.com` 短链；不支持 `self` 主页）。
- `--pages`：采集页数 1~10（默认 1，每页约 20 条）。
- `--wait`：等待任务终态再返回（推荐）；`--timeout` 轮询超时（默认 600s）；`--interval` 轮询间隔（默认 5s）。
- `--force`：跳过 24h 相同内容去重强制重提（幂等键混入时间戳）。

`--wait` 完成后的输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261015_ab12cd34","capability":"dy_profile","status":"done",
 "success_count":1,"fail_count":0,"charged_quota":15,"refunded_quota":0,
 "items":[{"id":"1","payload":{"profile_url":"https://www.douyin.com/user/MS4w...","pages":3},
   "result":{"profile_url":"https://www.douyin.com/user/MS4w...","sec_uid":"MS4wLjABAAAA...",
             "blogger_nickname":"老司机说车","requested_pages":3,"collected_count":52,
             "settle_charged":15,"refunded_diff":0,
             "videos":[{"aweme_id":"7312...","title":"机油怎么选？一篇讲透","media_type":"4",
                        "digg_count":"1.2万","comment_count":"156","collect_count":"890",
                        "share_count":"45","play_count":"56万","create_time":"03-15",
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
node cli.js export <task_id> --wait --out 主页视频.csv
```

下载任务结果 CSV（BOM 头，Excel 直开不乱码）：任务汇总（主页/状态/实采数/实收点数/退差点数）+ 视频明细（文案/互动数/作者/发布时间/封面/链接）。导出文件保留 7 天。

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

1. 用户说「帮我采集这个抖音博主的作品」→ `node cli.js quota` 确认余额。
2. 和用户确认主页链接、页数；算出预估点数 `页数×5`；**明确告知计费规则并等确认**。
3. `node cli.js collect --url <主页链接> --pages <N> --wait --timeout 600`（不重试）。
4. 如实汇报：实采条数、实收点数、退差点数；简要展示视频列表（文案/互动数/发布时间）。
5. 用户要文件 → `node cli.js export <task_id> --wait --out <文件>.csv`，交付路径。
6. 用户要继续分析 → 可基于视频链接用 dy-collect 补单篇完整互动数或 dy-comments 采评论。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 / 链接无效 | 检查主页链接形态（`/user/<sec_uid>` 或 v.douyin.com 短链）；视频链接引导用 dy-collect（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册走 `register --link`（送 10 点数），已有账号走 `login --link`；完成后 `--check`（退出码 2） |
| LOGIN_PENDING / LOGIN_EXPIRED | 用户未完成 / 会话过期 | 提醒用户完成扫码后重试 `--check`，或重新 `--link`（退出码 2） |
| 2003 | 需要图形验证码 | 终端无法完成，统一走 `--link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| TIMEOUT | 等待超时（任务仍在跑） | 任务未丢：稍后 `query <task_id>` 查终态；预扣仍在，终态后按实采结算 |
| 5001 | 采集服务暂不可用（无在线抖音节点/超时/风控/主页不可见） | 点数已全额返还；稍后重试；持续不可用提示联系客服 18722121663 |
| 4290 | 触发限流 | 稍等后重试（Retry-After） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- **免费**：quota / query / export / config，以及 collect 被参数校验拒绝的请求。
- **预扣**：`页数 × 5`，提交成功立即扣除。
- **结算退差**：任务成功后按 `ceil(实采条数/20) × 5` 实收，差值自动返还（`refunded_diff`）；实采多于预估量时不多收（封顶预扣额）。
- **全额返还**：零结果（博主无作品）、节点离线/超时、风控/登录拦截、主页不可见或账号被封等服务侧失败。
- **不返还**：已成功采集的部分（结果不足请求量时按实采结算，本身就是退差逻辑）。

## 红线

- 仅采集**公开**主页作品数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功或具体条数；风控/结果不足时如实透出（点数按实采结算，用户不损失）。
- 视频列表含作者公开昵称、发布时间等信息：**仅用于用户已授权或公开可获取的调研/分析场景**，遵守平台与数据合规要求；不在未授权场景下转售、滥用；CSV 导出文件请告知用户自行妥善保管。
