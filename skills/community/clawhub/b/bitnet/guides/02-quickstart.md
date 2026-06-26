# 快速开始

## 适用场景

- 运行 BitNet 模型进行文本生成和对话
- 使用对话模式进行交互式聊天
- 测试模型推理性能

---

## 运行基础推理

完成安装后，运行第一个推理：

```bash
# 确认 conda 环境已激活
conda activate bitnet-cpp

# 单次文本生成
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "The future of AI is" \
  -n 128
```

参数说明：
- `-m`：模型文件路径（`ggml-model-i2_s.gguf`）
- `-p`：提示词（prompt）
- `-n`：生成 token 数量（默认 128）

---

## 对话模式（推荐）

使用 `-cnv` 标志进入交互式对话模式，`-p` 变为系统提示：

```bash
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "You are a helpful AI assistant. Answer concisely and accurately." \
  -cnv
```

启动后进入交互式提示符，输入问题即可对话：
```
> What is machine learning?
Machine learning is a subset of artificial intelligence that enables systems to learn...

> Explain it like I'm five
Imagine teaching a dog tricks...
```

按 `Ctrl+C` 退出对话。

---

## 调整推理参数

```bash
# 增加并发线程数（提高速度）
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "Explain quantum computing" \
  -t 8 \          # 使用 8 个线程
  -n 256 \        # 生成 256 个 token
  -c 4096         # 上下文窗口大小

# 调整温度（创意度）
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "Write a poem about the moon" \
  -temp 0.8 \     # 0.0=确定性，1.0=创意，>1.0=随机
  -n 200
```

---

## 性能基准测试

```bash
# 基础基准（默认：128 token 生成，512 token 提示）
python e2e_benchmark.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf

# 自定义基准
python e2e_benchmark.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -n 256 \        # 生成 256 个 token
  -p 1024 \       # 使用 1024 token 的提示
  -t 4            # 使用 4 个线程
```

典型输出示例（Apple M2）：
```
Model: BitNet-b1.58-2B-4T
Threads: 4
Prompt processing: 125 tokens/sec
Token generation: 18.5 tokens/sec
Total time: 8.2s
```

---

## 不同量化类型对比

```bash
# 安装 I2_S 量化（x86 推荐）
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
python run_inference.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -p "test" -n 50

# 安装 TL1 量化（ARM 推荐，如 Apple Silicon）
python setup_env.py -md models/BitNet-b1.58-2B-4T -q tl1
python run_inference.py -m models/BitNet-b1.58-2B-4T/ggml-model-tl1.gguf -p "test" -n 50
```

---

## 使用 Falcon3 模型（已有指令调优）

```bash
# 下载 Falcon3 指令模型（支持更好的对话能力）
huggingface-cli download tiiuae/Falcon3-3B-Instruct-1.58bit-gguf \
  --local-dir models/Falcon3-3B-Instruct

python setup_env.py -md models/Falcon3-3B-Instruct -q i2_s

# 对话模式
python run_inference.py \
  -m models/Falcon3-3B-Instruct/ggml-model-i2_s.gguf \
  -p "You are Falcon, a helpful assistant." \
  -cnv
```

---

## 完成确认检查清单

- [ ] `run_inference.py` 成功生成文本（非空输出）
- [ ] 对话模式（`-cnv`）可以持续多轮对话
- [ ] `e2e_benchmark.py` 输出 tokens/sec 指标
- [ ] 生成速度基本达到预期（2B 模型 CPU 上应 > 5 tokens/sec）

---

## 下一步

- [高级用法](03-advanced-usage.md) — GPU 推理、多线程优化、更大模型
