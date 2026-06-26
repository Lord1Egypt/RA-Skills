# 运行前提

本 skill 依赖 [social-auto-upload](https://github.com/dreammis/social-auto-upload) 项目（以下简称 SAU）。OPclaw 内置 `uv` 工具，**自动准备**整个运行环境，agent 不应该让用户手动 pip install 或 clone。

---

## 安装位置（约定）

固定 clone 到用户主目录下：

| 平台 | 路径 |
| --- | --- |
| Windows | `%USERPROFILE%\.openclaw\social-auto-upload` |
| macOS / Linux | `~/.openclaw/social-auto-upload` |

下文统一记为 `<SAU_HOME>`。

---

## 自动准备流程（agent 执行任何 `sau_cli.py` 命令前必做）

### Step 1：检测 `<SAU_HOME>` 是否已存在

```bash
# Windows PowerShell
Test-Path "$env:USERPROFILE\.openclaw\social-auto-upload"

# macOS / Linux
test -d "$HOME/.openclaw/social-auto-upload"
```

- 存在 → 跳到 Step 4
- 不存在 → 进 Step 2

### Step 2：clone 仓库到 `<SAU_HOME>`

```bash
# Windows PowerShell
git clone https://github.com/dreammis/social-auto-upload.git "$env:USERPROFILE\.openclaw\social-auto-upload"

# macOS / Linux
git clone https://github.com/dreammis/social-auto-upload.git "$HOME/.openclaw/social-auto-upload"
```

**网络失败重试规则（agent 必须执行，不要询问用户）**：

如果直连 `git clone https://github.com/...` 出现以下任一信号：

- `Connection timeout` / `Connection reset`
- `TLS handshake timeout`
- `Failed to connect to github.com`
- `RPC failed`
- 任何 60 秒以上无进展的卡住状态

**agent 必须立刻自动用镜像重试，按下面顺序逐个尝试，直到一个成功**：

```bash
# 尝试 1：Gitee 镜像（国内最稳，强烈推荐放第一位）
git clone https://gitee.com/lonycn/social-auto-upload.git <SAU_HOME>

# 尝试 2：gh-proxy.org
git clone https://gh-proxy.org/https://github.com/dreammis/social-auto-upload.git <SAU_HOME>

# 尝试 3：gh-proxy.com
git clone https://gh-proxy.com/https://github.com/dreammis/social-auto-upload.git <SAU_HOME>

# 尝试 4：gitmirror
git clone https://hub.gitmirror.com/https://github.com/dreammis/social-auto-upload.git <SAU_HOME>
```

**严禁的行为**：

- ❌ 第一次直连失败就告诉用户"无法访问 GitHub，请手动处理"
- ❌ 让用户自己复制 `git clone` 命令到终端去跑
- ❌ 凭空编造仓库路径（必须严格用 `social-auto-upload`，不要写成 `social-auto-pload` 或其他变体）

只有上面 5 种 clone 方式（直连 + Gitee + 3 个 gh-proxy 镜像）**全部失败**时，才允许告知用户网络异常。

### Step 3：准备 conf.py + 同步依赖

```bash
cd <SAU_HOME>

# 复制示例配置（默认值即可，除非用户特别指定 Chrome 路径或自定义 BASE_DIR）
# Windows
copy conf.example.py conf.py
# macOS / Linux
cp conf.example.py conf.py

# 同步依赖（uv 会自动准备 Python 3.12 + .venv + 所有依赖）
uv sync --python 3.12
```

> 上游有 `uv.lock`，`uv sync` 会按锁文件版本精确还原，速度比 `pip install` 快很多。
> **必须显式 `--python 3.12`**，因为上游 `pyproject.toml` 限定 `>=3.10,<3.13`，避免 uv 误用系统 3.13。

### Step 4：验证 sau_cli.py 可用

```bash
uv run --project <SAU_HOME> python sau_cli.py --help
```

应输出 4 个子命令：`douyin / kuaishou / xiaohongshu / bilibili`。

### Step 5：兜底（极少触发）

如果 Step 2~4 任一失败：

1. 让用户检查 git、网络是否正常
2. 让用户手动 clone：`git clone https://github.com/dreammis/social-auto-upload.git ~/.openclaw/social-auto-upload`
3. 让用户进目录跑：`uv sync --python 3.12`
4. 装完后让用户重启对话

---

## 调用约定（重要）

**所有 `sau_cli.py` 命令都必须使用以下形式**：

```bash
uv run --project <SAU_HOME> python sau_cli.py bilibili <subcmd> [args...]
```

具体到平台：

```powershell
# Windows PowerShell
uv run --project "$env:USERPROFILE\.openclaw\social-auto-upload" python sau_cli.py bilibili --help
```

```bash
# macOS / Linux
uv run --project "$HOME/.openclaw/social-auto-upload" python sau_cli.py bilibili --help
```

> 不要用 `sau bilibili ...` 形式 —— 上游 `pyproject.toml` 虽然声明了 `[project.scripts] sau = "sau_cli:main"`，但 `conf.py` 是用户运行时生成的、不在 wheel 里，所以 `uv tool install` 装出来的 `sau` 命令一定会 ImportError。**必须从源码目录用 `uv run` 调用**。

---

## biliup 子组件（仅 Bilibili 相关）

`python sau_cli.py bilibili upload-video` 第一次执行时，SAU 会自动下载 `biliup` 二进制（GitHub Release）。

国内访问慢时，告诉用户可以手动下载后放到 SAU 期望的位置（具体路径见 SAU 报错信息），或用代理：

```
https://gh-proxy.org/https://github.com/biliup/biliup/releases/download/<version>/<asset>
https://gh-proxy.com/https://github.com/biliup/biliup/releases/download/<version>/<asset>
```

---

## 登录态准备

`python sau_cli.py bilibili login --account <name>` **必须由用户自己在本机真实终端执行**：

- 命令会打开二维码（终端 ASCII 或 `qrcode.png`）
- 用户扫码登录
- 完成后账号信息保存到本地文件

agent 在非交互环境（如 ChatGPT 调用工具）下绝不能硬跑这个命令，应该把命令打印给用户、让用户复制到自己的终端执行。

---

## 常见失败信号

| 错误信号 | 原因 | 处理 |
| --- | --- | --- |
| `'git' is not recognized` / `command not found: git` | 用户机器没装 git | 让用户先装 git |
| `Could not find a version that satisfies python==3.12` | uv 没有 3.12，会自动联网下载 | 联网即可 |
| `ModuleNotFoundError: No module named 'conf'` | 没复制 conf.example.py → conf.py | 重做 Step 3 |
| `Connection timeout` / `failed to fetch` | 网络问题 | 用 gh-proxy 代理 |
| `Login expired` / `cookie invalid` | 登录态失效 | 让用户跑 `login` |
| `biliup` 下载失败 | GitHub Release 网络问题 | 用 gh-proxy 手动下载 |

---

## 给 agent 的执行优先级

1. **先静默检测 `<SAU_HOME>` 存在性**，不要每次都告诉用户"我准备装环境"
2. **如果触发 clone + sync**，告诉用户"首次准备需要 1-2 分钟"
3. **登录命令永远让用户自己跑**，给出可复制粘贴的完整命令
4. **平台 cookie 失效时**直接给登录命令，不要试图自动处理