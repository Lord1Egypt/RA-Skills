---
name: ai-density
description: AI含量检测工具 - 检测文本AI生成占比，输出0-10级客观分级 | AI Content Detector - Detect AI-generated text with 0-10 objective grading
---

# AI Density / AI含量检测

一款双语AI含量检测工具，分析文本并输出AI生成内容占比的0-10级客观分级。

A bilingual AI content detection tool that analyzes text and outputs an objective 0-10 grading scale for AI-generated content proportion.

## 功能特点 / Features

- **AI含量检测**: 0-10级客观分级 / 0-10 objective grading
- **多维度分析**: 5个检测维度带权重 / 5 dimensions with weights
- **易于使用**: 一行代码调用 / One-line API

## 安装 / Installation

```bash
pip install -r requirements.txt
```

## 使用示例 / Usage

```python
from scripts.detector import AIDensityDetector

detector = AIDensityDetector()
result = detector.detect("Your text here / 你的文本")
print(f"AI含量等级: {result['level']}/10")
print(f"置信度: {result['confidence']}")
```

完整文档请查看 README.md / See README.md for full documentation.
