# SKILL.md - industrial-anomaly-detector

## 概述

**Skill 名称**: industrial-anomaly-detector

**版本**: 1.1.0

**功能描述**: 工业视觉异常检测 Skill，支持上传产品图片进行缺陷检测，返回异常热力图和检测结果。集成 anomalib 库（v2.3.3），支持 20+ 种异常检测模型。

**适用场景**: 工业质检、产品缺陷检测、制造业质量控制

---

## 目录结构

```
industrial-anomaly-detector/
├── SKILL.md                    # 本文件
├── references/
│   ├── models_guide.md         # 模型选择指南
│   └── examples/               # 使用示例
│       ├── basic_usage.py
│       └── batch_processing.py
├── scripts/
│   ├── detector.py             # 核心检测器类
│   ├── preprocessor.py         # 图片预处理
│   └── postprocessor.py        # 结果后处理
└── templates/
    ├── single_image.jinja2     # 单图检测模板
    └── batch_report.jinja2     # 批量报告模板
```

---

## 环境要求与安装

### 安装命令

```bash
# 标准安装
pip install anomalib

# CPU 支持
pip install "anomalib[cpu]"

# CUDA 13.0 支持
pip install "anomalib[cu130]"

# OpenVINO 加速
pip install "anomalib[openvino]"

# 完整安装
pip install "anomalib[full]"
```

### 当前环境

```
- Python: 3.13.12
- PyTorch: 2.11.0+cu130
- CUDA: 不可用 (CPU 模式)
- anomalib: 2.3.3
- OpenCV: 4.13.0
- Pillow: 可用
```

---

## 核心功能实现

### 1. AnomalyDetector 核心类

```python
import os
import time
from dataclasses import dataclass, field
from typing import Optional, Union
from pathlib import Path

import numpy as np
from PIL import Image
import cv2

from anomalib.data import MVTecAD, PredictDataset, Folder
from anomalib.models import Patchcore, Padim, EfficientAd
from anomalib.engine import Engine
from anomalib.deploy import ExportType


@dataclass
class DetectionResult:
    """异常检测结果数据类"""
    
    # 基础信息
    image_path: str
    image: Optional[Image.Image] = None
    
    # 异常判定
    is_anomaly: bool = False
    anomaly_score: float = 0.0
    anomaly_label: int = 0
    
    # 热力图
    anomaly_map: Optional[np.ndarray] = None
    heatmap_image: Optional[Image.Image] = None
    
    # 缺陷区域
    bounding_boxes: Optional[list[dict]] = None
    defect_regions: int = 0
    
    # 元数据
    model_name: str = ""
    inference_time: float = 0.0
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "image_path": self.image_path,
            "is_anomaly": self.is_anomaly,
            "anomaly_score": float(self.anomaly_score),
            "anomaly_label": int(self.anomaly_label),
            "defect_regions": self.defect_regions,
            "model_name": self.model_name,
            "inference_time": round(self.inference_time, 4),
            "timestamp": self.timestamp,
        }


class AnomalyDetector:
    """工业异常检测器"""
    
    # 支持的模型列表
    SUPPORTED_MODELS = {
        "patchcore": Patchcore,
        "padim": Padim,
        "efficientad": EfficientAd,
    }
    
    def __init__(
        self,
        model_name: str = "patchcore",
        device: str = "cpu",
        backbone: str = "resnet18",
        pre_trained: bool = True,
    ):
        """
        初始化检测器
        
        Args:
            model_name: 模型名称 (patchcore/padim/efficientad)
            device: 运行设备 (cpu/cuda/auto)
            backbone: 特征提取骨干网络
            pre_trained: 是否使用预训练权重
        """
        self.model_name = model_name.lower()
        self.device = device
        self.backbone = backbone
        self.pre_trained = pre_trained
        
        if self.model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"不支持的模型: {model_name}, "
                f"支持的模型: {list(self.SUPPORTED_MODELS.keys())}"
            )
        
        # 延迟初始化模型
        self._model = None
        self._engine = None
    
    @property
    def model(self):
        """懒加载模型"""
        if self._model is None:
            self._model = self.SUPPORTED_MODELS[self.model_name](
                backbone=self.backbone,
                pre_trained=self.pre_trained,
            )
        return self._model
    
    @property
    def engine(self):
        """创建引擎"""
        if self._engine is None:
            self._engine = Engine(accelerator=self.device)
        return self._engine
    
    def detect(
        self,
        image_path: Union[str, Path],
        return_heatmap: bool = True,
        threshold: float = 0.5,
    ) -> DetectionResult:
        """
        检测单张图片的异常
        
        Args:
            image_path: 图片路径
            return_heatmap: 是否返回热力图
            threshold: 异常阈值
            
        Returns:
            DetectionResult: 检测结果
        """
        start_time = time.time()
        
        # 验证图片
        image_path = str(image_path)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")
        
        # 读取图片
        image = Image.open(image_path).convert("RGB")
        
        # 创建预测数据集
        predict_ds = PredictDataset(path=os.path.dirname(image_path), image_size=(256, 256))
        
        # 执行预测
        predictions = self.engine.predict(model=self.model, dataset=predict_ds)
        
        # 处理结果
        result = DetectionResult(
            image_path=image_path,
            image=image,
            model_name=self.model_name,
            inference_time=time.time() - start_time,
        )
        
        if predictions and len(predictions) > 0:
            pred = predictions[0]
            result.anomaly_score = float(pred.pred_score)
            result.anomaly_label = int(pred.pred_label)
            result.is_anomaly = result.anomaly_score > threshold
            
            if return_heatmap and hasattr(pred, "anomaly_map"):
                result.anomaly_map = pred.anomaly_map
                result.heatmap_image = self._create_heatmap_image(
                    result.anomaly_map, image
                )
        
        result.inference_time = time.time() - start_time
        return result
    
    def detect_batch(
        self,
        image_paths: list[Union[str, Path]],
        threshold: float = 0.5,
    ) -> list[DetectionResult]:
        """
        批量检测多张图片
        
        Args:
            image_paths: 图片路径列表
            threshold: 异常阈值
            
        Returns:
            list[DetectionResult]: 检测结果列表
        """
        results = []
        for path in image_paths:
            try:
                result = self.detect(path, threshold=threshold)
                results.append(result)
            except Exception as e:
                # 记录错误但继续处理其他图片
                results.append(DetectionResult(
                    image_path=str(path),
                    model_name=self.model_name,
                    error=str(e),
                ))
        return results
    
    def train(
        self,
        datamodule,
        max_epochs: int = 1,
    ) -> None:
        """
        训练模型
        
        Args:
            datamodule: 数据模块 (MVTecAD 或 Folder)
            max_epochs: 训练轮数
        """
        datamodule.prepare_data()
        datamodule.setup()
        
        # 更新引擎配置
        engine = Engine(
            accelerator=self.device,
            max_epochs=max_epochs,
        )
        
        engine.fit(datamodule=datamodule, model=self.model)
    
    def export_model(
        self,
        export_path: str,
        export_type: str = "openvino",
    ) -> str:
        """
        导出训练好的模型
        
        Args:
            export_path: 导出路径
            export_type: 导出类型 (torch/onnx/openvino)
            
        Returns:
            str: 导出的模型路径
        """
        export_type_map = {
            "torch": ExportType.TORCH,
            "onnx": ExportType.ONNX,
            "openvino": ExportType.OPENVINO,
        }
        
        if export_type.lower() not in export_type_map:
            raise ValueError(f"不支持的导出类型: {export_type}")
        
        os.makedirs(export_path, exist_ok=True)
        self.engine.export(
            model=self.model,
            export_type=export_type_map[export_type.lower()],
            export_path=export_path,
        )
        
        return export_path
    
    def _create_heatmap_image(
        self,
        anomaly_map: np.ndarray,
        original_image: Image.Image,
    ) -> Image.Image:
        """生成异常热力图可视化"""
        # 归一化到 0-255
        if anomaly_map.max() > anomaly_map.min():
            normalized = (anomaly_map - anomaly_map.min()) / (anomaly_map.max() - anomaly_map.min())
            heatmap_uint8 = (normalized * 255).astype(np.uint8)
        else:
            heatmap_uint8 = np.zeros_like(anomaly_map, dtype=np.uint8)
        
        # 应用伪彩色
        heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(heatmap_color)
```

---

## 数据集支持

### 1. MVTecAD 数据集

```python
from anomalib.data import MVTecAD

# 创建数据集
datamodule = MVTecAD(
    root="./datasets/MVTecAD",
    category="bottle",  # 可选类别见下表
    train_batch_size=32,
    eval_batch_size=32,
)

# 可用类别
categories = [
    "bottle", "cable", "capsule", "carpet", "grid",
    "hazelnut", "leather", "metal_nut", "pill", "screw",
    "tile", "toothbrush", "transistor", "wood", "zipper"
]
```

### 2. Folder 自定义数据集

```python
from anomalib.data import Folder

datamodule = Folder(
    name="custom_dataset",
    root="./datasets/custom",
    normal_dir="good",        # 正常图片目录
    abnormal_dir="defect",    # 异常图片目录
)
```

### 3. PredictDataset 推理数据集

```python
from anomalib.data import PredictDataset

# 单张图片
predict_ds = PredictDataset(
    path="./test_images/image.jpg",
    image_size=(256, 256)
)

# 目录批量
predict_ds = PredictDataset(
    path="./test_images/",
    image_size=(256, 256)
)
```

---

## 完整使用流程

### 流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                         训练模式                                  │
├─────────────────────────────────────────────────────────────────┤
│  1. 创建数据模块 (MVTecAD / Folder)                               │
│  2. 创建模型 (Patchcore / Padim / EfficientAd)                   │
│  3. 创建引擎 (Engine)                                            │
│  4. 执行训练 (engine.fit)                                        │
│  5. 执行测试 (engine.test)                                       │
│  6. 导出模型 (engine.export)                                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         推理模式                                  │
├─────────────────────────────────────────────────────────────────┤
│  1. 加载模型 (from checkpoint)                                   │
│  2. 准备图片 (PredictDataset)                                    │
│  3. 执行推理 (engine.predict)                                    │
│  4. 处理结果 (anomaly_map, pred_score)                          │
│  5. 生成热力图可视化                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 训练示例

```python
from anomalib.data import MVTecAD
from anomalib.models import Patchcore
from anomalib.engine import Engine

# 1. 创建数据模块
datamodule = MVTecAD(
    root="./datasets/MVTecAD",
    category="bottle",
)
datamodule.prepare_data()
datamodule.setup()

# 2. 创建模型
model = Patchcore(
    backbone="resnet18",
    pre_trained=True  # 需要网络下载预训练权重
)

# 3. 创建引擎
engine = Engine(
    accelerator="cpu",  # 或 "cuda"
    max_epochs=1,
)

# 4. 训练
engine.fit(datamodule=datamodule, model=model)

# 5. 测试
test_results = engine.test(datamodule=datamodule, model=model)
print(f"测试结果: {test_results}")
```

### 推理示例

```python
from anomalib.data import PredictDataset
from anomalib.models import Patchcore
from anomalib.engine import Engine

# 加载模型
model = Patchcore()
engine = Engine()

# 准备预测数据
predict_ds = PredictDataset(
    path="./test_images",
    image_size=(256, 256)
)

# 执行预测
predictions = engine.predict(
    model=model,
    dataset=predict_ds
)

# 处理结果
for pred in predictions:
    print(f"图片: {pred.image_path}")
    print(f"异常分数: {pred.pred_score:.4f}")
    print(f"异常标签: {'异常' if pred.pred_label == 1 else '正常'}")
    if hasattr(pred, "anomaly_map"):
        print(f"热力图形状: {pred.anomaly_map.shape}")
```

---

## 模型选择指南

| 场景 | 推荐模型 | backbone | 特点 |
|------|---------|----------|------|
| 通用工业检测 | Patchcore | resnet18 | 效果好，易用，推荐入门 |
| 复杂纹理产品 | Padim | resnet18 | 多尺度特征 |
| 边缘设备部署 | EfficientAd | wide_resnet50_2 | 轻量级 |
| 金属表面检测 | FastFlow | WideResNet | 归一化流 |
| 缺乏训练数据 | WinCLIP | ViT | 零样本检测 |
| GAN 异常检测 | Ganomaly | resnet18 | 对抗生成 |

### 模型参数说明

```python
# Patchcore 参数
model = Patchcore(
    backbone="resnet18",        # 特征提取网络
    layers=["layer2", "layer3"], # 特征层
    num_neighbors=9,            # 近邻数量
    pre_trained=True,           # 预训练权重
)

# Padim 参数
model = Padim(
    backbone="resnet18",
    layers=["layer1", "layer2", "layer3"],
    pre_trained=True,
)

# EfficientAd 参数
model = EfficientAd(
    pre_trained=True,
)
```

---

## API 接口设计

### 1. 检测接口

```http
POST /api/v1/detect
Content-Type: multipart/form-data

请求参数:
  image: file (必填)
  model: string (可选, 默认 patchcore)
  threshold: float (可选, 默认 0.5)

响应示例:
{
  "status": "success",
  "data": {
    "is_anomaly": true,
    "anomaly_score": 0.8734,
    "defect_regions": 2,
    "inference_time": 0.234
  },
  "heatmap_url": "/results/heatmap_xxx.png"
}
```

### 2. 批量检测接口

```http
POST /api/v1/detect/batch
Content-Type: multipart/form-data

请求参数:
  images: file[] (必填, 最多 100 张)
  model: string (可选)

响应示例:
{
  "status": "success",
  "total": 10,
  "anomaly_count": 3,
  "results": [...]
}
```

---

## 错误处理

| 错误类型 | 错误码 | 处理建议 |
|---------|-------|---------|
| 图片格式不支持 | 400 | 提示用户转换格式 (jpg/png/bmp/tiff) |
| 图片尺寸过大 | 413 | 建议压缩或裁剪 (< 4096x4096) |
| 模型加载失败 | 500 | 检查网络连接或使用 pre_trained=False |
| GPU 不可用 | 500 | 自动切换到 CPU 模式 |
| 数据集下载失败 | 500 | 手动下载 MVTecAD 或使用 Folder |

### 常见问题

```python
# 1. 网络不可用时的处理
model = Patchcore(pre_trained=False)  # 不下载预训练权重

# 2. GPU 内存不足
engine = Engine(accelerator="cpu")  # 使用 CPU

# 3. 数据集下载失败
# 手动下载 MVTecAD: https://www.mvtec.com/company/research/datasets/mvtec-ad/
# 或使用 Folder 数据集格式
```

---

## 性能指标

| 指标 | CPU 目标 | GPU 目标 |
|------|---------|---------|
| 单图推理时间 | < 2s | < 500ms |
| 批量处理吞吐量 | > 1 img/s | > 10 img/s |
| 热力图分辨率 | 与输入一致 | 与输入一致 |
| 内存占用 | < 4GB | < 2GB |

---

## 依赖项

```yaml
Python: ">=3.10"
PyTorch: ">=2.0"
anomalib: ">=2.3.3"
opencv-python: ">=4.8"
Pillow: ">=10.0"
numpy: ">=1.24"
```

---

## 实战测试记录

### 测试环境

- **Python**: 3.13.12
- **PyTorch**: 2.11.0+cu130
- **anomalib**: 2.3.3
- **CUDA**: 不可用 (CPU 模式)

### 测试结果

| 测试项 | 状态 | 说明 |
|--------|------|------|
| 模块导入 | ✅ 成功 | 所有模块导入正常 |
| MVTecAD 数据集 | ✅ 成功 | 数据集类创建成功 |
| Patchcore 模型 | ✅ 成功 | 模型创建成功 |
| Padim 模型 | ✅ 成功 | 模型创建成功 |
| Engine 引擎 | ✅ 成功 | 引擎创建成功 |
| PredictDataset | ✅ 成功 | 预测数据集创建成功 |
| Folder 数据集 | ✅ 成功 | 自定义数据集创建成功 |
| 完整训练 | ⚠️ 待网络 | 需要下载预训练权重 |
| 完整推理 | ⚠️ 待网络 | 需要下载预训练权重 |

### 网络限制说明

由于当前环境网络不可用，以下功能需要网络支持：
1. 下载预训练模型权重 (HuggingFace)
2. 下载 MVTecAD 数据集

在有网络环境下，使用 `pre_trained=True` 可获得更好的检测效果。

---

## 作者与许可证

**开发者**: Coze Agent

**许可证**: Apache 2.0

**版本历史**:
- v1.1.0 (2025-01-xx): 补充实战测试结果，完善 API 实现
- v1.0.0 (2024-xx-xx): 初始版本
