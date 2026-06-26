# Ubuntu 开发工具清单（中国网络优化版）

本文档列出所有可自动安装的工具，包括安装方式、权限要求和注意事项。

## 目录
- [基础工具](#基础工具)
- [开发环境](#开发环境)
- [终端工具](#终端工具)
- [其他工具](#其他工具)
- [国内镜像源配置](#国内镜像源配置)
- [代理配置](#代理配置)

---

## 基础工具

### 浏览器类

#### Google Chrome
- **作用**：主流浏览器，比 Firefox 更流畅
- **安装方式**：deb 包下载安装
- **下载地址**：`https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`
- **需要 sudo**：是
- **包名**：`google-chrome-stable`

#### Microsoft Edge
- **作用**：微软浏览器，兼容性好
- **安装方式**：deb 包下载安装
- **下载地址**：`https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/`
- **需要 sudo**：是
- **包名**：`microsoft-edge-stable`

### 编辑器类

#### Visual Studio Code
- **作用**：必装的代码编辑器
- **安装方式**：deb 包下载安装
- **下载地址**：
  - 官方：`https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64`
  - 国内镜像：`https://mirrors.huaweicloud.com/vscode/`
- **需要 sudo**：是
- **包名**：`code`

#### Cursor
- **作用**：AI 代码编辑器
- **安装方式**：deb 包下载安装
- **下载地址**：`https://www.cursor.com/api/download?platform=linux&arch=x64`
- **需要 sudo**：是
- **包名**：`cursor`

### 办公通讯类

#### 飞书
- **作用**：企业协作工具
- **安装方式**：deb 包下载安装
- **下载地址**：`https://www.feishu.cn/api/download?platform=linux&arch=x64`
- **需要 sudo**：是
- **包名**：`feishu`

#### ToDesk
- **作用**：远程桌面工具
- **安装方式**：deb 包下载安装
- **下载地址**：`https://www.todesk.com/download/linux.html`
- **需要 sudo**：是
- **包名**：`todesk`

#### WPS Office
- **作用**：办公文档套件
- **安装方式**：deb 包下载安装
- **下载地址**：`https://www.wps.cn/product/wpslinux`
- **需要 sudo**：是
- **包名**：`wps-office`

#### 搜狗输入法
- **作用**：中文输入法
- **安装方式**：deb 包安装 + fcitx 配置
- **下载地址**：`https://shurufa.sogou.com/linux`
- **需要 sudo**：是
- **需要重启**：是
- **安装步骤**：
  ```bash
  # 1. 安装 fcitx 框架
  sudo apt install fcitx fcitx-bin fcitx-table-all fcitx-config-gtk
  
  # 2. 安装搜狗输入法 deb 包
  sudo dpkg -i sogoupinyin_xxx_amd64.deb
  
  # 3. 修复依赖
  sudo apt install -f
  
  # 4. 重启系统
  sudo reboot
  ```

### 代理工具

#### Clash Verge Rev
- **作用**：代理工具 GUI 版本，方便科学上网
- **安装方式**：deb 包下载安装
- **下载地址**：`https://github.com/clash-verge-rev/clash-verge-rev/releases`
- **版本选择**：
  - Ubuntu 22.04：选择 1.7 版本
  - Ubuntu 20.04：选择 1.6 版本
- **需要 sudo**：是
- **注意**：
  - 安装后需要导入订阅或配置文件
  - **推荐使用 GitHub 代理下载**

---

## 开发环境

### Conda (Anaconda/Miniconda)
- **作用**：Python 环境管理工具，深度学习必备
- **安装方式**：脚本安装
- **下载地址**：
  - 清华镜像：`https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/`
  - 官方：`https://www.anaconda.com/download`
- **需要 sudo**：否
- **国内镜像配置**：
  ```bash
  conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  conda config --set show_channel_urls yes
  ```

### Docker
- **作用**：容器化部署工具
- **安装方式**：使用阿里云镜像安装
- **安装脚本**：`scripts/install_docker.py`
- **需要 sudo**：是
- **安装命令**：
  ```bash
  python scripts/install_docker.py --install
  ```

### CUDA Toolkit
- **作用**：NVIDIA GPU 并行计算平台
- **安装方式**：deb 包安装
- **下载地址**：`https://developer.nvidia.com/cuda-downloads`
- **需要 sudo**：是
- **需要重启**：是
- **详细步骤**：参考 [references/cuda_guide.md](cuda_guide.md)

### cuDNN
- **作用**：深度学习加速库
- **安装方式**：deb 包安装
- **下载地址**：`https://developer.nvidia.com/cudnn`
- **需要 sudo**：是

### ROS (Robot Operating System)
- **作用**：机器人操作系统
- **安装方式**：一键安装脚本 (fishros)
- **安装命令**：
  ```bash
  wget http://fishros.com/install -O fishros
  chmod +x fishros
  sudo ./fishros
  ```

---

## 终端工具

#### Terminator
- **作用**：多窗口终端，可分屏
- **安装方式**：apt 安装
- **安装命令**：`sudo apt install terminator -y`
- **需要 sudo**：是
- **包名**：`terminator`

#### Zsh
- **作用**：增强型 shell
- **安装方式**：apt 安装 + oh-my-zsh
- **安装脚本**：`scripts/setup_zsh.py`
- **需要 sudo**：是

#### Oh-My-Zsh
- **作用**：zsh 配置管理框架
- **国内镜像**：`https://gitee.com/shmhlsy/oh-my-zsh-install.sh`
- **安装命令**：
  ```bash
  # 使用国内镜像安装
  sh -c "$(curl -fsSL https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh)"
  ```

#### Zsh 插件
- **zsh-autosuggestions**：命令自动补全
- **zsh-syntax-highlighting**：命令语法高亮

**安装命令**：
```bash
# 使用 Gitee 镜像
git clone https://gitee.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://gitee.com/Annihilater/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

---

## 其他工具

#### GParted
- **作用**：分区管理工具
- **安装命令**：`sudo apt install gparted -y`
- **需要 sudo**：是

#### Kazam
- **作用**：截图和录屏工具
- **安装命令**：`sudo apt install kazam -y`
- **需要 sudo**：是

---

## 国内镜像源配置

### pip 镜像源

```bash
# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 临时使用
pip install package_name -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### conda 镜像源

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --set show_channel_urls yes
```

### apt 镜像源

```bash
sudo sed -i 's@archive.ubuntu.com@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list
sudo apt update
```

### Docker 镜像源

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://2jgearuk.mirror.aliyuncs.com"]
}
EOF
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
- 所有 `git clone https://github.com/xxx` 操作自动通过代理加速
- 无需手动修改 URL

**取消代理**：
```bash
git config --global --unset url."https://gh-proxy.org/https://github.com/".insteadOf
```

### HuggingFace 镜像（hf-mirror.com）

**配置环境变量**：
```bash
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
```

**Python 代码中使用**：
```python
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from transformers import AutoModel
model = AutoModel.from_pretrained("bert-base-uncased")
```

---

## 安装建议

### 新系统初始化顺序
1. **配置 GitHub 代理** - 加速所有 GitHub 访问
2. **配置 HuggingFace 镜像** - 加速模型下载
3. **安装代理工具** - Clash Verge（可选）
4. **安装基础工具** - Chrome、vscode 等
5. **安装开发环境** - Docker、conda、CUDA
6. **安装终端工具** - zsh、terminator
7. **重启系统** - 使驱动生效

### 最小化安装
- **必装**：Chrome、vscode、conda、Docker
- **推荐**：terminator、zsh
- **可选**：其他工具

### 完整安装（算法工程师）
- **必装**：Chrome、vscode、conda、CUDA、cuDNN、Docker
- **推荐**：terminator、zsh + oh-my-zsh、kazam
- **可选**：Edge、Cursor、飞书、腾讯会议

---

## 常见问题

### Q: GitHub 访问慢或无法访问怎么办？
A: 
```bash
# 方案1：使用 gh-proxy 代理（推荐）
git config --global url."https://gh-proxy.org/https://github.com/".insteadOf "https://github.com/"

# 方案2：使用 Gitee 镜像（如 oh-my-zsh）
```

### Q: HuggingFace 模型下载慢？
A: 
```bash
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download model_name --local-dir ./model
```

### Q: Docker Hub 被封怎么办？
A: 
```bash
# 配置阿里云镜像加速器
python scripts/install_docker.py --config-mirror
```

### Q: pip 安装包很慢？
A: 
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
