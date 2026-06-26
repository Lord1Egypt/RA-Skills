# Encoding Converter

多格式编码转换工具 — 开发调试必备 Swiss Army Knife。

## Features

| 功能 | 说明 |
|------|------|
| Base64 | 编码 / 解码，支持 URL-safe 变体 |
| URL 编码 | encode / decode，支持空格处理 |
| HEX | 字符串与十六进制互转 |
| 哈希 | MD5, SHA1, SHA256, SHA512 |
| JWT 解码 | 解析 header + payload（不验证签名） |
| HTML 实体 | encode / decode |
| 进制转换 | 二/八/十/十六进制互转 |
| 随机生成 | UUID、随机字符串、随机十六进制 |

## Quick Start

```python
from scripts.encoding_engine import EncodingConverter

ec = EncodingConverter()

# Base64
ec.base64_encode("Hello")           # -> "SGVsbG8="
ec.base64_decode("SGVsbG8=")        # -> "Hello"

# URL
eq.url_encode("key=你好 world")      # -> "key%3D%E4%BD%A0%E5%A5%BD+world"

# 哈希
ec.md5("password")                  # -> "5f4dcc3b5aa765d61d8327deb882cf99"
ec.sha256("password")               # -> "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

# JWT 解码
ec.jwt_decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
# -> {"header": {"alg": "HS256", "typ": "JWT"}, "payload": {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}}

# 进制转换
ec.to_hex(255)                      # -> "ff"
ec.to_binary(255)                   # -> "11111111"
ec.hex_to_int("ff")                 # -> 255

# HTML
eq.html_encode("<script>")         # -> "&lt;script&gt;"

# 随机生成
ec.random_uuid()                    # -> "550e8400-e29b-41d4-a716-446655440000"
ec.random_hex(16)                   # -> "a3f7c9d2e8b1045f"
```

## Installation

```bash
pip install -r requirements.txt
```

纯 Python 内置模块实现，无需额外依赖即可运行核心功能。

## License
MIT