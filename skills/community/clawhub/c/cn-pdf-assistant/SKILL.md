---
name: cn-pdf-assistant
version: "1.3.0"
description: "PDF文档处理工具（含OCR）。本地处理PDF文件，支持文本提取、智能摘要、表格导出、关键词问答、PDF拆分、OCR扫描版识别。纯本地处理，保护文档隐私。"
metadata:
  openclaw:
    emoji: "📄"
    category: productivity
    tags:
      - pdf
      - document
      - extract
      - ocr
---

## 功能
- PDF文本提取（支持指定页码范围）
- 智能摘要生成（章节标题识别+关键词频率分析）
- 表格提取（pdfplumber引擎）
- 关键词问答（基于段落匹配）
- PDF按页拆分
- **OCR扫描版识别**（v1.3.0新增，支持中英文扫描版PDF）
- 纯本地处理，无需联网

## 使用方法
```
python3 scripts/pdf_assistant.py <PDF文件路径> --action text
python3 scripts/pdf_assistant.py <PDF文件路径> --action summary
python3 scripts/pdf_assistant.py <PDF文件路径> --action tables
python3 scripts/pdf_assistant.py <PDF文件路径> --action ask --question "关键词"
python3 scripts/pdf_assistant.py <PDF文件路径> --action split
python3 scripts/pdf_assistant.py <PDF文件路径> --action ocr  # v1.3.0新增
```

## 依赖
- Python 3.7+
- PyPDF2, pdfplumber, pandas, openpyxl
- **OCR功能依赖**: pdf2image, pytesseract, Pillow, Tesseract-OCR（可选，未安装时OCR功能不可用）

## 权限声明
- 读取本地PDF文件
- 生成输出文件

## 使用场景
- 论文阅读：快速提取核心内容
- 合同审查：提取关键条款
- 财报分析：提取表格数据
- 资料整理：批量拆分PDF文档
- **扫描版PDF识别**：将扫描版PDF转为可搜索文本（v1.3.0新增）

## v1.3.0 更新日志
- ✅ 新增OCR功能（`--action ocr`）
- ✅ 支持中英文扫描版PDF识别
- ✅ 自动保存OCR结果为TXT文件
- ✅ 显示OCR置信度评分

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
