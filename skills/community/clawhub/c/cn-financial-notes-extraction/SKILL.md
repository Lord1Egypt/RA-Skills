---
name: cn-financial-notes-extraction
version: 1.0.0
description: 提取中国 A 股上市公司年报 (PDF) 中的财务报表附注明细。适用于获取主表无法体现的深层数据（如 CapEx 明细、研发费用细分、应收账款账龄、关联方交易等）。
category: data-science
---

## 核心能力
从巨潮资讯 (CNINFO) 下载的年报 PDF 中，精准定位并提取**财务报表附注**中的表格数据。

## 适用场景
- **CapEx 分析**: 提取“在建工程”、“固定资产”、“无形资产”等附注中的本期增加/减少明细（MD&A 口径 vs 现金流表口径）。
- **风险排查**: 提取应收账款账龄、坏账准备计提比例、商誉减值明细。
- **关联交易**: 提取关联方往来余额、购销金额。
- **研发细分**: 提取研发费用资本化/费用化明细。

## 工作流程 (Workflow)
1.  **下载**: 通过 `CNInfo API Scraper` 或 `East Money Announcement Downloader` 下载最新年报 PDF。
2.  **定位**: 使用 `pdfplumber` (系统 Python 环境) 打开 PDF，全文检索关键字 `财务报表附注`。
3.  **提取**:
    - 从定位页开始，逐页扫描。
    - 提取表格 (`extract_tables()`)。
    - **智能过滤**: 根据表头关键词（如 `项目`, `期末余额`, `本期增加`, `本期减少`, `账面余额`）筛选有效表格。
    - 忽略纯文本页或无意义的排版表。
4.  **结构化**: 将提取的数据转换为 `Dict[List]` 或 `DataFrame` 格式输出。

## 关键参数与代码逻辑
```python
import pdfplumber

def extract_notes(pdf_path, keywords=None):
    found_data = []
    with pdfplumber.open(pdf_path) as pdf:
        # 1. 定位附注起始页
        start_idx = 0
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and "财务报表附注" in text:
                start_idx = i
                break
        
        # 2. 扫描表格
        for i in range(start_idx, len(pdf.pages)):
            page = pdf.pages[i]
            tables = page.extract_tables()
            for table in tables:
                # 过滤空表或短表
                if len(table) > 3 and any(row[0] for row in table if row):
                    # 可选：如果指定了 keywords，检查表头是否匹配
                    if keywords:
                        headers = " ".join([str(c) for c in table[0] if c])
                        if any(kw in headers for kw in keywords):
                            found_data.append({"page": i+1, "table": table})
                    else:
                        found_data.append({"page": i+1, "table": table})
    return found_data
```

## 注意事项
- **环境依赖**: 使用宿主机的 `python3` 和 `pdfplumber`，不要在沙箱 (subagent) 中直接运行，除非确认安装了库。
- **表格合并**: 跨页表格可能被拆分成两个，需逻辑合并（通过检查表头连续性）。
- **非标准排版**: 极少数老旧年报可能是扫描版，需 OCR（如 MinerU 或 Tesseract），但目前 A 股年报大多为原生 PDF，`pdfplumber` 效果最佳。