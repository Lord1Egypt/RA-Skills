# 文档处理参考资料

## API 文档

### Feishu Docs API
- https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYjN14SM7gTN

### Python 库文档
- python-docx: https://python-docx.readthedocs.io/
- openpyxl: https://openpyxl.readthedocs.io/
- pandas: https://pandas.pydata.org/docs/
- pdfplumber: https://github.com/jsvine/pdfplumber

## 格式规范

### Open XML 格式
- DOCX: Office Open XML (ECMA-376)
- XLSX: Office Open XML Spreadsheet
- PPTX: Office Open XML Presentation

### PDF 规范
- PDF 1.7 (ISO 32000-1)
- 使用 poppler-utils 进行文本提取

## 最佳实践

### 大文件处理
- 分块读取 >100MB 文件
- 使用流式处理避免内存溢出
- 设置合理的超时时间

### 错误处理
- 捕获依赖缺失错误
- 提供清晰的安装指引
- 优雅降级（功能不可用时）

## 常见问题

### Q: 为什么不支持 .doc 和 .xls？
A: 这些是旧的二进制格式，需要 LibreOffice 转换。建议先转换为 .docx/.xlsx。

### Q: PDF 写入支持吗？
A: 不支持。PDF 是只读格式。如需生成 PDF，可先创建 Word 文档再手动转换。

### Q: 如何处理超大 Excel 文件？
A: 使用 pandas 的 chunksize 参数分块读取：
```python
pd.read_excel('large.xlsx', sheet_name='Sheet1', chunksize=1000)
```
