# 安装指南

**适用场景**: 首次使用 fzf，需要在系统上安装并配置 Shell 集成

---

## 一、安装前准备

### 目标

确保系统满足安装条件，并了解安装后的功能范围

### 前置条件

- macOS / Linux / Windows（WSL 或 Git Bash）
- 终端模拟器（Terminal、iTerm2、Windows Terminal 等）
- Shell：bash 3.2+、zsh 5.0+、fish 2.3+、PowerShell 5.1+

### 检查是否已安装

**AI 执行说明**: AI 将自动检查 fzf 是否已存在于系统中

```bash
# 检查 fzf 是否已安装
fzf --version

# 检查 fzf 位置
which fzf
```

**期望结果**:
- 如显示版本号（如 `0.54.0`）则已安装，可跳至 [Shell 集成配置](#四配置-shell-集成)
- 如提示 `command not found`，则继续下面的安装步骤

---

## 二、安装 fzf

### 方法1: 使用 Homebrew 安装（macOS / Linux，推荐）

**AI 执行说明**: AI 可直接执行以下命令完成安装

```bash
# macOS 或 Linux（需先安装 Homebrew）
brew install fzf

# 验证安装
fzf --version
```

**期望结果**:
```
0.54.0 (brew)
```

---

### 方法2: 使用 git 克隆安装（Linux / macOS 通用）

**AI 执行说明**: AI 可自动完成克隆与安装脚本执行

```bash
# 克隆到 ~/.fzf 目录
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf

# 运行安装脚本（会询问是否配置 Shell 集成）
~/.fzf/install
```

安装脚本会询问三个问题：
- `Do you want to enable fuzzy auto-completion?` → 输入 `y`
- `Do you want to enable key bindings?` → 输入 `y`
- `Do you want to update your shell configuration files?` → 输入 `y`

---

### 方法3: 下载预编译二进制文件

**AI 执行说明**: AI 会根据系统架构自动选择正确版本

```bash
# 查询最新版本
# 访问 https://github.com/junegunn/fzf/releases 下载对应平台的压缩包

# Linux x86_64 示例
curl -LO https://github.com/junegunn/fzf/releases/latest/download/fzf-linux_amd64.tar.gz
tar -xzf fzf-linux_amd64.tar.gz
sudo mv fzf /usr/local/bin/

# macOS Apple Silicon 示例
curl -LO https://github.com/junegunn/fzf/releases/latest/download/fzf-darwin_arm64.tar.gz
tar -xzf fzf-darwin_arm64.tar.gz
sudo mv fzf /usr/local/bin/
```

---

### 方法4: 包管理器安装（Linux 各发行版）

**AI 执行说明**: AI 根据检测到的 Linux 发行版自动选择命令

```bash
# Ubuntu / Debian
sudo apt install fzf

# Fedora / RHEL / CentOS
sudo dnf install fzf

# Arch Linux / Manjaro
sudo pacman -S fzf

# openSUSE
sudo zypper install fzf

# Alpine Linux
sudo apk add fzf

# Nix
nix-env -iA nixpkgs.fzf
```

---

### 方法5: Windows 安装

**Scoop（推荐）**:
```powershell
scoop install fzf
```

**Chocolatey**:
```powershell
choco install fzf
```

**winget**:
```powershell
winget install fzf
```

---

## 三、升级 fzf

```bash
# Homebrew 升级
brew upgrade fzf

# git 安装方式升级
cd ~/.fzf && git pull && ./install

# 查看当前版本
fzf --version
```

---

## 四、配置 Shell 集成

Shell 集成是 fzf 最强大的特性之一，启用后可获得以下快捷键：

| 快捷键 | 功能 |
|--------|------|
| `CTRL-T` | 在命令行光标处插入选中的文件路径 |
| `CTRL-R` | 搜索历史命令并粘贴到命令行 |
| `ALT-C` | cd 进入选中的目录 |

### Bash 配置

**AI 执行说明**: AI 将自动添加以下内容到 ~/.bashrc

```bash
# 添加到 ~/.bashrc
eval "$(fzf --bash)"
```

使配置生效：
```bash
source ~/.bashrc
```

---

### Zsh 配置

**AI 执行说明**: AI 将自动添加以下内容到 ~/.zshrc

```bash
# 添加到 ~/.zshrc
eval "$(fzf --zsh)"
```

使配置生效：
```bash
source ~/.zshrc
```

---

### Fish 配置

```bash
# Fish shell 使用独立脚本方式
# 将以下内容加入 ~/.config/fish/config.fish
fzf --fish | source
```

---

### PowerShell 配置

```powershell
# 添加到 $PROFILE
# PSFzf 模块提供更完整的集成
Install-Module PSFzf -Scope CurrentUser
Import-Module PSFzf
```

---

## 五、安装推荐搭配工具

fzf 与以下工具搭配使用效果更佳：

### bat（带语法高亮的 cat）

```bash
# macOS
brew install bat

# Ubuntu/Debian
sudo apt install bat

# 用于 fzf 预览
fzf --preview 'bat --color=always {}'
```

### fd（更快的 find 替代品）

```bash
# macOS
brew install fd

# Ubuntu/Debian
sudo apt install fd-find

# 设置 fzf 使用 fd 作为文件来源
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
```

### ripgrep（更快的 grep）

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# 结合 fzf 实时搜索文件内容
fzf --ansi --disabled --query "" \
    --bind "change:reload:rg --line-number --color=always {q} || true" \
    --delimiter : --preview 'bat --color=always {1} --highlight-line {2}'
```

---

## 六、验证安装

**AI 执行说明**: AI 将依次执行以下验证命令

```bash
# 验证 fzf 版本
fzf --version

# 验证基础功能（按 Esc 退出）
echo -e "apple\nbanana\norange" | fzf

# 验证 Shell 集成（按 CTRL-R 应弹出历史搜索）
# 需要重新打开终端或 source 配置文件

# 测试文件选择（CTRL-T）
# 在命令提示符下按 CTRL-T
```

**成功标志**:
- fzf 版本号正确显示
- 基础模糊查找界面弹出
- CTRL-R 历史搜索可用
- CTRL-T 文件选择可用

---

## 七、常见安装问题

### 问题1: Homebrew 安装后命令未找到

```bash
# 检查 PATH 是否包含 Homebrew bin 目录
echo $PATH | tr ':' '\n' | grep brew

# 手动添加到 PATH（macOS Apple Silicon）
export PATH="/opt/homebrew/bin:$PATH"
```

### 问题2: Shell 集成未生效

```bash
# 检查配置文件是否包含 fzf 初始化
grep -n "fzf" ~/.bashrc ~/.zshrc 2>/dev/null

# 重新加载配置
source ~/.zshrc  # 或 source ~/.bashrc
```

### 问题3: CTRL-T / CTRL-R 无响应

```bash
# 确认 fzf 版本支持 --bash / --zsh 参数（需 0.48.0+）
fzf --version

# 旧版安装方式检查
ls ~/.fzf/shell/
```

---

## 完成确认

### 检查清单

- [ ] fzf 已安装并可执行
- [ ] `fzf --version` 显示正确版本
- [ ] Shell 集成已配置（eval "$(fzf --bash/--zsh)"）
- [ ] CTRL-R 历史搜索可用
- [ ] CTRL-T 文件选择可用
- [ ] （可选）bat、fd、ripgrep 已安装

### 下一步

继续阅读 [快速开始](02-quickstart.md) 学习 fzf 的核心用法
