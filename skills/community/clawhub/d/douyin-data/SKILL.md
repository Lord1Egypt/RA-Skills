---
name: douyin-data
slug: douyin-data
displayName: 抖音数据采集
summary: 采集抖音视频详情、评论（一级/二级）、用户信息与主页作品、综合搜索、衍生词与分享链接解析（统一 100 点/次，注册送 1000 点），支持翻页、批量、幂等防重复扣点、大响应落盘，适合选品分析、达人与评论分析。
description: 抖音数据采集（视频详情/评论/用户/搜索/衍生词/分享转ID）。当用户需要采集抖音视频详情、抖音评论、抖音用户信息与主页作品、抖音关键词搜索或解析抖音分享链接时使用。对接AI数据平台，按次扣点，批量任务前可免费查询余额与单价。
version: 1.0.9
license: MIT
---

# Skill：抖音数据采集（douyin-data）

对接「AI数据平台」，采集抖音视频、评论、用户与搜索结果。
每次调用消耗平台点数，**单价以 `GET /api/v1/account/balance` 返回的 `price` 字段为准**
（当前统一 100 点/次 = 0.1 元，查询余额本身不扣点）。

## 一、前置条件（缺一不可，先向用户确认）

| 项 | 说明 |
|---|---|
| 平台地址 | **https://zlh.aidata366.com**（正式服务，直接可用）；也可用环境变量 `DY_PLATFORM_BASE_URL` 覆盖 |
| API Key | **推荐直接运行 `login` 自动获取并保存到本机**（见下文「首次使用」）；也可显式设置环境变量 `DY_PLATFORM_API_KEY`，优先级更高 |
| 点数 | 新用户注册赠送 1000 点；不足时按「五、客服与充值」联系客服充值（当前为人工充值） |

> 没有 Key 时不要尝试调用：会返回 `40100`，且浪费排查时间。先执行 `login` 拿 Key。

### 首次使用：一条命令完成登录（推荐）

没有 API Key 时，不要让用户手动去创建，直接执行：

```bash
python dy_api.py login --skill-name douyin-data --ai-entry claude-code
```

把输出里的「二维码图片 / 授权链接」发给用户，让用户扫码或打开链接登录并点「确认授权」。
用户确认后执行（pending 时退出码为 6，3~5 秒后重试即可）：

```bash
python dy_api.py login_check --access-token <上一步输出的 access_token> --skill-name douyin-data --ai-entry claude-code
```

成功后 API Key 会自动保存到 `~/.zhi_liao_hou/config.json`（仅本机），以后所有命令直接调用即可，
无需再设置环境变量；四个 skill 共用这份凭证。授权链接 10 分钟内有效且只能使用一次。

### 备选：手动注册 + 创建 Key（浏览器操作，约 1 分钟）

没有账号或自动登录失败时走这条路；**先注册，再执行上面的 `login`** 即可自动保存 Key。

1. **注册**：浏览器打开 `https://zlh.aidata366.com/auth/register?skill=douyin-data`，填**手机号** →
   输入右侧**图片验证码** → 点「获取短信验证码」→ 填入收到的 6 位短信码 → 提交。
   **用户名和初始密码由平台自动分配**，注册成功页会一次性显示（请提醒用户立即记录，
   尤其是初始密码；登录后可在「总览」页修改）。注册即送 **1000 点**（同一 IP 每天最多
   注册 3 个账号）。注册必须由**用户本人在浏览器完成**（图片码与短信码无法、也不应被脚本绕过）。
2. **创建 API Key**：登录后进入左侧「API Key」页，起个名字点创建。**明文 Key 仅创建成功后
   的那一次页面显示**，立刻复制保存；关掉后只能看到前缀（`jh_` 开头 10 位），丢了只能重建。
3. **配置环境变量**后即可上手：
   ```bash
   export DY_PLATFORM_BASE_URL="https://zlh.aidata366.com"
   export DY_PLATFORM_API_KEY="jh_xxxxxxxx"
   ```

> 登录支持两种方式：**手机号 + 短信验证码**，或**用户名 + 密码**（注册成功页显示的自动分配凭据）。

## 二、安装与 30 秒上手

**安装**：本 skill 只有两个文件（`SKILL.md` + `dy_api.py`），`dy_api.py` 为 **Python 纯标准库实现
（零第三方依赖，Python 3.8+ 可跑）**，把整个 `douyin-data/` 目录放入 agent 的 skills 目录即完成安装。

## AI 调用来源参数（必填）

所有会访问后端 API 的命令必须携带 `--skill-name douyin-data` 和
`--ai-entry <AI工具标识>`（如 `claude-code`）。IP 无需传递，由服务端自动获取。
首次缺参会告警放行，第二次起拒绝。
`login` / `login_check` 也建议携带这两个参数，其余采集命令必须携带。

```bash
export DY_PLATFORM_BASE_URL="https://zlh.aidata366.com"
export DY_PLATFORM_API_KEY="jh_xxxxxxxx"

python dy_api.py balance --skill-name douyin-data --ai-entry claude-code  # 免费：余额 + 各接口单价
python dy_api.py video_detail 7579597758630268186 --skill-name douyin-data --ai-entry claude-code  # 视频详情
python dy_api.py comments aweme_id=7579597758630268186 --out ./c1.json --skill-name douyin-data --ai-entry claude-code  # 一级评论
python dy_api.py search keyword=美食 --out ./search1.json --skill-name douyin-data --ai-entry claude-code  # 综合搜索
```

参数支持三种写法：**位置参数** / **`key=value`** / **整段 JSON**。抖音接口可选参数多，
**批量脚本里建议统一用 `key=value`**，避免位置错位。

CLI 退出码：`0` 成功 ｜ `2` 参数或配置错误（**未发请求、未扣点**）｜ `3` 鉴权或点数问题 ｜ `4` 本次取数失败 ｜ `5` 网络问题 ｜ `6` 等待用户完成授权（`login_check` 轮询时）。
判断成败请看退出码，不要靠 grep 输出。

## 三、命令与接口清单（均 POST，JSON body）

| 命令 | 用途 | 平台路径 | 参数（* 为必填） |
|---|---|---|---|
| `video_detail` | 视频详情 | `/api/v1/douyin/aweme_detail` | `aweme_id`/`share_text` 二选一 |
| `video_detail_v3` | 视频详情 v3 | `/api/v1/douyin/aweme_detail_v3` | `aweme_id`/`share_text` 二选一 |
| `comments` | 一级评论 | `/api/v1/douyin/video_comment` | `aweme_id`/`share_text` 二选一、`cursor`、`count` |
| `replies` | 二级评论 | `/api/v1/douyin/video_sub_comment` | `aweme_id`*、`comment_id`*、`cursor` |
| `user` | 用户信息 | `/api/v1/douyin/user_data` | `sec_user_id`/`share_text` 二选一 |
| `user_posts` | 主页作品 | `/api/v1/douyin/user_post` | `sec_user_id`/`share_text` 二选一、`cursor`、`count` |
| `search` | 综合搜索（**推荐**） | `/api/v1/douyin/general_search2` | `keyword`*、`cursor`、`sort_type` 等筛选 |
| `search_v1` | 综合搜索 v1（**已下架**） | `/api/v1/douyin/general_search` | 同上；调用返回 `40201`，请改用 `search` |
| `suggest` | 衍生词 | `/api/v1/douyin/search_sug` | `keyword`* |
| `share_to_id` | 分享链转 ID | `/api/v1/douyin/share_id_to_web_id` | `share_link`*（**只传纯 URL**） |
| `balance` | 余额/单价（免费） | `GET /api/v1/account/balance` | — |
| `login` | 扫码/链接登录授权（**免费、不扣点**，无需 API Key） | `POST /auth/cli-session` | — |
| `login_check` | 校验授权并保存 API Key（**免费、不扣点**） | `POST /auth/cli-session/check` | `--access-token` |

**只允许传表内参数**：平台按参数白名单转发，未声明的字段会被**静默丢弃**（日志记 `dropped_params`）。
CLI 会在本地直接拒绝未知参数（退出码 2），避免"传了筛选条件却没生效"。

**`share_link` 与 `share_text` 不是一回事**：其它接口的 `share_text` 可以整段传（上游自己提取链接），
但 `share_to_id` 的 `share_link` **只接受纯 URL**。用户给的通常是
「4.87 复制打开抖音… https://v.douyin.com/xxxx/ 口令」这样的整段文案。
本 CLI **1.0.2 起会自动识别并抽出其中的 `https://v.douyin.com/...`**，并在 stderr 提示一行
`# 已从分享文案中提取短链: …`，所以整段直接传也能一次成功。
若你是**直接调 HTTP 接口**（不用本 CLI），必须自己先取纯 URL——整段直传会返回 `50000`
（平台自动退款、不扣点，但白跑一次）。

## 四、计费纪律（必须遵守）

1. **任何批量任务开始前**，先 `balance`：
   - 总成本 = 计划调用次数 × 对应接口 `price`（当前 100 点/次）
   - `总成本 > balance` 时**停止**并告知用户差额（按 `points_per_yuan` 折算成元），
     引导用户按「五、客服与充值」联系客服
2. 单次任务预计超过 **20 次**调用，先向用户确认预算再执行（抖音单次 0.1 元）
3. 循环中每 20 次复查一次 `balance`，发现余额骤降立即停止
4. 拿到 `40200`（点数不足）**立即停止，不要重试**
5. 拿到 `40300`（限频）等待约 60 秒再继续；批量任务默认串行 + 每次间隔 0.5~1 秒
6. 拿到 `50001`（数据服务暂不可用）停止任务，告知用户稍后再试

## 五、客服与充值

### 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、数据结果异常、批量采购等），
请引导用户联系客服，**不要自行尝试绕过或代用户操作**：

- **客服微信**（扫码添加）：<http://st.aidata366.com/assets/concat.png>
- **客服电话**：**18722121663**

### 充值方式（当前为人工充值阶段）

1. 联系客服确认充值金额，**批量/大额采购可洽谈优惠**；
2. 当前兑换率：**1 元 = 1000 点**（1 点 = 0.001 元；抖音各接口 100 点/次 = 0.1 元/次，
   以 `balance` 返回的实时 `price` 为准）；
3. 转账后把**平台用户名 + 转账凭证**告知客服，管理员加点后到平台「充值说明」页刷新即可看到余额；
4. **点数永不过期**；余额、冻结与累计消费可在平台「总览」页自助查询。

> 到账以平台「充值说明」页显示为准；充值前不需要把 API Key 或密码发给客服。

## 六、幂等与重试（防重复扣点）

平台按 `Idempotency-Key` + 「接口 + 请求体指纹」做幂等：

- **CLI 已内置**：默认自动生成幂等键，网络错误/响应超时/并发已满时自动重试 1 次并复用该键，
  重试不会重复扣点。键会打印在 stderr（`# 幂等键: task-xxx`），手工续跑时用 `--idem` 复用。
- 手工 curl 或自写脚本时：**同一次业务调用的所有重试必须复用同一个键**，换接口或改参数会被判 `40910`。
- **大响应特例（几乎所有抖音接口都会遇到）**：平台幂等缓存上限是 **64 KB**，而抖音实测
  视频详情 **78~90 KB**、一级评论约 **48 KB**、搜索 **850~950 KB**、主页作品约 **800 KB**
  —— 也就是说**多数接口的响应都超限**。此时用同一键重放会返回 **`40912`**
  （原响应过大未缓存）：**本次不扣费、也不返回数据**，换一个新 `--idem` 键重新调用即可，
  不要怀疑被重复扣钱。
  > 实践建议：抖音任务**不要指望"重试拿回原响应"**。要重试就把 `--idem` 换成新键（会重新扣 1 次点），
  > 或者把结果 `--out` 落盘后本地重跑。CLI 默认自动重试只在**网络错误**时触发，且会因 40912 而失败退出（退出码 4）。
- 调节重试次数：`--retry 0`（不重试）～`--retry 3`；超时：`--timeout 90`（搜索类建议给足）。

```bash
python dy_api.py video_detail aweme_id=7579597758630268186 --idem task-0001 --skill-name douyin-data --ai-entry claude-code
python dy_api.py search 美食 --retry 2 --timeout 90 --out ./s1.json --skill-name douyin-data --ai-entry claude-code
```

## 七、错误码与处置

| code | 含义 | 可重试 | 处置 |
|---|---|---|---|
| `40000` | 请求体非法 | 否 | 修正 payload（必须是 JSON 对象），不要原样重发 |
| `40100` | API Key 无效 | 否 | 检查 `DY_PLATFORM_API_KEY`，或让用户重新创建 Key |
| `40101` | API Key 已停用 | 否 | 让用户到平台「API Key」页启用/新建 |
| `40200` | 点数不足 | 否 | 停止任务，引导用户按「五、客服与充值」联系客服 |
| `40201` | 接口未开放 | 否 | 该接口已停用，联系客服确认 |
| `40300` | 触发限频 | 是 | 等约 60 秒，降低并发/加间隔 |
| `40910` | 幂等键冲突 | 否 | 该键已用于其它接口或其它参数 → **换新键** |
| `40911` | 同键请求处理中 | 是 | 等 2~3 秒用**同一键**重试一次 |
| `40912` | 原响应过大未缓存 | 否 | 本次未扣费 → 换新 `--idem` 键重新调用 |
| `50000` | 本次取数失败 | 否 | 把 `msg` 转告用户；响应显示退款点数，未退款表示成本已产生 |
| `50001` | 数据服务暂不可用 | 否 | 停止任务，稍后再试 |
| `50002` | 数据服务响应超时 | 是 | 用同一幂等键重试（平台保留幂等记录） |
| `50003` | 平台并发已满 | 是 | 降低并发后重试 |

响应包统一为 `{"code":0,"msg":"success","data":{...},"request_id":"req_..."}`。
`50000` 常见原因：**参数不合法**（如只传了 `cursor` 没传 `aweme_id`）、该视频已删除/私密、
该关键词当前无搜索结果。失败时 `data` 含 `balance`（当前余额）与 `refunded`（本次退回点数）。

## 八、批量采集范式

### 8.1 视频详情批量（串行 + 独立幂等键 + 落盘）

```bash
python dy_api.py balance --skill-name douyin-data --ai-entry claude-code  # 1) 预算预检
mkdir -p out
i=0
while read -r vid; do
  i=$((i+1))
  python dy_api.py video_detail "aweme_id=$vid" --idem "batch-$(date +%Y%m%d)-$i" \
      --out "out/$vid.json" --skill-name douyin-data --ai-entry claude-code
  rc=$?
  case $rc in
    0) ;;
    3) echo "第 $i 条：鉴权或点数问题，终止"; break ;;
    4) echo "第 $i 条：本次取数失败，跳过 $vid" ;;
    5) echo "第 $i 条：网络异常，稍后重跑（复用同一 --idem 键）"; sleep 5 ;;
  esac
  sleep 0.5
done < video_ids.txt
```

### 8.2 评论翻页（先一级、再按 cid 取二级）

```bash
# 一级评论：首页 cursor 留空，之后传响应里的 data.cursor
python dy_api.py comments aweme_id=7579597758630268186 --out out/c_p1.json --skill-name douyin-data --ai-entry claude-code
# 从结果里取 cid（jq 可用则：jq -r '.data.comments[].cid' out/c_p1.json）
# 二级评论
python dy_api.py replies aweme_id=7579597758630268186 comment_id=<cid> --out out/r_<cid>.json --skill-name douyin-data --ai-entry claude-code
```

翻页判断：一级/二级评论看 `data.has_more`，下一页把上次的 `data.cursor` 传回去；
主页作品看 `data.has_more`，下一页把 `data.max_cursor` 作为 `cursor` 传入。
**不要用页码猜**。搜索的翻页规则不同，见 8.3。

### 8.3 搜索（关键词 → 视频列表）

```bash
python dy_api.py search keyword=美食 --out out/search1.json --skill-name douyin-data --ai-entry claude-code  # 结果在 data.business_data[]
python dy_api.py search keyword=美食 cursor=12 --out out/search2.json --skill-name douyin-data --ai-entry claude-code  # 第 2 页
python dy_api.py search keyword=美食 cursor=24 --out out/search3.json --skill-name douyin-data --ai-entry claude-code  # 第 3 页
```

**搜索翻页必须按「已累计条数」传 cursor**（实测结论，很重要）：

- 响应里虽然有 `data.business_config.next_page.cursor`，但它**恒为 12，不会随页回增**，
  直接拿它翻页会一直拿到同一批数据 —— **不要用它翻页**。
- 正确做法：`cursor` = 前面各页已拿到的条数累计值（每页约 11~12 条）。
  实测 `cursor=0/12/24` 三页结果互不重复，累计策略有效。
- 相邻页仍可能出现少量重复（实测 2/11），**必须按 `aweme_id` 去重**后再入库。
- 判断是否还有下一页：看 `data.business_config.has_more`（1 有 / 0 无），
  **注意它不在 `data` 顶层**，别去 `data.has_more` 取。

## 九、数据要点（踩坑清单）

- **怎么拿 ID**：视频链接 `https://www.douyin.com/video/<aweme_id>`；用户主页看 `sec_uid`
  （`MS4wLjABAAAA...`）。只有**分享文案**时，直接把整段文本传给 `share_text`
  （如 `video_detail share_text="7.43 复制打开抖音..."`），或先 `share_to_id` 换成 `aweme_id`。
- **视频详情**：标题 `.desc`、作者 `.author.nickname`、点赞/评论/分享/收藏在 `.statistics`
  （`digg_count` / `comment_count` / `share_count` / `collect_count`）、下载地址在
  `.video.play_addr.url_list[]`。
- **搜索结果结构不同**：`search` 的结果在 **`data.business_data[]`**，每项取
  `.data.aweme_info`（结构与视频详情一致）；`type:1` 是视频卡，个别项是 `card_info` 而非
  `aweme_info`，取值前先判空。不要直接找 `data.data`。
  另：**排序条件下第一条可能是无用数据**，分析时注意剔除。
- **一级评论**：`data.comments[]`，每条含 `cid`（取回复要用）、`text`、`digg_count`、
  `create_time`、`user.nickname`。翻页用 `data.cursor` + `data.has_more`（**注意这里是顶层**）。
  `count` 参数上游**不生效**：传 `count=5` 实测仍返回 10 条，不要靠它控制条数。
- **二级评论**：入参 `comment_id` 必须是**一级评论的 `cid`**，不是视频的 `aweme_id`。
  结果在 `data.comments[]`，同样用 `cursor` + `has_more` 翻页。
- **用户信息**：`data.user{nickname, unique_id, sec_uid, uid, follower_count,
  total_favorited, aweme_count, signature}`。
- **主页作品**：`data.aweme_list[]`，翻页看 `data.has_more` + `data.max_cursor`
  （下一轮把 `max_cursor` 作为 `cursor` 传入）。
- **衍生词**：结果在 `data.sug_list[]`（搜索下拉建议词）。
- **分享链转 ID**：`data.aweme_id` 与 `data.web_link`（标准网页地址）。
- **评论为空是正常业务结果**：`code=0` 但 `comments` 为空，通常是该视频关闭评论或无评论，
  **不要当异常重试**（重试只会白扣点）。
- **响应很大**：综合搜索实测 **850~950 KB**、主页作品约 800 KB、视频详情 78~90 KB、
  一级评论约 48 KB。前两者务必用 `--out` 落盘，否则会刷屏并挤爆上下文。
- **图片/视频地址**：部分字段是 `//` 协议相对地址，展示时补 `https:`。

## 十、排障

1. 记录 `request_id`（响应体里，或错误信息末尾），到平台「调用记录」页按 request_id 查：
   可看到扣点、退款、失败原因与耗时。
2. `50000` 且退款为 0：该次取数成本已产生，按平台规则不退；如需申诉把 request_id
   通过客服（见「五、客服与充值」）提交给运营。
3. **`search_v1` 已于 2026-10-23 下架**（上游持续返回「抖音搜索内容失败」，每次调用会扣 100 再全额退款，
   用户无金钱损失但体验差）。现在调用返回 `40201 接口不存在或未开放`，**不要重试**，
   搜索统一用 `search`（v2），两者单价相同。
4. 全部请求都失败：先 `balance` —— 若返回 `40100/40101` 是 Key 问题；若连接被拒/超时，
   检查平台地址，以及本机是否挂了代理（CLI 默认**不使用**系统代理；确有需要时用
   `DY_PLATFORM_PROXY` 显式指定）。

## 十一、安全要求

- API Key 只从环境变量或本机配置 `~/.zhi_liao_hou/config.json` 读取，**不要写进脚本、
  不要提交到仓库**；登录成功时终端会显示一次，不要把该输出转发到公开渠道。
- 不要把 Key 拼进 URL 或日志；分享排障信息时只给 `request_id`。
- 不要并发轰炸平台（默认串行）；单个 Key 的频率上限由平台配置决定。
- 采集内容用于分析时遵守平台与法律要求，不要用于骚扰、人肉或非法用途。

## 触发词

抖音视频详情、抖音评论采集、抖音二级评论、抖音用户信息、抖音主页作品、
抖音搜索、抖音关键词搜索、抖音衍生词、抖音分享链接解析、抖音数据分析、达人分析
