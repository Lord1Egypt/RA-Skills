---
slug: cn-password-generator-v2
name: Password Generator V2
version: "1.1.0"
description: "Generate cryptographically secure random passwords with customizable character sets. Control length, include/exclude character types. Pure Python, no API key required."
keywords: password, generator, random, secure, security
license: MIT-0
tags:
  - tools
---

# Password Generator V2

Generate strong, random passwords.

## Features

- Cryptographically secure random generation
- Customizable length (default: 16 characters)
- Toggle character types: uppercase, lowercase, digits, symbols
- Generate multiple passwords at once
- Pure Python, no external dependencies

## Character Types

- Uppercase: A-Z (26 characters)
- Lowercase: a-z (26 characters)
- Digits: 0-9 (10 characters)
- Symbols: !@#$%^&* (8 characters)

## Usage

```
# Default: 16 chars, all types
python3 scripts/pwd_gen_v2.py

# 24 chars, no symbols
python3 scripts/pwd_gen_v2.py --length 24 --no-symbols

# 5 passwords, 12 chars each
python3 scripts/pwd_gen_v2.py --length 12 --count 5

# Letters only (no digits, no symbols)
python3 scripts/pwd_gen_v2.py --length 20 --no-digits --no-symbols
```

## Example Output

```json
{
  "passwords": [
    "Kj8#mNp2$xL9@vQw7",
    "Rt4&fBc6%Yn3*Hs8j"
  ],
  "length": 16
}
```

## Security Notes

- Uses Python's `secrets` module for cryptographic randomness
- Suitable for generating passwords, API keys, tokens

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
