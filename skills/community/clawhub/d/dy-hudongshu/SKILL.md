---
name: dy-collect
slug: dy-hudongshu
displayName: 抖音互动数采集
version: 1.0.0
summary: 提交抖音视频链接批量采集点赞/评论/收藏/分享/播放量（社媒指数）与视频文案，一键导出 CSV，用于投放结案、爆款分析与达人视频复盘（1 条视频 = 1 点数）。
description: 抖音视频互动数采集工具（社媒指数）。当用户需要采集/查询抖音视频的点赞数、评论数、收藏数、分享数、播放量等互动指标，提交一批抖音视频链接一键批量采集、导出采集结果 CSV（Excel 直开），或提到"抖音采集/互动数采集/视频数据/播放量/社媒指数"时使用本 skill。适合抖音投放结案、互动数统计、活动效果监测、爆款内容分析、达人视频分析等场景。支持 douyin.com/video/<id> 直链与 v.douyin.com 短链。收费服务（1 条视频 = 1 点数，注册送 10 点）。
---

# 抖音互动数采集 Skill（dy-collect）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用：提交抖音视频链接 → 平台调度内网浏览器节点打开视频页拦截官方接口 → 拿到该视频的**点赞 / 评论数 / 收藏 / 分享 / 播放量**等互动指标（社媒指数）。批量采集，结果直接导出 CSV（BOM 头，Excel 直开不乱码）。

- **能采什么**：公开视频的互动指标（`digg_count` 点赞、`comment_count` 评论数、`collect_count` 收藏、`share_count` 分享数、`play_count` 播放量）、视频文案（`title`）与作者昵称、`aweme_id`。
- **适用场景**：抖音投放结案、互动数统计、活动效果监测、爆款内容分析、达人视频分析等。
- **省心机制**：批量采（单次 1~50 条）、无效链接不扣费、服务侧失败按条自动返还点数（详见「计费规则提示」）、Agent 友好（stdout 纯 JSON + 统一退出码）。
- **不采集评论正文**。需要评论内容请改用评论采集 skill `dy-comments`（会话制，按步计费）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、采集结果异常、批量采购等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **每条有效视频 0.2 元**（每 1 点数抵扣 1 条视频的采集；无效链接不扣费）。
- 注册即送 **10 免费点数**（可采集 10 条视频）；点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 链接要求（重要，提交前必读）

**本 skill 只接受抖音视频链接**，这是硬性要求（客户端提交前会做本地预检——域名白名单与路径格式检查，不通过直接报错、不扣费；服务端还会做更严格校验，未通过的条目判 `invalid` 不计费）：

1. **支持的链接形态**（三种任选）：
   - `https://www.douyin.com/video/<aweme_id>`（标准网页直链）
   - `https://www.douyin.com/note/<aweme_id>`（图文笔记）
   - `https://v.douyin.com/<短码>/`（App 分享短链——**短链直接提交即可**，采集节点浏览器打开后自动跳转还原，无需人工转换）

2. **用户主页链接（`/user/<sec_uid>`）不要提交本 skill**：主页作品列表采集请用 `dy-profile` skill；评论采集请用 `dy-comments` skill。

3. 提交前逐条检查链接；批量场景中只要有一条不合规，本 skill 会拒绝整批提交并列出问题条目（不会部分扣费）。

> agent 工作流提示：拿到用户给的视频链接后先判断形态；`v.douyin.com` 短链直接提交即可，不要反复试错浪费轮次。

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
- 交互提示、轮询进度一律走 **stderr**，不要解析。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。

## 命令清单

### version — 查看版本与安装信息

```bash
node cli.js version
```

输出 skill 名、版本号、能力名、node 版本。升级后建议先跑一次确认版本：

```json
{"ok":true,"data":{"name":"dy-collect","version":"1.0.0","capability":"dy_collect"}}
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

### logout — 登出（切换账号）

```bash
node cli.js logout
```

### submit — 提交采集任务

```bash
node cli.js submit --url "https://www.douyin.com/video/7312345678901234567" \
                   --url "https://v.douyin.com/iAbCdEf/"
node cli.js submit --file urls.txt            # 每行一条视频链接, 忽略空行与 # 注释行
node cli.js submit --file urls.txt --wait     # 提交后轮询等待终态（推荐）
node cli.js submit --url <链接> --force       # 跳过 24h 内容去重强制重提
```

- `--url` 可重复；`--file` 按行读取；二者可混合；总数 1~50 条。
- **链接要求（客户端预检，不通过拒绝整批提交；服务端还有更严格校验，未通过条目判 invalid 不计费）**：`douyin.com/video/<id>`、`/note/<id>` 直链或 `v.douyin.com` 短链；用户主页链接请用 `dy-profile` skill。
- 每条自动生成递增 client_id；幂等键按链接内容派生，同批重试不重复扣费；同一用户同一视频 24h 内默认去重（防重复扣费），`--force` 可强制重提。

输出示例（不带 `--wait`）：

```json
{"ok":true,"data":{"task_id":"t_20261015_708f29","total":2,"valid_count":2,"invalid_count":0,"charged":2,"quota_balance":8,"status":"pending"}}
```

带 `--wait` 时最终输出同 `query` 的完整结果。

### query — 查询任务 / 拉取结果

```bash
node cli.js query <task_id>                          # 查一次
node cli.js query <task_id> --wait                   # 轮询直到终态
node cli.js query <task_id> --wait --interval 3 --timeout 300
```

- `--interval` 轮询间隔秒数（默认 2），`--timeout` 总超时秒数。
- 终态：`done`（全部成功）/ `partial_failed`（部分失败）/ `failed`（全部失败）。

终态输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261015_08b41751","status":"done","success_count":1,"fail_count":0,
 "items":[{"id":1,"video_url":"https://www.douyin.com/video/7312...","status":"success",
   "result":{"aweme_id":"7312345678901234567","title":"机油怎么选？一篇讲透",
             "digg_count":"1.2万","comment_count":"156","collect_count":"890",
             "share_count":"45","play_count":"56万","author_nickname":"老司机说车"}}]}}
```

**解读要点（agent 必读）**：
- 互动数字段为**字符串**；**空串 = 该指标未采集到**（页面未渲染/被拦截），不是 0——向用户解读时注意区分，缺失可稍后重提（24h 去重允许失败重试）。
- 失败条目的 `fail_reason` 会透出具体原因（视频不可见 / 风控拦截等）。

### export — 导出 CSV

```bash
node cli.js export <task_id> --wait --out out.csv
```

生成两段式 CSV（BOM 头，Excel 直开不乱码）：任务汇总 + 视频明细（文案/互动数/作者）。适合把结果直接交给用户。

### config — 配置管理

```bash
node cli.js config set base-url http://127.0.0.1:8084
node cli.js config show        # token 脱敏显示
```

## 典型工作流（agent 照此执行）

1. 检查每条视频链接形态（直链/短链均可直接提交；主页链接引导改用 `dy-profile`）。
2. `node cli.js quota` — 确认剩余点数 ≥ 待采集条数。
3. `node cli.js submit --url <链接1> --url <链接2> ... --wait` — 一步拿到终态结果（条数多时用 `--file`）。
4. 解析 stdout JSON：遍历 `data.items`，把 `status==="success"` 条目的 `result` 五指标整理成表格返回给用户；`failed`/`invalid` 条目附 `fail_reason` 说明。
5. 用户要文件时：`node cli.js export <task_id> --wait --out 社媒指数.csv`，把 CSV 路径交给用户。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 / **链接校验未通过** | 消息里逐条列出问题链接：主页链接改用 `dy-profile`；非官方域名替换正确链接后重提（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册走 `register --link`（送 10 点数），已有账号走 `login --link`；完成后 `--check`（退出码 2） |
| LOGIN_PENDING / LOGIN_EXPIRED | 用户未完成 / 会话过期 | 提醒用户完成扫码后重试 `--check`，或重新 `--link`（退出码 2） |
| 2003 | 需要图形验证码 | 终端无法完成，统一走 `--link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| 3002 | 超单次批量上限 | 拆分为 ≤50 条/批重新提交 |
| 3003 / 3004 | 任务或导出不存在 | 检查 task_id / export_id 是否属于当前账号 |
| 条目 `invalid` | 链接不合法 / 24h 内重复 | 按 fail_reason 提示；重复提交可 `--force` |
| 任务 `partial_failed` | 部分条目失败 | fail_reason 已透出；服务侧/风控原因失败的条目点数已自动返还，可稍后重提 |
| 4290 | 触发限流 | 稍等后重试（Retry-After） |
| TIMEOUT | 轮询超时 | 任务未结束，稍后 `query <task_id>` 再查（退出码 5） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- 提交时按**有效视频条数预扣**（1 条 = 1 点数）；无效链接（非官方域名/格式错误）不扣费。
- **自动返还**：服务侧故障（无在线抖音节点/超时/风控拦截）等未采集到数据的条目，点数按条自动返还（`refunded_quota` 体现），可稍后重提。
- **不返还**：视频不可见（已删除/私密/审核中）属业务性失败，不返还。
- 同一用户同一视频 24h 内默认去重；`--force` 强制重提会正常扣费。

## 红线

- 仅采集**公开**视频数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；风控导致的失败如实透出（fail_reason）。
