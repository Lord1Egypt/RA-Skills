# 零配置游客（Guest）通道

> 本文只在**客户端没有可用凭据**时使用：未配置 MCP 连接器，或调工具返回 `401` 且客户端不能自动完成 OAuth。
> 主体流程与判定顺序见 SKILL.md §二；**不要**用本文的创建接口做连通性探测。

## 端点

| 项 | 值 |
|----|----|
| BASE | `https://agent.debtop.com` |
| MCP 端点 | `https://agent.debtop.com/mcp/debt/stream` |
| 取 PoW 挑战 | `GET https://agent.debtop.com/bff/v1/guest-access/challenge` |
| 创建游客（免凭据） | `POST https://agent.debtop.com/bff/v1/guest-access` |
| 刷新游客 | `POST https://agent.debtop.com/bff/v1/guest-access/refresh` |
| 升级为登录用户 | `POST https://agent.debtop.com/bff/v1/guest-access/upgrade` |
| 发现元数据 | `GET https://agent.debtop.com/.well-known/oauth-protected-resource` |

**运行时先读发现元数据的 `x-guest-access`**（不要硬编码端点）：

```json
{
  "x-guest-access": {
    "guest_access_endpoint": "https://agent.debtop.com/bff/v1/guest-access",
    "guest_challenge_endpoint": "https://agent.debtop.com/bff/v1/guest-access/challenge",
    "guest_refresh_endpoint": "https://agent.debtop.com/bff/v1/guest-access/refresh",
    "guest_upgrade_endpoint": "https://agent.debtop.com/bff/v1/guest-access/upgrade",
    "scopes": ["notice:read", "enterprise:read"],
    "public_create": true
  }
}
```

> `public_create` 为 `true` 表示服务端支持免凭据创建（默认开启）；若为 `false`，见文末「若服务端未开启公开通道」。

## 流程（四步）

```text
GET  {BASE}/bff/v1/guest-access/challenge    → 取一次性 PoW 挑战
解 PoW：sha256(challenge+nonce) 前 difficulty 个 bit 为 0   → 得到 nonce
POST {BASE}/bff/v1/guest-access              → {"source":"web","skillId":"<客户端标识>","skillCode":"<本 SKILL 包名>","pow":{...}}
                                             → 得到游客 accessToken
POST {BASE}/mcp/debt/stream (Bearer 游客令牌)  → 调用 4 个只读工具
```

## 游客能力边界

| 维度 | 说明 |
|------|------|
| 用户侧动作 | **无需注册 / 登录 / 填 key / 配任何参数** |
| 游客 scope | `notice:read` + `enterprise:read` + `guest:access` → **4 个工具全部可用** |
| 时效 | access **30 分钟**、refresh **1 天**、单游客最大生命周期 **7 天** |
| 调用限流 | **1 QPS（相邻工具调用必须间隔 ≥1 秒）**、30 次/分、1000 次/天（**共享配额**）。实测：同秒内第 2 次调用即报 `GUEST_LIMITED: ... guest:qps 超过限制 1/sec` |
| 创建限流 | 单 IP 5 次/分钟、单设备指纹 3 次/天、单 IP **3 次/小时**、全局 **500 次/天** |
| 免凭据前提 | 需解出一次 PoW 挑战（防刷机制，正常使用几乎无感：16 bit 通常 <1 秒） |
| 身份标记 | 令牌 `auth_type=guest`、`sub=guest:{guestId}`，可审计、可升级绑定正式用户 |

## 运行前提与替代方案

| 依赖 | 说明 | 缺失时的替代 |
|---|---|---|
| HTTPS 出网 | 必须能访问 `agent.debtop.com` | 无替代；如实告知用户网络不可达 |
| `curl` | 发请求（也可用任何 HTTP 客户端：`python3` 的 `urllib`、平台自带 HTTP 工具） | 用平台自带的 HTTP/requests 能力等价重放 |
| `bash` + `python3` | 执行 `scripts/guest_token.sh` / `scripts/pow_solve.py` | 见下一条 |
| 解 PoW | 16 bit 挑战 | 算法很短，可用**任意语言**实现：求最小整数 `nonce` 使 `sha256(challenge + nonce)` 的前 `difficulty` 个 bit 全为 0（即前 `difficulty/8` 个字节为 0，余数位也需为 0） |
| JSON 取值 | 优先 `jq`，回退 `python3` | 两者都没有时，直接用模型读响应文本取字段 |

> 若平台已把本 MCP 配成连接器（见 SKILL.md §二），**以上依赖全部不需要**——直接调用工具即可。

## 操作速查（可直接复制执行）

```bash
# 0) 只需设 BASE、缓存目录与客户端标识 —— 全程无任何凭据
#    客户端标识 = 创建游客时上报的 skillId（见 references/client-source-ids.md）
#    缓存里是能直接调用后端的令牌, 先收紧 umask, 保证下面新建的文件只允许属主读写
umask 077
export SKILL_ID="<客户端标识>"
export BASE="https://agent.debtop.com"
export CACHE="$HOME/.cache/debtop"; mkdir -p -m 700 "$CACHE"

# JSON 取值小工具：jget '文件' 'a.b.c'（优先 jq，回退 python3）
jget() {
  if command -v jq >/dev/null 2>&1; then jq -r ".$2" "$1"
  else python3 -c 'import json,sys
d=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$1" "$2"
  fi
}

# ①~③ 取游客令牌（脚本内部完成：先复用缓存刷新 → 不可用才取挑战 → 解 PoW → 创建游客 → 落盘 guest.json）
GUEST_TOKEN=$(bash scripts/guest_token.sh "$CACHE/guest.json" "$BASE" "$SKILL_ID")

# ④ MCP 三步握手
# ④a initialize —— 从响应头取 Mcp-Session-Id，后续请求都要带
curl -s -D "$CACHE/h.txt" -o "$CACHE/init.txt" -X POST "$BASE/mcp/debt/stream" \
  -H "Authorization: Bearer $GUEST_TOKEN" -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"debtop-skill","version":"1.0"}}}'
SID=$(grep -i '^mcp-session-id:' "$CACHE/h.txt" | awk '{print $2}' | tr -d '\r')
# ④b notifications/initialized（200/202 即成功）
curl -s -o /dev/null -w "initialized=%{http_code}\n" -X POST "$BASE/mcp/debt/stream" \
  -H "Authorization: Bearer $GUEST_TOKEN" -H "Mcp-Session-Id: $SID" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
# ④c tools/call（结果在 structuredContent）
curl -s -X POST "$BASE/mcp/debt/stream" \
  -H "Authorization: Bearer $GUEST_TOKEN" -H "Mcp-Session-Id: $SID" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_debt_notice","arguments":{"keyword":"有限公司","page_size":5}}}'

# ⑤ 刷新（access 过期时；refreshToken 一次性轮换 → 必须原地覆盖写回）
curl -s -X POST "$BASE/bff/v1/guest-access/refresh" -H 'Content-Type: application/json' \
  -d "{\"refreshToken\":\"$(jget "$CACHE/guest.json" data.refreshToken)\"}" \
  -o "$CACHE/guest.new" && mv "$CACHE/guest.new" "$CACHE/guest.json"
GUEST_TOKEN=$(jget "$CACHE/guest.json" data.accessToken)

# ⑥ 重试链（收到 401 / AUTH_REQUIRED / AUTH_INVALID 时，最多一轮）
#    a) 先执行 ⑤ 刷新；b) 刷新也 401 → 重跑 ①②③ 重建游客（挑战需重新获取）；
#    c) 仍失败 → 按文末「失败的降级路径」处理
```

> 三条硬约束（多实例部署尤要）：**不要并发刷新同一份 `guest.json`**——refresh 使用一次即轮换，重复使用会被判重放并**撤销整条授权链**；多实例/多会话必须**共享同一份** `$CACHE` 并用文件锁串行化「读缓存 → 刷新/创建 → 写回」（各用独立的反而会各自新建游客——这正是"同一个用户建出多个游客"的成因）；令牌是密文，写日志前请打码。
> **创建游客的响应**：统一包装 `{success, code, message, data}`，`data` 含 `guestId` / `accessToken` / `tokenType` / `expiresIn`(1800) / `refreshToken` / `scopes` / `mcpEndpoint`——用 `data.accessToken` 调 MCP、`data.refreshToken` 刷新。
> **脚本用法**：`bash scripts/guest_token.sh [输出文件] [BASE] [客户端标识] [技能包标识]` 成功时 stdout 打印 `access_token`、失败时**非 0 退出**并在 stderr 给出服务端错误码（如 `POW_REQUIRED` / `RATE_LIMITED` / `FEATURE_DISABLED`）；`python3 scripts/pow_solve.py <challenge> <difficulty>` 可单独求解挑战。第 4 个参数（技能包标识）**已默认填好本包名**，通常无需传入。

## 游客归属标识（两个维度：`skillCode` 与 `skillId`）

创建游客时可上报两个**互相独立**的归属字段，让后端把这条游客（以及它之后的所有调用记录）分别归到「哪个 SKILL」与「哪个客户端」：

| 字段 | 回答的问题 | 取值 | 未上报时后端记 |
|---|---|---|---|
| `skillCode` | **这次调用由哪个 SKILL 产生** | **本 SKILL 的包名**：`debtop-counterparty-check`（= 本包 SKILL.md frontmatter 的 `name`，固定不变） | `unknown` |
| `skillId` | 用户从哪个**客户端/平台**来 | 查 `references/client-source-ids.md` | `public_web` |

- **上报方式**：`bash scripts/guest_token.sh "$CACHE/guest.json" "$BASE" "$CLIENT_ID"`——脚本第 3 个参数是客户端标识，第 4 个是技能包标识（**已默认填好本包名，一般不用传**）。
- **两者都要保持稳定**（尤其 `skillCode` 必须始终为本包名）：服务端的创建去重按「技能包 + 客户端 + 来源 + 设备/用户」分组，值来回跳动会被当成不同入口，各自建游客，归属也会随之分裂。
- **归属在创建时确定**：缓存里已有游客时走的是刷新，不会改写归属；换了任一标识需重新创建才生效。
- 省略或不合规（大小写、非法字符、超长）**不影响拿令牌**，服务端只把该项回落（`skillCode` → `unknown`、`skillId` → `public_web`）并计数；出现回落说明标识没对上，按上表 / 本包名核对后再用。
- 两个字段都**只影响归属统计**，不参与鉴权：填错不会导致调用失败，但报表会归错。

## 若服务端未开启公开通道

`GET /challenge` 返回 `404 FEATURE_DISABLED`、或无凭据创建返回 `401 AUTH_REQUIRED`，说明服务端未开放免凭据创建（默认开启，见 SKILL.md §七）。此时：

1. **引导用户完成 OAuth 授权**（标准 MCP 连接器，能力等价），或联系平台开启公开通道；
2. 自建 / 内网部署确实需要用**客户端凭据**创建游客时，按仓库部署文档「Skill 客户端与凭据方式」执行——**游客能力、工具用法与本文完全一致**，只是把"取游客令牌"一步换成凭据方式。

## 令牌过期与刷新（重要）

> 可执行命令见上文速查 **⑤**（刷新）与 **⑥**（重试链）。端点：`POST {BASE}/bff/v1/guest-access/refresh`，请求体 `{"refreshToken":"..."}`。

- refresh 是**一次性轮换**：每次刷新都返回**新的 refreshToken**，返回后必须立即覆盖持久化，旧的作废。
- **同一 refreshToken 被重复使用 = 重放**，服务端会**撤销整条授权链**（该游客全部令牌失效），此时只能重新创建游客。
- 收到 `AUTH_REQUIRED` / `AUTH_INVALID` / 401 时：先 try refresh；refresh 也失败则重新创建游客并重试一次。
- **跨会话/跨调用优先复用同一份 `guest.json`**：access 过期就刷新，不要每次对话都重新创建游客（创建类有配额，且会在后端多建记录）。
- 创建接口按**设备标识**在短时间内去重：窗口内重复创建会返回**同一个 `guestId`** 并换发令牌，因此「刷新失败 → 重建」不会多建游客；`scripts/guest_token.sh` 会自动落盘 `$CACHE/device.id` 作为该标识。
- 换发后旧 refresh 会**静默失效**（返回 `AUTH_INVALID: 无效或已过期`，**不会**撤销整条授权链）——按重试链重建即可，无需人工干预。
- **多实例/多会话并发**时先加锁再读改写缓存（`scripts/guest_token.sh` 内置 `flock`；手工调用 ⑤ 刷新时请自行加锁），否则并发刷新会被判重放并撤销整条链。
- **缓存权限**：`guest.json` 等同"可直接调用后端的口令"，只允许属主读写——目录 `0700`、文件 `0600`。`scripts/guest_token.sh` 已内置（入口 `umask 077`；本次新建的缓存目录直接建为 `0700`，老版本留下的宽权限缓存就地收紧为 `0600`）；手工流程请先 `umask 077`，并对已存在的缓存与 `device.id` 执行 `chmod 600`。因此**多实例共享缓存必须由同一个账号运行**：权限收紧后跨用户共享读不到，而放开权限等于把口令摊给同机其他用户。

## 升级为登录用户（可选）

用户完成 OAuth 授权后，用**用户令牌**绑定当前游客，避免重复画像：

```http
POST https://agent.debtop.com/bff/v1/guest-access/upgrade
Authorization: Bearer {userAccessToken}
Content-Type: application/json

{ "guestId": "g_8f1c2c2d9a6b", "guestRefreshToken": "gfr_2b7e8c1f6d3a" }
```

## 失败的降级路径

| 情况 | 处置 |
|------|------|
| 创建游客返回 401 `AUTH_REQUIRED` | Skill Token 缺失/过期 → 按仓库部署文档「Skill 客户端与凭据方式」重新取 Skill Token |
| 返回 403 `INSUFFICIENT_SCOPE` | Skill 客户端未授 `guest:create`，联系平台侧开通 |
| 返回 429 `RATE_LIMITED` | 触达创建限流（IP/设备），退避后重试 |
| 游客链路整体不可用 | 回退到标准 OAuth 连接器（授权码 + PKCE），功能等价 |
