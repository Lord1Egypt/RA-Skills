---
name: med-doc-preprocess
description: 医疗文档预处理公共库。将 pdf/doc/docx/xls/xlsx/csv/txt/json/图片等多格式文件统一加载为标准中间产物（pages / text / json / tables），供其他 skill 的 run.py 调用。
metadata:
  {
    "openclaw":
      {
        "emoji": "📂"
      }
  }
---

# 医疗文档预处理公共库

概述
----
本 skill 不独立运行，作为**共享工具库**被其他 skill 导入。

提供统一的文件读取与预处理能力：从各种原始格式文件中提取文本，返回标准化的中间产物（artifact），供下游 skill 进行各自的业务转换。

## 支持的输入格式

| 格式 | 处理方式 |
|------|---------|
| `txt` / `md` | 直接读取文本 |
| `json` | 解析 JSON 结构 |
| `csv` | 读取行列数据 |
| `xlsx` | 通过 openpyxl 读取（可选依赖） |
| `xls` | 通过 LibreOffice 转换 |
| `docx` | 解析 word/document.xml |
| `doc` | 通过 LibreOffice 转换 |
| `pdf` | pypdf / pdftotext 提取文本 |
| `png/jpg/jpeg/bmp/tif/tiff` | tesseract OCR 识别 |

## 输出的中间产物格式（artifact）

```python
{"kind": "text",   "text": str}                        # 单段纯文本
{"kind": "pages",  "pages": List[str]}                 # 多页文本（pdf 多页）
{"kind": "json",   "data": Any}                        # JSON 原始数据
{"kind": "tables", "tables": List[{"name": str, "rows": List[List[str]]}]}  # 行列数据
```

## 如何在其他 skill 中使用

在目标 skill 的 `scripts/run.py` 开头添加：

```python
from pathlib import Path
import sys

SKILLS_ROOT = Path(__file__).resolve().parents[2]
_preprocess_dir = SKILLS_ROOT / "_shared" / "doc-preprocess" / "scripts"
if str(_preprocess_dir) not in sys.path:
    sys.path.insert(0, str(_preprocess_dir))

from preprocess import (
    PreprocessError,
    SUPPORTED_FILE_TYPES,
    detect_input_type,
    normalize_header,
    load_input_artifact,
)
```

`load_input_artifact` 签名：

```python
def load_input_artifact(
    path: Path,
    input_type: str,
    encoding: str = "utf-8",
    sheet_name: str = "",
    *,
    pdf_as_single_text: bool = False,
) -> Dict[str, Any]: ...
```

- `pdf_as_single_text=False`（默认）：PDF 返回 `{"kind": "pages", "pages": [...]}` —— 适合需要逐页处理的 skill（慢病/大病审核）
- `pdf_as_single_text=True`：PDF 返回 `{"kind": "text", "text": "..."}` —— 适合把整份 PDF 当一段文本使用的 skill（复诊结构化/病历生成）

## 公开的工具函数

| 函数 | 说明 |
|------|------|
| `detect_input_type(path, explicit)` | 从文件后缀或显式参数推断输入类型 |
| `normalize_header(value)` | 去除空白/连字符，转小写，用于列名匹配 |
| `load_input_artifact(...)` | 主入口，返回 artifact dict |
| `extract_pdf_pages(path)` | 提取 PDF 各页文本，返回 `List[str]` |
| `extract_pdf_text(path)` | 提取 PDF 全文，返回 `str` |
| `extract_image_text(path)` | tesseract OCR，返回 `str` |

## 依赖

### 运行环境
- Python 3.7+

### Python 第三方包（可选，按输入格式需要）
| 包名 | 用途 | 必要条件 |
|------|------|---------|
| `openpyxl` | 读取 `.xlsx` | 输入为 xlsx 时必须 |
| `pypdf` | 提取 PDF 文本 | 输入为 pdf 时必须（或用 pdftotext 替代） |

安装：`pip install openpyxl pypdf`

### 外部工具（可选）
| 工具 | 用途 | 必要条件 |
|------|------|---------|
| LibreOffice (`soffice`) | 转换 `.doc` / `.xls` | 输入为 doc/xls 时必须 |
| `pdftotext`（poppler-utils） | 提取 PDF 文本 | 未安装 pypdf 时作为备选 |
| `tesseract`（含 chi_sim+eng） | 图片 OCR | 输入为图片时必须 |

安装（Ubuntu/Debian）：`sudo apt-get install libreoffice poppler-utils tesseract-ocr tesseract-ocr-chi-sim`

> 仅使用 JSON / txt 输入时，无需安装任何第三方包或外部工具。
