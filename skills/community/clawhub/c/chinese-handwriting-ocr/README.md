# Chinese Handwriting OCR 🇨🇳⚡

> 中文手写体OCR引擎 — 双引擎架构，手写日期/签名/工号智能提取

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 架构

| 引擎 | 角色 | 场景 |
|------|------|------|
| **PaddleOCR** 🏆 | 主力 | 印刷体文档、合同、报表 |
| **RapidOCR** | 备选 | 手写体、日期、签名、工号 |

## 快速使用

```bash
# 手写日期提取（默认RapidOCR）
python scripts/ocr_date_extractor.py 文档.pdf

# 指定引擎
python scripts/ocr_date_extractor.py 文档.pdf --engine rapid
python scripts/ocr_date_extractor.py 文档.pdf --engine paddle
python scripts/ocr_date_extractor.py 文档.pdf --engine both
python scripts/ocr_date_extractor.py 文档.pdf --engine auto
```

## 智能日期流水线

```
Step 1 动态定位 → 全页找"年/月/日"文本行
Step 2 高精度OCR → 450dpi提取年月日组件
Step 3 智能校验 → 值域检查 + 前导1推断
Step 4 上下文推断 → 同批文档常见值补充
```

## 安装

```bash
pip install rapidocr-onnxruntime    # 手写体引擎
pip install paddleocr paddlepaddle  # 文档OCR引擎
```

## 训练自定义模型

```bash
# 从零训练手写数字CRNN模型
python scripts/train_crnn.py --samples 5000 --epochs 30
```

## 开源协议

MIT
