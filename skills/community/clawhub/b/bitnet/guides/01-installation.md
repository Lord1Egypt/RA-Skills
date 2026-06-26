# 安装指南

## 适用场景

- 在 Linux/macOS/Windows 上从源码构建 BitNet
- 配置 conda 环境和编译依赖
- 下载官方模型并完成量化

---

## 环境要求

| 依赖 | 版本 | 安装方式 |
|------|------|---------|
| Python | >= 3.9 | conda 或系统 Python |
| CMake | >= 3.22 | `conda install cmake` |
| Clang | >= 18 | 系统包管理器 |
| conda | 任意 | [Miniconda](https://docs.conda.io/en/latest/miniconda.html) |

---

## macOS 安装

> **AI 可自动执行**

```bash
# 安装 Homebrew（如未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装编译依赖
brew install llvm cmake

# 配置 Clang 路径（Apple Silicon）
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
export CC=/opt/homebrew/opt/llvm/bin/clang
export CXX=/opt/homebrew/opt/llvm/bin/clang++

# 验证版本
clang --version  # 需要 >= 18
cmake --version  # 需要 >= 3.22
```

---

## Linux (Ubuntu/Debian) 安装

```bash
# 安装 Clang 18
bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"

# 安装 CMake
sudo apt-get install -y cmake

# 验证
clang-18 --version
cmake --version
```

---

## Windows 安装

在 Windows 上需要 Visual Studio 2022：

1. 下载 [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/)
2. 在安装程序中勾选：
   - Desktop-development with C++
   - C++-CMake Tools for Windows
   - C++-Clang Compiler for Windows
   - MS-Build Support for LLVM-Toolset (clang)
3. 使用 **Developer Command Prompt for VS2022** 运行所有命令

---

## 克隆并安装 Python 依赖

```bash
# 克隆（必须使用 --recursive 拉取子模块）
git clone --recursive https://github.com/microsoft/BitNet.git
cd BitNet

# 创建 conda 环境
conda create -n bitnet-cpp python=3.9
conda activate bitnet-cpp

# 安装 Python 依赖
pip install -r requirements.txt
```

---

## 下载模型

### 官方推荐模型（BitNet-b1.58-2B-4T）

```bash
# 使用 huggingface-cli 下载 GGUF 格式
pip install huggingface_hub
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf \
  --local-dir models/BitNet-b1.58-2B-4T
```

### 其他支持的模型

```bash
# 较小的 700M 模型（测试用）
huggingface-cli download 1bitLLM/bitnet_b1_58-large \
  --local-dir models/bitnet_b1_58-large

# 3.3B 模型
huggingface-cli download 1bitLLM/bitnet_b1_58-3B \
  --local-dir models/bitnet_b1_58-3B
```

---

## 编译量化环境

```bash
# 使用本地模型路径（x86 推荐 i2_s，ARM 推荐 tl1）
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# ARM CPU 使用 TL1 内核
python setup_env.py -md models/BitNet-b1.58-2B-4T -q tl1

# 使用预调优内核参数（可能更快）
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s --use-pretuned
```

编译成功后，会在模型目录生成 `ggml-model-i2_s.gguf` 文件。

---

## 完成确认检查清单

- [ ] `clang --version` 显示 >= 18
- [ ] `cmake --version` 显示 >= 3.22
- [ ] `git clone --recursive` 成功（含子模块）
- [ ] `pip install -r requirements.txt` 无报错
- [ ] 模型下载完成（几百 MB 到几 GB）
- [ ] `setup_env.py` 执行成功，生成 `.gguf` 文件

---

## 下一步

- [快速开始](02-quickstart.md) — 运行推理、对话模式、性能测试
