# 模型选择指南

本文档帮助你在不同场景下选择最合适的异常检测模型。

## 模型对比概览

| 模型 | 速度 | 精度 | 内存占用 | 适用场景 |
|------|------|------|----------|----------|
| Patchcore | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 通用工业检测 (推荐) |
| Padim | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 纹理缺陷、高精度需求 |
| EfficientAd | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | 小样本、边缘部署 |
| DRAEM | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 复杂纹理、高对比度缺陷 |
| GANomaly | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 细粒度缺陷检测 |
| CFA | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 少样本、细粒度分类 |
| FastFlow | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 通用、艺术纹理 |

---

## 场景推荐

### 🎯 通用工业检测（首选）

**推荐模型: Patchcore**

```python
from anomalib.models import Patchcore

model = Patchcore(
    backbone="wide_resnet50_2",  # 推荐骨干网络
    layers=["layer2", "layer3"],
    coreset_sampling_ratio=0.1,  # 核心集采样比例，越小越快
    pre_trained=True
)
```

**适用场景:**
- 半导体芯片检测
- 电子元器件外观检测
- 通用产品表面缺陷

**优点:**
- SOTA 性能，多个数据集排名第一
- 对新类别适应性好
- 推理速度适中

---

### 🧵 纹理缺陷检测

**推荐模型: Padim**

```python
from anomalib.models import Padim

model = Padim(
    backbone="resnet18",  # 可选 resnet18/34/50
    layers=["layer1", "layer2", "layer3"],  # 多层特征融合
    pre_trained=True
)
```

**适用场景:**
- 纺织品瑕疵检测
- 金属表面划痕
- 纸张印刷缺陷

**优点:**
- 推理极快（特征预计算）
- 多尺度特征融合
- 内存占用低

---

### 📦 小样本场景

**推荐模型: EfficientAd**

```python
from anomalib.models import EfficientAd

model = EfficientAd(
    teacher_backbone="efficientnet_b0",
    student_backbone="efficientnet_b0",
    pre_trained=True
)
```

**适用场景:**
- 缺陷样本稀少
- 新产品线快速部署
- 数据标注成本高

**优点:**
- 专为小样本设计
- 师生网络架构
- 训练收敛快

---

### 🎨 复杂纹理

**推荐模型: DRAEM**

```python
from anomalib.models import DRAEM

model = DRAEM(
    backbone="resnet18",
    beta=1.0,  # 重建-判别平衡
    pre_trained=True
)
```

**适用场景:**
- 复杂图案表面
- 纹理变化大的产品
- 需要分割定位缺陷

**优点:**
- 端到端训练
- 可同时定位缺陷
- 对噪声鲁棒

---

## 按数据集推荐

### MVTec AD 数据集

| 类别 | 推荐模型 | 备注 |
|------|----------|------|
| bottle | Patchcore / Padim | 纹理简单 |
| cable | Patchcore | 结构复杂 |
| capsule | DRAEM / CFA | 表面复杂 |
| carpet | Patchcore | 纹理均匀 |
| grid | Padim | 规则纹理 |
| hazelnut | Patchcore | 多视角 |
| leather | Patchcore | 纹理复杂 |
| pill | EfficientAd | 尺寸小 |
| screw | Patchcore | 形状复杂 |
| tile | Padim | 规则图案 |
| transistor | Patchcore | 结构单一 |
| wood | Padim | 天然纹理 |
| zipper | Patchcore | 细粒度 |

### 其他数据集

| 数据集 | 推荐模型 | 特点 |
|--------|----------|------|
| VisA | Patchcore | 多物体场景 |
| KolektorSDD | Padim | 工业印刷 |
| MVTec LOCO | Patchcore | 逻辑异常 |

---

## 性能调优

### 提升精度

```python
# 1. 使用更大的骨干网络
model = Patchcore(backbone="wide_resnet101_2")

# 2. 使用更多特征层
model = Patchcore(layers=["layer1", "layer2", "layer3", "layer4"])

# 3. 增加核心集采样（更精确但更慢）
model = Patchcore(coreset_sampling_ratio=0.5)
```

### 提升速度

```python
# 1. 使用轻量骨干
model = Patchcore(backbone="resnet18")

# 2. 减少特征层
model = Patchcore(layers=["layer3"])

# 3. 减少核心集采样
model = Patchcore(coreset_sampling_ratio=0.01)

# 4. 使用 Padim（特征预计算）
model = Padim()  # 推理极快
```

### 减少内存

```python
# 1. 减小图像尺寸
datamodule = MVTecAD(category="bottle", image_size=(224, 224))

# 2. 减小批处理大小
engine = Engine(devices=1)

# 3. 使用 CPU 卸载
engine = Engine(accelerator="cpu")
```

---

## 模型导出

### PyTorch 原生

```python
from anomalib.deploy import ExportType

engine.export(
    model=model,
    export_type=ExportType.PYTORCH,
    export_path="./export/"
)
```

### ONNX

```python
engine.export(
    model=model,
    export_type=ExportType.ONNX,
    export_path="./export/"
)
```

### OpenVINO（推荐生产部署）

```python
engine.export(
    model=model,
    export_type=ExportType.OPENVINO,
    export_path="./export/"
)
```

---

## 快速选择决策树

```
开始
  │
  ├─ 通用工业检测？
  │   └─ 是 → Patchcore
  │
  ├─ 纹理缺陷 / 需要快速推理？
  │   └─ 是 → Padim
  │
  ├─ 缺陷样本很少？
  │   └─ 是 → EfficientAd
  │
  ├─ 需要分割定位缺陷？
  │   └─ 是 → DRAEM / CFA
  │
  └─ 不确定 / 追求 SOTA？
      └─ → Patchcore
```

---

## 总结建议

| 优先级 | 推荐 | 场景 |
|--------|------|------|
| 🥇 首选 | Patchcore | 90% 的工业场景 |
| 🥈 备选 | Padim | 追求速度或纹理场景 |
| 🥉 特殊 | EfficientAd | 小样本场景 |
| 专业 | DRAEM | 需要分割的场景 |
