---
name: caesar-cipher
description: 凯撒密码加密、解密及暴力破解（fuzz）工具。当用户需要「凯撒加密」「凯撒解密」「凯撒暴力破解」「Caesar cipher」「移位密码」「fuzz凯撒」时使用。支持自定义移位值(1-25)和自动遍历所有偏移量。
---

# 凯撒密码工具 (Caesar Cipher)

## 概述

基于 Python 实现的凯撒密码（移位密码）工具，支持字母的加密、解密和暴力破解（遍历 1-25 所有偏移量）。仅处理英文字母（A-Z、a-z），非字母字符保持不变。

## 使用时机

- 用户需要凯撒密码加密/解密
- 用户说「凯撒暴力破解」「fuzz 凯撒」「遍历偏移量」
- 用户需要尝试所有可能的凯撒移位来破解密文

## 操作步骤

### 1. 调用加密/解密脚本

使用 `scripts/caesar.py`，支持三种模式：

```bash
# 加密（shift=3）
python3 scripts/caesar.py -m encrypt -s 3 "Hello World"

# 解密（shift=3）
python3 scripts/caesar.py -m decrypt -s 3 "Khoor Zruog"

# 暴力破解（遍历 1-25）
python3 scripts/caesar.py -m fuzz "Khoor Zruog"
```

### 2. 分析结果

- **加密/解密**：直接返回结果
- **暴力破解(fuzz)**：显示所有 25 个偏移量结果，供用户选择

## 命令参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `-m, --mode` | 模式：`encrypt` / `decrypt` / `fuzz` | `encrypt` |
| `-s, --shift` | 移位值 (1-25) | `3` |
| `text` | 待处理的文本（位置参数） | 必填 |

## 示例

```bash
# 加密
python3 scripts/caesar.py -m encrypt -s 5 "Attack at dawn"
# 输出: Fyyfhp fy ifbs

# 解密
python3 scripts/caesar.py -m decrypt -s 5 "Fyyfhp fy ifbs"
# 输出: Attack at dawn

# 暴力破解 fuzz
python3 scripts/caesar.py -m fuzz "Fyyfhp fy ifbs"
# Shift  1: Exxego ex hear
# Shift  2: Dwwdfn dw gdzq
# Shift  3: Cvvcem cv fcyp
# Shift  4: Buubdl bu ebxo
# Shift  5: Attack at dawn
# Shift  6: Zsszbj zs czvm
# ...
```

## Python API

```python
from scripts.caesar import encrypt, decrypt, fuzz

# 加密
result = encrypt("Hello World", shift=3)

# 解密
result = decrypt("Khoor Zruog", shift=3)

# 暴力破解（返回 [(偏移, 结果), ...]）
results = fuzz("Khoor Zruog")
for shift, text in results:
    print(f"Shift {shift:2d}: {text}")
```

## 注意事项

- 仅支持英文字母 (A-Z, a-z)，其他字符（数字、中文、标点等）保持不变
- 移位值范围为 1-25
- 字母大小写保持不变

## 验证

- [ ] 加密后再解密能还原原文
- [ ] fuzz 模式能正确遍历所有 25 个偏移量
- [ ] 非字母字符保持不变
- [ ] 大小写正确处理
