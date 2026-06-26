# Document Processing Skill

## Description
文档处理技能，支持多格式文档转换、内容提取和批量处理。

## Features
- 📄 格式转换（PDF/Word/Excel/PPT）
- 🔍 内容提取（文本、表格、图片）
- ✏️ 批量处理（重命名、格式统一）
- 🤝 飞书集成（云文档同步）

## Dependencies
- Python 3.13+
- PyPDF2, python-docx, openpyxl
- pdfplumber, python-docx2txt

## Usage
```python
from document_processing import DocumentProcessor

# 初始化文档处理器
processor = DocumentProcessor()

# 转换PDF到Word
processor.convert_format("input.pdf", "output.docx")

# 提取PDF内容
content = processor.extract_content("document.pdf")

# 批量处理文档
processor.batch_process("./docs", ".docx", ".pdf")
```

## Integration with Feishu
- 文档自动同步到飞书云文档
- 内容提取结果自动保存到飞书多维表格
- 批量处理结果推送到飞书消息

## Configuration
```yaml
document_processing:
  temp_dir: "/tmp/document_processing"
  default_format: "docx"
  ocr_enabled: true
  ocr_api_key: "your_ocr_api_key"

feishu:
  doc_folder_token: "your_folder_token"
  bitable_app_token: "your_bitable_token"
  bitable_table_id: "your_table_id"
```