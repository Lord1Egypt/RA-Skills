# 零配置游客（Guest）通道

> 本文只在**客户端没有可用凭据**时使用：未配置 MCP 连接器，或调工具返回 `401` 且客户端不能自动完成 OAuth。
> 主体流程与判定顺序见 SKILL.md §二；**不要**用本文的创建接口做连通性探测。
> **动手前先告知用户**（判定顺序见 SKILL.md §二）：游客兜底会在本机缓存目录写入只读凭据文件、并把匿名设备标识上报用于配额去重；
> 得到用户许可后再执行本文命令。

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

> **地址白名单（硬约束）**：携带令牌的请求**只允许发往 `https://agent.debtop.com`**。
> 发现文档里取到的动态端点也要过同一道校验：`scheme` 必须是 `https`、主机必须**恰为** `agent.debtop.com`、且不得带 userinfo；
> 主机不符（端点被改写、或调用方传了别的地址）就**中止并报错**，绝不把令牌发出去。`scripts/guest_token.sh` 已内置该校验，手工调用见下方速查。

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
GET  {BASE}/bff/v1/guest-access/challenge    → 取一次性 PoW 挑战（difficulty 一般为 16）
解 PoW：sha256(challenge+nonce) 前 difficulty 个 bit 为 0   → 得到 nonce
POST {BASE}/bff/v1/guest-access              → {"source":"web","skillId":"<客户端标识>","skillCode":"<本 SKILL 包名>","pow":{...}}
                                             → 得到游客 accessToken（写入本机缓存文件，不打印）
POST {BASE}/mcp/debt/stream (Bearer 游客令牌)  → 调用 4 个只读工具
```

## 游客能力边界

| 维度 | 说明 |
|------|------|
| 用户侧动作 | **无需注册 / 登录 / 填 key / 配任何参数**（但首次走游客兜底前应先告知用户，见文首） |
| 游客 scope | `notice:read` + `enterprise:read` + `guest:access` → **4 个工具全部可用** |
| 时效 | access **30 分钟**、refresh **1 天**、单游客最大生命周期 **7 天** |
| 调用限流 | **1 QPS（相邻工具调用必须间隔 ≥1 秒）**、30 次/分、1000 次/天（**共享配额**）。实测：同秒内第 2 次调用即报 `GUEST_LIMITED: ... guest:qps 超过限制 1/sec` |
| 创建限流 | 单 IP 5 次/分钟、单设备指纹 3 次/天、单 IP **3 次/小时**、全局 **500 次/天** |
| 免凭据前提 | 需解出一次 PoW 挑战（防刷机制，正常使用几乎无感：16 bit 通常 <1 秒）。`scripts/pow_solve.py` 对难度与耗时都有硬上限（默认 ≤20 bit、≤30 秒），超出即报错不求解 |
| 身份标记 | 令牌 `auth_type=guest`、`sub=guest:{guestId}`，可审计、可升级绑定正式用户 |

## 运行前提与替代方案

| 依赖 | 说明 | 缺失时的替代 |
|---|---|---|
| HTTPS 出网 | 必须能访问 `agent.debtop.com`（白名单主机） | 无替代；如实告知用户网络不可达 |
| `curl` | 发请求（也可用任何 HTTP 客户端：`python3` 的 `urllib`、平台自带 HTTP 工具） | 用平台自带的 HTTP/requests 能力等价重放 |
| `bash` + `python3` | 执行 `scripts/guest_token.sh` / `scripts/pow_solve.py`（**先取用户许可**） | 见下一条 |
| 解 PoW | 16 bit 挑战（难度上限 20 bit、求解上限 30 秒，均可由运行方下调） | 算法很短，可用**任意语言**实现：求最小整数 `nonce` 使 `sha256(challenge + nonce)` 的前 `difficulty` 个 bit 全为 0（即前 `difficulty/8` 个字节为 0，余数位也需为 0）；实现方**必须**自带难度上限与耗时上限 |
| JSON 取值 | 优先 `jq`，回退 `python3` | 两者都没有时，直接用模型读响应文本取字段 |
| 写缓存 | 令牌与设备标识只写入 `$HOME/.cache/debtop/`（或用 `DEBTOP_CACHE_DIR` 指到会话工作区内），权限 0700/0600 | 平台不允许写用户主目录时，设 `DEBTOP_CACHE_DIR` 指向可写目录；不允许任何写盘时，走 OAuth 连接器路径 |

> 若平台已把本 MCP 配成连接器（见 SKILL.md §二），**以上依赖全部不需要**——直接调用工具即可。

## 本地副作用与清理（如实披露）

走游客兜底时，脚本会在缓存目录（默认 `$HOME/.cache/debtop/`，可用 `DEBTOP_CACHE_DIR` 改到会话工作区内）产生下列文件，**除此之外不读取、不写入任何本地文件**：

| 文件 | 内容 | 权限 / 生命周期 |
|---|---|---|
| `guest.json` | 游客 `accessToken` / `refreshToken` / `guestId` / `scopes` 等（等同口令，可直接调用后端） | `0600`；refresh 时原地覆盖；access 30 分钟、refresh 1 天、最长 7 天后失效 |
| `device.id` | 本机随机生成的 128 bit 匿名标识（不含硬件与个人信息） | `0600`；创建游客时作为 `deviceFingerprint` 上报，**仅用于配额去重**（避免同一用户反复建游客）；长期保留直到删除缓存 |
| `guest.json.lock` / `guest.json.lock.d/` | 串行锁：有 `flock` 时用锁文件，没有时（如 macOS 默认）退化为 `mkdir` 原子锁目录 | `0600` / `0700`，进程退出即释放 |
| `guest.json.XXXXXX` / `guest.new` | 刷新/创建写回时的临时文件，按进程唯一（`mktemp`，失败即删） | `0600`，瞬时存在 |
| `curl-auth.conf` / `refresh.conf` / `h.txt` / `init.txt` | 手工速查流程用：`Authorization` 头与刷新请求体的 `curl` 配置文件、握手响应头与响应体（都不含新凭据，但含令牌的配置文件同样是敏感文件） | `0600`，用完即删 |

- **读取的宿主平台变量**：`DEBTOP_CLIENT_NAME`（若存在，仅用于推断客户端标识 `skillId`）；`DEBTOP_CACHE_DIR` / `DEBTOP_POW_MAX_DIFFICULTY` / `DEBTOP_POW_MAX_SECONDS`（可选，用于调整缓存位置与求解护栏）。
- **上报内容**：创建游客时报 `skillId`（客户端标识）、`skillCode`（本技能包名）、`deviceFingerprint`（上面的匿名标识），目的地为本服务 `agent.debtop.com`，**仅用于来源归属统计与配额防滥用**；不向任何第三方转发。
- **清理方式**：`rm -rf "$HOME/.cache/debtop"`（或用 `DEBTOP_CACHE_DIR` 指定的目录）。删除后本机不再保留任何游客凭据，下次使用会重新申请游客令牌。

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
#    脚本自带地址白名单（只发往 agent.debtop.com）与输出路径收敛（只能落在 $CACHE 内），
#    成功时**只把令牌写进 0600 的缓存文件**、不再打印到 stdout（避免进入命令行与会话记录）。
bash scripts/guest_token.sh "$CACHE/guest.json" "$BASE" "$SKILL_ID"

# ④ 把 Authorization 头放进 0600 的 curl 配置文件：令牌不出现在命令行（ps 看不到）
AUTH_CONF="$CACHE/curl-auth.conf"
python3 - "$CACHE/guest.json" "$AUTH_CONF" <<'PY'
import json, os, sys
token = (json.load(open(sys.argv[1])).get("data") or {}).get("accessToken")
if not token:
    sys.exit("guest.json 里没有 accessToken：先跑 guest_token.sh")
fd = os.open(sys.argv[2], os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
os.write(fd, f'header = "Authorization: Bearer {token}"\n'.encode())
os.close(fd)
PY

# ⑤ MCP 三步握手（Authorization 由 -K 配置文件注入，下文所有请求都复用同一份）
# ⑤a initialize —— 从响应头取 Mcp-Session-Id，后续请求都要带
curl -s -K "$AUTH_CONF" -D "$CACHE/h.txt" -o "$CACHE/init.txt" -X POST "$BASE/mcp/debt/stream" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"debtop-skill","version":"1.0"}}}'
SID=$(grep -i '^mcp-session-id:' "$CACHE/h.txt" | awk '{print $2}' | tr -d '\r')
# ⑤b notifications/initialized（200/202 即成功）
curl -s -K "$AUTH_CONF" -o /dev/null -w "initialized=%{http_code}\n" -X POST "$BASE/mcp/debt/stream" \
  -H "Mcp-Session-Id: $SID" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
# ⑤c tools/call（结果在 structuredContent）
curl -s -K "$AUTH_CONF" -X POST "$BASE/mcp/debt/stream" \
  -H "Mcp-Session-Id: $SID" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_debt_notice","arguments":{"keyword":"有限公司","page_size":5}}}'

# ⑥ 刷新（access 过期时；refreshToken 一次性轮换 → 必须原地覆盖写回）
#    三件事缺一不可: 加锁（并发刷新会被判重放并撤销整条授权链）、先校验响应成功、再覆盖缓存
#    优先直接调用 scripts/guest_token.sh（它自带锁与全部校验）；确需手工执行时按下述加锁
if command -v flock >/dev/null 2>&1; then
  exec 9>"$CACHE/guest.json.lock"; flock 9
else
  waited=0
  until mkdir "$CACHE/guest.json.lock.d" 2>/dev/null; do
    [ "$waited" -ge 60 ] && { echo "等待缓存锁超时：请改用 bash scripts/guest_token.sh" >&2; exit 1; }
    sleep 0.5; waited=$((waited + 1))
  done
  trap 'rm -rf "$CACHE/guest.json.lock.d"' EXIT
fi
# refreshToken 同样不进命令行: 请求体写进 0600 的临时配置文件, 用 curl -K 读取
python3 - "$CACHE/guest.json" "$CACHE/refresh.conf" <<'PY'
import json, os, sys
body = json.dumps({"refreshToken": (json.load(open(sys.argv[1])).get("data") or {}).get("refreshToken") or ""})
fd = os.open(sys.argv[2], os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
os.write(fd, ("data = " + json.dumps(body) + "\n").encode())
os.close(fd)
PY
curl -sS --max-time 20 -X POST "$BASE/bff/v1/guest-access/refresh" -H 'Content-Type: application/json' \
  -K "$CACHE/refresh.conf" -o "$CACHE/guest.new" -w 'http=%{http_code}\n' -S
rm -f "$CACHE/refresh.conf"
# 只有确实是成功体（含 data.accessToken）才覆盖缓存；错误响应一律不写进 guest.json
if python3 -c 'import json,sys
d=(json.load(open(sys.argv[1])).get("data") or {})
sys.exit(0 if d.get("accessToken") else 1)' "$CACHE/guest.new"; then
  mv "$CACHE/guest.new" "$CACHE/guest.json" && chmod 600 "$CACHE/guest.json"
  echo "已刷新并原地覆盖 guest.json（旧 refreshToken 作废）"
else
  echo "刷新失败，缓存未被覆盖（保留原令牌）" >&2
  rm -f "$CACHE/guest.new"
fi
# 刷新后要重跑 ④ 重建 curl-auth.conf（accessToken 已更换）

# ⑦ 重试链（收到 401 / AUTH_REQUIRED / AUTH_INVALID 时，最多一轮）
#    a) 先执行 ⑥ 刷新（复用缓存，无创建配额消耗）；b) 刷新也 401 → 重跑 ①~③ 重建游客
#    （重建会新建游客并消耗创建配额：需先告知用户，见 SKILL.md §二）；c) 仍失败 → 按文末降级
```

> 三条硬约束（多实例部署尤要）：**不要并发刷新同一份 `guest.json`**——refresh 使用一次即轮换，重复使用会被判重放并**撤销整条授权链**；多实例/多会话必须**共享同一份** `$CACHE` 并用文件锁串行化「读缓存 → 刷新/创建 → 写回」（各用独立的反而会各自新建游客——这正是"同一个用户建出多个游客"的成因）；**令牌不进命令行也不进日志**：用 `-K` 配置文件传 `Authorization`，任何日志输出都要把令牌打码。
> **创建游客的响应**：统一包装 `{success, code, message, data}`，`data` 含 `guestId` / `accessToken` / `tokenType` / `expiresIn`(1800) / `refreshToken` / `scopes` / `mcpEndpoint`——用 `data.accessToken` 调 MCP、`data.refreshToken` 刷新。
> **脚本用法**：`bash scripts/guest_token.sh [输出文件] [BASE] [客户端标识] [技能包标识]` 成功时把 `access_token` 写进 0600 的输出文件（**不打印令牌**，stderr 只给路径提示）、失败时**非 0 退出**并在 stderr 给出服务端错误码（如 `POW_REQUIRED` / `RATE_LIMITED` / `FEATURE_DISABLED`），参数越界/地址不在白名单/远端字段异常时以 `64` 拒绝执行；`python3 scripts/pow_solve.py <challenge> <difficulty>` 可单独求解挑战（自带难度上限 20 bit 与 30 秒上限，`--max-seconds` / `--max-difficulty` 可调）。第 4 个参数（技能包标识）**已默认填好本包名**，通常无需传入。

## 游客归属标识（两个维度：`skillCode` 与 `skillId`）

创建游客时可上报两个**互相独立**的归属字段，让后端把这条游客（以及它之后的所有调用记录）分别归到「哪个 SKILL」与「哪个客户端」：

| 字段 | 回答的问题 | 取值 | 未上报时后端记 |
|---|---|---|---|
| `skillCode` | **这次调用由哪个 SKILL 产生** | **本 SKILL 的包名**：`debtop-collateral-check`（= 本包 SKILL.md frontmatter 的 `name`，固定不变） | `unknown` |
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

> 可执行命令见上文速查 **⑥**（刷新）与 **⑦**（重试链）。端点：`POST {BASE}/bff/v1/guest-access/refresh`，请求体 `{"refreshToken":"..."}`。

- refresh 是**一次性轮换**：每次刷新都返回**新的 refreshToken**，返回后必须立即覆盖持久化，旧的作废。
- **同一 refreshToken 被重复使用 = 重放**，服务端会**撤销整条授权链**（该游客全部令牌失效），此时只能重新创建游客（需先告知用户）。
- 收到 `AUTH_REQUIRED` / `AUTH_INVALID` / 401 时：先 try refresh；refresh 也失败则按「重试链」重建游客并重试一次。
- **跨会话/跨调用优先复用同一份 `guest.json`**：access 过期就刷新，不要每次对话都重新创建游客（创建类有配额，且会在后端多建记录）。
- 创建接口按**设备标识**在短时间内去重：窗口内重复创建会返回**同一个 `guestId`** 并换发令牌，因此「刷新失败 → 重建」不会多建游客；`scripts/guest_token.sh` 会自动落盘 `$CACHE/device.id` 作为该标识。
- 换发后旧 refresh 会**静默失效**（返回 `AUTH_INVALID: 无效或已过期`，**不会**撤销整条授权链）——按重试链重建即可，无需人工干预。
- **多实例/多会话并发**时先加锁再读改写缓存（`scripts/guest_token.sh` 内置锁：优先 `flock`，没有 `flock` 的平台退化为 `mkdir` 原子锁目录并按 0.5 秒退避重试、超时 30 秒报错；手工调用 ⑥ 刷新时已自带加锁），否则并发刷新会被判重放并撤销整条链。
- **缓存权限与位置**：`guest.json` 等同"可直接调用后端的口令"，只允许属主读写——目录 `0700`、文件 `0600`。`scripts/guest_token.sh` 已内置（入口 `umask 077`；本次新建的缓存目录直接建为 `0700`，老版本留下的宽权限缓存就地收紧为 `0600`），并且**只允许把缓存写在 `$HOME/.cache/debtop`（或 `DEBTOP_CACHE_DIR` 指定的目录）之内**、拒绝符号链接与越界路径；手工流程请先 `umask 077`，并对已存在的缓存与 `device.id` 执行 `chmod 600`。因此**多实例共享缓存必须由同一个账号运行**：权限收紧后跨用户共享读不到，而放开权限等于把口令摊给同机其他用户。

## 升级为登录用户（可选）

用户完成 OAuth 授权后，用**用户令牌**绑定当前游客，避免重复查询（`guestId` 与 refresh 令牌从本机 `guest.json` 读取，示例中是**占位符**，不要写入任何真实游客的取值）：

```http
POST https://agent.debtop.com/bff/v1/guest-access/upgrade
Authorization: Bearer {userAccessToken}
Content-Type: application/json

{ "guestId": "g_<guestId>", "guestRefreshToken": "gfr_<refreshToken>" }
```

## 失败的降级路径

| 情况 | 处置 |
|------|------|
| 创建游客返回 401 `AUTH_REQUIRED` | Skill Token 缺失/过期 → 按仓库部署文档「Skill 客户端与凭据方式」重新取 Skill Token |
| 返回 403 `INSUFFICIENT_SCOPE` | Skill 客户端未授 `guest:create`，联系平台侧开通 |
| 返回 429 `RATE_LIMITED` | 触达创建限流（IP/设备），退避后重试 |
| 脚本以 `64` 退出（地址不在白名单 / 输出路径越界 / 远端字段不合法） | **不要改脚本绕过校验**：核对 `BASE` 与输出路径是否符合白名单与缓存目录约束；远端难度异常时停止重试并如实告知用户 |
| 游客链路整体不可用 | 回退到标准 OAuth 连接器（授权码 + PKCE），功能等价 |
