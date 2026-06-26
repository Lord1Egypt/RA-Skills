# 安装指南 / Installation Guide — Win / Mac / Linux

> Claude Code CLI 的安装是所有平台通用的 `npm install -g @anthropic-ai/claude-code`。
> 真正的差异在于前置条件和平台特有的坑。

---

## 通用前置条件 (所有平台)

| 组件 | 最低版本 | 检查命令 |
|---|---|---|
| Node.js | 18.x | `node --version` |
| npm | 9.x | `npm --version` |
| Git | 任意 | `git --version` |

---

## Windows (10/11, x64/ARM64)

### 第一步：安装 Git for Windows

**必须** — npm 全局包安装依赖 Git。

1. 下载: https://git-scm.com/download/win
2. 安装时选择默认选项即可
3. 验证: `git --version`

### 第二步：安装 Node.js

1. 下载: https://nodejs.org/ (选 LTS 版本, .msi 安装包)
2. 安装时确保勾选 **"Add to PATH"**
3. 安装完成后**重启终端**
4. 验证: `node --version` 和 `npm --version`

### 第三步：安装 Claude Code

```cmd
npm install -g @anthropic-ai/claude-code
```

验证:
```cmd
claude --version
```

### Windows 特殊注意事项

- **终端选择**: 推荐 Windows Terminal 或 CMD（管理员模式）。PowerShell 也可以，但某些配置脚本可能用 CMD。
- **npm 全局路径**: 如果 `claude --version` 不成功，可能是 npm 全局包路径不在 PATH。运行 `npm config get prefix` 查看全局路径，确保它在系统 PATH 中。
- **PATH 刷新**: 安装后如果命令不生效，关闭并重新打开终端。

---

## macOS

### 第一步：安装 Homebrew (如果没有)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 第二步：安装 Git 和 Node.js

```bash
# Git (通常系统自带)
xcode-select --install

# Node.js
brew install node@20
```

验证:
```bash
git --version
node --version
npm --version
```

### 第三步：安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

### macOS 特殊注意事项

- **Xcode Command Line Tools**: 如果 `git` 不可用，运行 `xcode-select --install`。
- **Homebrew 路径**: Apple Silicon (M1/M2/M3) Mac 的 Homebrew 路径是 `/opt/homebrew/bin`。如果在 Intel Mac 上是 `/usr/local/bin`。
- **权限问题**: npm 全局安装通常不会遇到权限问题，但如果遇到 `EACCES`，参考 npm 官方文档修改全局路径。

---

## Linux (Ubuntu/Debian / Fedora / Arch)

### 第一步：安装 Git

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install git -y

# Fedora
sudo dnf install git -y

# Arch
sudo pacman -S git
```

### 第二步：安装 Node.js (推荐使用 nvm)

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# 重新加载 shell
source ~/.bashrc   # 或 source ~/.zshrc

# 安装 Node.js LTS
nvm install 20
nvm use 20

# 验证
node --version
npm --version
```

> 不推荐用 `sudo apt install nodejs` — apt 源的 Node.js 版本通常太老。

### 第三步：安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

### Linux 特殊注意事项

- **WSL2 (Windows)**: 如果用 WSL2，此时你在 Linux 环境，不是 Windows。配置文件的路径是 `~/.claude/` (即 `/home/用户/.claude/`)，不是 Windows 的 `C:\Users\...`。Git 和 Node.js 在 WSL2 内单独安装，不需要 Windows 版本。
- **headless 服务器**: 如果没有桌面环境，Claude Code 完全支持。但某些交互提示可能需要配置。
- **包管理器差异**: 以上命令按发行版不同。用你的发行版对应的包管理器即可。

---

## 安装后统一验证

```bash
# 1. 检查 Claude Code 版本
claude --version

# 2. 进入项目目录
cd /path/to/your/project

# 3. 启动 Claude Code
claude

# 4. 在交互界面中输入
/status
```

如果 `/status` 显示 Connected，安装成功。接下来配置 Provider（回到 SKILL.md Phase 3）。
