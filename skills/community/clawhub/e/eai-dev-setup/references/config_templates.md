# 配置文件模板（中国网络优化版）

本文档提供各类配置文件的模板，包括环境变量、conda 配置、shell 配置、国内镜像源、代理配置等。

## 目录
- [Shell 环境变量配置](#shell-环境变量配置)
- [Conda 配置](#conda-配置)
- [Zsh 配置](#zsh-配置)
- [国内镜像源配置](#国内镜像源配置)
- [代理配置](#代理配置)
- [桌面快捷方式](#桌面快捷方式)

---

## Shell 环境变量配置

### .bashrc 完整模板

将以下内容追加到 `~/.bashrc` 文件末尾：

```bash
# ==============================================================================
# EAI Dev Setup - 环境变量配置（中国网络优化版）
# 由 eai-dev-setup 自动添加
# ==============================================================================

# ------------------------------------------------------------------------------
# HuggingFace 镜像配置
# ------------------------------------------------------------------------------
export HF_ENDPOINT=https://hf-mirror.com

# ------------------------------------------------------------------------------
# CUDA 环境变量 (根据实际安装版本调整)
# ------------------------------------------------------------------------------
export CUDA_PATH=/usr/local/cuda-12.6
export PATH=$CUDA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH
export CUDADIR=$CUDA_PATH

# cuDNN 环境变量
export CUDNN_INCLUDE_DIR=$CUDA_PATH/include
export CUDNN_LIB_DIR=$CUDA_PATH/lib64

# ------------------------------------------------------------------------------
# Conda 环境变量
# ------------------------------------------------------------------------------
# >>> conda initialize >>>
__conda_setup="$('/home/YOUR_USERNAME/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/YOUR_USERNAME/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/YOUR_USERNAME/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/YOUR_USERNAME/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# ------------------------------------------------------------------------------
# pip 镜像别名（快速安装）
# ------------------------------------------------------------------------------
alias pipi='pip install -i https://pypi.tuna.tsinghua.edu.cn/simple'
alias pipia='pip install -i https://mirrors.aliyun.com/pypi/simple/'

# ------------------------------------------------------------------------------
# 自定义环境变量
# ------------------------------------------------------------------------------
export PYTHONIOENCODING=utf-8

# ------------------------------------------------------------------------------
# 别名设置
# ------------------------------------------------------------------------------
# 常用命令别名
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias grep='grep --color=auto'

# Git 别名
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph'

# Conda 别名
alias cenv='conda env list'
alias cact='conda activate'
alias cdeact='conda deactivate'

# HuggingFace 别名
alias hfd='huggingface-cli download'

# ------------------------------------------------------------------------------
# PATH 扩展
# ------------------------------------------------------------------------------
export PATH=$HOME/.local/bin:$PATH
```

---

## Conda 配置

### .condarc 基础模板（国内镜像）

创建 `~/.condarc` 文件：

```yaml
# Conda 配置文件（清华镜像源）
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - defaults

show_channel_urls: true

# 将环境存储在指定路径（避免占用主目录空间）
envs_dirs:
  - ~/workspace/anaconda3/envs
  - ~/.conda/envs

pkgs_dirs:
  - ~/workspace/anaconda3/pkgs
  - ~/.conda/pkgs
```

---

## Zsh 配置

### .zshrc 完整模板

```bash
# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# 主题设置
ZSH_THEME="robbyrussell"
# ZSH_THEME="agnoster"  # 更美观的主题

# 插件配置
plugins=(
    git
    extract
    zsh-autosuggestions
    zsh-syntax-highlighting
    sudo
    copypath
    history
    python
)

source $ZSH/oh-my-zsh.sh

# 用户配置
# ------------------------------------------------------------------------------

# 环境变量
export PATH=$HOME/bin:$HOME/.local/bin:$PATH
export LANG=en_US.UTF-8

# HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com

# CUDA 环境变量
export CUDA_PATH=/usr/local/cuda-12.6
export PATH=$CUDA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH

# Conda 初始化
# >>> conda initialize >>>
__conda_setup="$('/home/YOUR_USERNAME/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/YOUR_USERNAME/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/YOUR_USERNAME/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/YOUR_USERNAME/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# pip 镜像别名
alias pipi='pip install -i https://pypi.tuna.tsinghua.edu.cn/simple'
alias pipia='pip install -i https://mirrors.aliyun.com/pypi/simple/'

# 别名
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias cls='clear'
alias ..='cd ..'
alias ...='cd ../..'

# Git 别名
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'

# HuggingFace 别名
alias hfd='huggingface-cli download'

# 历史记录配置
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
```

---

## 国内镜像源配置

### pip 配置

**永久配置（推荐）**：
```bash
# 清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**配置文件 `~/.pip/pip.conf`**：
```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

**常用镜像源**：
| 源 | URL |
|---|---|
| 清华 | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| 阿里云 | `https://mirrors.aliyun.com/pypi/simple/` |

### conda 配置

```bash
# 配置清华源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --set show_channel_urls yes
```

### apt 配置（Ubuntu 22.04）

```bash
# 替换为清华源
sudo sed -i 's@archive.ubuntu.com@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list
sudo sed -i 's@security.ubuntu.com@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list
sudo apt update
```

### Docker 镜像配置

```bash
# 配置阿里云镜像加速器
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://2jgearuk.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 代理配置

### GitHub 代理（gh-proxy.org）

**全局配置**：所有 git 操作自动通过代理加速

```bash
# 配置全局代理
git config --global url."https://gh-proxy.org/https://github.com/".insteadOf "https://github.com/"
```

**效果**：
```bash
# 克隆仓库会自动通过代理加速
git clone https://github.com/user/repo.git

# 实际访问的是
# https://gh-proxy.org/https://github.com/user/repo.git
```

**取消代理**：
```bash
git config --global --unset url."https://gh-proxy.org/https://github.com/".insteadOf
```

### HuggingFace 镜像（hf-mirror.com）

**配置环境变量**：
```bash
# 添加到 .bashrc
echo "export HF_ENDPOINT=https://hf-mirror.com" >> ~/.bashrc
source ~/.bashrc
```

**使用方法**：
```bash
# 下载模型
huggingface-cli download --resume-download gpt2 --local-dir gpt2

# 下载数据集
huggingface-cli download --repo-type dataset --resume-download wikitext --local-dir wikitext

# 禁用软链接（所见即所得）
huggingface-cli download --resume-download gpt2 --local-dir gpt2 --local-dir-use-symlinks False

# 在 Python 代码中使用
from huggingface_hub import snapshot_download
snapshot_download(repo_id="bert-base-uncased", local_dir="./bert-base")
```

**Python 代码中设置镜像**：
```python
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from transformers import AutoModel
model = AutoModel.from_pretrained("bert-base-uncased")
```

### Git 代理（Clash 等）

**配置本地代理**：
```bash
# 配置代理（如使用 Clash，默认端口 7890）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 仅对 GitHub 使用代理
git config --global http.https://github.com.proxy http://127.0.0.1:7890
```

---

## 桌面快捷方式

### 创建桌面快捷方式方法

```bash
# 创建 .desktop 文件
nano ~/.local/share/applications/appname.desktop

# 设置权限
chmod +x ~/.local/share/applications/appname.desktop
```

### Chrome 桌面快捷方式

```desktop
[Desktop Entry]
Version=1.0
Name=Google Chrome
GenericName=Web Browser
Exec=/usr/bin/google-chrome-stable %U
Icon=google-chrome
Type=Application
Categories=Network;WebBrowser;
```

### VSCode 桌面快捷方式

```desktop
[Desktop Entry]
Name=Visual Studio Code
Comment=Code Editing. Redefined.
Exec=/usr/share/code/code --unity-launch %F
Icon=vscode
Type=Application
Categories=TextEditor;Development;IDE;
```

### Clash Verge 桌面快捷方式

```desktop
[Desktop Entry]
Name=Clash Verge
Comment=Clash GUI Client
Exec=/opt/clash-verge/clash-verge
Icon=clash-verge
Type=Application
Categories=Network;
```

---

## 使用脚本配置

### 配置环境变量

```bash
# 配置 CUDA 环境
python scripts/config_env.py --setup-cuda --cuda-version 12.6

# 配置 cuDNN 环境
python scripts/config_env.py --setup-cudnn --cuda-version 12.6

# 配置 conda 环境
python scripts/config_env.py --setup-conda --conda-path ~/anaconda3
```

### 配置代理

```bash
# 配置 GitHub 代理
git config --global url."https://gh-proxy.org/https://github.com/".insteadOf "https://github.com/"

# 配置 HuggingFace 镜像
echo "export HF_ENDPOINT=https://hf-mirror.com" >> ~/.bashrc
source ~/.bashrc
```

### 安装 Docker

```bash
python scripts/install_docker.py --install
```

### 安装 Zsh

```bash
python scripts/setup_zsh.py --use-sudo --install-oh-my-zsh --china-mirror \
    --plugins "git zsh-autosuggestions zsh-syntax-highlighting"
```
