# 高级用法

## GPU 推理

BitNet 官方 GPU 内核（2025 年 5 月发布），支持 CUDA GPU 加速：

```bash
# 查看 GPU 推理文档
cat gpu/README.md

# GPU 版本需要 CUDA 环境
# 参考: https://github.com/microsoft/BitNet/blob/main/gpu/README.md
```

---

## 多线程性能优化

CPU 线程数对性能影响显著，建议实验找到最优值：

```bash
# 测试不同线程数的性能
for threads in 1 2 4 8; do
    echo "=== Threads: $threads ==="
    python e2e_benchmark.py \
        -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
        -t $threads \
        -n 128 \
        -p 256
done
```

**经验规则：**
- 单用户推理：物理核心数的 50-75%
- 服务化推理：物理核心数的 100%
- 超线程（HT）对推理加速有限，优先使用物理核心数

---

## 使用嵌入量化（减少内存）

```bash
# 启用嵌入量化（进一步降低内存使用）
python setup_env.py \
  -md models/BitNet-b1.58-2B-4T \
  -q i2_s \
  --quant-embd    # 嵌入量化到 f16
```

---

## 不同模型大小的性能对比

```bash
# 对比不同大小模型的速度
# 700M 模型
python e2e_benchmark.py -m models/bitnet_b1_58-large/ggml-model-i2_s.gguf -t 4

# 2.4B 官方模型
python e2e_benchmark.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -t 4

# 3.3B 模型（ARM 专用 TL1 内核）
python e2e_benchmark.py -m models/bitnet_b1_58-3B/ggml-model-tl1.gguf -t 4
```

典型速度参考（Apple M2）：
| 模型 | 速度 | 内存 |
|------|------|------|
| bitnet_b1_58-large (700M) | ~45 t/s | ~0.5 GB |
| BitNet-b1.58-2B-4T (2.4B) | ~18 t/s | ~1.2 GB |
| bitnet_b1_58-3B (3.3B) | ~12 t/s | ~1.8 GB |

---

## 使用预调优内核

预调优内核为特定硬件配置优化了 tile 大小等参数：

```bash
# 使用预调优参数（通常比默认快 15-100%）
python setup_env.py \
  -md models/BitNet-b1.58-2B-4T \
  -q i2_s \
  --use-pretuned
```

---

## 最新优化内核（2026 年 1 月）

新版并行内核实现，带可配置 tiling 和嵌入量化支持：

```bash
# 查看优化指南
cat src/README.md

# 该优化在原实现基础上额外提速 1.15-2.1x
# 无需额外配置，setup_env.py 自动使用最新内核
```

---

## 内存估算

BitNet 模型的内存使用公式（约）：

| 参数量 | I2_S 量化内存 |
|--------|--------------|
| 700M | ~0.5 GB |
| 2.4B | ~1.5 GB |
| 3.3B | ~2.0 GB |
| 8.0B | ~5.0 GB |

BitNet 1.58-bit 量化比传统 FP16（~2 bytes/param）约低 87%，运行 100B 模型仅需约 20 GB 内存。

---

## 批量文本生成（无对话）

```python
# 通过 Python 脚本批量生成
import subprocess

prompts = [
    "Translate to French: Hello world",
    "Summarize in one sentence: Machine learning is...",
    "What is the capital of Japan?",
]

for prompt in prompts:
    result = subprocess.run(
        [
            "python", "run_inference.py",
            "-m", "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf",
            "-p", prompt,
            "-n", "100",
            "-t", "4",
        ],
        capture_output=True, text=True
    )
    print(f"Prompt: {prompt[:50]}...")
    print(f"Output: {result.stdout[:200]}")
    print()
```

---

## 完成确认检查清单

- [ ] 多线程测试找到最优线程数
- [ ] 预调优内核性能明显提升（可选）
- [ ] GPU 推理配置成功（如有 NVIDIA GPU）
- [ ] 嵌入量化降低内存使用（可选）

---

## 相关链接

- [故障排查](../troubleshooting.md)
- [GPU 推理文档](https://github.com/microsoft/BitNet/blob/main/gpu/README.md)
- [优化指南](https://github.com/microsoft/BitNet/blob/main/src/README.md)
- [技术论文](https://arxiv.org/abs/2410.16144)
