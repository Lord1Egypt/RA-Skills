---
name: eai-dev-setup
version: 1.0.0
description: 自动化配置 Ubuntu 算法开发环境（中国网络优化版）；当用户需要初始化新系统、配置深度学习开发环境、批量安装开发工具时使用
author: Jessy-Huang
license: MIT
repository: https://github.com/Jessy-Huang/Embodied_ubuntu-dev-setup
dependency:
  python:
    - requests==2.31.0
---

# EAI 开发环境自动配置

## 任务目标

- 本 Skill 用于：自动化配置 Ubuntu 系统的算法开发环境
- 能力包含：系统检测、工具安装、环境配置、GPU 驱动安装
- 触发条件：新系统初始化、环境重置、批量安装开发工具

## 重要约定

1. **分步执行**：按步骤引导用户完成配置，每步询问是否执行
2. **进度提示**：长时间操作（下载、安装）显示进度信息
3. **用户确认**：涉及 sudo 权限的操作必须用户确认
4. **禁止删除**：不会删除任何已有文件

---

## 安装步骤流程

### 第一步：系统检测（必需）

**目的**：了解当前系统状态，确定后续安装内容

**操作**：
```bash
python scripts/system_check.py
```

**输出内容**：
- Ubuntu 版本和内核
- 已安装的开发工具
- GPU 信息（如有）
- 可用磁盘空间

**时间**：约 10 秒

---

### 第二步：配置网络代理（推荐优先）

**目的**：加速后续 GitHub 和 HuggingFace 访问

#### 2.1 GitHub 代理配置

**说明**：使用 gh-proxy.org 加速所有 GitHub 访问

**是否执行**：询问用户

**命令**：
```bash
git config --global url."https://gh-proxy.org/https://github.com/".insteadOf "https://github.com/"
```

**验证**：
```bash
git config --global --get url."https://gh-proxy.org/https://github.com/".insteadOf
```

#### 2.2 HuggingFace 镜像配置

**说明**：使用 hf-mirror.com 加速模型下载

**是否执行**：询问用户

**命令**：
```bash
echo "export HF_ENDPOINT=https://hf-mirror.com" >> ~/.bashrc
```

**验证**：
```bash
echo $HF_ENDPOINT
```

**时间**：约 5 秒

---

### 第三步：安装基础工具

**目的**：安装浏览器、编辑器等日常工具

**工具列表**：
| 工具 | 说明 | 时间 |
|------|------|------|
| Chrome | 浏览器 | 约 1 分钟 |
| Edge | 浏览器（可选） | 约 1 分钟 |
| VSCode | 代码编辑器 | 约 1 分钟 |
| Cursor | AI 编辑器（可选） | 约 1 分钟 |
| 飞书 | 协作工具（可选） | 约 1 分钟 |

**安装方式**：逐个询问用户是否安装

**示例命令**：
```bash
# 安装 Chrome
python scripts/install_package.py --package-name google-chrome-stable \
    --install-type url \
    --deb-url "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" \
    --use-sudo
```

**进度提示**：
- 下载时显示：`[下载中] 正在下载 Chrome...`
- 安装时显示：`[安装中] 正在安装 Chrome...`
- 完成时显示：`[完成] Chrome 安装成功`

---

### 第四步：安装开发环境

**目的**：安装 Docker、conda、CUDA 等开发工具

#### 4.1 Docker 安装

**说明**：容器化工具，使用阿里云镜像安装

**是否执行**：询问用户

**命令**：
```bash
python scripts/install_docker.py --install
```

**进度提示**：
- `[1/6] 卸载旧版本 Docker...`
- `[2/6] 安装依赖包...`
- `[3/6] 添加 GPG 密钥...`
- `[4/6] 添加软件源...`
- `[5/6] 安装 Docker CE...`（约 2-5 分钟）
- `[6/6] 配置镜像加速器...`

**时间**：约 3-5 分钟

#### 4.2 Conda 安装

**说明**：Python 环境管理工具

**是否执行**：询问用户

**安装步骤**：
1. 询问安装 Anaconda 还是 Miniconda
2. 询问安装路径（默认 `~/anaconda3`）
3. 下载安装脚本（清华镜像）
4. 执行安装

**进度提示**：
- `[下载中] 正在从清华镜像下载 Anaconda...（约 500MB，可能需要几分钟）`
- `[安装中] 正在安装 Anaconda...`
- `[配置中] 正在配置环境变量...`

**时间**：约 5-10 分钟（取决于网速）

#### 4.3 CUDA/cuDNN 安装

**说明**：GPU 深度学习环境

**是否执行**：询问用户（检测到 NVIDIA GPU 时推荐）

**详细步骤**：参考 [references/cuda_guide.md](references/cuda_guide.md)

**重要提示**：
- ⚠️ CUDA 安装后需要重启系统
- 建议在最后一步执行

**进度提示**：
- `[检测中] 正在检测 GPU 和驱动...`
- `[下载中] 正在下载 CUDA Toolkit...（约 3GB）`
- `[安装中] 正在安装 CUDA...（约 2-5 分钟）`

**时间**：约 10-20 分钟

---

### 第五步：安装终端工具

**目的**：增强终端体验

#### 5.1 Terminator 安装

**说明**：多窗口终端

**是否执行**：询问用户

**命令**：
```bash
python scripts/install_package.py --package-name terminator --install-type apt --use-sudo
```

**时间**：约 30 秒

#### 5.2 Zsh + Oh-My-Zsh 安装

**说明**：增强型 shell

**是否执行**：询问用户

**命令**：
```bash
python scripts/setup_zsh.py --use-sudo --install-oh-my-zsh --china-mirror \
    --plugins "git zsh-autosuggestions zsh-syntax-highlighting"
```

**进度提示**：
- `[1/4] 安装 zsh...`
- `[2/4] 安装 oh-my-zsh（使用 Gitee 镜像）...`
- `[3/4] 安装插件...`
- `[4/4] 配置 .zshrc...`

**时间**：约 1-2 分钟

---

### 第六步：系统重启（如有需要）

**触发条件**：
- 安装了 NVIDIA 驱动
- 安装了 CUDA
- 修改了系统级配置

**提示**：
```
⚠️  检测到以下操作需要重启系统：
  - NVIDIA 驱动安装
  - CUDA Toolkit 安装

请保存当前工作后重启系统：
  sudo reboot
```

---

## 资源索引

### 必要脚本
- **系统检测**：[scripts/system_check.py](scripts/system_check.py)
- **工具安装**：[scripts/install_package.py](scripts/install_package.py)
- **Docker 安装**：[scripts/install_docker.py](scripts/install_docker.py)
- **环境配置**：[scripts/config_env.py](scripts/config_env.py)
- **终端配置**：[scripts/setup_zsh.py](scripts/setup_zsh.py)

### 领域参考
- **工具清单**：[references/tools_guide.md](references/tools_guide.md)
- **CUDA 指南**：[references/cuda_guide.md](references/cuda_guide.md)
- **配置模板**：[references/config_templates.md](references/config_templates.md)

---

## 执行指导

### 智能体执行规范

1. **分步询问**：每完成一步，询问用户是否继续下一步
2. **进度显示**：执行脚本时，实时显示输出信息
3. **时间预估**：长时间操作提前告知预估时间
4. **错误处理**：失败时提供解决方案，询问是否重试

### 进度提示格式

```
========================================
[步骤 X/N] 正在执行：操作名称
========================================
⏳ 预计时间：X 分钟
📥 进度：正在下载/安装/配置...
✅ 完成：操作名称 完成
```

### 用户确认格式

```
========================================
即将执行：操作名称
========================================
说明：简要说明该操作的作用
影响：是否需要 sudo / 是否需要重启
时间：预计耗时

是否继续？(yes/no):
```

---

## 国内镜像源汇总

| 类型 | 镜像源 | 地址 |
|------|--------|------|
| GitHub | gh-proxy | `https://gh-proxy.org/https://github.com/` |
| HuggingFace | hf-mirror | `https://hf-mirror.com` |
| pip | 清华 | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| conda | 清华 | `https://mirrors.tuna.tsinghua.edu.cn/anaconda/` |
| Docker | 阿里云 | `https://mirrors.aliyun.com/docker-ce/` |
| oh-my-zsh | Gitee | `https://gitee.com/shmhlsy/oh-my-zsh-install.sh` |
