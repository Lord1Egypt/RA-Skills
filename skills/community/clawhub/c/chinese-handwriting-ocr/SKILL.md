---
name: chinese-handwriting-ocr
description: 中文OCR双引擎 — PaddleOCR(主力文档OCR) + RapidOCR(手写体特化)，按需灵活切换
---

# 中文OCR双引擎技能 v2.0

> 双引擎：**PaddleOCR** 通用文档OCR + **RapidOCR** 手写体特化，按场景自动/手动切换

## 引擎分工

| 场景 | 推荐引擎 | 理由 |
|------|---------|------|
| **印刷体文档**、合同、报表 | `--engine paddle` | PaddleOCR中文印刷体识别率最高 |
| **手写体**、日期、签名、工号 | `--engine rapid` | RapidOCR手写数字/文字准确率更高 |
| **混合文档**（印刷+手写） | `--engine auto` | 自动检测内容类型切换 |
| 不确定用哪个 | `--engine both` | 双引擎交叉验证，取置信度高者 |

## 快速开始

```bash
# 手写体日期提取（默认RapidOCR）
python scripts/ocr_date_extractor.py 文档.pdf

# 指定引擎
python scripts/ocr_date_extractor.py 文档.pdf --engine rapid
python scripts/ocr_date_extractor.py 文档.pdf --engine paddle
python scripts/ocr_date_extractor.py 文档.pdf --engine both

# 提取特定区域手写文本
python scripts/ocr_rapid.py 文档.pdf --date-mode
python scripts/ocr_rapid.py 文档.pdf --signature-mode
```

## 核心脚本

### ocr_date_extractor.py — 日期提取引擎

```
python scripts/ocr_date_extractor.py 文档.pdf [--engine rapid|paddle|both|auto]
```

四层流水线：
1. 动态日期行定位
2. 选定引擎OCR
3. 智能值域校验
4. 文档上下文推断

### ocr_rapid.py — 手写体区域提取

```bash
python scripts/ocr_rapid.py 文档.pdf --date-mode --engine paddle
python scripts/ocr_rapid.py 文档.pdf --region 0.1 0.4 0.9 0.6 --engine both
```

### ocr_batch.py — 批量处理

```bash
# 批量处理目录下所有PDF
python scripts/ocr_batch.py --batch-dir ./pdfs --engine auto

# 双引擎交叉验证
python scripts/ocr_batch.py --batch-dir ./pdfs --engine both --json -o results.json
```

## 引擎对比

| 指标 | PaddleOCR 2.8 | RapidOCR 1.4 |
|------|:-------------:|:------------:|
| 印刷体中文 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 手写体数字 | ⭐⭐ | ⭐⭐⭐⭐ |
| 手写日期完全正确率 | 20% | 60% |
| 手写日期部分识别率 | 60% | 90%+ |
| 首次加载 | 慢（下载模型） | 快（缓存） |
| 速度 | 3-5s/页 | 2-3s/页 |
| 安装包 | ~200MB+模型 | ~55MB |

## 自动引擎选择逻辑 (`--engine auto`)

```
1. 全页低分OCR快速分析内容类型
2. 检测到"年/月/日"等日期关键字 → RapidOCR
3. 检测到大量印刷体文字 → PaddleOCR
4. 混合内容 → both（双引擎交叉验证）
```

## 参数参考

| 参数 | 说明 |
|------|------|
| `--engine rapid\|paddle\|both\|auto` | OCR引擎选择 |
| `--json` | JSON格式输出 |
| `-p, --pages` | 指定页码(1-based) |
| `--region X1 Y1 X2 Y2` | 自定义区域(百分比0-1) |
| `--batch` | 批量处理目录 |
| `--dpi` | OCR分辨率(默认400) |

## 依赖

```bash
pip install rapidocr-onnxruntime    # 手写体引擎（已安装 ✅）
pip install paddleocr paddlepaddle  # 文档OCR引擎（已安装 ✅）
```

## 已知问题

- PaddleOCR 3.x + PaddlePaddle 3.x 存在 OneDNN 兼容问题，当前使用 2.x 版本
- 首次启动 PaddleOCR 需下载模型（~18MB）
- RapidOCR 多次调用可能产生进程残留，需定期清理
