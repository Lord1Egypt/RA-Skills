# 容错设计与故障排查

> 本文件回答两个问题：**出事之前怎么防**（容错设计）与 **出事之后怎么办**（故障速查）。
> 主流程见 SKILL.md。
> **平台相关的排查差异（shell、Tailscale 服务模型、路径大小写）见 `references/cross-platform.md`。**

下文用到的脚本目录变量（与 SKILL.md 一致）：

```bash
SK=~/.workbuddy/skills/chatgpt-mcp-connector/scripts          # macOS / Linux
# Windows: set "SK=%USERPROFILE%\.workbuddy\skills\chatgpt-mcp-connector\scripts"
```

Windows 上 `~` 不展开；示例里的 `$SK` 换成 `%SK%`（cmd）或 `"$SK"`（PowerShell）。

## 容错设计：先定原则，再看具体怎么坏

### 五条原则

| 原则 | 做法 | 落到本流程哪里 |
| --- | --- | --- |
| **幂等优先** | 任何一步都能安全重跑，不依赖「上次跑到哪」 | `env-check` 可反复跑；`bootstrap apply` 内容不变就不写盘 |
| **改前先备份** | 动文件前先留退路 | `apply` 自动写 `<文件>.bak`；`rollback` 可整文件回退 |
| **不留半成品** | 所有校验在写盘**之前**完成，失败就在写盘前退出 | URL 形态、`/mcp` 后缀、JSON 可解析性都先验完再落盘 |
| **坏了要能自证** | 给出「谁坏了、证据在哪、下一步做什么」 | 损坏配置另存 `.corrupt-<时间戳>`；先用 `doctor`/`check` 定位 |
| **该停就停** | 需要人登录/授权/点后台开关的步骤，明确交给用户 —— 不静默等待，也不代做。但**阶段 6 不是**：建连接器与 OAuth 授权由 agent 用 browser-harness 自动完成 | 见 SKILL.md「🙋 必须由用户亲自完成的步骤」；脚本检测到未登录会打 🙋 并在末尾汇总 |

### 错误分级：先判断该不该救

| 级别 | 典型现象 | 处置 |
| --- | --- | --- |
| **致命（必须停）** | Node 版本超出 `<27`；`config.json` / `auth.json` 损坏；`publicBaseUrl` 非法 | 停下修根源。**不要**用 `--force` 去掩盖 |
| **可恢复（重试）** | `npm install` 网络抖动、包管理器源超时（**winget / brew / apt 都会**）、Funnel 首次启用等后台批准 | 重试 1–2 次；仍失败改手动执行 |
| **可降级（绕开）** | Tailscale Funnel 用不了（没开 MagicDNS / 组织策略禁用 / 版本太老） | 换临时隧道（见下），用 `DEVSPACE_PUBLIC_BASE_URL` 注入 |
| **纯噪音（忽略）** | `ERR_ERL_UNEXPECTED_X_FORWARDED_FOR`；无 `/mcp` 后缀的 well-known 404；日志 `path` 字段记成 `GET /` | **不要修**。已实测不影响功能，为它搭反向代理纯属浪费时间 |

### 每阶段的前置检查 / 失败分支 / 恢复动作

| 阶段 | 前置检查 | 常见失败 | 恢复动作 |
| --- | --- | --- | --- |
| 0 环境 | `env-check` 报全绿 | 装完仍找不到命令 | **新开终端**刷新 PATH，再重跑 `env-check`（macOS 上还需 `eval "$(/opt/homebrew/bin/brew shellenv)"`，见 `references/cross-platform.md`） |
| 1 DevSpace | `devspace -v` 能输出版本 | `Cannot find module ...dist\cli.js`（**Windows 特有**：npm 的 POSIX shim 依赖 `sed`/`dirname`/`uname`，PATH 残缺时算错路径） | 绕开 shim 直连 CLI：`node "$(npm root -g)/@waishnav/devspace/dist/cli.js" serve`，或走 `npx` |
| 2 Tailscale | `tailscale status` 有 Self | 未登录 / 守护进程没起 | Windows：确认**托盘程序**在跑；macOS：先启动 **App（菜单栏图标）**，CLI 可能不在 PATH（在 app bundle 内）；Linux：`sudo systemctl enable --now tailscaled`，用 `sudo tailscale up --operator=$USER` |
| 3 Funnel | `funnel status` 有 `proxy` 行 | MagicDNS 没开；节点未批准 funnel 属性 | 后台开 MagicDNS / 点终端给的批准链接，再 `funnel --bg <port>` |
| 4 配置 | `bootstrap check` 无 `[FAIL]` | JSON 损坏 | 脚本会**拒绝写盘**并另存 `.corrupt-*`；人工修好后重跑，或 `--force` 重建 |
| 5 serve | 启动日志 `allowed roots:` 符合预期 | 端口被占；非 TTY 下缺配置文件直接退出 | 换 `--port`；补齐 `config.json` + `auth.json`（或给 `DEVSPACE_OAUTH_OWNER_TOKEN`） |
| 6 连接器 | 公网 `/healthz` 200 且 `/mcp` 401 | `Something went wrong...` | 九成是入口走错（见 `references/chatgpt-connector.md` 铁律）；先确认隧道域名没变 |

### 降级路径：Funnel 用不了时

ChatGPT 只需要「一个公网 HTTPS origin」。Funnel 只是其中一种实现，可替换成任意临时隧道：

```bash
cloudflared tunnel --url http://127.0.0.1:7676   # 会打印一个 https://xxx.trycloudflare.com
# 拿到 URL 后注入（官方 help 里的用法）：
DEVSPACE_PUBLIC_BASE_URL=https://xxx.trycloudflare.com devspace serve
```

临时隧道**每次重启换域名** → 换了就要 `devspace config set publicBaseUrl <新origin>`（或用环境变量）
→ **重启 serve** → 回 ChatGPT 插件页 Refresh。
`allowedHosts` 会自动跟着 `publicBaseUrl` 推导，不用另配。

### 恢复与回滚

```bash
node $SK/devspace-bootstrap.mjs rollback            # config.json + auth.json 都从 .bak 恢复
node $SK/devspace-bootstrap.mjs rollback --config   # 只回滚配置
tailscale funnel reset                              # 关掉公网入口
```

回滚前会把当前文件另存为 `.pre-rollback`，所以**回滚本身也可再回滚**。
产物都在 `~/.devspace/`：`config.json` / `auth.json` 及其 `.bak` / `.corrupt-*` / `.pre-rollback`。

> **要不要用 `--force`？** 只有当你确认「旧配置已不可用、宁可重建」时才用。
> 它会丢弃损坏文件里的内容（虽然已另存），作用在 `auth.json` 上意味着**生成新的 Owner password**，
> 需要在 ChatGPT 里重新授权一次。

## 故障速查表

| 现象 | 大概率原因 | 处理 |
| --- | --- | --- |
| `tailscale up` 一直挂着 / 反复跑也登录不上 | 它在等用户去浏览器点授权链接 | **🙋 让用户打开那个链接完成登录**，别反复重跑命令 |
| `tailscale status` 没有 Self | 还没登录，或 Tailscale 服务没运行 | 🙋 让用户 `tailscale up`；「服务没起」按平台看：Windows 托盘图标、macOS 菜单栏 App、Linux `sudo systemctl start tailscaled` |
| `Something went wrong...` | **① 在「设置」里建连接器（入口错）** ② 隧道没起/域名变了 ③ 提交后没等够 6 秒 | 改用 `chatgpt.com/plugins` → 右上角 `创建应用`；或直接用深链接 `chatgpt.com/plugins#settings/Connectors?create-connector=true&redirectAfter=%2Fplugins` |
| **阶段 6 自动化**：`browser-harness --doctor` 报 `daemon alive` / `active browser connections` FAIL | Chrome 没开远程调试（首次必经） | harness 会打开 `chrome://inspect/#remote-debugging` → 🙋 请用户勾选 "Allow remote debugging for this browser instance" 并点 Allow。**只需一次**；⚠️ **不要在循环里重试**，Chrome 每个新连接都弹一个新对话框 |
| **阶段 6 自动化**：操作到错误的标签页 / 点击没落在目标上 | 每次 `browser-harness` 调用都会重置当前标签页 | 每个脚本开头用 `list_tabs()` + `switch_tab()` 重选；⚠️ 授权流程会把域名从 `chatgpt.com` 变成**隧道域名**，匹配条件别写死 `chatgpt.com` |
| **阶段 6 自动化**：点了按钮没反应 | 用了 JS `.click()`，对 ChatGPT 的 React 按钮经常无效 | 改用坐标 `click_at_xy()`；坐标从 DOM 枚举（`js(...)` 扫 `button,a,[role=button]` 拿 `getBoundingClientRect`）取。`y > ph` 时先 `scrollIntoView({block:'center'})` 再量 |
| **阶段 6 自动化**：表单看着填了，提交时值是空的 | React 受控输入：直接 `el.value = v` 不会更新组件内部状态 | 用原生 setter + 派发 `input`/`change` 事件，代码见 `references/chatgpt-connector.md` D 步 |
| **阶段 6 自动化**：日志里冒出登录页 / 一直停在登录页 | 撞上登录墙 | **停下来让用户登录**（密码 / 验证码 / MFA / 账号选择一律不得代填）；Chrome 已登录时可直接走 SSO |
| `does not implement OAuth` | ① 连接器是隧道配好之前建的（ChatGPT 侧缓存了失败预检）② 隧道没起 | 删掉重建；先跑通 `/healthz` |
| 服务端日志**完全没有** ChatGPT 的请求 | UI/入口/缓存问题，请求没发出来 | 查 UI 路径，**别在服务端瞎改** |
| `invalid_client` | 1.0.8 上不该出现；出现说明 SQLite 里没有这个 client | 查 `oauth_clients` 表；重建连接器 |
| 公网 `/mcp` 返回 **404** 而不是 401 | 用了 `--set-path=/mcp`，路径被剥掉了 | 重跑 `tailscale funnel --bg <port>`（代理整个端口） |
| 公网 `/healthz` 失败、本地成功 | 隧道/DNS/证书问题；Tailscale 版本过老 | 升级 Tailscale，重跑 funnel，`funnel status` 逐层查 |
| `Path is outside allowed roots` | 传的路径不在白名单内。**Linux 上还要注意大小写**（`~/Projects` 与 `~/projects` 是两个不同目录） | 见 `references/devspace-config.md`「换可访问目录」 |
| `Path is outside allowed roots: /mnt/f/xxx`（报错里带 `/mnt/`） | **给了 WSL 路径**。DevSpace 是 Windows 进程，`path.resolve('/mnt/f/xxx')` 把开头的 `/` 当成**当前盘**的根 → `C:\mnt\f\xxx` → 必然不在白名单里。⚠️ 报错回显的是**原始输入**，不是解析结果，别被误导成「白名单没配 F 盘」 | 改成本机原生写法 `F:\xxx`。这类路径通常抄自 WSL 的 `pwd -P` / `realpath` / `git rev-parse --show-toplevel` —— **取路径去 PowerShell / cmd 里取** |
| `Path is outside allowed roots`，但路径**看起来明明**在白名单目录下 | 那个目录是 **junction / symlink**，真实目标在白名单之外。`isPathInsideRoot()` 只做字符串比较、**不解析链接**（issue #45），所以「逻辑路径在根内」能过，「真实路径在根外」被拒 | `realpath` 看一眼目标，把**真实路径**也加进 `allowedRoots`（或不用 junction，把项目实体放进白名单目录） |
| 隧道域名变了 | 临时隧道每次换 URL | `devspace config set publicBaseUrl <新origin>` 或用 `DEVSPACE_PUBLIC_BASE_URL`，然后重启 + 在插件页 Refresh |
| `devspace` 命令找不到 / `Cannot find module ...dist\cli.js` | ① PATH 里没有 npm 全局命令目录 ② **Windows 特有**：POSIX shim 依赖 `sed`/`dirname`/`uname`，PATH 残缺时会算错路径 | 绕开 shim 直连：`node "$(npm root -g)/@waishnav/devspace/dist/cli.js"`，或用 `npx`；macOS/Linux 另确认 `$(npm prefix -g)/bin` 在 PATH 里 |
| `better-sqlite3` 加载失败 | 原生依赖装在了别的 Node 运行时下 | `npm rebuild better-sqlite3` |
| Node 版本超出 `<27` 区间 | 装成了 current（26.x 已逼近上限）或版本过老 | Windows：`winget install -e --id OpenJS.NodeJS.LTS`；macOS：`brew install node@22 && brew link --overwrite --force node@22`；Linux：用 nvm / fnm 装 22 LTS。装完 `node -v` 确认 |
| `'C:\Program' 不是内部或外部命令` | Windows 上 shell 模式 spawn 没给含空格路径加引号 | 见 `references/env-setup.md`「装完之后的环境坑」第 2 条 |
| 找不到 Bash / 只找到 PortableGit（**Windows**） | 没装 Git for Windows | `winget install -e --id Git.Git`；`env-check` 会列出全部候选并标推荐项。⚠️ Windows 上 bash 是硬依赖，没有兜底 |
| **`bash` 工具持续异常**：`git status` / `cargo fmt` / `cargo test` / `echo` / `ls` **全部**失败，ChatGPT 里显示 `RuntimeException` 或一段乱码（如 `?????`） | **Windows 上 DevSpace 把 `C:\Windows\System32\bash.exe` 当成了 shell。** 那不是 shell，是 WSL 启动器：忽略 `-c`、不执行命令，只把 WSL 的错误吐回来。触发条件是 Git for Windows **没装在 `%ProgramFiles%\Git`**（例如装在 D 盘）—— DevSpace 只在 Program Files 下找，落空后掉进 `where bash.exe`，而 `System32` 在**系统** PATH 里、必然比用户 PATH 更早命中 | 见下节「Windows：bash 被 WSL 启动器顶掉」。**注意：`echo` 也失败是关键判据** —— `echo` 是 bash 内建命令，它失败说明 shell 根本没起来，而不是 PATH 找不到工具 |
| `bash` 能起来，但 `ls` / `grep` / `dirname` 报 `command not found` | 用的不是完整 Git Bash，而是某工具自带的 **PortableGit 精简副本**（缺 coreutils，或没把 `usr\bin` 放进 PATH） | 与上一条**是两种病**：这条是「shell 活了但缺工具」，那条是「shell 根本没活」。`echo` 能过、`ls` 不过 = 本条。建议另装官方 Git for Windows |
| Linux 上只有 `sh` 没有 `bash` | Alpine 等精简发行版默认不带 bash | `sudo apk add bash`（Debian/Ubuntu 是 `sudo apt install bash`）。不装也能跑，但 bash 专有语法会失败 |
| ChatGPT 里看不到 `download_artifact` 工具 | 这个工具**只在 Linux 上注册**（源码 `ARTIFACT_DOWNLOAD_PLATFORMS = {linux}`） | 正常现象，不是配置问题。Windows / macOS 上用普通读写工具即可 |
| 装完依赖但命令仍找不到 | 当前终端 PATH 是旧的 | **新开一个终端**（或重启工具），再重跑 `env-check` |
| 包管理器不存在（`winget` / `brew` / `apt`） | Windows 缺「应用安装程序」；macOS 没装 Homebrew；Linux 发行版对不上 | Windows 从 Microsoft Store 装 App Installer；macOS 装 Homebrew；Linux 按发行版换 `dnf`/`pacman`/`zypper`/`apk`。也可按 `references/env-setup.md` 的表格手动下载。脚本遇到这种情况会**跳过并说明**，不会硬报错 |
| `config.json` / `auth.json` 损坏或被截断 | 手改时写错（尾逗号、漏右括号），或写入过程被中断 | 脚本会**拒绝写盘**并另存 `.corrupt-*`。人工修好后重跑，或 `apply --force` 重建 |
| `ERR_ERL_UNEXPECTED_X_FORWARDED_FOR` 刷 stderr | Express `trust proxy` 未开，express-rate-limit 校验告警 | **非致命**，只出现在 OAuth 端点流量上（实测日常 `tool_call` 不触发）。想消掉设 `DEVSPACE_TRUST_PROXY=true`（但会让限流键改用 XFF，隧道下可被伪造，自行权衡） |
| 插件建好了，但新对话里看不到工具 | 需要手动在对话工具菜单里挂上 | 打开连接详情 → **Refresh** → 再新开一个对话 |

## Windows：bash 被 WSL 启动器顶掉（shell 工具全废）

### 现象

ChatGPT 那边 `bash` 工具**持续**异常，报 `RuntimeException` 或一段乱码（本地复现时是 `?????`）。
且**每一条**命令都一样失败 —— `git status`、`cargo fmt`、`cargo test`、`cargo check`、`echo`、`ls` 无一例外。

> **`echo` 失败是最重要的判据。** `echo` 是 bash 的**内建命令**，不需要 coreutils、不需要 PATH。
> 它都能失败，就说明 **shell 进程根本没起来**，而不是「PATH 里找不到某个工具」。
> 反过来，如果 `echo` 能过、`ls` 报 `command not found`，那是 PortableGit 缺 coreutils，见速查表另一行。

### 根因

DevSpace 在 Windows 上按**死写的顺序**找 shell（源码 `pi-coding-agent/dist/utils/shell.js` → `getShellConfig()`）：

1. `%ProgramFiles%\Git\bin\bash.exe`
2. `%ProgramFiles(x86)%\Git\bin\bash.exe`
3. `where bash.exe` 的**第一个**命中
4. 都没有 → 抛 `No bash shell found`

它**不会**去扫 D:/E:/F: 盘。所以只要 Git for Windows 装在非默认盘（D 盘很常见），
第 ①② 步就落空，掉到第 ③ 步 —— 而 `C:\Windows\System32\bash.exe`（**WSL 启动器**）
几乎必定排在第一个，因为 `System32` 在**系统** PATH 里。

更进一步：源码会识别这个路径（`isLegacyWslBashPath()`），把调用方式切成「`-s` + 命令走 stdin」。
但那个 exe **根本不是 shell**，它只是转发给 `wsl.exe`；`-s` 也救不了它。
（即使 WSL 装了发行版也不行：那会在 **Linux 文件系统**里执行，`D:\...` 这类路径和你的 Windows 工具链都不存在。）

### 先确认

```bash
node $SK/env-check.mjs
```

看 `Bash` 那一项：如果显示 `[不可用]` 且路径是 `C:\WINDOWS\system32\bash.EXE`，就是这个问题。
同时它会列出「发现的 Bash」—— 你通常能在里面看到那个真正可用的 Git Bash，只是**不在 DevSpace 会找的位置**。

> 它列候选的方式是**跑命令**：`where bash.exe` 拿 PATH 上的全部 bash，再从 `where git` 反推同一份安装里的
> Git Bash —— 而不是去遍历固定安装目录。所以 Git 装在哪个盘、或用的是 MSYS2，都照样能看见。

### 三条修法（按侵入性从低到高，任选其一）

> 下面用 `<GIT>` 代表你的 Git for Windows 安装根目录（默认是 `C:\Program Files\Git`，
> 装在别的盘则形如 `<盘符>:\Program Files\Git`）。
> **不用自己拼** —— `node $SK/env-check.mjs` 会把这三条命令按你机器的实际位置填好
> （它从 PATH 上的 `git.exe` 反推同一份安装里的 Git Bash，所以 Git 装在哪个盘都对）。

```bash
# ① 临时：启动 serve 时把 Git 的 bin 前置到 PATH（无需管理员）
#    cmd:
set "PATH=<GIT>\bin;%PATH%" && devspace serve
#    bash:
PATH="<GIT 的 POSIX 形式>/bin:$PATH" devspace serve

# ② 一劳永逸：建目录 junction，让 DevSpace 的第 ① 步就能命中（需管理员终端）
mklink /J "C:\Program Files\Git" "<GIT>"
#    撤销：rmdir "C:\Program Files\Git"   （只删这个链接，不动 <GIT> 里的真身）

# ③ 把 Git 的 bin 前置到【系统】PATH
#    必须是「系统变量」而不是「用户变量」—— 见下方「为什么这样排」
```

### 为什么这样排（几个容易走弯路的点）

- **把 Git 加进「用户变量」的 PATH 是没用的。** 进程的 PATH = **系统** PATH + 用户 PATH，
  系统在前。`C:\Windows\System32` 是系统变量，所以用户变量里加多少都会被它抢先。
  要么改**系统**变量（修法 ③），要么不靠 PATH（修法 ②）。
- **`DEVSPACE_*` 环境变量里没有能指定 shell 的。** 翻遍 `dist/config.js` 只有
  `DEVSPACE_LOG_SHELL_COMMANDS`（只用来打日志），没有 shell 路径项。
- **`settings.json` 里的 `shellPath` 对 `serve` 无效。** `settings-manager` 确实支持 `shellPath`，
  `agent-session.js` 也会读它，**但** `serve` 的 MCP shell 工具走的是另一条路：
  `dist/pi-tools.js` 调 `createBashTool(context.cwd)` —— 没传 options，拿不到 `shellPath`。
  所以别去改 settings.json，改了也没用。
- **不要 `winget install Git.Git` 重装。** Git 已经装好了，重装到 C 盘只会让你有两份 Git。
  `env-check` 检测到「本机已有可用 bash、只是找不到」时会明确说 **⛔ 不用重装**。

### 验证

```bash
# 修完再跑一次自检，Bash 应变成 [ok] 且注明「冒烟测试通过」
node $SK/env-check.mjs
```

`env-check` 的 Bash 项现在会**真跑一条命令**（`echo`）确认它活着，不再只看路径存不存在 ——
所以它不会再对这种情况亮假绿灯。如果图省事只想手验：

```bash
where bash.exe        # 第一个结果必须不是 C:\Windows\System32\bash.exe
```

然后重启 `devspace serve`，回 ChatGPT 重试 `echo hi`。

---

## 已证伪的伪根因：不要为 well-known 404 加反向代理

`/.well-known/openid-configuration`、`/.well-known/oauth-protected-resource`（**无 `/mcp` 后缀**）、
`/.well-known/oauth-authorization-server/mcp` 确实返回 **404**，
但 ChatGPT 探到 404 **照样继续走 DCR 并成功**。这些 404 **不影响**连接。
不要为此搭路径重写代理，纯属浪费时间。
