---
name: cn-hash-generator
version: "1.2.6"
description: "Generate MD5/SHA-1/SHA-256/SHA-512/BLAKE2b hashes, Base64 encode/decode, HMAC signatures."
metadata:
  openclaw:
    emoji: "#️⃣"
    category: developer_tools

Generate hashes and encode/decode Base64 strings.

## Features

- MD5, SHA-1, SHA-256, SHA-512, BLAKE2b hashes
- Base64 encode/decode
- HMAC signatures

## Usage

```bash
python3 scripts/hash_toolkit.py --string "Hello"
python3 scripts/hash_toolkit.py --string "Hello" --algo sha256
python3 scripts/hash_toolkit.py --string "SGVsbG8=" --decode
```

## Requirements

Python 3.7+ (stdlib only).

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
