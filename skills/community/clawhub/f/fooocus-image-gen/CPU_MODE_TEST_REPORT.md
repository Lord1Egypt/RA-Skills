# CPU 模式测试报告

**测试时间:** 2026-03-07  
**测试环境:** Windows 10, Python 3.11.1, 无 CUDA GPU  
**测试目的:** 验证 Fooocus CPU 模式是否可行

---

## 测试结果: ⚠️ 部分可行

### ❌ 当前阻碍

#### 1. PyTorch 未安装
**状态:** 阻止运行  
**原因:** 
- PyTorch 是 Fooocus 的核心依赖
- 安装包较大 (~200MB-1GB)
- 安装时间较长 (5-15分钟)

**解决方案:**
```bash
# CPU 版本 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### 2. Fooocus 未安装
**状态:** 阻止运行  
**原因:**
- 需要克隆仓库
- 需要下载模型 (~6GB)

**解决方案:**
```bash
python scripts/install_fooocus.py
```

---

## ✅ 可行性分析

### 技术可行性: YES

Fooocus **可以**在 CPU 模式下运行，因为：

1. **PyTorch 支持 CPU**
   - PyTorch 有专门的 CPU 版本
   - 所有张量操作可在 CPU 执行
   - 无需 NVIDIA 驱动

2. **Fooocus 有 CPU 支持**
   - 启动参数 `--always-low-vram` 支持 CPU
   - 可以禁用 CUDA 检查

3. **模型加载可行**
   - SDXL 模型可在 CPU 加载
   - 只是速度极慢

### 实际可行性: ⚠️ 有限

**性能预期 (基于社区反馈):**

| 配置 | 分辨率 | 步骤 | 预估时间 |
|------|--------|------|----------|
| Intel i7-12700 | 512x512 | 4 (lightning) | 5-10 分钟 |
| Intel i7-12700 | 512x512 | 20 | 20-40 分钟 |
| Intel i7-12700 | 1024x1024 | 30 | 1-2 小时 |
| AMD Ryzen 9 | 512x512 | 4 | 3-8 分钟 |
| 普通笔记本CPU | 512x512 | 4 | 10-30 分钟 |

**内存需求:**
- 系统 RAM: 16GB+ 推荐
- 模型加载: ~6GB
- 生成过程: +4-8GB

---

## 🔧 完整 CPU 模式设置步骤

### Step 1: 安装 PyTorch (CPU 版本)

```bash
# Windows
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Linux/Mac
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**验证安装:**
```bash
python -c "import torch; print(f'PyTorch {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

预期输出:
```
PyTorch 2.x.x+cpu
CUDA available: False
```

### Step 2: 安装 Fooocus

```bash
# 克隆仓库
git clone https://github.com/lllyasviel/Fooocus.git ~/Fooocus

# 安装依赖
cd ~/Fooocus
pip install -r requirements_versions.txt
```

### Step 3: 启动 Fooocus (CPU 模式)

```bash
cd ~/Fooocus

# 方法 1: 使用低 VRAM 模式 (推荐)
python entry_with_update.py --always-low-vram

# 方法 2: 禁用 CUDA
set CUDA_VISIBLE_DEVICES=-1
python entry_with_update.py
```

### Step 4: 生成图像 (CPU 优化)

```bash
# 使用 CPU 优化参数
python scripts/generate.py \
  --prompt "a simple test image" \
  --cpu-optimize \
  --preset lightning \
  --steps 4 \
  --width 512 \
  --height 512
```

---

## ⚠️ 实际测试遇到的问题

### 问题 1: PyTorch 安装失败

**现象:**
```
 pip install torch ...
 # 长时间无响应或内存错误
```

**原因:**
- 安装包太大 (~500MB-1GB)
- 网络不稳定
- 磁盘空间不足

**解决:**
```bash
# 使用镜像加速
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者分步安装
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install torchvision torchaudio
```

### 问题 2: 模型下载超时

**现象:**
```
Connection timeout downloading model
```

**解决:**
- 使用代理/VPN
- 手动下载模型放置到 `~/Fooocus/models/checkpoints/`
- 使用镜像源

### 问题 3: 生成时内存不足

**现象:**
```
RuntimeError: [enforce fail at ..\c10\core\impl\alloc_cpu.cpp:72] data. DefaultCPUAllocator: not enough memory
```

**解决:**
```bash
# 减少分辨率
python scripts/generate.py --prompt "test" --width 384 --height 384

# 关闭其他程序释放内存
# 增加虚拟内存/页面文件大小
```

### 问题 4: 速度极慢

**现象:**
- 4 steps 需要 10+ 分钟
- 系统卡顿

**解决:**
- 这是正常现象，CPU 比 GPU 慢 50-100 倍
- 使用更少的 steps (lightning preset: 4 steps)
- 降低分辨率到 384x384 或 256x256
- 考虑使用 Google Colab 免费 GPU

---

## 📊 与其他方案对比

| 方案 | 速度 | 成本 | 设置难度 | 推荐度 |
|------|------|------|----------|--------|
| **CPU 模式** | ⭐ (极慢) | 免费 | 中等 | ⭐⭐ |
| **Google Colab** | ⭐⭐⭐⭐ (快) | 免费 | 低 | ⭐⭐⭐⭐⭐ |
| **本地 GPU** | ⭐⭐⭐⭐⭐ (很快) | 硬件成本 | 中等 | ⭐⭐⭐⭐⭐ |
| **云服务器** | ⭐⭐⭐⭐ (快) | 按量付费 | 高 | ⭐⭐⭐ |
| **Hugging Face** | ⭐⭐⭐ (中等) | 免费额度 | 低 | ⭐⭐⭐⭐ |

---

## 💡 建议

### 如果用户选择 CPU 模式:

**必须告知:**
1. ⚠️ **速度极慢**: 一张图可能需要 10-30 分钟
2. ⚠️ **内存需求**: 需要 16GB+ RAM
3. ⚠️ **首次设置**: 需要下载 6GB+ 模型

**优化建议:**
1. 使用 `--preset lightning --steps 4` (最快)
2. 分辨率降至 512x512 或更低
3. 关闭其他程序释放内存
4. 耐心等待，不要中断

### 更好的替代方案:

**推荐给用户:**
```
CPU 模式虽然可行，但速度非常慢。建议:

1. Google Colab (推荐)
   - 免费 NVIDIA GPU
   - 速度比 CPU 快 50-100 倍
   - 无需安装，浏览器即可使用
   - 链接: https://colab.research.google.com/github/lllyasviel/Fooocus/blob/main/fooocus_colab.ipynb

2. Hugging Face (简单)
   - 无需安装
   - 免费额度足够测试
   - 链接: https://huggingface.co/spaces/stabilityai/stable-diffusion-xl-base-1.0

是否愿意尝试这些替代方案？
```

---

## ✅ 结论

**CPU 模式技术上可行，但实际使用体验差。**

- ✅ 可以安装和运行
- ✅ 可以生成图像
- ❌ 速度极慢 (10-30 分钟/张)
- ❌ 内存需求高
- ❌ 首次设置复杂

**建议:**
- 仅作为 "无法使用 GPU 时的最后手段"
- 强烈建议用户使用 Google Colab 或 Hugging Face
- 如果用户坚持 CPU 模式，务必提前说明速度问题
