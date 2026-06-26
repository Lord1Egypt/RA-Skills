# Download Guard v5.4 — Reference

> 本文件是 SKILL.md 的支持文档，包含详细参考信息。
> SKILL.md 只保留核心执行逻辑，详细信息按需从此文件加载。

---

## 一、三类路径详细参考

### 类型 A — 缓存目录（改路径：完全安全）

| 工具 | 缓存路径命令 | 说明 |
|------|------------|------|
| pip cache | `pip cache dir` | 临时文件，改了只影响下载速度 |
| npm cache | `npm config get cache` | 同上 |
| conda pkgs | `conda config --show pkgs_dirs` | 同上 |
| yarn cache | `yarn cache dir` | 同上 |
| pnpm store | `pnpm store path` | 同上 |
| uv cache | `uv cache dir` | 同上 (v5.4) |
| cargo registry | `$CARGO_HOME\registry` | Rust 包缓存 (v5.4) |
| go module cache | `$GOPATH\pkg` | Go 模块缓存 (v5.4) |

> ✅ 缓存是临时文件，删掉重建没副作用，随意迁移。

### 类型 B — 包安装目录（改路径：必须同步更新 PATH）

#### B1 — npm 全局包

```
安装位置 = (npm prefix)\node_modules\xxx
可执行文件 = (npm prefix)\xxx.cmd   ← 必须在 PATH 里
```

**Agent 在修改 npm prefix 前必须检查**：
1. 新路径是否存在 → 不存在则创建
2. 新路径是否已在 PATH → 若未在，输出修复命令并等用户确认
3. 新路径是否含空格 → 含空格会导致 .cmd 脚本在 Windows 上解析失败

#### B2 — pip 包

```
pip cache dir   ← 类型 A，改了没问题
site-packages   ← 类型 B，由 Python 解释器决定，不建议改
```

> 如需隔离依赖，推荐 `python -m venv`，不要改全局 site-packages。

**`pip install --user` 特殊情况** (v5.4)：
- `--user` 模式安装到 `%APPDATA%\Python\PythonXX\site-packages`，通常在 C 盘
- 如果检测到 `--user` 安装 → 建议改用 venv 替代
- 这是 B2+ 类型：虽然可以迁移 `PYTHONUSERBASE`，但容易引发兼容性问题

#### B3 — conda 环境

```powershell
# 添加额外的 envs 目录，而不是移动默认位置
conda config --add envs_dirs "D:\conda-envs"
```

#### B4 — cargo 全局安装 (v5.4)

```
安装位置 = $CARGO_HOME\bin\xxx.exe
CARGO_HOME 默认 = %USERPROFILE%\.cargo
```

- 默认在 C 盘，可以通过设置 `CARGO_HOME` 环境变量迁移
- 迁移后需要把新的 `bin` 目录加入 PATH

#### B5 — go 全局安装 (v5.4)

```
安装位置 = $GOPATH\bin\xxx.exe  或  $HOME\go\bin\xxx.exe
```

- 默认在 C 盘，可以通过设置 `GOPATH` 环境变量迁移
- 迁移后需要把新的 `bin` 目录加入 PATH

### 类型 C — 文件存放目录（改路径：完全安全）

| 操作 | 说明 |
|------|------|
| curl/wget 下载 | 纯文件，放哪都行 |
| git clone | 本地副本，与程序无关 |
| HuggingFace/Ollama 模型 | 数据文件，改路径只需更新加载配置 |
| 数据集 | 纯数据 |

> ✅ 这是本 Skill 管控的主要对象，指定到任何非系统目录均安全。

---

## 二、含空格路径安全规则

| 操作 | 含空格路径 | 说明 |
|------|----------|------|
| 存放下载文件（类型 C） | ✅ 安全 | |
| git clone 目标 | ✅ 安全 | git 支持引号路径 |
| pip cache 目录 | ✅ 安全 | pip 内部处理引号 |
| npm prefix | ❌ **危险** | .cmd 脚本已知 bug |
| conda envs | ⚠️ 风险 | 部分激活脚本不兼容 |
| cargo home | ⚠️ 风险 | 部分构建脚本不兼容 |
| go path | ✅ 安全 | Go 原生支持 |

---

## 三、PATH 修复模板

### npm prefix 不在 PATH

```powershell
$prefix = (npm config get prefix) -replace "`n",""

# 临时生效
$env:PATH += ";$prefix"

# 永久生效（重启终端后生效）
[Environment]::SetEnvironmentVariable(
    "PATH",
    ([Environment]::GetEnvironmentVariable("PATH","User") + ";$prefix"),
    "User"
)
Write-Output "PATH updated. Restart your terminal to take effect."
```

### cargo/bin 不在 PATH (v5.4)

```powershell
$cargoBin = "$env:CARGO_HOME\bin"
if (-not $env:CARGO_HOME) { $cargoBin = "$env:USERPROFILE\.cargo\bin" }

# 临时生效
$env:PATH += ";$cargoBin"

# 永久生效
[Environment]::SetEnvironmentVariable(
    "PATH",
    ([Environment]::GetEnvironmentVariable("PATH","User") + ";$cargoBin"),
    "User"
)
```

### go/bin 不在 PATH (v5.4)

```powershell
$goBin = if ($env:GOPATH) { "$env:GOPATH\bin" } else { "$env:USERPROFILE\go\bin" }

# 临时生效
$env:PATH += ";$goBin"

# 永久生效
[Environment]::SetEnvironmentVariable(
    "PATH",
    ([Environment]::GetEnvironmentVariable("PATH","User") + ";$goBin"),
    "User"
)
```

---

## 四、配置参数详细说明

**一份 config.md，Agent 直接读写，用户也可以手动编辑。**

| 参数 | 说明 | 初始值 |
|------|------|--------|
| `SETUP_DONE` | 是否已完成首次配置 | `false` → 首次激活后改为 `true` |
| `DOWNLOAD_ROOT` | 文件存放根目录 | 首次激活时由用户指定 |
| `MIN_FREE_GB` | 低于此值阻止下载 | `0.5` |
| `WARN_FREE_GB` | 低于此值警告 | `2` |
| `C_DRIVE_WARN_GB` | C 盘低于此值附加警告 | `5` |
| `ALLOW_SPACE_IN_TOOL_PATH` | 是否允许工具路径含空格 | `false` |
| `EXEMPT_PATHS` | 豁免路径 | 空 |
| `LOG_RETENTION_DAYS` | 日志保留天数 | `30` |
| `LOG_ARCHIVE_MAX_MB` | 归档文件最大 MB | `10` |

**关键规则**：
- 首次激活时 Agent 直接在对话中问用户，把答案写入 config.md
- 已配置过的用户（SETUP_DONE: true）跳过引导
- 手动编辑 config.md 立即生效，无需重启
- Agent 写入 config.md 后必须读回验证（v5.4）

---

## 五、脚本文件清单

| 脚本 | 用途 | exit codes |
|------|------|------------|
| `scripts/check-space.ps1` | 检查目标盘剩余 + 路径可用性 | 0=OK/WARN, 1=空间不足, 2=路径不可用 (v5.4) |
| `scripts/log-download.ps1` | 追加下载记录 + 自动清理过期日志 | 0=正常 |
| `scripts/scan-tool-cache.ps1` | 扫描工具缓存位置，识别 C 盘项 | 0=正常 |
| `scripts/migrate-cache.ps1` | 一键将工具缓存迁移到 DOWNLOAD_ROOT | 0=正常, 1=未配置 |

---

## 六、已知局限

| 局限 | 说明 |
|------|------|
| 仅 Windows | PowerShell 脚本，macOS/Linux 暂不支持 |
| 不拦截系统后台下载 | Windows Update / Defender 不在管控范围 |
| 无法预知 git clone 大小 | 下载后补记日志 |
| npm 含空格路径 bug | Agent 会主动警告，但无法修复 npm 本身 |
| 仅追踪 Agent 触发的下载 | 用户手动下载不会被记录 |
| nvm 管理的 Node.js | nvm 切版本后 npm prefix 可能变回 C 盘，不在自动管控范围 (v5.4) |
| pip install --user | 默认装到 C 盘的 user site-packages，建议改用 venv (v5.4) |
| 编译中间产物 | cmake build、cargo build 等编译输出不在管控范围 |
| Docker 镜像存储路径 | docker pull 下载的镜像由 Docker Desktop 管理，默认在 C 盘 WSL2 虚拟磁盘中 |

---

## 七、版本历史

| 版本 | 主要变化 |
|------|---------|
| v1.0 | 基础路径锁定 + 空间检查 + 下载日志 |
| v2.0 | 新增缓存扫描 + 一键迁移脚本 |
| v3.0 | 重构触发规则 + 强制状态卡 + 自然语言速查表 |
| v4.0 | 新增三类路径区分 + PATH 联动检查 + 含空格路径警告 |
| v5.0 | 面向公开发布：移除硬编码路径，两级配置，新增 setup-wizard |
| v5.1 | 简化架构：移除 config.local.md 和 setup-wizard.ps1，一份 config.md |
| v5.2 | 下载透明 + 清理规则：每次下载必须告知用户位置和状态；日志自动归档清理；路径询问策略 |
| v5.3 | **精简+智能**：SKILL.md瘦身到275行、精准description、下载大小感知、重复下载检测、venv识别、智能推荐默认盘、下载后验证 |
| v5.4 | **健壮性+覆盖面**：路径可用性校验（盘掉了/不可写→阻止，不 fallback 到 C:）、config 保护（写后读回验证+备份旧值）、扩展触发词（cargo/go/uv/pnpm/bun）、扫描覆盖更多工具（pnpm/bun/cargo/go/uv/nvm/HF/Ollama）、pip --user 和 nvm 场景提示 |
