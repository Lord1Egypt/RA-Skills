> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 本地 OCR 集成指南（V6）

## 概述
本指南说明如何将 OpenVINO 优化的 OCR 能力集成到 AI 通识课教学系统中，实现教材扫描识别、手写批注识别、表格提取、公式识别等教学生产力场景。

## 技术选型

### 推荐模型
| 模型 | 用途 | OpenVINO 优化 | 模型大小 | 推理速度 |
|------|------|--------------|---------|---------|
| PaddleOCR v4 (PP-OCRv4) | 通用文字识别 | INT8 量化 | ~10MB | <50ms/页 (GPU) |
| PaddleOCR 手写体模型 | 手写批注识别 | INT8 量化 | ~12MB | <80ms/页 (GPU) |
| PaddleOCR 表格识别 | 表格结构提取 | FP16 | ~15MB | <100ms/页 (GPU) |
| LaTeX-OCR | 数学公式识别 | FP16 | ~30MB | <200ms/公式 (GPU) |

### 硬件加速策略
- **NPU**：常驻 PP-OCRv4 检测模型（低功耗持续运行）
- **GPU**：处理识别模型和复杂表格/公式
- **CPU**：后处理（NMS、文字行聚合）

## 部署架构

### Client/Server 模式
```python
# ocr_service.py — 本地 OCR 微服务
from fastapi import FastAPI, UploadFile
from openvino.runtime import Core
import paddleocr
import numpy as np

app = FastAPI(title="AI通识课 OCR 服务", version="6.0.0")

# OpenVINO 推理引擎初始化
ie = Core()
# 加载 PP-OCRv4 检测模型（INT8 量化）
det_model = ie.compile_model(
    model="models/ppocrv4_det_int8.xml",
    device_name="GPU.NPU"  # 异构调度
)
# 加载 PP-OCRv4 识别模型
rec_model = ie.compile_model(
    model="models/ppocrv4_rec_int8.xml",
    device_name="GPU"
)

@app.post("/api/v1/ocr/recognize")
async def recognize_text(file: UploadFile):
    """通用文字识别 — 教材扫描件/PDF→结构化文本"""
    image_data = await file.read()
    # OCR 推理流程
    result = paddleocr_pipeline(image_data, det_model, rec_model)
    return {
        "status": "success",
        "data": {
            "texts": result["texts"],
            "boxes": result["boxes"],
            "confidence": result["confidence"],
            "layout": result["layout"]  # 版面分析结果
        },
        "ai_tool": "ocr",
        "hardware": {"gpu": True, "npu": True},
        "inference_time_ms": result["time_ms"]
    }

@app.post("/api/v1/ocr/table")
async def extract_table(file: UploadFile):
    """表格结构提取 — 教材表格→HTML/CSV"""
    ...

@app.post("/api/v1/ocr/formula")
async def recognize_formula(file: UploadFile):
    """数学公式识别 — 手写/印刷公式→LaTeX"""
    ...

@app.post("/api/v1/ocr/handwriting")
async def recognize_handwriting(file: UploadFile):
    """手写批注识别 — 学生手写→结构化文本"""
    ...
```

### 启动服务
```bash
# 启动 OCR 微服务（推荐端口 8901）
uvicorn ocr_service:app --host 127.0.0.1 --port 8901
```

## 教学场景集成

### 场景一：教材素材自动提取
```javascript
// 在 p5.js 课件中调用 OCR 服务
async function extractTextbookContent(imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);
    
    const response = await fetch('http://127.0.0.1:8901/api/v1/ocr/recognize', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    // 将识别结果注入课件内容
    return result.data.texts;
}
```

### 场景二：学生作业 OCR 批改
```javascript
// 识别学生手写答案并与标准答案对比
async function gradeHandwrittenAssignment(imageFile, answerKey) {
    const response = await fetch('http://127.0.0.1:8901/api/v1/ocr/handwriting', {
        method: 'POST',
        body: new FormData().append('file', imageFile)
    });
    const result = await response.json();
    // 对比批改
    return compareWithAnswerKey(result.data.texts, answerKey);
}
```

## OpenVINO 优化步骤

### 1. 模型转换
```bash
# PaddleOCR → OpenVINO IR
omz_downloader --name ppocrv4_mobile_rec --num_attempts 5
omz_converter --name ppocrv4_mobile_rec --precisions FP16,INT8
```

### 2. 量化优化
```python
# NNCF INT8 量化
import nncf
quantized_model = nncf.quantize(
    model=ov_model,
    calibration_dataset=calibration_loader,
    quantization_config=nncf.QuantizationConfig(
        preset=nncf.QuantizationPreset.MIXED
    )
)
```

### 3. 性能验证
| 指标 | 目标值 | 测试方法 |
|------|--------|---------|
| 检测延迟 | <30ms/页 | 100 页教材测试集 |
| 识别准确率 | ≥95% | ICDAR2019 + 教材测试集 |
| 手写识别率 | ≥85% | 自建教学手写数据集 |
| 内存占用 | <500MB | 峰值内存监控 |

## 错误降级
| 场景 | 降级方案 |
|------|---------|
| GPU 不可用 | 降级为 CPU 推理（延迟增加 3-5x） |
| OCR 服务崩溃 | 降级为手动文本输入 |
| 模型加载失败 | 降级为 PaddleOCR 原生推理（无 OpenVINO 加速） |
| 识别置信度 <60% | 标记为「待人工确认」 |

## 质量门控
- [ ] OCR 准确率 ≥95%（印刷体）
- [ ] 手写识别率 ≥85%
- [ ] 表格提取完整率 ≥90%
- [ ] 单页处理时间 <200ms（GPU）/ <1s（CPU）
- [ ] 内存峰值 <500MB
- [ ] 服务可用性 ≥99%（本地运行）
