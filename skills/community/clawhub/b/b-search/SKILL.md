---
name: b-search
slug: b-keyword-search
displayName: B站搜索采集
version: 1.0.0
description: B站关键词搜索采集工具。当用户需要按关键词搜索 B站视频并采集结果列表——标题、简介、播放量、弹幕、收藏、点赞、UP主、封面、视频链接，导出搜索结果 CSV（Excel 直开），或提到"B站搜索/关键词采集/搜索结果采集/话题找稿/竞品关键词调研"时使用本 skill。提交 1 个关键词 + 页数，由内网浏览器节点真人翻页采集，按页计费（一页约 42 条 = 1 点数，注册送 10 点）。适合选题调研、热点监测、竞品内容分析、达人筛选等场景。
---

# B站搜索采集 Skill（b-search）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用：提交搜索关键词 + 页数 → 平台调度内网浏览器节点打开 B站搜索页（`search.bilibili.com/all?keyword=<kw>`）并**点分页器翻页**，拦截官方搜索接口（`x/web-interface/wbi/search/type`）响应 → 采集搜索结果视频列表。

- **能采什么**：搜索结果视频的标题、简介、播放量（`view_count`）、弹幕（`danmaku_count`）、收藏（`collect_count`）、点赞（`like_count`）、UP 主昵称、封面、视频链接与 BV 号。
- **不返回**：评论数/分享数/投币数（B站搜索接口不返回这三项，对应列为空串）。
- **排序**：按 B站默认结果序采集（Web 端无排序/发布时间筛选 UI，本 skill 不提供 `--sort` 参数）。
- **适用场景**：选题调研、热点监测、竞品内容分析、达人筛选。
- **省心机制**：按页计费（1~10 页，每页约 42 条）、结算按实采量退差、零结果或失败全额返还、Agent 友好（stdout 纯 JSON + 统一退出码）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、采集结果异常、批量采购等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **点数换算：0.1 元 = 1 点数。**
- **一页（约 42 条）= 1 点数**：预扣 `页数`，结算按实采量 `ceil(实采条数/42)` 退还差额（不满 42 条的零头按一页计）。
- 注册即送 **10 免费点数**（可采 2 页）；点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 输入要求（重要，提交前必读）

- **只能填搜索关键词**（≤64 字符），**不是链接**：填了 `bilibili.com` 或 `b23.tv` 的链接会被本地预检拒绝（不扣费）。单稿互动数请用 `b-collect`，评论请用 `b-comments`。
- 每任务 **1 个关键词**；需要多个关键词请分多次提交任务。
- 页数 `--pages` 取值 1~10，默认 1。

> agent 工作流提示：用户说「帮我搜一下 B站上关于『机油』的视频」→ 直接 `--keyword 机油 --pages 2`。不要试图传排序/时间筛选参数，B站 Web 搜索不支持。

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
- 交互提示、轮询进度一律走 **stderr**，不要解析。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。

## 命令清单

### version — 查看版本与安装信息

```bash
node cli.js version
```

```json
{"ok":true,"data":{"name":"b-search","version":"1.0.0","capability":"b_search"}}
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

### submit — 提交搜索采集任务

```bash
node cli.js submit --keyword "机油 评测"
node cli.js submit --keyword "机油" --pages 3 --wait
node cli.js submit --keyword "机油" --pages 3 --force     # 跳过 24h 内容去重强制重提
```

- `--pages` 采集页数（1~10，默认 1；每页约 42 条）。
- `--wait` 提交后轮询等待终态（推荐，默认超时 600s；节点翻页约 3-5 分钟）。
- 幂等键按「关键词+页数」派生，同参数重试不重复扣费；同一用户同一关键词 24h 内默认去重，`--force` 可强制重提。

不带 `--wait` 输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261019_7f3a2b","total":1,"valid_count":1,"invalid_count":0,
 "charged":15,"quota_balance":0,"status":"pending",
 "estimated_points":15,"price_per_page":5}}
```

带 `--wait` 的终态输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261019_7f3a2b","status":"done","success_count":1,"fail_count":0,
 "items":[{"id":1,"status":"success",
   "result":{"keyword":"机油","requested_pages":3,"collected_count":126,
             "settle_charged":15,"refunded_diff":0,
             "videos":[{"bvid":"BV1GJ411x7h7","aid":"80433022","title":"机油怎么选？一篇讲透",
                        "description":"...","view_count":"560000","danmaku_count":"2300",
                        "collect_count":"3200","like_count":"12000",
                        "author_nickname":"老司机说车","cover_url":"...",
                        "url":"https://www.bilibili.com/video/BV1GJ411x7h7"}]}}]}}
```

**解读要点（agent 必读）**：
- `collected_count` 是**实采条数**；`settle_charged` 是实收点数，`refunded_diff` 是退还的差额点数——向用户汇报时用这两个字段，不要只报预扣数。
- 互动数字段为**字符串**，**空串 = 该指标未采集到**（搜索接口不返回评论/分享/投币，这几列恒为空），不是 0。
- 一页约 42 条是实测值，实际每页条数由浏览器视口动态算出，会有浮动。

### query — 查询任务 / 拉取结果

```bash
node cli.js query <task_id>                          # 查一次
node cli.js query <task_id> --wait                   # 轮询直到终态
node cli.js query <task_id> --wait --interval 5 --timeout 600
```

终态：`done`（成功）/ `failed`（失败，点数全额返还）。

### export — 导出 CSV

```bash
node cli.js export <task_id> --wait --out out.csv
```

生成两段式 CSV（BOM 头，Excel 直开不乱码）：任务汇总 + 视频明细（标题/简介/播放/弹幕/收藏/点赞/UP主/封面/BV号/链接）。

### config — 配置管理

```bash
node cli.js config set base-url http://127.0.0.1:8084
node cli.js config show        # token 脱敏显示
```

## 典型工作流（agent 照此执行）

1. 确认是**关键词**不是链接（含 `bilibili.com`/`b23.tv` 的一律拒绝，引导改用 `b-collect`）。
2. `node cli.js quota` — 确认剩余点数 ≥ `页数`。
3. `node cli.js submit --keyword "<关键词>" --pages N --wait` — 一步拿到终态结果（节点翻页约 3-5 分钟）。
4. 解析 stdout JSON：把 `result.videos` 整理成表格返回给用户（标题/UP主/播放/弹幕/收藏/点赞），并如实汇报 `settle_charged`（实收点数）与 `refunded_diff`（退差点数）。
5. 用户要文件时：`node cli.js export <task_id> --wait --out B站搜索结果.csv`，把 CSV 路径交给用户。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误（关键词为空/过长/是链接、页数非法） | 换成纯关键词（≤64 字符）后重提；链接请用 `b-collect` skill（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册走 `register --link`（送 10 点数），已有账号走 `login --link`；完成后 `--check`（退出码 2） |
| LOGIN_PENDING / LOGIN_EXPIRED | 用户未完成 / 会话过期 | 提醒用户完成扫码后重试 `--check`，或重新 `--link`（退出码 2） |
| 2003 | 需要图形验证码 | 终端无法完成，统一走 `--link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，或减少 `--pages` 后重提（退出码 3） |
| 3003 / 3004 | 任务或导出不存在 | 检查 task_id / export_id 是否属于当前账号 |
| 任务 `failed` | 零结果 / 采集失败 | fail_reason 已透出；点数已全额返还，可换关键词或稍后重提 |
| 4290 | 触发限流 | 稍等后重试（Retry-After） |
| TIMEOUT | 轮询超时 | 任务未结束，稍后 `query <task_id>` 再查（退出码 5） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- 提交时按**请求页数预扣**（一页 = 1 点数）；关键词不合法不扣费。
- **自动退差**：结算按实采量 `ceil(实采条数/42)`，多扣的差额自动返还（`refunded_diff`）。
- **全额返还**：零结果、采集失败、服务侧故障（无在线 B站节点/超时/风控拦截）。
- 同一用户同一关键词 24h 内默认去重；`--force` 强制重提会正常扣费。

## 红线

- 仅采集**公开**搜索结果数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；风控导致的失败如实透出（fail_reason）。
