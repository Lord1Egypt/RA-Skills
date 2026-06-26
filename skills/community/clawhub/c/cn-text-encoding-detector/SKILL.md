---
slug: cn-text-encoding-detector
name: Text Encoding Detector
version: "1.0.0"
description: "Detect text file encoding (UTF-8, GBK, Latin-1, etc). Auto-detect BOM markers. Pure Python standard library, no API key required."
keywords: encoding, charset, utf-8, gbk, detect
license: MIT-0
tags:
  - tools
---

# Text Encoding Detector

Automatically detect the character encoding of text files.

## Features

- Support common Chinese encodings (UTF-8, GBK, GB2312)
- Detect BOM (Byte Order Mark) markers
- Report file size along with encoding
- Pure Python, no external dependencies

## Supported Encodings

- UTF-8 (with or without BOM)
- UTF-16 LE/BE
- GBK / GB2312
- Latin-1 / ISO-8859-1
- Unknown (when detection fails)

## Usage

```
python3 scripts/encoding_detector.py --file document.txt
```

## Example Output

```json
{
  "file": "document.txt",
  "encoding": "UTF-8",
  "size_bytes": 15234
}
```

## Use Cases

- Fix garbled text files
- Batch convert files between encodings
- Verify file encoding before processing

## Notes

Detection tries UTF-8 first, then GBK. If both fail, returns "UNKNOWN".

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
