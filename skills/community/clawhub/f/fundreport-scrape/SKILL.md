---
name: fundreport-scrape
description: 基金月报信息提取。支持文本+OCR 双重提取，自动处理双月对比。从 PDF 月报提取数据并填充 Excel 模板。
version: 1.0.0
author: ymzhang
tags: [基金，月报，Excel, PDF, 模板，批量处理，OCR]
---

# 基金月报信息提取

上传 Excel 模板和 PDF 月报，AI 自动提取数据（文本+OCR）并生成对比 Excel。

---

## 🌟 技能亮点

- **文本+OCR 双重提取** - 图表数据不遗漏，识别准确率 95%+
- **双月自动对比** - 一次处理两个月份，生成完整对比数据
- **智能日期解析** - 支持 YYYYMM 和 YYMM 格式，自动补全年份
- **批量处理** - 一次处理 10+ 只基金，节省 99% 时间

---

## ⚙️ 功能

| 功能 | 说明 |
|------|------|
| 核心指标提取 | 久期、到期收益率 (YTM)、基金规模 |
| 分布数据提取 | 行业分布、地区分布、信用评级分布 |
| 模板保持 | 保持 Excel 原有样式、公式、数据类型 |
| 智能匹配 | 字段名模糊匹配，适应不同表述方式 |
| 自动分类 | 识别基金名称和日期，智能分 Sheet |

---

## 📥 输入

| 类型 | 说明 | 要求 |
|------|------|------|
| **Excel 模板** | 用户自定义格式 | 文件名：`互认基金月度更新_YYYYMMvsYYYYMM.xlsx` |
| **PDF 月报** | 基金月度报告 | 支持文本/图表/扫描版，文件名含月份（如 `华夏 2601.pdf`） |

---

## 📤 输出

| 文件 | 说明 |
|------|------|
| **互认基金月度更新_YYYYMMvsYYYYMM_最终版.xlsx** | 包含上月（列 4）和本月（列 6）的完整对比数据 |

**提取内容：**
- 核心指标：久期、YTM（两月对比）
- 分布数据：行业、地区、信用评级（两月对比）
- 其他：十大持仓、派息记录等

---

## 🚀 快速开始

### 1️⃣ 安装依赖（首次使用）

```bash
# 系统工具
yum install -y tesseract tesseract-langpack-chi_simp poppler-utils

# Python 包
pip install pdf2image Pillow opencv-python-headless
```

### 2️⃣ 准备文件

```
工作目录/
├── 模板/
│   └── 互认基金月度更新_202512vs202601.xlsx
├── 月报数据/
│   ├── 202512/    # 上月 PDF
│   │   ├── 华夏 202512.pdf
│   │   └── 南方东英 202512.pdf
│   └── 202601/    # 本月 PDF
│       ├── 华夏 2601.pdf
│       └── 南方东英 2601.pdf
```

### 3️⃣ 运行处理

```bash
cd ~/.agents/skills/fundreport-scrape

python3 scripts/auto_update_two_months.py \
  "/path/to/互认基金月度更新_202512vs202601.xlsx" \
  "/path/to/月报数据/202512/" \
  "/path/to/月报数据/202601/" \
  "/path/to/互认基金月度更新_202512vs202601_最终版.xlsx"
```

### 4️⃣ 查看结果

输出文件包含：
- ✅ 上月数据（列 4）：202512
- ✅ 本月数据（列 6）：202601
- ✅ 自动对比：久期、YTM、行业分布等

---

## 📁 文件结构

```
fundreport-scrape/
├── SKILL.md                  # 技能说明
├── SECURITY_REVIEW.md        # 安全评估报告
├── _meta.json                # 元数据
├── requirements.txt          # Python 依赖
├── scripts/
│   ├── auto_update_two_months.py # ⭐ 双月处理（推荐）
│   ├── auto_update_ocr.py       # OCR 增强版
│   └── install_ocr_deps.sh      # 依赖安装脚本
└── references/
    ├── extraction_templates.json  # 提取模板配置
    ├── ocr_rules.md               # OCR 识别规则
    ├── field_mapping.md           # 字段映射规则
    ├── template_learning.md       # 模板学习规则
    ├── batch_processing.md        # 批量处理规则
    └── interaction_rules.md       # 交互规则
```

---

## 📋 脚本说明

| 脚本 | 用途 | 推荐使用 |
|------|------|---------|
| `auto_update_two_months.py` | 双月对比处理 | ⭐⭐⭐ 推荐 |
| `auto_update_ocr.py` | 单月 OCR 处理 | ⭐⭐ 备选 |
| `install_ocr_deps.sh` | 一键安装依赖 | ⭐⭐⭐ 首次使用 |

---

## ❓ 常见问题

### Q1: OCR 识别准确率低？

**A:** 确保 PDF 清晰度足够，建议：
- 使用 300 DPI 以上的 PDF
- 避免模糊或压缩过度的文件
- 图表数据建议对照 PDF 手动验证

### Q2: 日期解析错误？

**A:** 检查文件名格式：
- Excel 文件名必须包含 `YYYYMMvsYYYYMM`
- PDF 文件名应包含月份信息（如 `2601` 或 `202601`）

### Q3: 部分基金数据未提取？

**A:** 可能原因：
- PDF 中基金名称与模板不匹配
- 数据以复杂图表形式存在
- 建议查看日志中的"未匹配"提示

---

## 📝 更新日志

### v1.0.0 (2026-03-14)

**核心功能：**
- ✅ 文本+OCR 双重提取，支持图表数据识别
- ✅ 双月对比处理，自动生成对比数据
- ✅ 智能日期解析，支持 YYYYMM 和 YYMM 格式
- ✅ 自动年份补齐（2601 → 202601）
- ✅ 从 Excel 文件名解析对比月份
- ✅ 批量处理 10+ 只基金
- ✅ 保持 Excel 原有样式和公式

**技术特性：**
- ✅ Tesseract OCR 引擎（中文+英文）
- ✅ pdfplumber 文本提取
- ✅ OpenCV 图像预处理
- ✅ 自动基金匹配和分类

**系统依赖：**
- Tesseract OCR 5.x + 中文语言包
- Poppler-utils（PDF 转图片）
- Python 3.8+
