# GPU GROMACS 源码编译安装

> 适用场景：需要 GPU 加速的 GROMACS，而从包管理器安装的版本不支持 GPU（如 Ubuntu 的 `apt install gromacs`）。

## 前置检查

```bash
# 1. 检查 GPU
nvidia-smi
# 记下: GPU 型号, Compute Capability, CUDA Version (driver 支持的最高 CUDA)

# 2. 检查当前 GROMACS GPU 支持
gmx --version 2>&1 | grep -i "GPU support"
# 如果显示 "disabled" → 需要源码编译 GPU 版

# 3. 检查系统
gcc --version | head -1    # 需要 GCC 9+
cmake --version | head -1  # GROMACS 2025 需要 CMake ≥3.28
nproc                       # 编译并行度
```

## CMake 版本升级

GROMACS 2025+ 需要 CMake ≥3.28。如果系统 CMake 过旧：

```bash
# 方案 A: 下载官方二进制
cd /tmp
wget https://github.com/Kitware/CMake/releases/download/v4.0.1/cmake-4.0.1-linux-x86_64.tar.gz
tar xzf cmake-4.0.1-linux-x86_64.tar.gz
mv cmake-4.0.1-linux-x86_64 /opt/cmake-4.0.1
ln -sf /opt/cmake-4.0.1/bin/cmake /usr/local/bin/cmake
cmake --version
```

## CUDA Toolkit 安装

### 如果已有 CUDA 但不在 PATH

```bash
# 查找已有安装
find / -name "nvcc" -type f 2>/dev/null
# 常见路径: /usr/local/cuda-12.8/bin/nvcc

# 验证
/usr/local/cuda-12.8/bin/nvcc --version
```

### 全新安装 (Ubuntu 22.04+)

```bash
# 安装 NVIDIA CUDA keyring
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
dpkg -i cuda-keyring_1.1-1_all.deb
apt-get update

# 安装 CUDA 编译器 + 开发库
apt-get install -y cuda-compiler-12-8 cuda-libraries-dev-12-8 cuda-command-line-tools-12-8
```

## GROMACS 源码编译

### 下载源码

```bash
# 查看最新版本
wget -qO- https://ftp.gromacs.org/gromacs/ | grep -oP 'gromacs-2025[^"]*tar.gz' | sort -V | tail -3

# 下载
wget https://ftp.gromacs.org/gromacs/gromacs-2025.4.tar.gz
tar xzf gromacs-2025.4.tar.gz
```

### CMake 配置

```bash
export PATH=/usr/local/cuda-12.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH

mkdir -p gromacs-2025.4/build && cd gromacs-2025.4/build

cmake .. \
  -DGMX_GPU=CUDA \
  -DCMAKE_CUDA_ARCHITECTURES=120 \  # RTX 50 系列用 120 (Blackwell)
  -DGMX_SIMD=AVX2_256 \              # Intel 用 AVX2_256; AMD 用 AVX2_256
  -DCMAKE_INSTALL_PREFIX=/opt/gromacs-2025.4-gpu \
  -DGMX_BUILD_OWN_FFTW=ON \          # 自动编译 FFTW
  -DGMX_MPI=OFF \                    # 单 GPU 不需要 MPI
  -DGMX_OPENMP=ON \
  2>&1 | tail -30
```

### 关键 CMake 参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `GMX_GPU` | GPU 后端 | `CUDA` |
| `CMAKE_CUDA_ARCHITECTURES` | CUDA 架构版本 | RTX 50xx=`120`, RTX 40xx=`89`, RTX 30xx=`86`, A100=`80` |
| `GMX_SIMD` | CPU SIMD 指令集 | Intel=`AVX2_256`, AMD=`AVX2_256`, ARM=`ARM_NEON_ASIMD` |
| `GMX_BUILD_OWN_FFTW` | 自动编译 FFTW | `ON` (推荐) |
| `GMX_MPI` | MPI 并行 | `OFF` (单节点/单GPU) |
| `GMX_OPENMP` | CPU 多线程 | `ON` |

### CMake 验证 GPU 检测

```bash
grep -iE "gpu|cuda" CMakeCache.txt | head -10
# 确认: GMX_GPU=CUDA, CMAKE_CUDA_COMPILER 指向 nvcc
```

### 编译

```bash
make -j$(nproc) 2>&1 | tail -5
# 约 10-30 分钟，取决于 CPU 核心数

make install
```

## 环境配置

```bash
# 创建环境脚本
cat > /opt/gromacs-2025.4-gpu/env.sh << 'EOF'
export GMX=/opt/gromacs-2025.4-gpu
export PATH=$GMX/bin:$PATH
export LD_LIBRARY_PATH=$GMX/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda-12.8
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
EOF

# 自动加载（写入 .bashrc）
echo 'source /opt/gromacs-2025.4-gpu/env.sh' >> ~/.bashrc
```

## 验证

```bash
source /opt/gromacs-2025.4-gpu/env.sh
gmx --version 2>&1 | grep -iE "GPU|CUDA|SIMD"
```

期望输出：
```
GPU support:         CUDA
SIMD instructions:   AVX2_256
GPU FFT library:     cuFFT
CUDA compiler:       /usr/local/cuda-12.8/bin/nvcc
```

## CUDA 架构对照表

| GPU 系列 | 架构 | CMAKE_CUDA_ARCHITECTURES |
|----------|------|--------------------------|
| RTX 5090/5080/5070/5060 | Blackwell | `120` |
| RTX 4090/4080/4070/4060 | Ada Lovelace | `89` |
| RTX 3090/3080/3070 | Ampere | `86` |
| A100/H100 | Ampere/Hopper | `80`/`90` |
| V100 | Volta | `70` |
| Tesla T4 | Turing | `75` |
| GTX 1080 | Pascal | `61` |
