# 来源与提取

[English](formats.md)

需要 Python 3.10+。Agent 负责阅读材料和生成导师；提取脚本只处理文档内容。

| 格式 | 依赖 | 范围与限制 |
| --- | --- | --- |
| TXT、MD、Markdown | 标准库 | UTF-8 或 BOM 声明编码；不猜测未知编码 |
| HTML、HTM | 标准库 | 可见文本；不是网页截图或完整表格重建 |
| EPUB | 标准库 | OPF spine 阅读顺序；不处理 DRM 或提取插图 |
| DOCX | 标准库 | 正文段落与表格；复杂对象和图片需核对 |
| PDF / text | `pypdf` 或 `pdfminer.six` | 文字层；扫描件需另行 OCR |
| PDF / technical | 优先 `docling` | 降级为文本时告警；公式、表格需核对 |
| RTF | `striprtf` | 缺依赖明确失败，不采用吞字的正则回退 |

暂不支持 MOBI/AZW，先用合适工具转换；修改扩展名不等于转换格式。

```bash
python scripts/extract.py --check
python -m pip install pypdf striprtf  # 按实际格式安装
python -m pip install docling        # 可选：技术 PDF
python scripts/extract.py /path/to/book.pdf --mode text --workdir /path/to/extraction
```

输出 `full_text.txt` 与 `metadata.json`。退出码为 `success` / 0、`partial` / 2、`failed` / 1。混合输入保留成功部分，同时报告失败原因；生成导师时须标明实际覆盖。

`total_tokens` 是分段规划用的保守启发式估算，并非实际 tokenizer 数量、账单或严格上界。提取成功也不能保证图片、公式与语义完整。提取器的部分终端提示仍是中文，JSON 字段与状态值保持稳定。
