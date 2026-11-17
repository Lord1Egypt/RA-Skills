# 环境与 DevSpace 安装（阶段 0–1）

> 阶段 0 = 环境自检 + 补齐依赖；阶段 1 = 安装 DevSpace。
> 主流程见 SKILL.md；本文件是这两步的完整细节。
> **平台差异（安装方式 / PATH 坑 / shell 解析）汇总在 `references/cross-platform.md`。**

## 阶段 0：环境自检 + 补齐依赖

**第一步永远是跑自检，不要凭感觉假设环境是好的。**

```bash
SK=~/.workbuddy/skills/chatgpt-mcp-connector/scripts          # macOS / Linux
# Windows: set "SK=%USERPROFILE%\.workbuddy\skills\chatgpt-mcp-connector\scripts"
node $SK/env-check.mjs              # 只读自检
node $SK/env-check.mjs --install    # 确认缺失项后再加这个（先征得用户同意）
```

Windows 上 `~` 不展开，用 `%USERPROFILE%`（cmd）或 `$env:USERPROFILE`（PowerShell）；
示例里的 `$SK` 换成 `%SK%`（cmd）或 `"$SK"`（PowerShell）。

### 依赖清单与要求

| 依赖 | 要求 | 为什么需要 | 缺失后果 |
| --- | --- | --- | --- |
| **Node** | README 写 `>=22.19 <27`；CLI 内 `assertSupportedNode` 实际放宽到 `>=20.12 <27` | 跑 DevSpace | 启动即报错 |
| **npm** | 随 Node | 装 DevSpace | 装不上 |
| **Git** | 任意版本 | worktree 模式；Windows 上 Git 同时提供 Git Bash | 只能用 checkout 模式 |
| **Bash** | Windows：**必须**有（Git Bash / WSL / MSYS2 / Cygwin），**没有兜底**；且 DevSpace 只在 `%ProgramFiles%\Git\bin` 找，装到别的盘还要另做一步（见下第 5 条）<br>macOS / Linux：`/bin/bash`（一般自带），缺了就退化 `/bin/sh` | DevSpace 的 shell 工具用它执行命令 | Windows 缺 bash **直接失败**；**更常见也更隐蔽的是「有 bash 但 DevSpace 用不上」，表现为所有命令全失败**（见下第 5 条）；macOS/Linux 降级可用，但 bash 专有语法会挂 |
| **Tailscale** | `>=1.38.3`（1.52 起 CLI 语法变更，建议新版） | 提供公网 HTTPS 端点（ChatGPT 够不到 `127.0.0.1`） | ChatGPT 无法连接 |
| **DevSpace** | `@waishnav/devspace` 最新版 | 本体 | — |
| **better-sqlite3** | 能加载 | DevSpace 的状态存储（OAuth/workspace 持久化） | 启动时原生依赖检查失败 |

### 各平台安装命令（实测/官方来源）

| 依赖 | Windows | macOS | Linux |
| --- | --- | --- | --- |
| Node | `winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements` | `brew install node@22 && brew link --overwrite --force node@22` | `curl -fsSL https://deb.nodesource.com/setup_22.x \| sudo -E bash - && sudo apt-get install -y nodejs` / `sudo dnf install -y nodejs` / `sudo pacman -S nodejs npm` |
| Git | `winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements` | `brew install git` | `sudo apt-get install -y git` 等 |
| Bash | 同上装 Git.Git（自带 Git Bash）；或 `winget install -e --id Microsoft.WSL` | `brew install bash`（**可选**，系统自带的 3.2 对 DevSpace 够用） | 通常自带 `/bin/bash`；Alpine 等精简发行版要 `sudo apk add bash` |
| Tailscale | `winget install -e --id Tailscale.Tailscale --accept-package-agreements --accept-source-agreements` | `brew install --cask tailscale` | `curl -fsSL https://tailscale.com/install.sh \| sh` |
| DevSpace | `npm install -g @waishnav/devspace` | 同左 | 同左 |
| better-sqlite3 | `npm rebuild better-sqlite3` | 同左 | 同左 |

> winget 包 ID 已核实存在：`OpenJS.NodeJS.LTS`（**24.19.0**）、`OpenJS.NodeJS`（26.7.0）、
> `Git.Git`（2.55.0.3）、`Tailscale.Tailscale`（1.102.4）。
> **选 LTS 而不是 current** —— current 已经是 26.x，逼近 DevSpace 的 `<27` 上限，LTS 更稳。

### 装完之后的几个坑

> 这几个坑都是**环境没接上**而不是装失败，表现都是「明明装了却说找不到命令」。
> 分平台列出来，遇到时对号入座；平台差异总览见 `references/cross-platform.md`。

1. **PATH 不会自动刷新（三平台通用）。** 用包管理器装完 Node/Git 后，**当前终端识别不到**，
   需要新开一个终端（或重启工具）。装完务必**重跑一次 `env-check`** 确认。

2. **Windows：`npm` 不能直接 spawn。** Node 不允许直接执行 `.cmd`／`.bat`（会 EINVAL），
   必须 `shell: true`；而 shell 模式下 Node 只把命令和参数用空格拼接、**不给带空格的路径加引号**，
   于是 `C:\Program Files\nodejs\npm.cmd` 会被从空格处截断，报
   `'C:\Program' 不是内部或外部命令`。正确写法是自己加引号后再走 shell：

   ```js
   execFileSync(`"${npmPath}"`, args, { shell: true, windowsHide: true })
   ```

   本技能的 `env-check.mjs` 已处理；手写脚本时注意这个坑。
   同一个坑在 `devspace-bootstrap.mjs` 的 `run()` 里也做了处理 —— tailscale 也可能被装成 `.cmd` shim。

3. **macOS：Homebrew 的 `bin` 不在非交互 shell 的 PATH 里。**
   Homebrew 只把它写进 `~/.zprofile`（Apple Silicon 是 `/opt/homebrew/bin`，Intel 是 `/usr/local/bin`），
   而 agent / 非登录 shell 不读这个文件，于是 `brew`、`node` 全都找不到。
   补救：先 `eval "$(/opt/homebrew/bin/brew shellenv)"`，或把该目录直接写进 `~/.zshrc`。

4. **Linux：用 nvm / fnm 装的 Node 不在全局 PATH 里。**
   这类版本管理器靠 shell 初始化脚本注入 PATH，非交互 shell 同样读不到。
   要么在新终端里先 `nvm use 22`，要么直接用绝对路径调用 node。

5. **Windows：Git 装在非 C 盘时，bash 会被 WSL 启动器顶掉（最隐蔽的一个）。**
   DevSpace 只在 `%ProgramFiles%\Git\bin` 和 `%ProgramFiles(x86)%\Git\bin` 找 bash，
   都没有才去扫 PATH 的第一个命中 —— 而 `C:\Windows\System32\bash.exe`（WSL 启动器）
   几乎必定抢先。那个 exe **不是 shell**，忽略 `-c`、不执行命令，
   于是**所有**命令（包括 `echo`）全部失败，ChatGPT 那边显示 `RuntimeException` 或乱码。

   判据：**`echo` 也失败 = 这个坑**；`echo` 能过而 `ls` 报 `command not found` 则是 bash 缺 coreutils，是另一回事。

   修法三条（临时前置 PATH / 建 junction / 改**系统** PATH），完整说明见
   `references/troubleshooting.md` 的「Windows：bash 被 WSL 启动器顶掉」。
   注意往**用户变量** PATH 里加 Git 是没用的 —— 系统 PATH 排在用户 PATH 前面。

### 检查原则：跑命令，不要看目录

判断「某个依赖装没装」，**一律跑它自己的命令**，不要去看固定安装目录：

| 依赖 | 正确的检查方式 | 不要这样做 |
| --- | --- | --- |
| Node | `node -v`（脚本内读 `process.versions.node`） | 去 `C:\Program Files\nodejs` 看有没有 `node.exe` |
| npm | `npm -v` | 同上 |
| Git | `git --version`，定位用 `where git` / `which -a git` | 猜 `C:\Program Files\Git` |
| Bash | `where bash.exe` / `which -a bash`，再**真跑一条命令**验收 | 遍历各盘符下的 `Program Files\Git\bin\bash.exe` |
| Tailscale | `tailscale version`，定位用 `where tailscale` | 猜安装目录 |
| DevSpace | `npm root -g` 推出的路径 + `devspace -v` | 猜 npm 全局目录 |

为什么这条原则重要：

1. **猜目录必然漏。** 装在非 C 盘、PortableGit、MSYS2、Homebrew、`snap`……组合是无穷的；
   `where` / `which` 直接问系统，一次问全。
2. **猜目录会把作者本机的布局带进公开代码。** 「某个具体盘符 + 某个具体安装目录」这样的字面量
   一旦写进脚本，公开仓库就带上了机器指纹 —— 对用户没用，对作者有害。

只有两个**必要**的例外，而且它们都不是「猜」，是**复刻别人的行为**：

- **Tailscale（Windows）**：官方安装器**不把 CLI 写进 PATH**，`where tailscale` 查不到，
  所以要回退到 `%ProgramFiles%\Tailscale\tailscale.exe`（路径由环境变量推导，不写死盘符）。
- **DevSpace 会选哪个 bash**：DevSpace 自己就是**写死在 `%ProgramFiles%\Git\bin` 里找**的。
  要预测它的行为就必须照抄这套顺序 —— 这是本技能唯一一处「看目录」，且路径同样由 `%ProgramFiles%` 推导。

### 快速手工确认

```bash
node -v; npm -v; git --version

# bash 这项要单独看一眼：「能找到」和「DevSpace 会用它」不是一回事
bash --version
# Windows 上再确认解析顺序（第一个结果不能是 System32\bash.exe）：
where bash.exe

# 最省事：让自检替你判定（它会复刻 DevSpace 的解析顺序 + 真跑一条命令）
node $SK/env-check.mjs
```

> ⚠️ 只看 `bash --version` 是有欺骗性的 —— Windows 上它可能通过
> （`System32\bash.exe` 会响应，只是不干活），但 DevSpace 拿它执行命令时全废。
> 多花两秒跑 `env-check` 比后面在 ChatGPT 里对着乱码排查划算得多。

## 阶段 1：安装 DevSpace

```bash
npm install -g @waishnav/devspace      # 或一次性用 npx @waishnav/devspace <cmd>
devspace -v                            # 期望 1.0.8（查最新：npm view @waishnav/devspace version）
devspace doctor                        # 诊断 Node/ABI/平台/Git/Bash/publicUrl/allowedHosts/sqlite
```

常见安装问题：

- **`better-sqlite3` 加载失败**（原生依赖装在了另一个 Node 运行时下）：
  `npm rebuild better-sqlite3`，再 `devspace doctor`。
- **Node 版本不符**：用 `nvm` / `fnm` / `mise` 装 22 LTS。
- **命令找不到**：改用 `npx @waishnav/devspace <cmd>`。
- **`Cannot find module '...\dist\cli.js'`（Windows 特有）**：npm 在 Windows 上还会生成一个
  POSIX shell 版 shim，它依赖 `sed` / `dirname` / `uname`，在 PATH 残缺的 shell 里会算错路径。
  **macOS / Linux 没有这个问题**（npm 只建软链）。绕过办法是绕开 shim、直连 CLI：

  ```bash
  # 通吃三平台：用「当前这个 Node」去跑全局包里的 cli.js
  node "$(npm root -g)/@waishnav/devspace/dist/cli.js" serve
  ```

  Windows 上 `npm root -g` 会返回反斜杠路径（如 `C:\Users\<你>\AppData\Roaming\npm\node_modules`），
  Node 本身两种分隔符都认，直接拼即可。

### CLI 命令面（1.0.8 实测 `--help`）

```
devspace                 运行首次设置（如需要）然后启动服务
devspace serve           启动服务
devspace init            创建/更新 ~/.devspace/config.json 与 auth.json
devspace doctor          显示配置、运行时、原生依赖状态
devspace config get      打印持久化配置
devspace config set publicBaseUrl <url|null>     ← 注意：只支持这一个键
devspace agents ls|run|continue|show|daemon
devspace -v, --version
```

> `config set` **只能改 `publicBaseUrl`**。改 `allowedRoots` 必须直接编辑 `config.json` 或用环境变量。
