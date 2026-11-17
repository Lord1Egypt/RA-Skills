# 跨平台兼容（Windows / macOS / Linux）

> 三个平台都能用，差异集中在**四处**：依赖安装方式、shell 的解析、Tailscale 的服务模型、路径写法。
> 本文把这些差异集中列出来；各阶段的完整操作仍在对应 reference 里，这里只讲「哪不一样、注意什么」。

**结论来源与可信度**（重要）：

| 内容 | 依据 | 可信度 |
| --- | --- | --- |
| shell 解析、平台门控、目录默认值 | DevSpace `1.0.8` 源码：`dist/config.js`、`dist/roots.js`、`dist/user-config.js`、`dist/process-platform.js`、`dist/artifact-tools.js`、`node_modules/@earendil-works/pi-coding-agent/dist/utils/shell.js` | 读源码确认 |
| Windows 全流程 | 实机跑通（Windows 11 + Git Bash） | ✅ 已实测 |
| macOS 全流程 | 实机跑通（Intel Mac，含阶段 6 建连接器 + OAuth 授权） | ✅ 已实测 |
| Linux 的「坑」与安装命令 | 官方文档 + 源码推断 | ⚠️ **未实机验证** |

> 三个平台的可信度**不一样，请按上面的标注区别对待**：
> Windows / macOS 是实测结论；**Linux 那列的安装命令与「坑」是推断的**。
> Linux（以及任何平台）上跑出与本文不符的结果时，**以实际输出为准**，并把差异回报过来。

---

## 一、平台支持一览

| 能力 | Windows | macOS | Linux |
| --- | --- | --- | --- |
| DevSpace 本体（`package.json` 无 `os`/`cpu` 限制） | ✅ | ✅ | ✅ |
| shell 工具实际用哪个 shell | **强制 Git Bash** | `/bin/bash`（存在即用） | `/bin/bash`（存在即用） |
| 找不到 bash 时 | ❌ 直接抛 `No bash shell found`，**无兜底** | 退化 `/bin/sh` | 退化 `/bin/sh` |
| `download_artifact`（把 ChatGPT 里的文件落到本机） | ❌ 未注册 | ❌ 未注册 | ✅ **仅 Linux** |
| 进程树终止方式 | `taskkill /T /F` | `kill(-pid)` | `kill(-pid)` |
| 配置文件目录 | `C:\Users\<你>\.devspace` | `/Users/<你>/.devspace` | `/home/<你>/.devspace` |
| 状态目录（SQLite） | `C:\Users\<你>\.local\share\devspace` | `/Users/<你>/.local/share/devspace` | `/home/<你>/.local/share/devspace` |
| 平台适配脚本检查项 | 全部 | 全部 | 全部 |

### 两个值得单独拎出来的结论

**① `download_artifact` 只在 Linux 上注册。**
源码里 `ARTIFACT_DOWNLOAD_PLATFORMS = new Set(["linux"])`。在 Windows / macOS 上这个工具**根本不会出现**
（`devspace doctor` 会显示 `artifact download: unsupported on win32` / `unsupported on darwin`）。
这影响的是「让 ChatGPT 把它那边的附件直接写到你本机」这一条路 —— 普通读写文件不受影响。

**② 状态目录三平台完全一致，且不遵循 XDG。**
`defaultStateDir()` 是写死的 `join(homedir(), '.local', 'share', 'devspace')`，
**不读 `XDG_DATA_HOME`**，macOS 上也不用 `~/Library/Application Support`。
Linux 用户按 XDG 规范去 `~/.local/share` 找是对的，但改了 `XDG_DATA_HOME` 不会生效 —— 要用 `DEVSPACE_STATE_DIR` 显式指定。

---

## 二、shell 是怎么被选中的（最容易出问题的一环）

DevSpace 的 shell 工具解析顺序（源码 `pi-coding-agent/dist/utils/shell.js`）：

| 平台 | 顺序 |
| --- | --- |
| **Windows** | ① `%ProgramFiles%\Git\bin\bash.exe` ② `%ProgramFiles(x86)%\Git\bin\bash.exe` ③ PATH 上的任意 bash ④ **都没有 → 抛错** |
| **macOS / Linux** | ① `/bin/bash`（存在就用，**不看版本**） ② PATH 上的 bash ③ 退化 `/bin/sh` |

由此推出三个实用结论：

- **Windows 上 Git Bash 是硬依赖**，而且 DevSpace 只认 `%ProgramFiles%\Git\bin\bash.exe` 和
  `%ProgramFiles(x86)%\Git\bin\bash.exe` 这两个位置，都没有才去扫 PATH 的**第一个**命中。
  它**不会扫 D:/E:/F: 盘** —— 所以「Git 装在 D 盘」这种再正常不过的安装会直接踩雷（见下方 ⚠️）。
- **macOS / Linux 上装再新的 bash 也不会被选中** —— 只要 `/bin/bash` 存在，DevSpace 就用它。
  所以在 macOS 上它用的是系统自带的 **bash 3.2**（GPLv2 版）。这对 DevSpace 够用，但别指望
  bash 4/5 的语法（`mapfile`、`globstar`、关联数组）在你让 ChatGPT 执行的命令里可用。
- **Linux 上没有 bash 不算致命**（会退化成 `/bin/sh`），但 Alpine 这类精简发行版默认只有 `ash`，
  bash 专有语法会失败。要补：`sudo apk add bash`。

> ### ⚠️ Windows 最恶的一坑：bash 被 WSL 启动器顶掉
>
> Git for Windows 装在非默认盘时，DevSpace 的第 ①② 步落空，顺着第 ③ 步命中
> `C:\Windows\System32\bash.exe`。那是 **WSL 启动器，不是 shell**：它忽略 `-c`、不执行命令，
> **所有命令**（连 `echo` 都算）立刻失败并返回乱码，在 ChatGPT 那边表现为「bash 接口持续异常」。
>
> 而且**「把 Git 加进 PATH」并不够**：进程的 PATH = **系统** PATH + 用户 PATH，系统在前，
> `C:\Windows\System32` 是系统变量，永远比用户变量里加的 Git 更早命中。
> （另外 `settings.json` 的 `shellPath` 对 `serve` 的 shell 工具也无效 —— 它没把该参数传下去；
> `DEVSPACE_*` 环境变量里也没有 shell 路径项。所以只能从「让真 bash 被找到」入手。）
>
> 三条修法，按侵入性从低到高：
>
> | # | 做法 | 权限 |
> | --- | --- | --- |
> | ① | 启动 serve 时前置 PATH：`set "PATH=<你的Git安装路径>\bin;%PATH%"` | 无需管理员 |
> | ② | 建 junction：`mklink /J "C:\Program Files\Git" "<你的Git安装路径>"` | 需管理员 |
> | ③ | 把 Git 的 bin 前置到**系统** PATH（不是用户变量） | 需管理员 |
>
> 路径不用自己拼 —— `env-check` 会**按你机器上的实际安装位置**把三条命令生成好
> （它从 PATH 上的 `git.exe` 反推同一份安装里的 Git Bash，Git 装在哪个盘都对）。
>
> 完整说明见 `references/troubleshooting.md` 的「Windows：bash 被 WSL 启动器顶掉」。
>
> **判定口诀**：`echo` 也失败 = shell 根本没起来（本坑）；
> `echo` 能过、`ls` 报 `command not found` = bash 起了但缺 coreutils（PortableGit 精简副本）。

> `env-check.mjs` 已按上述逻辑分平台判定：Linux 无 bash 但 `/bin/sh` 在 → 报**警告**而不是缺失；
> Windows 无 bash → 报**缺失**（因为真的跑不了）。
> Windows 上它还会**复刻 DevSpace 的解析顺序**，并对解析出的 bash **真跑一条命令**做冒烟测试 ——
> 光看路径存在是不够的（`System32\bash.exe` 也在那儿，`existsSync` 同样为真）。
>
> 另外，**它不靠「猜安装目录」判断装没装**：一律跑命令 —— `where bash.exe`、`where git` 反推同一份安装、
> `git --version`、`npm -v`、`tailscale version`。唯一照抄目录的地方是复刻 DevSpace 的
> `%ProgramFiles%\Git\bin` 解析顺序（要预测它的行为就只能照抄），且那条路径由 `%ProgramFiles%` 推导。
> 完整理由见 `references/env-setup.md` 的「检查原则：跑命令，不要看目录」。

---

## 三、依赖与安装命令

| 依赖 | Windows | macOS | Linux |
| --- | --- | --- | --- |
| Node | `winget install -e --id OpenJS.NodeJS.LTS` | `brew install node@22 && brew link --overwrite --force node@22` | `curl -fsSL https://deb.nodesource.com/setup_22.x \| sudo -E bash - && sudo apt-get install -y nodejs`<br>`sudo dnf install -y nodejs`<br>`sudo pacman -S --noconfirm nodejs npm` |
| Git | `winget install -e --id Git.Git` | `brew install git` | `sudo apt-get install -y git` / `sudo dnf install -y git` / `sudo pacman -S git` |
| Bash | 装 Git for Windows 即带上 | `brew install bash`（可选，系统已有 3.2） | 一般自带；Alpine `sudo apk add bash` |
| Tailscale | `winget install -e --id Tailscale.Tailscale` | `brew install --cask tailscale` | `curl -fsSL https://tailscale.com/install.sh \| sh` |
| DevSpace | `npm install -g @waishnav/devspace` | 同左 | 同左 |
| better-sqlite3 | `npm rebuild better-sqlite3` | 同左 | 同左 |

> macOS / Linux 的安装一行命令都用 `curl`，确认它在（macOS 与主流发行版都自带）。
> macOS 上 `brew install --cask tailscale` 会**要求输入管理员密码**，属于正常现象，不是卡死。

---

## 四、路径写法对照

| 用途 | Windows | macOS / Linux |
| --- | --- | --- |
| 家目录 | `C:\Users\<你>` | `/Users/<你>`（macOS）· `/home/<你>`（Linux） |
| DevSpace 配置 | `C:\Users\<你>\.devspace\config.json` | `~/.devspace/config.json` |
| 状态库 | `C:\Users\<你>\.local\share\devspace\devspace.sqlite` | `~/.local/share/devspace/devspace.sqlite` |
| npm 全局包目录 | `npm root -g` → 如 `C:\Users\<你>\AppData\Roaming\npm\node_modules` | `npm root -g` → 如 `/usr/local/lib/node_modules` |
| npm 全局**命令**目录 | 与 `npm prefix -g` 同目录（直接放 `devspace.cmd`） | `$(npm prefix -g)/bin` ← **容易漏加进 PATH** |

**给 ChatGPT 的路径必须是本机原生写法**：Windows 用 `D:\projects\my-app`，
macOS / Linux 用 `/home/you/projects/my-app`。从 Windows 文档抄反斜杠路径到 Linux 上，
会被当成「文件名里带反斜杠」，目录当然找不到 —— `devspace-bootstrap.mjs` 在非 Windows 平台检测到反斜杠会告警。

### ⚠️ 最容易写错的一点：`DEVSPACE_ALLOWED_ROOTS` 用**逗号**分隔

```bash
# ✅ 三个平台都是逗号
DEVSPACE_ALLOWED_ROOTS="/home/you/a,/home/you/b" devspace serve
# ❌ 不是 Windows 的 ; 也不是 PATH 的 :（源码里统一 split(",")）
```

同理 `DEVSPACE_ALLOWED_HOSTS`、`DEVSPACE_SUBAGENTS`、`DEVSPACE_SKILL_PATHS` 也都是逗号分隔。

### 大小写敏感性

| 平台 | 文件系统默认 | 影响 |
| --- | --- | --- |
| Windows | 不敏感 | `D:\X` 与 `d:\x` 是同一目录 |
| macOS | 不敏感（APFS/HFS+ 默认） | 同上 |
| Linux | **敏感** | `~/Projects` 与 `~/projects` 是**两个不同目录** |

`devspace-bootstrap.mjs` 的 `allowedRoots` 去重按平台处理（`CASE_INSENSITIVE_FS`）。
早先无条件 `toLowerCase()` 的版本在 Linux 上会把两个目录合并成一个、**静默丢掉一个白名单项**，已修。

---

## 五、Tailscale：三平台的服务模型不同

| 平台 | 客户端形态 | CLI 位置 | 登录注意 |
| --- | --- | --- | --- |
| Windows | 常驻托盘程序 | `C:\Program Files\Tailscale\tailscale.exe`（**不在 PATH**） | 托盘启动后 `tailscale up` 会自动弹浏览器 |
| macOS | 菜单栏 App | `/usr/local/bin/tailscale`、`/opt/homebrew/bin/tailscale`，**App Store 版在 `/Applications/Tailscale.app/Contents/MacOS/Tailscale`（不在 PATH）** | 先启动 App 再 `tailscale up` |
| Linux | systemd 守护进程 `tailscaled` | `/usr/bin/tailscale`、`/usr/sbin`、`/snap/bin` | **CLI 默认要 root** |

Linux 上推荐一次性把权限交给自己，之后就不用每条命令都 `sudo`：

```bash
sudo systemctl enable --now tailscaled     # 确保守护进程在跑
sudo tailscale up --operator=$USER         # --operator：把 CLI 权限交给当前用户
```

`tailscale funnel --bg <port>` 的**语法三平台一致**（`--set-path=/mcp` 的禁令也一致，见铁律 1）。
关闭用 `tailscale funnel reset`。

---

## 六、三平台各自最容易踩的坑

### Windows ✅ 已实机验证（Windows 11 + Git Bash，完整 0→1 跑通）
| 坑 | 表现 | 处理 |
| --- | --- | --- |
| bash 是硬依赖 | `No bash shell found` | 装 Git for Windows；确保 `%ProgramFiles%\Git\bin\bash.exe` 或 PATH 上的 bash 存在 |
| **Git 装在非 C 盘 → bash 被 WSL 启动器顶掉** | **所有**命令失败（含 `echo`），ChatGPT 显示 `RuntimeException` / 乱码 | DevSpace 只找 `%ProgramFiles%\Git`，落空后命中 `System32\bash.exe`（WSL 启动器，不是 shell）。三条修法见第二节 ⚠️ |
| 把 Git 加进**用户变量** PATH 想修上一条 | 无效，还是命中 System32 | 进程 PATH = **系统** PATH + 用户 PATH，系统在前。要改就改**系统**变量，或改用 junction |
| PortableGit 精简副本 | bash 能起，但 `ls`/`grep`/`dirname` 报 `command not found` | 与上一条是两种病：那条 `echo` 也失败，这条 `echo` 能过。建议另装官方 Git for Windows |
| `npm` 不能直接 spawn `.cmd` | `'C:\Program' 不是内部或外部命令` | 手动加引号再走 shell（两个脚本已处理） |
| 装完 PATH 不刷新 | 刚装完仍报命令找不到 | **新开一个终端**，重跑 `env-check` |
| POSIX 版 CLI shim 依赖 `sed`/`dirname` | `Cannot find module '...dist\cli.js'` | 用绝对路径直连 `dist/cli.js`（**Windows 特有**，macOS/Linux 上 npm 只建软链，没这问题） |

### macOS ✅ 已实机验证（Intel Mac，完整 0→1 跑通）

| 坑 | 表现 | 处理 |
| --- | --- | --- |
| Homebrew 不在 PATH | 非交互 shell 里找不到 `brew`/`node` | `eval "$(/opt/homebrew/bin/brew shellenv)"` 写进 `~/.zprofile`（Apple Silicon 路径是 `/opt/homebrew`，Intel 是 `/usr/local`） |
| App Store 版 Tailscale 没有 CLI | `tailscale: command not found` | 用 `/Applications/Tailscale.app/Contents/MacOS/Tailscale`，或 `brew install tailscale` |
| 系统 bash 是 3.2 | bash 5 语法不可用 | 对 DevSpace 够用；要 bash 5 就 `brew install bash`（但 DevSpace 仍会用 `/bin/bash`） |
| `brew install --cask` 要密码 | 安装过程停在密码提示 | 正常，不是卡死；非交互环境会直接失败，改由用户手动执行 |

### Linux ⚠️ 未实机验证（下表为源码 + 官方文档推断）

| 坑 | 表现 | 处理 |
| --- | --- | --- |
| `tailscale` 要 root | `access denied` / `permission denied` | `sudo tailscale up --operator=$USER`，之后免 sudo |
| 守护进程没起 | `BackendState` 读不到 | `sudo systemctl enable --now tailscaled` |
| `XDG_DATA_HOME` 无效 | 改了环境变量但状态库还在 `~/.local/share` | 用 `DEVSPACE_STATE_DIR` 显式指定 |
| 精简发行版没有 bash | shell 退化成 `sh`，脚本语法报错 | Alpine：`sudo apk add bash`；装完 `env-check` 会从「警告」变「就绪」 |
| snap 版 Tailscale | 路径在 `/snap/bin/tailscale` | 两个脚本的约定位置列表已包含（`which -a tailscale` 本来也能查到） |
| 大小写敏感 | 白名单目录「明明写了却不在里面」 | 确认大小写与磁盘一致 |

---

## 七、脚本的平台适配说明

两个脚本（`env-check.mjs` / `devspace-bootstrap.mjs`）都能三平台直接跑，无需改代码。

| 脚本行为 | 处理方式 |
| --- | --- |
| 包管理器探测 | Windows `winget` ｜ macOS `brew` + `port` ｜ Linux `apt-get`/`dnf`/`yum`/`pacman`/`zypper`/`apk` |
| 安装命令选择 | 按平台返回对应命令；含 `sudo`/管道的交给用户手动执行，不代跑 |
| 找不到包管理器 | **跳过并说明**，不会抛 `ENOENT`（早年 Windows-only 的判断已泛化到三平台） |
| 依赖是否已安装 | **跑命令判断，不看安装目录**：`where bash.exe` / `where git` / `which -a tailscale` / `git --version` / `npm -v`；bash 候选另从 PATH 上的 `git.exe` 反推（Git 装在哪个盘都对）。脚本里不写死 `C:/D:/E:/F:` 盘符 |
| bash 判定 | **复刻 DevSpace 的解析顺序**（`resolveDevspaceBash()`），以解析结果为准 —— 不再只看「推荐排序」；再对非 WSL 的 bash **真跑一条命令**做冒烟测试（`smokeTestBash()`）。Windows 缺失 = 直接判失败；macOS/Linux 无 bash 但有 `/bin/sh` → 只警告 |
| WSL 入口识别 | 解析到 `System32\bash.exe` / `WindowsApps\bash.exe` → 判 `[不可用]` 并给出三条修法；**不执行**它（会拉起 `wsl.exe`，慢且可能被安全策略拦截） |
| 「装了但用不了」的措辞 | 此类条目标 `[不可用]`（而非 `[缺失]`），且**不给重装建议** —— 本机已有可用 bash 时，重装只会多出一份 Git |
| Tailscale 提示 | 按平台给出「托盘 / 菜单栏 App / systemd + --operator」的不同说法 |
| `allowedRoots` 去重 | 按平台决定是否大小写不敏感（见上） |
| 主目录 / 盘符根告警 | 三平台一致（`/`、`C:\`、`~` 都会告警） |

**平台翻转测试**：Windows 上跑不了 POSIX 分支，早期用「复制脚本 + 改 `IS_WIN`/`IS_MAC` 常量」
的方式验证过去重、反斜杠告警、主目录告警等逻辑（5/5 通过）；
`env-check` 的 POSIX 分支同样用这个手法验证过（两个变体都不崩、且走到正确的判定分支）。

> **macOS 现已实机跑通完整 0→1**，因此 macOS 这一列不再依赖翻转测试。
> **Linux 仍然只有「翻转测试 + 源码推断」**，没有实机运行记录 —— 按这个差别看待可信度。

**反向验证**：Windows 上的「bash 被 WSL 顶掉」这条，实测对照过头 ——
不修 PATH 时 `env-check` 报 `[不可用]`（exit 1），把 Git 的 bin 前置到 PATH 后立刻变 `[ok] Git Bash（冒烟测试通过）`（exit 0）。

---

## 八、让 `devspace serve` 常驻（三平台）

进程一停 ChatGPT 就断。开机自启按平台选：

| 平台 | 方案 |
| --- | --- |
| Windows | 任务计划程序（登录时启动），或 `nssm install DevSpace` |
| macOS | `launchd`：写 `~/Library/LaunchAgents/*.plist`，`RunAtLoad` + `KeepAlive` |
| Linux | systemd：user unit（`systemctl --user enable --now`）或 system unit |

启动命令都指向**绝对路径的 `dist/cli.js`**，避免 PATH/shim 差异：

```bash
node <npm root -g>/@waishnav/devspace/dist/cli.js serve
```

---

## 九、不支持的组合

| 组合 | 状态 | 原因 |
| --- | --- | --- |
| 原生 PowerShell / cmd 里跑 `devspace serve` | ✅ 可以（服务本身能起） | 但 **shell 工具仍要 bash** —— 让 ChatGPT 执行命令时走的是 Git Bash |
| 没有 bash 的 Windows | ❌ 不可用 | DevSpace 直接抛错，无兜底 |
| 没有 bash 的 Linux | ⚠️ 降级可用 | 退化成 `/bin/sh`，bash 专有语法失败 |
| Windows / macOS 上用 `download_artifact` | ❌ 未注册 | 源码限定 `linux` |
| WSL 作为唯一 bash | ⚠️ 可行但绕 | `env-check` 会识别 WSL 入口；建议改用 Git Bash |
| 用 `XDG_DATA_HOME` 改状态目录 | ❌ 无效 | 需改用 `DEVSPACE_STATE_DIR` |
