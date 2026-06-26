# CUDA 和 cuDNN 安装指南

本文档提供详细的 CUDA 和 cuDNN 安装步骤，包括版本选择、安装流程和环境配置。

## 目录
- [前置检查](#前置检查)
- [NVIDIA 驱动安装](#nvidia-驱动安装)
- [CUDA Toolkit 安装](#cuda-toolkit-安装)
- [cuDNN 安装](#cudnn-安装)
- [环境变量配置](#环境变量配置)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

---

## 前置检查

### 1. 检查 GPU 型号
```bash
lspci | grep -i nvidia
```

### 2. 检查 Ubuntu 版本
```bash
lsb_release -a
# CUDA 12.x 需要 Ubuntu 20.04 或 22.04
```

### 3. 检查内核版本
```bash
uname -r
# 建议使用 5.x 以上内核
```

---

## NVIDIA 驱动安装

### 方法一：使用 ubuntu-drivers（推荐）

#### 1. 检查推荐驱动
```bash
ubuntu-drivers devices
```

输出示例：
```
== /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
modalias : pci:v000010DEd00002504sv00001458sd00004022bc03sc00i00
vendor   : NVIDIA Corporation
model    : GA102 [GeForce RTX 3090]
driver   : nvidia-driver-535 - distro non-free recommended
driver   : nvidia-driver-545 - distro non-free
driver   : nvidia-driver-470 - distro non-free
driver   : nvidia-driver-525 - distro non-free
```

#### 2. 安装推荐驱动
```bash
# 安装推荐版本
sudo apt install nvidia-driver-535 -y

# 或安装指定版本
sudo apt install nvidia-driver-545 -y
```

#### 3. 重启系统
```bash
sudo reboot
```

#### 4. 验证驱动
```bash
nvidia-smi
```

输出示例：
```
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 3090        Off | 00000000:01:00.0  On |                  N/A |
|  0%   32C    P8              21W / 350W |    874MiB / 24576MiB |      3%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
```

---

## CUDA Toolkit 安装

### 版本选择建议

| CUDA 版本 | 支持的 GPU | TensorFlow 版本 | PyTorch 版本 |
|-----------|-----------|----------------|-------------|
| 12.6 | 最新 GPU (RTX 4090 等) | 待支持 | PyTorch 2.3+ |
| 12.1 | RTX 30/40 系列 | TensorFlow 2.15+ | PyTorch 2.0+ |
| 11.8 | 所有 Pascal+ GPU | TensorFlow 2.12+ | PyTorch 2.0+ |

### CUDA 12.6 安装步骤

#### 1. 下载 CUDA 仓库包
```bash
cd /tmp
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600

wget https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda-repo-ubuntu2204-12-6-local_12.6.0-560.28.03-1_amd64.deb
```

#### 2. 安装仓库包
```bash
sudo dpkg -i cuda-repo-ubuntu2204-12-6-local_12.6.0-560.28.03-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-6-local/cuda-*-keyring.gpg /usr/share/keyrings/
```

#### 3. 安装 CUDA Toolkit
```bash
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-6
```

#### 4. 安装 NVIDIA 驱动（如果之前未安装）
```bash
sudo apt-get -y install cuda-drivers
```

### CUDA 12.1 安装步骤

```bash
cd /tmp
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600

wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-1-local/cuda-*-keyring.gpg /usr/share/keyrings/

sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-1
```

---

## cuDNN 安装

### 1. 下载 cuDNN

访问 NVIDIA 官网：https://developer.nvidia.com/cudnn

**需要 NVIDIA 开发者账号**

选择与 CUDA 版本匹配的 cuDNN：
- CUDA 12.6 → cuDNN 9.7+
- CUDA 12.1 → cuDNN 8.9+
- CUDA 11.8 → cuDNN 8.7+

### 2. 安装 cuDNN (Ubuntu 22.04 + CUDA 12.6)

```bash
cd /tmp

# 下载 cuDNN（需替换为实际下载链接）
wget https://developer.download.nvidia.com/compute/cudnn/local_installers/cudnn-local-repo-ubuntu2204-9.7.1_1.0-1_amd64.deb

# 安装仓库包
sudo dpkg -i cudnn-local-repo-ubuntu2204-9.7.1_1.0-1_amd64.deb

# 添加密钥
sudo cp /var/cudnn-local-repo-ubuntu2204-9.7.1/cudnn-*-keyring.gpg /usr/share/keyrings/

# 更新并安装
sudo apt-get update
sudo apt-get -y install cudnn
```

### 3. 安装特定版本的 cuDNN

```bash
# 查看可用版本
apt-cache policy cudnn

# 安装特定版本
sudo apt-get install cudnn=9.7.1.* -y
```

---

## 环境变量配置

### 1. 编辑配置文件
```bash
nano ~/.bashrc
# 或
gedit ~/.bashrc
```

### 2. 添加环境变量

根据 CUDA 版本调整路径：

#### CUDA 12.6
```bash
# CUDA 环境变量
export CUDA_PATH=/usr/local/cuda-12.6
export PATH=$CUDA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH
export CUDADIR=$CUDA_PATH

# cuDNN 环境变量
export CUDNN_INCLUDE_DIR=$CUDA_PATH/include
export CUDNN_LIB_DIR=$CUDA_PATH/lib64
```

#### CUDA 12.1
```bash
export CUDA_PATH=/usr/local/cuda-12.1
export PATH=$CUDA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH
export CUDADIR=$CUDA_PATH
```

### 3. 使配置生效
```bash
source ~/.bashrc
```

### 4. 使用脚本自动配置

```bash
# 配置 CUDA 环境
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --setup-cuda --cuda-version 12.6

# 配置 cuDNN 环境
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --setup-cudnn --cuda-version 12.6
```

---

## 验证安装

### 1. 验证 NVIDIA 驱动
```bash
nvidia-smi
```

### 2. 验证 CUDA
```bash
nvcc --version
```

输出示例：
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Thu_Mar_28_02:18:24_PDT_2024
Cuda compilation tools, release 12.6, V12.6.65
Build cuda_12.6.r12.6/compiler.35044473_0
```

### 3. 验证 cuDNN

创建测试程序：
```python
# test_cudnn.py
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"cuDNN version: {torch.backends.cudnn.version()}")
print(f"GPU count: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
```

运行测试：
```bash
python test_cudnn.py
```

### 4. 测试 GPU 计算

```python
import torch

# 创建张量并移动到 GPU
x = torch.rand(1000, 1000).cuda()
y = torch.rand(1000, 1000).cuda()

# GPU 矩阵乘法
z = torch.mm(x, y)

print("GPU 计算测试成功！")
print(f"结果张量形状: {z.shape}")
```

---

## 常见问题

### Q1: nvidia-smi 找不到命令

**原因**：驱动未安装或未加载

**解决**：
```bash
# 检查驱动是否安装
dpkg -l | grep nvidia-driver

# 如果未安装，安装驱动
sudo apt install nvidia-driver-535 -y
sudo reboot
```

### Q2: CUDA 版本不匹配

**现象**：`nvcc --version` 显示的版本与 `nvidia-smi` 显示的 CUDA Version 不一致

**说明**：
- `nvidia-smi` 显示的是驱动支持的最高 CUDA 版本
- `nvcc --version` 显示的是实际安装的 CUDA Toolkit 版本
- 两者可以不同，实际使用的以 `nvcc` 为准

### Q3: 找不到 cudnn.h

**原因**：cuDNN 未正确安装或路径未配置

**解决**：
```bash
# 检查 cuDNN 头文件
ls /usr/local/cuda/include/cudnn*.h

# 如果不存在，重新安装 cuDNN
sudo apt-get install cudnn -y
```

### Q4: PyTorch 无法使用 GPU

**检查步骤**：
```bash
# 1. 检查 PyTorch 是否支持 CUDA
python -c "import torch; print(torch.version.cuda)"

# 2. 检查 CUDA 是否可用
python -c "import torch; print(torch.cuda.is_available())"

# 3. 如果返回 False，重新安装 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Q5: 内存不足

**原因**：GPU 显存被其他进程占用

**解决**：
```bash
# 查看显存使用情况
nvidia-smi

# 杀掉占用 GPU 的进程
sudo kill -9 <PID>
```

---

## 卸载和重装

### 卸载 CUDA
```bash
sudo apt-get --purge remove "*cuda*" "*libcuda*"
sudo apt-get autoremove
```

### 卸载 NVIDIA 驱动
```bash
sudo apt-get --purge remove "*nvidia*"
sudo apt-get autoremove
sudo reboot
```

### 完全重装
```bash
# 1. 卸载所有 NVIDIA 相关软件
sudo apt-get --purge remove "*nvidia*" "*cuda*" "*cudnn*"
sudo apt-get autoremove
sudo rm -rf /usr/local/cuda*

# 2. 重启
sudo reboot

# 3. 重新安装
# 按照上述步骤安装驱动 → CUDA → cuDNN
```

---

## 参考链接

- NVIDIA 驱动下载：https://www.nvidia.com/Download/index.aspx
- CUDA Toolkit 下载：https://developer.nvidia.com/cuda-downloads
- cuDNN 下载：https://developer.nvidia.com/cudnn
- CUDA 兼容性文档：https://docs.nvidia.com/deploy/cuda-compatibility/index.html
- PyTorch 安装指南：https://pytorch.org/get-started/locally/
- TensorFlow 安装指南：https://www.tensorflow.org/install/gpu
