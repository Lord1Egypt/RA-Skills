# 格式批量互转 · SkillHub 上架信息

**Skill 名称：** 格式批量互转
**副标题：** 一键批量转换，支持 CSV/Excel/JSON/PDF/Markdown
**分类：** 办公效率 > 文档处理 > 格式转换

---

## 功能详细描述

格式批量互转是一款强大的文件格式批量转换工具，支持 CSV、Excel（xlsx/xls）、JSON、PDF、Markdown 五种常用格式之间的互相转换。

### 核心功能

- **多格式支持** — 支持五种主流格式（CSV、Excel、JSON、PDF、Markdown）之间的互相转换
- **批量处理** — 支持多文件同时转换，并行处理加速
- **智能解析** — 自动识别文件编码，智能解析表格结构
- **PDF 文字识别** — 内置 OCR 功能，可从扫描版 PDF 中提取文字
- **飞书推送** — 转换完成后自动推送结果到飞书群聊
- **灵活配置** — YAML 配置文件，可自定义所有转换参数
- **命令行支持** — 支持 CLI 操作，方便自动化集成

### 适用场景

- 数据分析师批量处理不同格式的数据文件
- 运营人员导出/导入 Excel 与 CSV 数据
- 财务人员转换报表格式
- 开发者在不同数据格式间快速转换
- 文档工作者批量转换 Markdown 与 PDF

---

## 套餐说明

| 套餐   | 价格      | 功能说明                                              |
|--------|-----------|-------------------------------------------------------|
| FREE   | ¥0        | 每次最多 10 个文件，支持单一格式对转换               |
| STD    | ¥9.9/月   | 每次最多 100 个文件，全格式支持                      |
| PRO    | ¥29/月    | 文件数量无限制，开启 OCR 识别，支持飞书结果推送     |
| MAX    | ¥69/月    | PRO 全部功能 + API 接口调用权限 + 优先技术支持      |

---

## 技术要求

### Python 依赖

```
pandas>=2.0.0
openpyxl>=3.0.0
python-docx>=1.0.0
pytesseract>=0.3.10
pdf2image>=1.16.0
Pillow>=10.0.0
requests>=2.28.0
```

### 系统级依赖

**Tesseract OCR**（用于 PDF 文字识别）：
- Ubuntu/Debian: `sudo apt install tesseract-ocr tesseract-ocr-chi-sim`
- macOS: `brew install tesseract tesseract-lang`
- Windows: 从 [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装，并安装中文语言包

### 环境要求

- Python 3.8+
- 内存建议 4GB 以上（大文件处理时）
- 磁盘空间根据待处理文件大小而定

---

## 上架前清理命令

在提交上架前，请运行以下命令清理临时文件和测试数据：

```bash
# 清理 Python 缓存
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

# 清理 .pytest_cache
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# 清理 output 目录（如果有）
rm -rf ./output 2>/dev/null || true

# 清理测试生成的文件
find . -type f -name "*.tmp" -delete
find . -type f -name "test_*" -type f -delete 2>/dev/null || true

# 清理 config.yaml（如果包含敏感信息）
rm -f config.yaml 2>/dev/null || true

# 清理日志文件
find . -type f -name "*.log" -delete 2>/dev/null || true

# 清理 .DS_Store（macOS）
find . -type f -name ".DS_Store" -delete 2>/dev/null || true

# 最终确认没有多余文件
ls -la
```
