# DevSpace 配置与启动（阶段 4–5）

> 阶段 4 = 写配置；阶段 5 = 启动服务。另含**环境变量总表**、**换可访问目录**、
> **重启与 OAuth 持久化**三个横切主题。
> 主流程见 SKILL.md；本文件是完整细节。
> **路径写法、大小写敏感性、状态目录的平台差异见 `references/cross-platform.md`。**

下文用到的脚本目录变量（与 SKILL.md 一致）：

```bash
SK=~/.workbuddy/skills/chatgpt-mcp-connector/scripts          # macOS / Linux
# Windows: set "SK=%USERPROFILE%\.workbuddy\skills\chatgpt-mcp-connector\scripts"
```

Windows 上 `~` 不展开；示例里的 `$SK` 换成 `%SK%`（cmd）或 `"$SK"`（PowerShell）。

## 阶段 4：写 DevSpace 配置

产物就两个文件，都在 DevSpace 的**配置目录**里（源码 `devspaceConfigDir()` = `DEVSPACE_CONFIG_DIR` ?? `~/.devspace`）：

| 平台 | 配置目录 |
| --- | --- |
| Windows | `C:\Users\<你>\.devspace\` |
| macOS | `/Users/<你>/.devspace/` |
| Linux | `/home/<你>/.devspace/` |

两个文件：

- `config.json` — `host` / `port` / `publicBaseUrl` / `allowedRoots` / `subagents` / …
- `auth.json` — `{ "ownerToken": "<43 字符>" }`，即授权页要填的 **Owner password**

### 路径 A：交互式（人手动做）

```bash
devspace init            # 会问：用途(ChatGPT/Coding Agents/两者) → 项目根 → 子代理 → publicBaseUrl
devspace init --force    # 重新生成（**会重问所有问题**，慎用）
```

要点：用途要选含 **ChatGPT**，否则**根本不会写 `allowedRoots`**（见下面「坑」）；
`publicBaseUrl` 填 **origin，不带 `/mcp`**（如 `https://xxx.ts.net`）。

### 路径 B：全自动（agent 用）★

**关键机制（读 `dist/cli.js` 确认）**：

```js
const files = loadDevspaceFiles();
if (files.configExists && files.authExists) return;       // ← 两个文件都在 → 直接跳过 init
if (process.env.DEVSPACE_OAUTH_OWNER_TOKEN) return;
if (!input.isTTY || !output.isTTY) { throw new Error([... "Or provide DEVSPACE_OAUTH_OWNER_TOKEN."]) }
await runInit({ force: false });
```

结论：

1. **只要 `config.json` + `auth.json` 都存在，`devspace serve` 完全不需要交互** → 直接写这两个文件即可。
2. 在**非 TTY 环境**（agent、CI、管道）下，如果这两个文件缺失，`serve` 会**直接报错退出**，
   除非提供 `DEVSPACE_OAUTH_OWNER_TOKEN`。**所以别指望在非交互环境里跑 `devspace init`。**

推荐用自带脚本（它会保留已有 ownerToken、幂等、写前备份）：

```bash
node $SK/devspace-bootstrap.mjs apply --roots "D:\projects\my-app"          # Windows
node $SK/devspace-bootstrap.mjs apply --roots "/home/you/projects/my-app"   # macOS / Linux
```

或手写。`ownerToken` 的生成方式与官方一致（`dist/user-config.js`）：

```js
// generateOwnerToken() === randomBytes(32).toString("base64url")  → 43 字符
{ "ownerToken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" }  // auth.json 是【明文】
```

> 网上有说法称 `auth.json` 存的是哈希 —— **错的**，实测是明文 `ownerToken`，
> 可直接填进授权页，不需要向用户索要，也不需要重新生成。

### 配置解析优先级（读 `dist/config.js` 确认）

| 键 | 优先级 |
| --- | --- |
| 可访问目录 | `DEVSPACE_ALLOWED_ROOTS` > `config.allowedRoots` > **`process.cwd()`（兜底）** |
| 公网地址 | `DEVSPACE_PUBLIC_BASE_URL` > `config.publicBaseUrl` > `localPublicBaseUrl(host, port)` |
| 端口 / 主机 | `PORT` / `HOST` env > 配置文件 > `7676` / `127.0.0.1` |

**坑**：`devspace init` 里收集 `allowedRoots` 的代码包在 `if (useChatGpt) { … }` 分支内。
所以如果初始化时**没选 ChatGPT 路径**，`config.json` 里**根本没有 `allowedRoots` 这个键**，
运行时就一直兜底成「启动时的当前目录」—— 表现是「它只认那一个文件夹」。别以为配置坏了。

> 另外 `allowedHosts` 是**从 `publicBaseUrl` 自动推导**的（`new URL(publicBaseUrl).hostname` 会进白名单），
> 所以改了 `publicBaseUrl` 不用另外配 host 白名单。

## 阶段 5：启动服务

```bash
cd <你想当默认工作目录的文件夹>     # allowedRoots 未配时，这里决定它能碰哪儿
devspace serve
```

启动日志（实测）—— **`allowed roots:` 这一行就是验收点**：

```
devspace listening on http://127.0.0.1:7676/mcp
public base url: https://my-desktop.tail1234.ts.net
allowed roots: D:\projects\my-app
allowed hosts: localhost, 127.0.0.1, ::1, my-desktop.tail1234.ts.net
auth: Owner password approval required
subagent providers: codex (usable), claude (usable), opencode (usable), pi (usable), cursor (disabled), ...
```

注意 **`devspace serve` 必须常驻**：进程一停 ChatGPT 就断。Funnel 配置本身是持久的，不用重配。

### 健康检查

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:7676/healthz              # 200
curl -s -o /dev/null -w "%{http_code}\n" https://<域名>/healthz                     # 200
curl -s -o /dev/null -w "%{http_code}\n" https://<域名>/mcp                         # 401 ← 正常！
curl -s https://<域名>/.well-known/oauth-protected-resource/mcp                     # 200 + JSON
```

`/mcp` 匿名返回 **401** 是**正确**的，响应头带
`WWW-Authenticate: Bearer ... resource_metadata="https://<域名>/.well-known/oauth-protected-resource/mcp"`，
这是 OAuth 触发点，不是故障。

## 换可访问目录（allowedRoots）

```bash
# A. 环境变量（临时/脚本，优先级最高）
#    ⚠️ 分隔符【三平台都是逗号】—— 不是 Windows 的 ; 也不是 PATH 的 :（源码里统一 split(",")）
DEVSPACE_ALLOWED_ROOTS="D:\\projects\\my-app,D:\\workspace" devspace serve     # Windows
DEVSPACE_ALLOWED_ROOTS="/home/you/projects/my-app,/srv/repos" devspace serve   # macOS / Linux

# B. 写进配置目录下的 config.json（持久，推荐）
#    Windows 的 JSON 里反斜杠要转义；macOS / Linux 用正斜杠
# { "allowedRoots": ["D:\\projects\\my-app"] }       ← Windows
# { "allowedRoots": ["/home/you/projects/my-app"] }  ← macOS / Linux
```

改完**必须重启 `devspace serve`**（配置只在启动时读一次）。
用 `devspace config set` **改不了**这个键（它只支持 `publicBaseUrl`）。
也**别用** `devspace init --force` 去改 —— 会重问所有问题，且不走 ChatGPT 分支时反而不写 roots。

推荐用脚本（幂等、自动归一化、会告警盘符级白名单）：

```bash
node $SK/devspace-bootstrap.mjs apply --roots "D:\projects\my-app" --dry-run   # 先预演（Windows）
node $SK/devspace-bootstrap.mjs apply --roots "D:\projects\my-app"            # 再落盘（Windows）
# macOS / Linux 把路径换成 /home/you/projects/my-app 这种正斜杠写法即可
```

> **大小写敏感性按平台不同**：Windows 与 macOS 的文件系统不敏感（`~/Projects` 与 `~/projects` 同一个），
> Linux 敏感（是**两个不同目录**）。脚本的去重逻辑已按平台处理，别手动去重时按小写合并。

### ⚠️ 两个会让人误判「白名单配错了」的坑

**① WSL 的 `/mnt/c/...` 路径永远不通（在 Windows 上）**

DevSpace 是 **Windows 进程**，它眼里的 `/mnt/f/projectL` 不是「F 盘」——
`path.resolve('/mnt/f/projectL')` 在 Windows 上把开头的 `/` 当成**当前盘**的根，得到 `C:\mnt\f\projectL`。
于是报错 `Path is outside allowed roots: /mnt/f/projectL`（报错回显的是**原始输入**，不是解析结果，容易误导）。

| 你给的路径 | Windows 上解析成 | 结果 |
| --- | --- | --- |
| `/mnt/f/projectL` | `C:\mnt\f\projectL` | ❌ 拒绝 |
| `/mnt/f/chatgpt_work/projectL` | `C:\mnt\f\chatgpt_work\projectL` | ❌ 拒绝（连白名单里的那个也拒） |
| `F:\chatgpt_work\projectL` | `F:\chatgpt_work\projectL` | ✅ 通过 |

**结论：交给 ChatGPT / DevSpace 的路径必须是本机原生写法**（Windows 用 `F:\...`，macOS/Linux 用 `/home/...`）。
`/mnt/...` 只在 WSL 内部有意义，跨到 Windows 进程就必然失败。
这个路径通常是从 WSL 里的 `pwd -P` / `realpath` / `git rev-parse --show-toplevel` 抄出来的 ——
**取路径要在 PowerShell / cmd 里取**，别在 WSL 里取。

**② 白名单检查不解析 junction / symlink（issue #45）→ 两道反直觉**

`isPathInsideRoot()` 只做 `path.resolve()` 的**纯字符串比较，不调 realpath**（`dist/roots.js`）。
于是：

- **junction 放在白名单里 = 白名单被绕过**：`F:\chatgpt_work\projectL` 若是指向 `F:\projectL` 的 junction，
  逻辑路径看起来在根内 → **通过**，但实际读写的是根**外**的 `F:\projectL`。
- **把 junction 解析后的真实路径交上去 = 被拒**：`F:\projectL` 不在白名单里 → 拒绝。

排查时先跑一句 `realpath` 看目标落在哪，别只看 `config.json`：

```bash
# Windows（PowerShell）
(Get-Item 'F:\chatgpt_work\projectL').Target      # 是 junction 时显示目标
# 跨平台（Node）
node -e "console.log(require('fs').realpathSync.native('F:\\chatgpt_work\\projectL'))"
```

想要真实约束，就把**真实路径**写进白名单（`--roots "F:\projectL,D:\workspace\lunhuiwendao"`），
或者干脆不用 junction、把项目实体放进白名单目录里。

### ⚠️ Git Bash 会把 `D:\x` 改写成 `D:/x`

MSYS / Git Bash 的参数路径转换会动 `\`。`D:\projects\my-app` 传给脚本后可能变成 `D:/projects/my-app`。
Node 的 path 解析两者等价，**功能不受影响**，但会让「内容是否变化」的判断失效。
所以脚本里统一用 `path.resolve()` 归一化（Windows 上归成 `D:\x`）。
手写配置时直接写 `"D:\\projects\\my-app"` 即可。

## 环境变量总表（读 `dist/config.js` 汇总）

| 变量 | 作用 | 默认 |
| --- | --- | --- |
| `DEVSPACE_ALLOWED_ROOTS` | 可访问根，**逗号分隔** | `process.cwd()` |
| `DEVSPACE_PUBLIC_BASE_URL` | 公网 origin（临时隧道用） | 配置文件 / `http://host:port` |
| `DEVSPACE_ALLOWED_HOSTS` | Host 头白名单，`*` 关闭（会 warn） | 由 `publicBaseUrl` 推导 |
| `DEVSPACE_OAUTH_OWNER_TOKEN` | 免配置文件提供 Owner password | — |
| `DEVSPACE_OAUTH_ACCESS_TOKEN_TTL_SECONDS` | access token 有效期 | 内置默认 |
| `DEVSPACE_OAUTH_REFRESH_TOKEN_TTL_SECONDS` | refresh token 有效期 | 内置默认（实测约 30 天） |
| `DEVSPACE_OAUTH_SCOPES` | 作用域 | `devspace` |
| `DEVSPACE_OAUTH_ALLOWED_REDIRECT_HOSTS` | 允许的重定向主机 | `chatgpt.com,localhost,127.0.0.1` |
| `DEVSPACE_TOOL_MODE` | `minimal` / `full` / `codex` | `minimal` |
| `DEVSPACE_WIDGETS` | `full` / `off` / `changes` | — |
| `DEVSPACE_SUBAGENTS` | 开关子代理 | 配置文件 |
| `DEVSPACE_STATE_DIR` | 状态目录（SQLite） | `~/.local/share/devspace` |
| `DEVSPACE_WORKTREE_ROOT` | worktree 根 | `~/.devspace/worktrees` |
| `DEVSPACE_LOG_LEVEL` | `silent`/`error`/`warn`/`info`/`debug` | `info` |
| `DEVSPACE_LOG_FORMAT` | `json` / `pretty` | `json` |
| `DEVSPACE_LOG_REQUESTS` / `_ASSETS` / `_TOOL_CALLS` / `_SHELL_COMMANDS` | 各类日志开关 | 见源码 |
| `DEVSPACE_TRUST_PROXY` | 开 Express trust proxy | `false` |
| `DEVSPACE_CONFIG_DIR` | **配置目录**（放 `config.json` / `auth.json`） | `~/.devspace` |
| `DEVSPACE_ARTIFACTS` | 开关 `download_artifact` 工具 | 配置文件 |
| `DEVSPACE_ARTIFACT_MAX_FILE_BYTES` | 单个附件大小上限 | 内置默认 |
| `DEVSPACE_AGENT_DIR` | 本地子代理目录 | `~/.codex` |
| `DEVSPACE_SKILLS` / `DEVSPACE_SKILL_PATHS` | skills 开关 / 搜索路径（**逗号**分隔） | — |
| `DEVSPACE_MINIMAL_TOOLS` | 工具集裁剪 | 见源码 |
| `PORT` / `HOST` | 监听端口 / 地址 | 配置文件 / `7676` / `127.0.0.1` |

> **`download_artifact` 只在 Linux 上注册。** 源码 `ARTIFACT_DOWNLOAD_PLATFORMS = new Set(["linux"])`，
> 在 Windows / macOS 上这个工具**根本不会出现**（`devspace doctor` 会显示 `unsupported on win32` / `unsupported on darwin`）。
> 它影响的是「让 ChatGPT 把它那边的附件直接落到你本机」这一条路；普通读写文件不受影响。
> 详见 `references/cross-platform.md`。

> 临时隧道示例（官方 help 原文）：
> `DEVSPACE_PUBLIC_BASE_URL=https://example.trycloudflare.com devspace serve`

## 重启 serve 是安全的，授权不会丢

网上（如 CSDN 的 DevSpace 补丁文）流传「重启后 ChatGPT 拿着旧 `client_id`，服务端不认识，
报 `invalid_client`」—— **那是 v1.0.1 的问题，v1.0.8 已内置修复**：OAuth 状态持久化在 SQLite。

> **stateDir 默认是 `~/.local/share/devspace/`，不是 `~/.devspace/`**
> （后者只有 `config.json` + `auth.json`）。
>
> 三平台**完全一样**：Windows 是 `C:\Users\<你>\.local\share\devspace\`，
> macOS 是 `/Users/<你>/.local/share/devspace/`（**不是** `~/Library/Application Support`）。
> 源码 `defaultStateDir()` 写死 `join(homedir(), '.local','share','devspace')`，
> **不读 `XDG_DATA_HOME`** —— Linux 上想挪地方只能用 `DEVSPACE_STATE_DIR`。

`dist/oauth-store.js` 的 `SqliteOAuthStore` 用了这几张表：

| 表 | 内容 |
| --- | --- |
| `oauth_clients` | DCR 注册的客户端（`client_id` = `devspace-<uuid>`） |
| `oauth_access_tokens` | access token（按 hash 存） |
| `oauth_refresh_tokens` | refresh token（按 hash 存，带 `expires_at`） |

> 库文件是 `~/.local/share/devspace/devspace.sqlite`（WAL 模式，会有 `-wal` / `-shm`）。
> 另外还有 `workspace_sessions` / `workspace_conversation_bindings` 等业务表。

查看方法（借用 devspace 自带的 better-sqlite3，**只读**打开）：

```js
// 借用 devspace 自带的 better-sqlite3，**只读**打开。
// 路径全部推导出来，不要写死盘符 —— 这样三平台都能直接跑。
const { createRequire } = require('module');
const { execFileSync } = require('child_process');
const { join } = require('path');
const { homedir } = require('os');

const globalRoot = execFileSync('npm', ['root', '-g'], { encoding: 'utf8' }).trim();
const req = createRequire(join(globalRoot, '@waishnav/devspace', 'package.json'));
const Database = req('better-sqlite3');

// 状态目录三平台都是 ~/.local/share/devspace（且不遵循 XDG_DATA_HOME）
const dbFile = join(homedir(), '.local', 'share', 'devspace', 'devspace.sqlite');
const db = new Database(dbFile, { readonly: true });

console.log(db.prepare('select client_id, client_json from oauth_clients').all());
console.log(db.prepare('select client_id, expires_at from oauth_refresh_tokens').all());
```

> 若改过 `DEVSPACE_STATE_DIR`，把 `dbFile` 换成那个目录下的 `devspace.sqlite`。

**验证重启后授权仍有效的正确姿势**：拿库里的 ChatGPT `client_id` 走一次 `/authorize`，
带**全参数**，期望 **200** 且渲染出 `Connect DevSpace` 页面：

```
/authorize?response_type=code
  &client_id=devspace-<uuid>
  &redirect_uri=<必须在该 client 的 redirect_uris 里>
  &scope=devspace
  &code_challenge=<43 字符>
  &code_challenge_method=S256
  &resource=https%3A%2F%2F<域名>%2Fmcp      ← 漏了它就会报错！
```

> **别误判的陷阱**：漏掉 `resource` 参数会 302 到
> `?error=invalid_request&error_description=Invalid or missing OAuth resource`。
> 这是**参数缺失**，**不是** `invalid_client`，服务端和授权都好好的。
> 区分方法：看 `error_description` 文本 —— 只有 `invalid_client` 才是真的 client 丢了。
