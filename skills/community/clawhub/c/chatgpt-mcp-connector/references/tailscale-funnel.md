# Tailscale 安装 / 登录 / Funnel 隧道（阶段 2–3）

> 阶段 2 = 安装并登录 Tailscale；阶段 3 = 开公网隧道。
> 主流程见 SKILL.md；本文件是这两步的完整细节。
> **三平台的安装方式、CLI 位置、服务模型差异见 `references/cross-platform.md`。**

## 为什么必须用 Tailscale Funnel

ChatGPT 跑在云端，**够不到 `127.0.0.1`**，所以必须有公网 HTTPS 端点。
Tailscale **Serve 不行**（只在 tailnet 内可见），必须用 **Funnel**（对公网开放）。

## 阶段 2：安装并登录

### 安装

| 平台 | 命令 |
| --- | --- |
| Windows（推荐，实测可用） | `winget install -e --id Tailscale.Tailscale` |
| Windows 静默（自动化） | `winget install -e --id Tailscale.Tailscale --silent --accept-package-agreements --accept-source-agreements` |
| Windows 手动 | 从 `tailscale.com/download/windows` 下 `.msi` |
| macOS | `brew install --cask tailscale`（会要求管理员密码，**正常**，不是卡死） |
| Linux | `curl -fsSL https://tailscale.com/install.sh \| sh` |

**CLI 在哪 —— 三平台不一样，照平台取：**

| 平台 | CLI 位置 | 是否在 PATH |
| --- | --- | --- |
| Windows | `C:\Program Files\Tailscale\tailscale.exe` | ❌ **不在**。脚本里用绝对路径，或 `& "C:\Program Files\Tailscale\tailscale.exe" status`。某些安装方式（scoop / winget）会装成 `.cmd` shim，调用要兼容 `.cmd`（见 `references/env-setup.md` 的 shell 引号坑） |
| macOS | `brew install tailscale` → `/usr/local/bin`（Intel）或 `/opt/homebrew/bin`（Apple Silicon） | ✅ 在 |
| macOS（App Store / 独立 App 版） | `/Applications/Tailscale.app/Contents/MacOS/Tailscale` | ❌ **不在**，必须写全路径 |
| Linux | `/usr/bin/tailscale`（官方脚本）、`/usr/sbin`（发行版包）、`/snap/bin`（snap） | ✅ 在 |

本技能两个脚本**先跑命令**（`where tailscale` / `which -a tailscale`），命令查不到才回退到以上约定位置
（`findTailscale()` / `checkTailscale()`）—— Windows 的安装器不把 CLI 写进 PATH，所以这层回退是必需的。

### 登录

```bash
tailscale up          # 打印一个 URL，浏览器里登录授权（会加进 tailnet）
tailscale status      # 确认本机出现在列表里
tailscale ip -4       # 本机的 Tailscale IPv4（100.x.y.z）
```

**服务模型三平台不同 —— 先看这一行，否则最容易卡在「命令跑不动」：**

| 平台 | 先做什么 | 常见报错 |
| --- | --- | --- |
| Windows | 确认托盘图标在运行（客户端是常驻 GUI 程序） | `failed to connect` |
| macOS | 先启动 Tailscale App（菜单栏图标）；CLI 不在 PATH 时用 `/Applications/Tailscale.app/Contents/MacOS/Tailscale` | `command not found` |
| Linux | `sudo systemctl enable --now tailscaled` 确保守护进程在跑；用 `sudo tailscale up --operator=$USER` —— **加了 `--operator` 之后就不用每次都 sudo** | `access denied` / `permission denied` |

> 🙋 **需要用户操作**：`tailscale up` 会在终端打印一个登录链接 ——
> **必须由用户用浏览器打开、登录并授权该设备加入 tailnet**。这一步脚本做不了，
> 不要自己反复重试。做完跑 `tailscale status` 确认（能看到 Self 且 IP 是 `100.x`）。

### 版本要求

- Funnel 官方要求 Tailscale ≥ `1.38.3`（**实测用 1.102.4**）。
- **1.52 改过 `serve` / `funnel` 的 CLI 语法**：低于 1.52 老语法不同，先升级再看本文命令。

### Funnel 前置条件（容易卡住的点）

1. **必须开启 MagicDNS**（在 Tailscale 后台 DNS 页打开）。没开会拿不到 `<device>.<tailnet>.ts.net`。
2. **首次启用 Funnel** 需要在 Tailscale 后台批准该节点的 `funnel` 属性 —— 终端会打印一个链接让你去点。
3. 相关说明：`https://tailscale.com/kb/1247/funnel-serve-use-cases`

> 🙋 **需要用户操作**：以上两条都是**后台/浏览器里的开关**，脚本改不了 ——
> MagicDNS 要用户去 Tailscale admin 后台 DNS 页打开；
> 首次启用 Funnel 时终端会再给一个**批准链接**，也要用户去浏览器点同意。
> 判断是否已满足：`tailscale status --json` 里有 `Self.DNSName`，且 `funnel status` 出现 `(Funnel on)`。

### 判断登录态（脚本可自动检测）

`tailscale status --json` 的 **`BackendState`** 字段：

| 值 | 含义 |
| --- | --- |
| `Running` | 已登录且在运行 |
| `NeedsLogin` | 装了但没登录 → 需要用户 `tailscale up` |
| `Stopped` / `NoState` | 服务没起或刚装好 |

本技能两个脚本都据此判断，并在未登录时打 `🙋` 提醒用户。

## 阶段 3：开公网隧道（Tailscale Funnel）

DevSpace 默认监听 `127.0.0.1:7676`。把**整个端口**代理出去：

```bash
# 正确：代理整个 7676，端口换成本机实际值
tailscale funnel --bg 7676
tailscale funnel --bg http://127.0.0.1:7676     # 等价写法（老文档常见）
tailscale funnel --bg --yes 7676                # 免交互确认

# 查看
tailscale funnel status
```

`funnel status` 正常输出长这样（实测）：

```
# Funnel on:
#     - https://my-desktop.tail1234.ts.net

https://my-desktop.tail1234.ts.net (Funnel on)
|-- / proxy http://127.0.0.1:7676
```

### ⚠️ 绝对不要 `--set-path=/mcp`

`tailscale funnel --set-path=/mcp 7676` 会让公网 `/mcp` 到服务端时**变成 `/`**（Tailscale 转发前剥掉挂载路径）
→ 404。而且 DevSpace 的 OAuth discovery / `authorize` / `token` / `register` 路由都在 `/mcp` **之外**，
所以必须服务**整个 origin**。

### 关闭隧道

```bash
tailscale funnel reset          # ✅ 1.102+ 的正确语法（实测 help 里的 subcommand）
tailscale funnel --https=443 off  # 仅老版本；新版本 help 里已无此形式
```

### 自动拿到隧道域名（不要让人手抄）

```bash
tailscale status --json                                     # macOS / Linux：CLI 在 PATH
"C:/Program Files/Tailscale/tailscale.exe" status --json    # Windows：CLI 不在 PATH，写全路径
```

关键字段（实测）：

| 字段 | 实测值 | 用途 |
| --- | --- | --- |
| `Self.DNSName` | `my-desktop.tail1234.ts.net.` | **就是 Funnel 域名**（注意末尾有个点，要去掉） |
| `Self.HostName` | `DESKTOP-ABCDEF` | 机器名 |
| `MagicDNSSuffix` | `tail1234.ts.net` | tailnet 后缀 |
| `CurrentTailnet.Name` | `<你的 Tailscale 账号>` | 账号 |

于是 `publicBaseUrl = "https://" + DNSName.replace(/\.$/,'')`，MCP 端点 = 它 + `/mcp`。
本技能的 `devspace-bootstrap.mjs` 已封装这一步（`check` 与 `apply` 都会自动推导）。

### Funnel 用不了时的降级方案

ChatGPT 只需要「一个公网 HTTPS origin」。Funnel 只是其中一种实现，可替换成任意临时隧道：

```bash
cloudflared tunnel --url http://127.0.0.1:7676   # 会打印一个 https://xxx.trycloudflare.com
# 拿到 URL 后注入（官方 help 里的用法）：
DEVSPACE_PUBLIC_BASE_URL=https://xxx.trycloudflare.com devspace serve
```

临时隧道**每次重启换域名** → 换了就要 `devspace config set publicBaseUrl <新origin>`（或用环境变量）
→ **重启 serve** → 回 ChatGPT 插件页 Refresh。
`allowedHosts` 会自动跟着 `publicBaseUrl` 推导，不用另配。
