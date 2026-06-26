# 文件类型处理快速参考

> Agent 处理不同文件类型的快速决策指南

## 快速决策表

| 文件类型 | 扩展名 | 处理方式 | 是否需要额外依赖 |
|---------|--------|---------|----------------|
| **文本文件** | .md, .txt, .json, .yaml, .yml | 直接使用 Read 工具 | 否 |
| **代码文件** | .py, .js, .ts, .java, .go, .rs 等 | 直接使用 Read 工具 | 否 |
| **PDF 文件** | .pdf | 使用 PyMuPDF (fitz) + Python 脚本 | **是** (>=1.25.0) |
| **图片文件** | .png, .jpg, .jpeg, .gif, .bmp | 直接使用 Read 工具（视觉模型） | 否 |
| **Office 文档** | .docx, .xlsx, .pptx | 使用 python-docx/openpyxl 等 | 是 |
| **压缩文件** | .zip, .tar, .gz | 先解压，再处理内部文件 | 否 |

## PDF 文件处理流程

### 步骤 1：检查依赖

```bash
# 检查是否已安装 PyMuPDF
python -c "import fitz; print(fitz.__doc__[:30])"
```

**如果失败，安装依赖**：

```bash
pip install pymupdf>=1.25.0
```

### 步骤 2：读取 PDF

**方法 A：使用现有脚本（推荐）**

```bash
# 读取全部页面
python scripts/read_pdf.py sources/paper.pdf

# 读取指定页面范围（1-10页）
python scripts/read_pdf.py sources/paper.pdf 1-10
```

**方法 B：使用 Python 代码（推荐：PyMuPDF）**

```python
import fitz  # PyMuPDF

doc = fitz.open("sources/paper.pdf")
for page in doc:
    print(page.get_text())
doc.close()
```

**方法 C：读取完整内容**

```python
import fitz

def read_full_pdf(pdf_path):
    """读取 PDF 全部内容"""
    doc = fitz.open(pdf_path)
    full_text = []
    for i, page in enumerate(doc):
        text = page.get_text()
        if text:
            full_text.append(f"=== Page {i+1} ===\n{text}")
    doc.close()
    return "\n\n".join(full_text)

# 使用
content = read_full_pdf("sources/paper.pdf")
print(content)
```

**回退方案：pdfplumber（表格提取）**

如果 PyMuPDF 在提取复杂表格时效果不佳，可回退使用 `pdfplumber`（注意需安装安全版本 >= 0.11.8 以修复 CVE-2025-64512）：

```python
import pdfplumber

with pdfplumber.open("sources/paper.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

**OCR 最后手段**

对于扫描版 PDF 或上述方法均失败的情况，可使用 `pdf2image` + `pytesseract` 进行 OCR。

### 常见错误处理

**错误 1：pdftoppm not found**

```
pdftoppm failed: Command 'pdftoppm' not found
```

**原因**：Read 工具尝试使用系统工具 `pdftoppm` 处理 PDF，但系统未安装

**解决方案**：使用 PyMuPDF 或 pdfplumber 代替 Read 工具

---

**错误 2：UnicodeEncodeError**

```
UnicodeEncodeError: 'gbk' codec can't encode character '\u2022'
```

**原因**：Windows 控制台编码问题

**解决方案**：在脚本中强制使用 UTF-8 编码

```python
import sys
import io

# 强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

---

**错误 3：API Error 422**

```
API Error: 422 {"detail":"validation errors for ClaudeMessagesRequest..."}
```

**原因**：Read 工具处理 PDF 失败，导致 API 验证错误

**解决方案**：不使用 Read 工具，改用 PyMuPDF + Python 脚本

## 文本文件处理

**直接使用 Read 工具**：

```python
# Markdown 文件
Read("sources/notes.md")

# JSON/YAML 配置文件
Read("sources/config.yaml")
Read("sources/data.json")

# 代码文件
Read("sources/script.py")
Read("sources/app.js")
```

## 图片文件处理

**Read 工具支持视觉模型**：

```python
# PNG 图片
Read("sources/diagram.png")

# JPEG 图片
Read("sources/screenshot.jpg")

# Read 会自动识别图片并返回视觉内容
```

## Office 文档处理

需要安装相应的 Python 库：

```bash
# Word 文档
pip install python-docx

# Excel 表格
pip install openpyxl

# PowerPoint
pip install python-pptx
```

**示例：读取 Word 文档**

```python
from docx import Document

doc = Document("sources/report.docx")
for para in doc.paragraphs:
    print(para.text)
```

## 依赖检查脚本

快速检查所有依赖是否已安装：

```python
import importlib.util

def check_dependencies():
    """检查关键依赖"""
    deps = {
        'fitz': 'pymupdf>=1.25.0',
        'yaml': 'pyyaml>=6.0',
        'click': 'click>=8.0.0',
    }

    missing = []
    for module, package in deps.items():
        if importlib.util.find_spec(module) is None:
            missing.append(package)

    if missing:
        print(f"缺少依赖: {', '.join(missing)}")
        print(f"安装命令: pip install {' '.join(missing)}")
        return False
    else:
        print("✓ 所有依赖已安装")
        return True

check_dependencies()
```

## 参考文档

- [AGENTS.md](../AGENTS.md) - 完整的 Agent 实现指南
- [sources/README.md](../sources/README.md) - sources 目录说明
- [src/requirements.txt](../src/requirements.txt) - 依赖定义文件

---

*文档版本：1.1.0*
*最后更新：2026-04-16*
