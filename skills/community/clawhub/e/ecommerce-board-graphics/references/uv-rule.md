# 紫光效果规则（uv-rule）

## 目标

模拟紫光灯照射下，**抠图（荧光/装饰部位）反光发光**，其余部分压暗。
关键是：发光必须**贴合抠图形状**，不能发散到整张图。

## 输入

- 原图 png（完整卡片图，RGBA/RGB）
- PSD 文件（含抠图图层）

## 抠图来源（最重要）

读 PSD 的**最上方可见、非"背景"图层**：

```python
from psd_tools import PSDImage
psd = PSDImage.open(psd_path)
best = None
for layer in psd:            # psd_tools 自底向上迭代
    if layer.is_group(): continue
    if not layer.visible or "背景" in layer.name: continue
    img = layer.composite(psd.bbox)
    if img and img.split()[-1].getbbox() is not None:
        best = img            # 最后一个 = 最上方图层
```

## 效果参数（已验证）

| 步骤 | 参数 |
|------|------|
| 基础压暗 | 原图 × 0.5 |
| 光晕 | 抠图alpha 高斯模糊 2.5px，阈值 0.2 |
| 主体色增强 | 抠图RGB × 1.45 + (28, 10, 54) |
| 核心提亮 | alpha>0.55 区域 → 抠图RGB × 1.55 |
| 环境紫光 | 抠图区域内加 (34, 9, 52) × 0.04 |
| 光晕半径 | 模糊 2.5（紧贴）~ 4（环境），禁止大半径发散 |

## 常见错误

- 光晕模糊半径过大 → 紫光发散糊全图 ✗
- 没用抠图alpha做蒙版 → 全图变紫 ✗
- 抠图尺寸和原图不一致没resize → 发光位置偏移 ✗
