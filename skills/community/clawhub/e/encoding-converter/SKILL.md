# encoding-converter

## 技能概述
多格式编码转换工具集。支持 Base64、URL 编码、HEX、MD5/SHA 哈希、JWT 解码、HTML 实体编码等常见编码格式的互转与校验。

## 何时使用
- 需要 Base64 编码/解码数据时
- 需要 URL encode/decode 文本时
- 需要计算文件或字符串的 MD5/SHA 哈希时
- 需要解码 JWT Token 查看 payload 时
- 需要 HTML 实体编码/解码时
- 需要进行进制转换（二进制/八进制/十进制/十六进制）时

## 使用方法

### 基础用法
```python
from scripts.encoding_engine import EncodingConverter

ec = EncodingConverter()

# Base64 编解码
encoded = ec.base64_encode("Hello World")
decoded = ec.base64_decode(encoded)

# URL 编码
url_encoded = ec.url_encode("你好 世界")

# MD5 / SHA256 哈希
md5_hash = ec.md5("secret data")
sha256_hash = ec.sha256("secret data")

# JWT 解码（不验证签名）
payload = ec.jwt_decode("eyJhbGciOiJIUzI1NiIs...")

# HTML 实体编码
html = ec.html_encode("<div>Hello & 你好</div>")

# 进制转换
hex_val = ec.to_hex(255)      # -> "ff"
bin_val = ec.to_binary(255)   # -> "11111111"
```

## 文件结构
```
encoding-converter/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   └── encoding_engine.py     # 核心引擎
├── examples/
│   └── basic_usage.py          # 使用示例
└── tests/
    └── test_encoding.py        # 单元测试
```

## 依赖
- Python 内置: `base64`, `urllib.parse`, `hashlib`, `html`, `json`, `binascii`
- 可选: `PyJWT` 用于 JWT 编码

## 标签
encoding, decoding, base64, hash, jwt, developer-tools, security