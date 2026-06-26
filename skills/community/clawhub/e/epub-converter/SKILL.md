---
name: epub-converter
description: Convert EPUB ebooks between Traditional and Simplified Chinese. Use when: (1) user provides an EPUB file and asks to convert between Traditional/Simplified Chinese, (2) user mentions "繁简转换", "繁体转简体", "简体转繁体", "EPUB转换", (3) user wants to convert Chinese text encoding in ebook files. Supports bidirectional conversion (Traditional→Simplified and Simplified→Traditional).
---

# EPUB Chinese Converter

Convert EPUB ebooks between Traditional Chinese (繁體中文) and Simplified Chinese (简体中文).

## Quick Start

**Convert Traditional to Simplified (most common):**

```bash
python3 scripts/convert_epub.py <input.epub>
```

**Convert Simplified to Traditional:**

```bash
python3 scripts/convert_epub.py <input.epub> --direction s2t
```

**Specify output filename:**

```bash
python3 scripts/convert_epub.py <input.epub> -o <output.epub>
```

## How It Works

The script:

1. **Auto-installs dependencies** - Creates a virtual environment at `~/.openclaw/epub_venv` and installs `ebooklib` and `opencc-python-reimplemented` on first run
2. **Reads EPUB structure** - Parses the EPUB file using ebooklib
3. **Converts all text content** - Processes all HTML/XHTML documents inside the EPUB
4. **Converts metadata** - Updates book title and other metadata
5. **Fixes TOC structure** - Repairs any broken table of contents entries
6. **Saves new EPUB** - Writes a properly formatted EPUB file

## Conversion Directions

- `t2s` (default): Traditional → Simplified (繁體 → 简体)
- `s2t`: Simplified → Traditional (简体 → 繁體)

## Output Naming

If no output filename is specified:
- Traditional→Simplified: adds `_简体` suffix
- Simplified→Traditional: adds `_繁體` suffix

Example: `book.epub` → `book_简体.epub`

## Technical Details

**Dependencies:**
- `ebooklib` - EPUB file parsing and writing
- `opencc-python-reimplemented` - Chinese text conversion

**Conversion coverage:**
- All HTML/XHTML content files (chapters, cover, etc.)
- Book metadata (title, author, etc.)
- Table of contents entries

**Not converted:**
- Image files (covers, illustrations)
- CSS stylesheets
- Binary resources

## Troubleshooting

**If dependencies fail to install:**

```bash
# Manual installation
python3 -m venv ~/.openclaw/epub_venv
source ~/.openclaw/epub_venv/bin/activate
pip install ebooklib opencc-python-reimplemented
```

**If EPUB structure is corrupted:**

The script automatically fixes common issues:
- Missing TOC entry UIDs
- Malformed EPUB headers
- Encoding problems

**If conversion fails:**

Check that:
1. Input file is a valid EPUB (not PDF or other format)
2. File is not DRM-protected
3. File size is reasonable (<100MB recommended)

## Examples

**Basic conversion:**
```bash
python3 scripts/convert_epub.py "自我升级第一原理.epub"
# Output: 自我升级第一原理_简体.epub
```

**Custom output:**
```bash
python3 scripts/convert_epub.py input.epub -o simplified_version.epub
```

**Reverse conversion:**
```bash
python3 scripts/convert_epub.py simplified.epub --direction s2t
# Output: simplified_繁體.epub
```

## Success Indicators

When conversion succeeds, you'll see:
- ✅ Successfully read EPUB
- ✅ Successfully converted X documents
- 📝 Converted book title
- 🎉 Conversion complete!
- File size comparison

The output EPUB can be opened in any standard ebook reader (Apple Books, Calibre, etc.).
