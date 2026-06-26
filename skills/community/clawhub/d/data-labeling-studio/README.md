# Data Labeling Studio | 数据标注工作室

English | [中文](#中文文档)

## Overview

Data Labeling Studio is an intelligent data annotation toolkit supporting image, text, audio, and video. It includes active learning for efficient labeling and quality control mechanisms.

## Features

- 🏷️ **Multi-Modal Support**: Image, text, audio, video annotation
- 🤖 **Active Learning**: AI suggests samples needing annotation
- ✔️ **Quality Control**: Consistency and accuracy checks
- 📤 **Multi-Format Export**: COCO, YOLO, Pascal VOC, TFRecord
- 👥 **Collaboration Ready**: Support for multi-user workflows

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Image Annotation
```python
from labeling_studio import ImageAnnotator

annotator = ImageAnnotator(
    annotation_type="bounding_box",
    labels=["person", "car", "dog"],
    output_format="coco"
)
annotator.annotate(image_dir="./images", output_file="./annotations.json")
```

### Quality Check
```python
from labeling_studio import QualityChecker

checker = QualityChecker()
report = checker.check(
    annotations="./annotations.json",
    ground_truth="./ground_truth.json",
    metrics=["iou", "consistency"]
)
```

## License
MIT

---

## 中文文档

## 概述

数据标注工作室是一个智能数据注释工具包，支持图像、文本、音频和视频。包含主动学习以实现高效标注和质量控制机制。

## 功能特性

- 🏷️ **多模态支持**: 图像、文本、音频、视频标注
- 🤖 **主动学习**: AI建议需要标注的样本
- ✔️ **质量控制**: 一致性和准确性检查
- 📤 **多格式导出**: COCO、YOLO、Pascal VOC、TFRecord
- 👥 **协作就绪**: 支持多用户工作流

## 许可证
MIT
