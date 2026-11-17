# NPU 智能调度（V7 硬件优化）

> V7 的端侧推理优化核心：Intel 酷睿 Ultra NPU 11 TOPS 优先调度 + CPU/iGPU 异构协作。

## 1. Intel 酷睿 Ultra 硬件架构

### 1.1 三级算力单元
| 单元 | 算力 | 擅长任务 | 典型延迟 |
|------|------|----------|----------|
| **NPU** (Neural Processing Unit) | **11 TOPS** | 低功耗持续推理（OCR/ASR/TTS 实时任务） | < 200ms |
| **iGPU** (Xe-LPG / Arc) | **8 TFLOPS** | 视觉/并行计算（VLM 多模态/批量推理） | < 500ms |
| **CPU** (P-core + E-core) | **通用** | 协调调度 + 复杂逻辑（RAG 检索/统计分析） | < 1s |

### 1.2 任务分配矩阵
| 任务 | 推荐单元 | 备选单元 | 理由 |
|------|----------|----------|------|
| OCR 文字识别 | **NPU** | CPU | 低功耗 + 实时性 |
| ASR 语音转写 | **NPU** | iGPU | 流式推理 + 长时监听 |
| TTS 语音合成 | **NPU** | CPU | 流式输出 |
| RAG 检索 | **CPU** | iGPU | 内存密集 + 复杂逻辑 |
| 数据分析 | **CPU** | iGPU | 统计计算 |
| VLM 视频理解 | **iGPU** | NPU | 高吞吐 + 大模型 |
| LLM 创意生成 | **NPU + iGPU** | 云端 | 端云协同 |
| 复杂逻辑决策 | **CPU** | 云端 | 端云协同 |
| LLM 文本推理（1.5B DeepSeek-R1） | **CPU + iGPU** | NPU | 端云协同重活端侧做，适合持续流式输入 |

> **MR-2.1 备注**：`OpenVINO/DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov` 属于轻量文本推理模型（1.5B 参数，INT4 量化约 1~2GB）。与 VLM（7B）不同，1.5B 模型在 CPU + iGPU 异构调度下即可获得可接受延迟（< 3s/段），NPU 作为备选适合持续流式输入场景（如逐段分析长课程材料）。设备降级链：NPU → GPU → CPU（`scripts/analyze_courseware.py` `init_text_pipeline` 已实现）。

## 2. NPU 调度策略

### 2.1 任务分类
```python
TASK_TYPES = {
    'lightweight_continuous': {  # 轻量持续
        'unit': 'npu',
        'examples': ['ocr', 'asr_stream', 'tts_stream'],
        'priority': 'realtime',
    },
    'medium_batch': {  # 中等批量
        'unit': 'igpu',
        'examples': ['vlm_inference', 'asr_full', 'rag_embed'],
        'priority': 'fast',
    },
    'heavy_logic': {  # 重逻辑
        'unit': 'cpu',
        'examples': ['rag_query', 'analysis', 'pipeline_orchestration'],
        'priority': 'balanced',
    },
    'creative': {  # 创意决策
        'unit': 'cloud',  # 默认云端
        'examples': ['courseware_design', 'learning_path'],
        'priority': 'cloud_first',
    }
}
```

### 2.2 调度算法
```python
def schedule_task(task):
    # 1. 判断任务类型
    task_type = classify(task)
    
    # 2. 检查硬件可用性
    if task_type['unit'] == 'npu' and npu_available():
        return npu.execute(task)
    elif task_type['unit'] == 'igpu' and igpu_available():
        return igpu.execute(task)
    elif task_type['unit'] == 'cpu':
        return cpu.execute(task)
    else:
        # 降级到云端
        return cloud.execute_with_zup(task)
```

## 3. NPU 性能基准

### 3.1 OCR (PaddleOCR v4 INT8)
- NPU 推理：**< 200ms** / 帧
- CPU 推理：~800ms / 帧
- 加速比：**4x**

### 3.2 ASR (Whisper-small INT4)
- NPU 流式：**< 500ms** / 30s 音频
- iGPU 批量：~1.2s / 30s 音频
- CPU 推理：~3s / 30s 音频
- 加速比：**6x**

### 3.3 TTS (FastSpeech2 IR)
- NPU 流式：**< 300ms** / 100 字
- CPU 推理：~1s / 100 字
- 加速比：**3x**

### 3.4 VLM (Qwen2.5-VL-7B INT4)
- iGPU 推理：**< 2s** / 帧
- NPU 推理：~3s / 帧
- CPU 推理：> 10s / 帧（不可用）
- 加速比：**5x**（iGPU vs CPU）

## 4. 调度器实现

### 4.1 调度器入口
```python
class NPUScheduler:
    def __init__(self):
        self.queue = PriorityQueue()
        self.npu_load = 0
        self.igpu_load = 0
        self.cpu_load = 0
    
    def submit(self, task, task_type):
        priority = self._get_priority(task_type)
        self.queue.put((priority, task))
        return self._dispatch()
    
    def _dispatch(self):
        while not self.queue.empty():
            priority, task = self.queue.get()
            unit = self._choose_unit(task)
            unit.execute(task)
    
    def _choose_unit(self, task):
        if task.is_continuous() and self.npu_load < 0.8:
            return NPU()
        elif task.is_visual() and self.igpu_load < 0.8:
            return iGPU()
        else:
            return CPU()
```

### 4.2 性能监控
```python
class PerformanceMonitor:
    def get_metrics(self):
        return {
            'npu_utilization': self.npu.get_utilization(),
            'igpu_utilization': self.igpu.get_utilization(),
            'cpu_utilization': self.cpu.get_utilization(),
            'avg_latency': self.get_avg_latency(),
            'throughput': self.get_throughput(),
            'power_consumption': self.get_power(),
        }
```

## 5. NPU 优化技巧

### 5.1 模型量化
- **INT8 量化**：精度损失 < 2%，速度提升 3-4x（OCR/RAG 推荐）
- **INT4 量化**：精度损失 < 5%，速度提升 5-6x（ASR/VLM 推荐）
- **FP16 量化**：精度损失 < 1%，速度提升 2-3x（TTS 推荐）

### 5.2 算子融合
- Conv + BN + ReLU 融合
- Multi-Head Attention 融合
- Softmax + MatMul 融合

### 5.3 动态批处理
- 短任务自动批处理（如 OCR 多个图片）
- 长任务独占（如 VLM 视频分析）

## 6. 6 项检查清单

部署 V7 NPU 调度前必查：

- [ ] 确认 Intel 酷睿 Ultra 处理器（含 NPU 11 TOPS）
- [ ] 安装 OpenVINO 2024.x + NPU 驱动
- [ ] 下载 5 本地 AI 模型（OCR/ASR/TTS/RAG/VLM）
- [ ] 转换模型为 OpenVINO IR 格式
- [ ] 验证 NPU 推理可用（运行基准测试）
- [ ] 启用性能监控仪表盘

## 7. 性能基准测试方法

```bash
# 1. 下载 OpenVINO NNCF
pip install nncf

# 2. 转换模型
python -c "
import openvino as ov
import nncf
model = ov.convert_model('paddleocr_v4.onnx')
quantized = nncf.quantize(model, calibration_dataset)
ov.save_model(quantized, 'paddleocr_v4_int8.xml')
"

# 3. 运行基准（使用 OpenVINO 自带 benchmark_app 工具）
# benchmark_app -m paddleocr_v4_int8.xml -d NPU

# 4. 验证延迟 < 200ms
```

---

> **核心价值**：V7 NPU 调度让 AI PC 真正发挥「端云协同」中的「端侧」算力优势 —— 11 TOPS 持续推理能力，让 5 个本地 AI 工具同时运行不卡顿。
