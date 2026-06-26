---
slug: cn-unicode-info
name: Unicode Info
version: "1.0.0"
description: "Get Unicode codepoint, name, and category for characters. Support Chinese characters, English text, emoji. Pure Python standard library, no API key required."
keywords: unicode, character, emoji, codepoint, chinese
license: MIT-0
tags:
  - tools
---

# Unicode Info

Look up detailed Unicode information for any character.

## Features

- Display Unicode codepoint in hex format
- Show Unicode character name
- List character category (Letter, Number, Punctuation, etc.)
- Support all Unicode characters including Chinese and emoji
- Pure Python, no external dependencies

## Usage

```
python3 scripts/unicode_info.py --text "你好世界🔧"
```

## Example Output

```json
{
  "chars": [
    {"char": "你", "codepoint": "0x4f60", "name": "CJK UNIFIED IDEOGRAPH-4F60", "category": "Lo"},
    {"char": "好", "codepoint": "0x597d", "name": "CJK UNIFIED IDEOGRAPH-597D", "category": "Lo"},
    {"char": "世", "codepoint": "0x4e16", "name": "CJK UNIFIED IDEOGRAPH-4E16", "category": "Lo"},
    {"char": "界", "codepoint": "0x754c", "name": "CJK UNIFIED IDEOGRAPH-754C", "category": "Lo"},
    {"char": "\U0001f527", "codepoint": "0x1f527", "name": "WRENCH", "category": "So"}
  ],
  "length": 5
}
```

## Use Cases

- Identify unknown characters or emoji
- Debug encoding issues
- Extract character properties for text processing

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
