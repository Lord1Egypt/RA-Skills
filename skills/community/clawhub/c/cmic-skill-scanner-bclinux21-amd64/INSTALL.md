# 给 Agent 的安装说明

当用户要求安装 `cmic-skill-scanner` 时，按下面流程执行。

## 目标

- 从 release 分支读取 `latest.json`
- 下载匹配平台的 ZIP 附件
- 使用 `latest.json` 中的 SHA-256 校验 ZIP
- 解压后得到 skill 目录
- 运行内置二进制确认安装成功

## 安装步骤

1. 读取仓库根目录的 `latest.json`。
2. 在 `assets[*]` 里选择匹配当前平台的条目。
3. 使用 `download_url` 下载 ZIP。
4. 计算 ZIP 的 SHA-256，与 `assets[*].sha256` 比对。
5. 解压 ZIP，进入解压后的 skill 根目录。
6. 打开其中的 `SKILL.md` 和 `INSTALL.md`。
7. 运行内置程序确认可用：

```bash
./assets/bin/skillscan version
./assets/bin/skillscan review /path/to/skill
./assets/bin/skillscan review /path/to/skills --output-dir /tmp/skillscan-out
```

## 引擎模式说明

默认使用 `auto` 模式：
- 优先使用 Cisco Skill Scanner（external backend）获得更强检测能力
- External 不可用时自动回退到内置 native 引擎
- **单二进制即可运行**，无需额外依赖

## Linux 平台兼容性

Linux 平台提供两种 x86_64 二进制包，请根据系统 glibc 版本选择合适的包：

| 包名称 | 适用系统 | glibc 要求 | 编译方式 |
|--------|---------|-----------|----------|
| `linux-amd64` | Ubuntu 20.04+, Debian 11+, RHEL 9+, Fedora 31+ 等 | glibc >= 2.30 | cross (GNU) |
| `bclinux21-amd64` | BCLinux 21, BCLinux 8.2, CentOS 7/8, RHEL 7/8, Amazon Linux 2 等 | 无 (musl 静态链接) | BCLinux 21 VM 本地编译 |

> 💡 **如何判断你的系统应该用哪个包？**
>
> 1. 先尝试 `linux-amd64`（标准包），运行 `ldd --version` 查看 glibc 版本，>= 2.30 即可使用
> 2. 如果运行时提示 `GLIBC_2.30 not found` 等错误，请使用 `bclinux21-amd64` 包
> 3. `bclinux21-amd64` 使用 musl libc，不受系统 glibc 版本限制
>
> **常见系统判断：**
> - `cat /etc/os-release | grep -i "bclinux\|bigcloud"` → BCLinux 系统 → 用 `bclinux21-amd64`
> - `ldd --version 2>&1 | head -1` → glibc < 2.30 → 用 `bclinux21-amd64`

## 安装 External Scanner（可选）

如需使用 Cisco Skill Scanner 获得更强检测能力：

### 方式一：Git Submodule（推荐）

```bash
# 克隆时一并获取
git clone --recursive https://github.com/your-org/cmic-skill-scanner.git

# 已有仓库中初始化
git submodule update --init --recursive
```

### 方式二：独立安装

```bash
# 克隆 Cisco Skill Scanner
git clone https://github.com/cisco-ai-defense/skill-scanner.git external/skill-scanner

# 或指定工作目录
skillscan scan /path/to/target --engine external \
  --scanner-workdir /path/to/skill-scanner
```

### External Scanner 依赖

External scanner 需要：
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 包管理器

首次运行时会自动创建虚拟环境并安装依赖。

## 说明

- `latest.json`、`benchmark-summary.md` 和 `SHA256SUMS` 位于 release 分支。
- ZIP 文件只存在于 Gitee Release 附件，不在 git 分支内。
- 如需批量部署，优先使用 `examples/enterprise/install-openclaw-skillscan.sh`。

## 异常处理

- 当前平台无对应资产时，终止安装流程。
- 校验失败时，删除下载内容并终止安装。
- Agent 不支持固定技能目录时，保留解压目录并在后续任务中显式引用该本地路径。
- External scanner 不可用时，auto 模式自动回退到 native，不影响基本功能。
