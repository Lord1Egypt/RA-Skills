# 📖 Ebook Converter Pro

全功能電子書轉換工具箱，支援 EPUB / PDF / MOBI / AZW3 / FB2 的讀取、轉換、組織、元資料管理。

## 安裝

```bash
# 安裝依賴（macOS）
brew install poppler tesseract

# 安裝依賴（Ubuntu/Debian）
sudo apt install poppler-utils tesseract-ocr tesseract-ocr-chi-tra
```

## 快速開始

```bash
# EPUB → TXT
python3 scripts/epub_converter.py book.epub

# PDF → Markdown
python3 scripts/pdf_converter.py md book.pdf

# 批量轉換
python3 scripts/batch_converter.py ./books/ -f md -r --report
```

## 腳本總覽

| 腳本 | 功能 |
|------|------|
| `epub_converter.py` | EPUB 轉 TXT / MD / HTML / JSON，封面萃取 |
| `pdf_converter.py` | PDF 轉 TXT / MD / 圖片，OCR，分割/合併 |
| `batch_converter.py` | 多目錄批量轉換，並行 + 進度條 + 報告 |
| `ebook_metadata.py` | 元資料讀寫，BibTeX 書目匯出 |
| `ebook_organizer.py` | 圖書館自動分類（作者/格式）|

## 功能亮點

- 🐍 **純 Python**：無需 Calibre 或商業軟體
- ⚡ **批量並行**：多執行緒 + 進度條
- 📚 **作者分類**：從 EPUB 自動讀取作者元資料
- 🔗 **軟連結**：不移動原檔，保持書庫安全
- 📋 **轉換報告**：Markdown 格式，清楚記錄每次批次結果

## License

MIT
