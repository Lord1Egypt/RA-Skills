---
name: arcgis-training-data-fix
description: 补全ArcGIS Pro深度学习训练数据缺失文件，支持9种元数据格式（PASCAL_VOC_rectangles、KITTI_rectangles、Classified_Tiles、RCNN_Masks、Labeled_Tiles、MultiLabeled_Tiles、Exported_Tiles、CycleGAN、Imagenet）和4种图像格式（TIFF、MRF、JPG、PNG），自动生成esri_model_definition.emd、esri_accumulated_stats.json、map.txt、stats.txt。当用户遇到Export Training Data卡在100%导致文件缺失、训练数据目录不被Pro识别、或需要手动补全训练数据文件时使用此技能。
---

# ArcGIS Pro 深度学习训练数据补全

补全 ArcGIS Pro Export Training Data for Deep Learning 工具因卡在100%而未生成的4个关键文件。自动检测元数据格式，严格按Pro标准格式生成标准命名文件。

## 支持范围

### 元数据格式（9种）
| 格式 | 标签结构 | 适用模型 |
|------|---------|---------|
| PASCAL_VOC_rectangles | labels/*.xml | SSD、YOLO、Faster R-CNN |
| KITTI_rectangles | labels/*.txt | 自动驾驶目标检测 |
| Classified_Tiles | labels/类别名/*.tif 或 labels/*.tif | U-Net、语义分割 |
| RCNN_Masks | labels/*.tif（像素级掩膜） | Mask R-CNN 实例分割 |
| Labeled_Tiles | labels/*.tif（分类切片） | 语义分割 |
| MultiLabeled_Tiles | labels/*.tif（多标注切片） | 多任务分割 |
| Exported_Tiles | labels/*.tif（导出切片） | 通用分割 |
| CycleGAN | images/A/ + images/B/ | 图像翻译/风格迁移 |
| Imagenet | labels/类别名/*.jpg|png | 图像分类 |

### 图像格式（4种）
TIFF (.tif/.tiff)、MRF (.mrf)、JPG (.jpg/.jpeg)、PNG (.png)

## 工作流程

### 1. 确认输入
- 询问用户：训练数据目录路径
- 用 bash 扫描目录结构，确认 images/ 和 labels/ 存在
- 脚本自动检测元数据格式和图像格式

### 2. 执行补全脚本

将 `main.py` 写入桌面后执行：

```bash
python main.py "D:\Deeplearn\Vehicle\sample"
```

脚本自动完成：
1. 检测元数据格式（矢量/栅格/CycleGAN/Imagenet）
2. 扫描所有影像计算波段统计（Min/Max/Mean/StdDev）
3. 根据格式解析标签（xml/txt/栅格/子目录结构）
4. 读取坐标文件获取像素大小和空间参考
5. 生成4个Pro标准文件

### 3. 输出文件

- `esri_model_definition.emd` — 模型定义（MetaDataMode 与导出格式一致）
- `esri_accumulated_stats.json` — 累积统计（含 NumBands/TileSizeX/Y 等Pro必需字段）
- `map.txt` — 影像-标签映射（正斜杠路径）
- `stats.txt` — 文本统计摘要

### 4. 验证结果

脚本自动验证4个文件是否生成并输出检查结果。

## 关键规则

- 所有文件名必须是 Pro 标准命名，自命名文件 Pro 不识别
- map.txt 路径用正斜杠 `/`，禁用反斜杠 `\`
- esri_accumulated_stats.json 必须包含 NumBands、TileSizeX/Y、TotalTiles 等字段，否则 Pro 报 KeyError
- AllTilesStats 和 BandStatsState 必须按波段排序，键名严格匹配
- 如目录中有非标准命名的 .emd/.json 文件，脚本自动清理

## 已知Pro报错与对应修复

| 报错 | 原因 | 修复 |
|------|------|------|
| Error 260303 | 文件名不是标准命名 | 本脚本自动使用标准文件名 |
| KeyError: 'NumBands' | json缺少必需字段 | 脚本自动补全所有必需字段 |
| KeyError: 'TileSizeX' | json缺少尺寸字段 | 脚本自动补全 |
| ERROR 004486 RCNN_Masks | 数据格式与预训练模型不匹配 | 需重新导出为匹配格式 |
| shape mismatch | 预训练模型类别数与训练数据不匹配 | 去掉预训练模型或调整数据 |
