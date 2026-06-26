# Anomalib Industrial Anomaly Detector

<div align="center">

![Anomalib Version](https://img.shields.io/badge/anomalib-v2.3.3-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/License-MIT%20Zero-blue)

**工业级视觉异常检测 Skill，基于 Intel anomalib 库，支持 20+ 种异常检测模型**

[功能介绍](#功能介绍) • [快速开始](#快速开始) • [安装配置](#安装配置) • [使用示例](#使用示例) • [模型列表](#支持的模型) • [注意事项](#注意事项)

</div>

---

## 功能介绍

`anomalib-detector` 是一款面向工业场景的视觉异常检测 Skill，集成 Intel 开源的 anomalib 深度学习库，提供：

- ✅ **20+ 异常检测模型**：Patchcore、Padim、DFKD、EfficientAd 等
- ✅ **MVTec AD 数据集**：15 种工业品缺陷类别
- ✅ **丰富的后处理**：异常热力图、分割掩码、阈值优化
- ✅ **多硬件支持**：CPU、CUDA、OpenVINO 加速
- ✅ **灵活部署**：支持 PyTorch、ONNX、OpenVINO 格式导出

## 快速开始

### 5 分钟快速体验

```python
from anomalib.data import MVTecAD
from anomalib.models import Patchcore
from anomalib.engine import Engine

# 1. 准备数据（以 bottle 为例）
datamodule = MVTecAD(category="bottle")
datamodule.setup()  # 下载并加载数据

# 2. 创建模型
model = Patchcore()
model.backbone.layers[-1]  # WideResNet50 骨干网络

# 3. 训练
engine = Engine()
engine.fit(model=model, datamodule=datamodule)

# 4. 预测
predictions = engine.predict(model=model, datamodule=datamodule)
```

### 一行代码调用检测

```python
# 使用封装好的检测器
from detector import AnomalyDetector

detector = AnomalyDetector(model_name="patchcore")
result = detector.detect("path/to/product_image.jpg")
print(f"异常分数: {result.anomaly_score:.3f}")
```

---

## 安装配置

### 环境要求

| 要求 | 版本 |
|------|------|
| Python | 3.9 - 3.13 |
| PyTorch | 2.0+ |
| CUDA (可选) | 11.8+ / 13.0+ |

### 安装命令

```bash
# 标准安装
pip install anomalib

# CPU 模式（无 GPU）
pip install "anomalib[cpu]"

# CUDA 13.0 支持
pip install "anomalib[cu130]"

# OpenVINO 加速（Intel 硬件）
pip install "anomalib[openvino]"

# 完整安装（包含所有依赖）
pip install "anomalib[full]"
```

### 依赖列表

```
anomalib>=2.3.0
torch>=2.0.0
torchvision>=0.15.0
opencv-python>=4.8.0
pillow>=10.0.0
kornia>=0.7.0
timm>=0.9.0
```

---

## 使用示例

### 示例 1：单图缺陷检测

```python
import cv2
from anomalib.deploy import OpenVINOInferencer

# 加载导出模型
inferencer = OpenVINOInferencer(
    metadata="path/to/metadata.json",
    weights="path/to/model.bin"
)

# 检测单张图片
image = cv2.imread("product.jpg")
result = inferencer.predict(image)

print(f"是否为异常: {result.pred_mask}")
print(f"异常分数: {result.anomaly_score:.3f}")
```

### 示例 2：批量产品检测

```python
from pathlib import Path
from detector import BatchDetector

detector = BatchDetector(
    model_name="padim",
    threshold="otsu"  # 自动阈值
)

# 批量检测
results = detector.detect_folder(
    folder_path="path/to/products/",
    extensions=[".jpg", ".png"],
    output_dir="results/"
)

# 汇总报告
summary = results.summary()
print(f"检测总数: {summary['total']}")
print(f"异常数量: {summary['anomalies']}")
```

### 示例 3：自定义数据集

```python
from anomalib.data import Folder

# 使用自定义数据集
datamodule = Folder(
    name="custom_dataset",
    root="path/to/dataset/",
    normal_dir="normal/",      # 正常样本目录
    abnormal_dir="defects/",   # 异常样本目录
    mask_dir="masks/",         # 分割标注（可选）
    normal_split_ratio=0.2    # 验证集比例
)
```

---

## 支持的模型

| 模型 | 特点 | 适用场景 | 速度 |
|------|------|----------|------|
| **Patchcore** | 记忆库 + 核心集采样 | 通用工业检测 ⭐ | 中 |
| **Padim** | 多层特征融合 | 纹理缺陷检测 | 快 |
| **EfficientAd** | 师生网络 | 小样本场景 | 快 |
| **DFKD** | 知识蒸馏 | 边缘部署 | 快 |
| **DRAEM** | 重建 + 判别 | 复杂纹理 | 慢 |
| **GANomaly** | GAN 重建 | 细粒度缺陷 | 慢 |

### MVTec AD 支持类别

```
bottle        瓶子          cable        线缆
capsule      胶囊          carpet       地毯
grid         网格          hazelnut     榛子
leather      皮革          pill         药片
screw         螺丝          tile         瓷砖
transistor   晶体管        wood         木材
zipper       拉链
```

---

## API 快速参考

### AnomalyDetector 类

```python
class AnomalyDetector:
    def __init__(self, model_name: str, device: str = "auto"):
        """初始化检测器
        
        Args:
            model_name: 模型名称 (patchcore/padim/efficientad/...)
            device: 运行设备 ("cpu"/"cuda"/"auto")
        """
    
    def detect(self, image_path: str, threshold: float = 0.5):
        """检测单张图片
        
        Returns:
            DetectionResult: 包含异常判定、热力图、分数
        """
    
    def detect_batch(self, image_paths: list):
        """批量检测
        """
```

### DetectionResult 数据类

```python
@dataclass
class DetectionResult:
    image_path: str           # 图片路径
    is_anomaly: bool         # 是否异常
    anomaly_score: float     # 异常分数 (0-1)
    heatmap: np.ndarray      # 异常热力图
    mask: np.ndarray         # 分割掩码（可选）
    bbox: List[int]          # 异常区域边界框（可选）
```

---

## 注意事项

### ⚠️ 网络要求

- **预训练模型**：首次运行需要访问 HuggingFace 下载权重（约 100-500MB）
- **MVTec AD 数据集**：完整数据集 5.26GB，可按类别选择性下载
- **离线模式**：可预先下载模型和数据，参考 [模型缓存配置](#离线使用)

### 离线使用

```python
import os
os.environ["HF_HUB_OFFLINE"] = "1"  # 离线模式

# 手动指定模型路径
model = Patchcore(pre_trained=False)  # 不自动下载
```

### GPU 内存优化

```python
# 减少批处理大小
model = Patchcore(pre_trained=True, coreset_sampling_ratio=0.1)

# 使用半精度
from torch.cuda.amp import autocast
```

### 常见问题

**Q: 预训练模型下载失败？**
> 检查网络连接，或设置代理：
> ```bash
> export HTTP_PROXY=http://proxy:8080
> export HTTPS_PROXY=http://proxy:8080
> ```

**Q: CUDA out of memory？**
> 减小图像尺寸或批处理大小，参考 GPU 内存优化部分。

**Q: 如何选择合适的模型？**
> 通用场景推荐 Patchcore，高精度需求推荐 Padim，速度优先推荐 EfficientAd。

---

## 目录结构

```
anomalib-detector/
├── SKILL.md              # Skill 核心文档
├── README.md             # 本文件
├── skill.json            # ClawHub 配置文件
├── examples/
│   ├── example_usage.py  # 基础使用示例
│   └── batch_processing.py # 批量处理示例
├── references/
│   └── models_guide.md   # 模型选择指南
└── requirements.txt      # Python 依赖列表
```

---

## License

本 Skill 基于 Apache 2.0 License 开源，使用时请遵守 [anomalib](https://github.com/openvinotoolkit/anomalib) 的许可协议。

---

<div align="center">

**Made with ❤️ for Industrial Quality Control**

</div>
