> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# OpenVINO 推理优化指南

> V6 新增 · 本地 AI 推理性能优化核心参考

## 1. OpenVINO 概述

OpenVINO（Open Visual Inference and Neural network Optimization）是 Intel 开源的深度学习推理优化框架，支持 CPU/GPU/NPU/VPU 异构加速。

### 1.1 核心价值
- **推理加速**：INT8/FP16 量化 + 图优化，延迟降低 2-4 倍
- **内存优化**：模型体积缩减 50-75%（FP32→INT8）
- **异构调度**：自动分配 CPU/GPU/NPU 负载
- **跨平台**：Windows/Linux/macOS + 嵌入式设备

### 1.2 版本要求
- OpenVINO >= 2024.1
- NNCF（Neural Network Compression Framework）>= 2.7
- Python >= 3.9

## 2. 模型转换流程

### 2.1 PyTorch → OpenVINO IR

```python
import torch
from openvino.runtime import Core

# Step 1: 导出 ONNX
model = load_model()  # 你的 PyTorch 模型
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, "model.onnx", 
                  opset_version=14, input_names=["input"], output_names=["output"])

# Step 2: ONNX → OpenVINO IR
from openvino.tools import mo
ov_model = mo.convert_model("model.onnx", 
                            compress_to_fp16=True,  # FP16 压缩
                            input_shape="[1,3,224,224]")
# Step 3: 保存
from openvino.runtime import serialize
serialize(ov_model, xml_path="model.xml", bin_path="model.bin")
```

### 2.2 HuggingFace → OpenVINO

```python
from optimum.intel import OVModelForSequenceClassification
from transformers import AutoTokenizer

# 直接加载并转换
model = OVModelForSequenceClassification.from_pretrained(
    "bert-base-chinese", export=True, load_in_4bit=False)
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")

# 保存 OpenVINO IR
model.save_pretrained("ov-bert-base-zh")
```

## 3. 量化策略

### 3.1 INT8 动态量化（推荐首选）

```python
from openvino.runtime import Core
from openvino.tools import mo

# 转换为 IR 并压缩到 INT8
ov_model = mo.convert_model(
    "model.onnx",
    compress_to_fp16=False,   # 不压缩权重
    compress_weights="INT8"   # 仅权重量化
)
```

### 3.2 NNCF 训练后量化（PTQ）

```python
import nncf
from openvino.runtime import Core

# 1. 加载 FP32 模型
core = Core()
ov_model = core.read_model("model.xml")

# 2. 准备校准数据集
def transform_fn(data_item):
    return data_item["input"]

calibration_dataset = nncf.Dataset(calibration_data, transform_fn)

# 3. 量化
quantized_model = nncf.quantize(
    ov_model,
    calibration_dataset,
    preset=nncf.QuantizationPreset.MIXED,  # 权重 INT8 + 激活 FP16
    subset_size=300  # 校准样本数
)

# 4. 保存
from openvino.runtime import serialize
serialize(quantized_model, "model_int8.xml", "model_int8.bin")
```

### 3.3 量化精度对比

| 精度 | 模型大小 | 推理延迟 | 精度损失 | 适用场景 |
|------|----------|----------|----------|----------|
| FP32 | 基准 1x | 基准 1x | 无 | 精度敏感场景 |
| FP16 | ~0.5x | ~0.6x | <0.1% | GPU 推理首选 |
| INT8 | ~0.25x | ~0.3x | 0.5-2% | CPU/NPU 推理首选 |
| INT4 | ~0.12x | ~0.2x | 2-5% | 极致压缩场景 |

## 4. 异构调度策略

### 4.1 设备优先级

```python
from openvino.runtime import Core

core = Core()

# 策略 1: GPU 优先，CPU 降级
compiled_model = core.compile_model(ov_model, "GPU")

# 策略 2: 自动批处理（GPU 自动调整 batch）
config = {"PERFORMANCE_HINT": "THROUGHPUT", "NUM_STREAMS": "2"}
compiled_model = core.compile_model(ov_model, "GPU", config)

# 策略 3: 低延迟模式
config = {"PERFORMANCE_HINT": "LATENCY", "INFERENCE_NUM_THREADS": "4"}
compiled_model = core.compile_model(ov_model, "CPU", config)
```

### 4.2 多模型异构分配

```
┌─────────────────────────────────────────────────┐
│              异构调度策略表                        │
├──────────┬──────────┬──────────┬────────────────┤
│ 模型      │ 推荐设备  │ 精度     │ 理由           │
├──────────┼──────────┼──────────┼────────────────┤
│ OCR 检测  │ GPU      │ INT8     │ 高吞吐，图像密集 │
│ OCR 识别  │ GPU      │ FP16     │ 序列解码，精度敏感│
│ ASR 编码  │ NPU/GPU  │ INT8     │ 长时推理，功耗敏感│
│ TTS 声码  │ CPU      │ FP16     │ 流式输出，CPU 够用│
│ RAG 嵌入  │ GPU      │ INT8     │ 批量编码，吞吐优先│
│ VAD 检测  │ NPU      │ INT8     │ 实时检测，极低功耗│
└──────────┴──────────┴──────────┴────────────────┘
```

## 5. 性能优化技巧

### 5.1 动态 Batch Size

```python
# 根据输入量动态调整 batch
class DynamicBatcher:
    def __init__(self, max_batch=8, timeout_ms=50):
        self.buffer = []
        self.max_batch = max_batch
        self.timeout_ms = timeout_ms
    
    def add(self, item):
        self.buffer.append(item)
        if len(self.buffer) >= self.max_batch:
            return self.flush()
        return None
    
    def flush(self):
        batch = self.buffer.copy()
        self.buffer.clear()
        return batch
```

### 5.2 模型缓存

```python
import hashlib
import os

class ModelCache:
    """模型缓存管理，避免重复加载"""
    def __init__(self, cache_dir="model_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.core = Core()
        self.core.set_property({"CACHE_DIR": cache_dir})
    
    def load(self, model_xml, device="CPU"):
        return self.core.compile_model(model_xml, device)
```

### 5.3 流式推理

```python
from openvino.runtime import Core, InferRequest

class StreamingInference:
    def __init__(self, model_xml, device="CPU"):
        core = Core()
        self.model = core.compile_model(model_xml, device)
        self.infer_request = self.model.create_infer_request()
    
    def stream(self, input_data, callback):
        """流式推理，逐块输出"""
        for chunk in input_data:
            self.infer_request.start_async(chunk)
            self.infer_request.wait()
            result = self.infer_request.get_output_tensor().data
            callback(result)
```

## 6. 性能基准测试

### 6.1 基准测试脚本

```python
import time
import numpy as np
from openvino.runtime import Core

def benchmark(model_xml, device, input_shape, n_iterations=100, warmup=10):
    core = Core()
    model = core.compile_model(model_xml, device)
    infer_request = model.create_infer_request()
    
    input_data = np.random.randn(*input_shape).astype(np.float32)
    
    # Warmup
    for _ in range(warmup):
        infer_request.infer(input_data)
    
    # Benchmark
    latencies = []
    for _ in range(n_iterations):
        start = time.perf_counter()
        infer_request.infer(input_data)
        latencies.append((time.perf_counter() - start) * 1000)
    
    latencies = np.array(latencies)
    return {
        "device": device,
        "mean_ms": np.mean(latencies),
        "p50_ms": np.percentile(latencies, 50),
        "p95_ms": np.percentile(latencies, 95),
        "p99_ms": np.percentile(latencies, 99),
        "throughput_fps": 1000 / np.mean(latencies),
    }
```

### 6.2 典型基准结果

| 模型 | 设备 | FP32 (ms) | FP16 (ms) | INT8 (ms) | 加速比 |
|------|------|-----------|-----------|-----------|--------|
| PaddleOCR-det | GPU | 45 | 28 | 15 | 3.0x |
| PaddleOCR-rec | GPU | 32 | 20 | 12 | 2.7x |
| Whisper-small | CPU | 180 | 120 | 65 | 2.8x |
| BGE-embed | GPU | 8 | 5 | 3 | 2.7x |
| FastSpeech2 | CPU | 25 | 18 | - | 1.4x |

## 7. 质量门控

### 7.1 量化精度验证

```python
def verify_quantization(original_model, quantized_model, test_data, threshold=0.02):
    """验证量化后精度损失在阈值内"""
    core = Core()
    orig = core.compile_model(original_model, "CPU")
    quant = core.compile_model(quantized_model, "CPU")
    
    max_diff = 0
    for data in test_data:
        orig_out = orig(data)[0]
        quant_out = quant(data)[0]
        diff = np.abs(orig_out - quant_out).mean()
        max_diff = max(max_diff, diff)
    
    passed = max_diff < threshold
    return {"max_diff": max_diff, "threshold": threshold, "passed": passed}
```

### 7.2 性能门控标准

| 检查项 | 标准 | 测试方法 |
|--------|------|----------|
| 量化精度损失 | <2% | 对比 FP32 基准 |
| 推理延迟 | <原始 50% | 100 次迭代均值 |
| 内存占用 | <原始 50% | 进程 RSS 监控 |
| 首次加载 | <3s | 冷启动计时 |
| 模型文件大小 | <原始 30% | 文件对比 |

## 8. 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| GPU 推理失败 | 驱动不兼容 | 更新 Intel GPU 驱动 >= 31.0.101.4502 |
| NPU 不可用 | 固件未安装 | 安装 Intel NPU Driver |
| INT8 精度下降大 | 校准数据不足 | 增加 subset_size 到 500+ |
| 内存溢出 | batch 过大 | 减小 NUM_STREAMS 或 batch_size |
| 首次推理慢 | 模型编译缓存 | 启用 CACHE_DIR |
