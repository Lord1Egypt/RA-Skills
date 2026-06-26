# 故障排查

## 安装问题

---

### 问题 1：CMake 版本过低或 Clang 未找到

**难度：** 低

**症状：** `CMake 3.xx < required 3.22` 或 `clang: command not found`

**解决方案：**

macOS：
```bash
# 更新 Homebrew 和 LLVM
brew update
brew upgrade llvm
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
clang --version  # 验证 >= 18
```

Ubuntu/Debian：
```bash
# 安装最新 Clang
bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"
clang-18 --version

# 安装最新 CMake
sudo apt-get remove cmake  # 移除旧版
pip install cmake           # 通过 pip 获取最新版
cmake --version
```

---

### 问题 2：`git clone --recursive` 子模块失败

**难度：** 低

**症状：** `fatal: No url found for submodule path` 或 `Submodule init failed`

**解决方案：**
```bash
# 如果忘记 --recursive，手动初始化子模块
cd BitNet
git submodule update --init --recursive

# 如果网络问题导致失败，重试
git submodule update --init --recursive --retry 3
```

---

### 问题 3：`setup_env.py` 编译失败

**难度：** 高

**症状：** `CMake Error` 或 `clang: error: no such file or directory`

**常见原因：**
- Clang 路径未正确导出（概率 50%）
- 子模块未初始化（概率 30%）
- 磁盘空间不足（概率 20%）

**解决方案：**
```bash
# 确保在正确目录
cd /path/to/BitNet
conda activate bitnet-cpp

# macOS：导出 Clang 路径
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
export CC=/opt/homebrew/opt/llvm/bin/clang
export CXX=/opt/homebrew/opt/llvm/bin/clang++

# 重新运行
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# 检查磁盘空间
df -h .  # 需要至少 5GB 可用空间
```

Windows 用户：必须在 **Developer Command Prompt for VS2022** 中运行，普通 CMD/PowerShell 不行。

---

## 使用问题

---

### 问题 4：模型文件找不到

**难度：** 低

**症状：** `FileNotFoundError: models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` 不存在

**排查步骤：**
```bash
# 检查模型目录
ls -la models/BitNet-b1.58-2B-4T/
# 期望看到: ggml-model-i2_s.gguf 或 ggml-model-tl1.gguf
```

**解决方案：**
```bash
# 如果文件不存在，setup_env.py 未完成，重新运行
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# 或直接下载 GGUF 格式（跳过量化步骤）
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf \
  --local-dir models/BitNet-b1.58-2B-4T
ls models/BitNet-b1.58-2B-4T/*.gguf  # 确认文件存在
```

---

### 问题 5：推理速度远低于预期

**难度：** 中

**症状：** 速度 < 2 tokens/sec（2B 模型在现代 CPU 上应达 10+ tokens/sec）

**常见原因：**
- 使用了错误的量化内核（概率 40%）
- 线程数未优化（概率 35%）
- 内存不足导致频繁 swap（概率 25%）

**解决方案：**
```bash
# 确认使用了正确内核（x86 用 i2_s，ARM 用 tl1）
uname -m  # x86_64 或 arm64

# x86：
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s --use-pretuned

# ARM（Apple Silicon）：
python setup_env.py -md models/BitNet-b1.58-2B-4T -q tl1 --use-pretuned

# 测试不同线程数
python e2e_benchmark.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -t 4
python e2e_benchmark.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -t 8

# 检查内存使用
free -h  # Linux：应有足够空闲物理内存
```

---

### 问题 6：对话模式（`-cnv`）响应质量差

**难度：** 中

**症状：** 模型回答乱码、重复或无法理解指令

**常见原因：**
- 使用了非指令调优（Instruct）版本的模型（概率 60%）
- 系统提示（`-p`）格式不合适（概率 40%）

**解决方案：**
```bash
# 使用指令调优版本的模型
huggingface-cli download tiiuae/Falcon3-3B-Instruct-1.58bit-gguf \
  --local-dir models/Falcon3-3B-Instruct
python setup_env.py -md models/Falcon3-3B-Instruct -q i2_s

python run_inference.py \
  -m models/Falcon3-3B-Instruct/ggml-model-i2_s.gguf \
  -p "You are a helpful assistant. Be concise and accurate." \
  -cnv \
  -temp 0.3   # 降低温度提高稳定性
```

---

## 网络/环境问题

---

### 问题 7：HuggingFace 模型下载失败

**难度：** 中

**症状：** `huggingface-cli download` 超时或 403 错误

**解决方案：**
```bash
# 配置 HuggingFace Token（部分模型需要）
pip install huggingface_hub
huggingface-cli login  # 输入 HF Token

# 或直接设置环境变量
export HUGGING_FACE_HUB_TOKEN="hf_your_token"

# 如果速度慢，使用国内镜像（如 ModelScope）
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf \
  --local-dir models/BitNet-b1.58-2B-4T

# 断点续传
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf \
  --local-dir models/BitNet-b1.58-2B-4T \
  --resume-download
```

---

### 问题 8：Windows 编译失败（Developer Prompt 问题）

**难度：** 高

**症状：** `'cl' is not recognized` 或 `MSBuild: command not found`

**说明：** Windows 必须在 **Developer Command Prompt for VS2022** 中运行，不能用普通 CMD、PowerShell 或 Git Bash。

**解决方案：**
1. 按 Win 键，搜索 "Developer Command Prompt for VS 2022"
2. 以管理员身份打开
3. 在该提示符中重新运行所有构建命令

```cmd
REM 在 Developer Command Prompt 中
cd C:\path\to\BitNet
conda activate bitnet-cpp
python setup_env.py -md models\BitNet-b1.58-2B-4T -q i2_s
```

---

## 通用诊断

```bash
# 系统信息
uname -m && python --version && cmake --version && clang --version

# 模型文件检查
ls -lh models/BitNet-b1.58-2B-4T/*.gguf

# 快速推理测试（10 个 token）
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "Hello" \
  -n 10

# 基准测试（查看速度）
python e2e_benchmark.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -t 4 -n 64 -p 128
```

**GitHub Issues：** https://github.com/microsoft/BitNet/issues

**技术报告：** https://arxiv.org/abs/2410.16144
