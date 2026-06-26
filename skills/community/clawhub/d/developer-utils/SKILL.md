# DevToolkit | 开发者工具箱

**English** | **中文**

A comprehensive developer toolkit - 80+ tools for encoding, formatting, time, regex, crypto, code generation, network, color, data conversion, and more.

一站式开发者常用工具集 - 80+ 工具涵盖编码转换、格式化、时间、正则、加密、代码生成、网络、颜色、数据转换等。

---

## Features | 功能

**English:**
- **Text Processing**: Statistics, case conversion (16 formats), diff, sort, dedupe, line numbering
- **Encoding**: Base64, URL, Unicode, HTML entity, Hex, JWT decode, Punycode
- **Formatting**: JSON, XML, YAML, TOML, INI, SQL, HTML format/beautify/minify
- **Time**: Timestamp, timezone, cron parser, date calculator, countdown
- **Regex**: Test, generate, explain, common patterns library
- **Crypto**: Hash (MD5/SHA/RIPEMD), AES/RSA encrypt, HMAC, BIP39, password generator & strength
- **Code**: UUID/ULID/NanoID, JSON to struct (Go/Rust/Python), QR code, ASCII art
- **Data**: CSV/JSON/XML/YAML converter, mock data generator
- **Network**: IP lookup, HTTP test, port check, user agent parser
- **Color**: HEX/RGB/HSL/CMYK conversion, palette generator
- **Number**: Base conversion (2-36), Roman numerals, unit converter
- **Unix**: Chmod calculator, file permissions, cron expressions
- **Finance**: IBAN validator, credit card validator, Luhn algorithm
- **Geo**: Coordinate converter (WGS84/GCJ02/BD09)

**中文:**
- **文本处理**：统计、大小写转换(16种格式)、差异对比、排序、去重、行号
- **编码转换**：Base64、URL、Unicode、HTML实体、Hex、JWT解码、Punycode
- **格式化工具**：JSON、XML、YAML、TOML、INI、SQL、HTML 格式化/压缩
- **时间工具**：时间戳转换、时区转换、Cron解析、日期计算、倒计时
- **正则工具**：测试、生成、解释、常用正则库
- **加密解密**：哈希(MD5/SHA/RIPEMD)、AES/RSA加解密、HMAC、BIP39、密码生成与强度检测
- **代码工具**：UUID/ULID/NanoID生成、JSON转结构体(Go/Rust/Python)、二维码、ASCII艺术
- **数据转换**：CSV/JSON/XML/YAML 互转、Mock数据生成
- **网络工具**：IP查询、HTTP测试、端口检测、UserAgent解析
- **颜色工具**：HEX/RGB/HSL/CMYK 转换、调色板生成
- **数字工具**：进制转换(2-36)、罗马数字、单位转换
- **Unix工具**：Chmod计算器、文件权限、Cron表达式
- **金融工具**：IBAN验证、信用卡验证、Luhn算法
- **地理工具**：坐标转换(WGS84/GCJ02/BD09)

---

## 1. Text Processing Tools | 文本处理工具

### Text Statistics | 文本统计

**English:**
```bash
# Comprehensive text statistics
python3 << 'EOF'
import re

text = "Hello World 你好世界 123"

stats = {
    "Total characters": len(text),
    "Characters (no spaces)": len(text.replace(" ", "")),
    "Words": len(re.findall(r'[a-zA-Z]+|[\u4e00-\u9fff]', text)),
    "Lines": text.count('\n') + 1,
    "Chinese chars": len(re.findall(r'[\u4e00-\u9fff]', text)),
    "English chars": len(re.findall(r'[a-zA-Z]', text)),
    "Digits": len(re.findall(r'\d', text)),
    "Punctuation": len(re.findall(r'[^\w\s\u4e00-\u9fff]', text)),
}

for k, v in stats.items():
    print(f"{k}: {v}")
EOF
```

**中文:**
```bash
# 文本统计
python3 << 'EOF'
import re

text = "Hello World 你好世界 123"

stats = {
    "总字符数": len(text),
    "字符数(不含空格)": len(text.replace(" ", "")),
    "单词数": len(re.findall(r'[a-zA-Z]+|[\u4e00-\u9fff]', text)),
    "行数": text.count('\n') + 1,
    "中文字符": len(re.findall(r'[\u4e00-\u9fff]', text)),
    "英文字符": len(re.findall(r'[a-zA-Z]', text)),
    "数字": len(re.findall(r'\d', text)),
    "标点符号": len(re.findall(r'[^\w\s\u4e00-\u9fff]', text)),
}

for k, v in stats.items():
    print(f"{k}: {v}")
EOF
```

---

### Case Conversion | 大小写转换

**English:**
```bash
# 16 case formats supported
python3 << 'EOF'
text = "hello world example"

conversions = {
    "UPPERCASE": text.upper(),
    "lowercase": text.lower(),
    "Title Case": text.title(),
    "Sentence case": text.capitalize(),
    "camelCase": ''.join(word.capitalize() if i else word for i, word in enumerate(text.split())),
    "PascalCase": ''.join(word.capitalize() for word in text.split()),
    "snake_case": text.replace(' ', '_').lower(),
    "kebab-case": text.replace(' ', '-').lower(),
    "CONSTANT_CASE": text.replace(' ', '_').upper(),
    "dot.case": text.replace(' ', '.').lower(),
    "path/case": text.replace(' ', '/').lower(),
    "Train-Case": '-'.join(word.capitalize() for word in text.split()),
}

for name, result in conversions.items():
    print(f"{name}: {result}")
EOF
```

**中文:**
```bash
# 支持16种大小写格式
python3 << 'EOF'
text = "hello world example"

conversions = {
    "大写": text.upper(),# HELLO WORLD EXAMPLE
    "小写": text.lower(),# hello world example
    "标题": text.title(),# Hello World Example
    "驼峰": ''.join(word.capitalize() if i else word for i, word in enumerate(text.split())),  # helloWorldExample
    "帕斯卡": ''.join(word.capitalize() for word in text.split()),  # HelloWorldExample
    "蛇形": text.replace(' ', '_').lower(),  # hello_world_example
    "短横线": text.replace(' ', '-').lower(),  # hello-world-example
    "常量": text.replace(' ', '_').upper(),  # HELLO_WORLD_EXAMPLE
}

for name, result in conversions.items():
    print(f"{name}: {result}")
EOF
```

---

### Text Diff | 文本差异对比

**English:**
```bash
# Compare two texts line by line
python3 << 'EOF'
import difflib

text1 = """Hello World
Line 2
Line 3
Old Line"""

text2 = """Hello World
Line 2 modified
Line 3
New Line"""

diff = difflib.unified_diff(
    text1.splitlines(keepends=True),
    text2.splitlines(keepends=True),
    fromfile='original',
    tofile='modified'
)

print(''.join(diff))
EOF
```

---

## 2. Encoding Tools | 编码转换工具

### Base64 Encode/Decode | Base64 编解码

**English:**
```bash
# Encode
echo -n "hello" | base64
# Output: aGVsbG8=

# Decode
echo "aGVsbG8=" | base64 -d
# Output: hello
```

**中文:**
```bash
# 编码
echo -n "你好" | base64
# 输出: 5L2g5aW9

# 解码
echo "5L2g5aW9" | base64 -d
# 输出: 你好
```

---

### URL Encode/Decode | URL 编解码

**English:**
```bash
# Encode (Python)
python3 -c "import urllib.parse; print(urllib.parse.quote('hello world'))"
# Output: hello%20world

# Decode
python3 -c "import urllib.parse; print(urllib.parse.unquote('hello%20world'))"
# Output: hello world
```

---

### Hex Encode/Decode | 十六进制编解码

**English:**
```bash
# Text to Hex
python3 -c "print('hello'.encode().hex())"
# Output: 68656c6c6f

# Hex to Text
python3 -c "print(bytes.fromhex('68656c6c6f').decode())"
# Output: hello
```

---

### JWT Decode | JWT 解码

**English:**
```bash
# Decode JWT token
python3 << 'EOF'
import json
import base64

jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

def decode_base64url(data):
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

header, payload, signature = jwt.split('.')
print("Header:", json.loads(decode_base64url(header)))
print("Payload:", json.loads(decode_base64url(payload)))
print("Signature:", signature)
EOF
```

---

## 3. Formatting Tools | 格式化工具

### JSON Format | JSON 格式化

**English:**
```bash
# Format JSON
echo '{"name":"john","age":30}' | python3 -m json.tool

# Compact JSON
echo '{"name": "john", "age": 30}' | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin),separators=(',',':')))"

# Validate JSON
echo '{"name":"john"}' | python3 -c "import json,sys; json.load(sys.stdin); print('Valid JSON')"
```

---

### Config Format Conversion | 配置格式转换

**English:**
```bash
# JSON to YAML
python3 -c "import json,yaml,sys; print(yaml.dump(json.load(sys.stdin), allow_unicode=True))" <<< '{"name":"john","age":30}'

# YAML to JSON
python3 -c "import json,yaml,sys; print(json.dumps(yaml.safe_load(sys.stdin)))" <<< 'name: john'

# JSON to TOML (requires toml library)
python3 << 'EOF'
import json

def json_to_toml(data, indent=0):
    result = []
    for key, value in data.items():
        if isinstance(value, dict):
            result.append(f"{'  ' * indent}[{key}]")
            result.append(json_to_toml(value, indent + 1))
        elif isinstance(value, str):
            result.append(f"{'  ' * indent}{key} = \"{value}\"")
        elif isinstance(value, bool):
            result.append(f"{'  ' * indent}{key} = {str(value).lower()}")
        else:
            result.append(f"{'  ' * indent}{key} = {value}")
    return '\n'.join(result)

data = {"name": "john", "age": 30, "settings": {"theme": "dark"}}
print(json_to_toml(data))
EOF
```

---

### SQL Format | SQL 格式化

**English:**
```bash
# Basic SQL formatting
python3 << 'EOF'
sql = "SELECT id,name,email FROM users WHERE age>18 AND status='active' ORDER BY created_at DESC LIMIT 10"

keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'ON']

formatted = sql
for kw in keywords:
    formatted = formatted.replace(f' {kw} ', f'\n{kw} ')

print(formatted)
EOF
```

---

## 4. Time Tools | 时间工具

### Timestamp Conversion | 时间戳转换

**English:**
```bash
# Current timestamp (seconds)
date +%s

# Current timestamp (milliseconds)
echo $(($(date +%s) * 1000))

# Timestamp to datetime (macOS)
date -r 1710489600
# Linux: date -d @1710489600

# Datetime to timestamp (macOS)
date -j -f "%Y-%m-%d %H:%M:%S" "2024-03-15 12:00:00" +%s
# Linux: date -d "2024-03-15 12:00:00" +%s

# ISO 8601 format
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

---

### Cron Parser | Cron 解析器

**English:**
```bash
# Parse cron expression
python3 << 'EOF'
from datetime import datetime, timedelta
import re

def parse_cron(expr):
    parts = expr.split()
    if len(parts) < 5:
        return "Invalid cron expression"
    
    minute, hour, day, month, weekday = parts[:5]
    
    descriptions = {
        'minute': minute if minute != '*' else 'every minute',
        'hour': hour if hour != '*' else 'every hour',
        'day': day if day != '*' else 'every day',
        'month': month if month != '*' else 'every month',
    }
    
    return f"Runs at minute {descriptions['minute']}, hour {descriptions['hour']}, on day {descriptions['day']} of {descriptions['month']}"

print(parse_cron("0 9 * * 1-5"))  # Every weekday at 9 AM
print(parse_cron("*/15 * * * *"))  # Every 15 minutes
EOF
```

---

## 5. Regex Tools | 正则工具

### Regex Templates | 常用正则模板

**English:**
```markdown
| Pattern | Regex |
|---------|-------|
| Email | `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` |
| Phone (CN) | `^1[3-9]\d{9}$` |
| URL | `^https?://[\w\-]+(\.[\w\-]+)+[/#?]?.*$` |
| IP (IPv4) | `^(\d{1,3}\.){3}\d{1,3}$` |
| Date | `^\d{4}-\d{2}-\d{2}$` |
| Time | `^\d{2}:\d{2}:\d{2}$` |
| Hex Color | `^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$` |
| Username | `^[a-zA-Z][a-zA-Z0-9_]{2,15}$` |
| Password (strong) | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$` |
| Credit Card | `^\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}$` |
| Chinese | `^[\u4e00-\u9fa5]+$` |
| ID Card (CN) | `^\d{17}[\dXx]$` |
```

---

### Regex Test | 正则测试

**English:**
```bash
# Test regex pattern
python3 << 'EOF'
import re

pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
test_strings = ['test@example.com', 'invalid-email', 'user.name@domain.co.uk']

for s in test_strings:
    result = '✓ Match' if re.match(pattern, s) else '✗ No match'
    print(f"{s}: {result}")
EOF
```

---

## 6. Crypto Tools | 加密解密工具

### Hash Functions | 哈希函数

**English:**
```bash
# MD5
echo -n "hello" | md5
# Output: 5d41402abc4b2a76b9719d911017c592

# SHA1
echo -n "hello" | shasum -a 1
# Output: aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d

# SHA256
echo -n "hello" | shasum -a 256
# Output: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

# SHA512
echo -n "hello" | shasum -a 512

# RIPEMD160 (Python)
python3 -c "import hashlib; print(hashlib.new('ripemd160', b'hello').hexdigest())"
```

---

### Password Generator | 密码生成器

**English:**
```bash
# Generate random password (16 chars)
openssl rand -base64 12

# Generate strong password
python3 << 'EOF'
import secrets
import string

def generate_password(length=16, include_upper=True, include_lower=True, include_digits=True, include_special=True):
    chars = ''
    if include_upper: chars += string.ascii_uppercase
    if include_lower: chars += string.ascii_lowercase
    if include_digits: chars += string.digits
    if include_special: chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    return ''.join(secrets.choice(chars) for _ in range(length))

print("Password:", generate_password(20))
print("PIN:", generate_password(6, False, False, True, False))
EOF
```

---

### Password Strength Checker | 密码强度检测

**English:**
```bash
# Check password strength with detailed analysis
python3 << 'EOF'
import re

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length checks
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ At least 8 characters recommended")
    
    if len(password) >= 12:
        score += 1
    
    if len(password) >= 16:
        score += 1
    
    # Character type checks
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("❌ Add lowercase letters")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("❌ Add uppercase letters")
    
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("❌ Add numbers")
    
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        score += 2
    else:
        feedback.append("❌ Add special characters")
    
    # Common pattern checks
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        feedback.append("⚠️ Avoid repeated characters")
    
    if re.search(r'(123|abc|qwe|password|admin)', password.lower()):
        score -= 2
        feedback.append("⚠️ Avoid common patterns")
    
    # Entropy calculation
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'\d', password): charset_size += 10
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password): charset_size += 32
    
    import math
    entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
    
    # Determine strength level
    if score >= 8:
        level = "🟢 Very Strong"
        crack_time = "Centuries"
    elif score >= 6:
        level = "🟢 Strong"
        crack_time = "Years"
    elif score >= 4:
        level = "🟡 Medium"
        crack_time = "Days to Weeks"
    elif score >= 2:
        level = "🟠 Weak"
        crack_time = "Hours to Days"
    else:
        level = "🔴 Very Weak"
        crack_time = "Seconds to Minutes"
    
    return {
        "password": password[:3] + "*" * (len(password) - 3),
        "score": f"{score}/10",
        "level": level,
        "entropy": f"{entropy:.1f} bits",
        "crack_time": crack_time,
        "feedback": feedback if feedback else ["✅ All checks passed!"]
    }

# Example usage
passwords = ["password", "Password1", "P@ssw0rd!2024", "Tr0ub4dor&3Horse!"]
for pwd in passwords:
    result = check_password_strength(pwd)
    print(f"\n{'='*40}")
    print(f"Password: {result['password']}")
    print(f"Strength: {result['level']} ({result['score']})")
    print(f"Entropy: {result['entropy']}")
    print(f"Crack Time: {result['crack_time']}")
    print("Feedback:")
    for f in result['feedback']:
        print(f"  {f}")
EOF
```

**中文:**
```bash
# 密码强度检测与详细分析
python3 << 'EOF'
import re

def check_password_strength(password):
    score = 0
    feedback = []
    
    # 长度检测
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ 建议至少8个字符")
    
    if len(password) >= 12:
        score += 1
    
    if len(password) >= 16:
        score += 1
    
    # 字符类型检测
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("❌ 添加小写字母")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("❌ 添加大写字母")
    
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("❌ 添加数字")
    
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        score += 2
    else:
        feedback.append("❌ 添加特殊字符")
    
    # 常见模式检测
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        feedback.append("⚠️ 避免重复字符")
    
    if re.search(r'(123|abc|qwe|password|admin)', password.lower()):
        score -= 2
        feedback.append("⚠️ 避免常见模式")
    
    # 计算熵值
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'\d', password): charset_size += 10
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password): charset_size += 32
    
    import math
    entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
    
    # 强度等级
    if score >= 8:
        level = "🟢 非常强"
        crack_time = "数百年"
    elif score >= 6:
        level = "🟢 强"
        crack_time = "数年"
    elif score >= 4:
        level = "🟡 中等"
        crack_time = "数天到数周"
    elif score >= 2:
        level = "🟠 弱"
        crack_time = "数小时到数天"
    else:
        level = "🔴 非常弱"
        crack_time = "数秒到数分钟"
    
    return {
        "password": password[:3] + "*" * (len(password) - 3),
        "score": f"{score}/10",
        "level": level,
        "entropy": f"{entropy:.1f} 位",
        "crack_time": crack_time,
        "feedback": feedback if feedback else ["✅ 所有检测通过！"]
    }

# 示例
passwords = ["123456", "Password123", "P@ssw0rd!2024", "Tr0ub4dor&3Horse!"]
for pwd in passwords:
    result = check_password_strength(pwd)
    print(f"\n{'='*40}")
    print(f"密码: {result['password']}")
    print(f"强度: {result['level']} ({result['score']})")
    print(f"熵值: {result['entropy']}")
    print(f"破解时间: {result['crack_time']}")
    print("建议:")
    for f in result['feedback']:
        print(f"  {f}")
EOF
```

---

### BIP39 Mnemonic | BIP39 助记词

**English:**
```bash
# Generate BIP39 mnemonic (requires mnemonic library)
python3 << 'EOF'
import os
import hashlib

# Simple 12-word mnemonic generator (simplified)
words = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
    "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid"
    # ... full wordlist would be 2048 words
]

# Generate random entropy
entropy = os.urandom(16)
entropy_hash = hashlib.sha256(entropy).digest()

# For demo, just show random selection
import random
mnemonic = ' '.join(random.choice(words) for _ in range(12))
print("Mnemonic (demo):", mnemonic)
print("Note: Use proper BIP39 library for production")
EOF
```

---

## 7. Code Tools | 代码工具

### UUID/ULID Generator | UUID/ULID 生成器

**English:**
```bash
# Generate UUID v4
uuidgen

# Generate UUID v7 (time-ordered, Python)
python3 << 'EOF'
import time
import random

def uuid_v7():
    ts = int(time.time() * 1000)
    rand = random.getrandbits(74)
    return f"{ts:012x}-{random.getrandbits(16):04x}-7{random.getrandbits(12):03x}-{random.getrandbits(2):02x}{random.getrandbits(12):03x}-{random.getrandbits(48):012x}"

print("UUID v7:", uuid_v7())
EOF

# Generate ULID
python3 << 'EOF'
import time
import random

def ulid():
    ts = int(time.time() * 1000)
    rand = random.getrandbits(80)
    chars = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
    result = ''
    
    # Encode timestamp (10 chars)
    for _ in range(10):
        result = chars[ts % 32] + result
        ts //= 32
    
    # Encode randomness (16 chars)
    for _ in range(16):
        result += chars[rand % 32]
        rand //= 32
    
    return result

print("ULID:", ulid())
EOF
```

---

### JSON to Struct | JSON 转结构体

**English:**
```bash
# JSON to Go struct
python3 << 'EOF'
import json

json_str = '{"name": "john", "age": 30, "email": "john@example.com", "active": true}'
data = json.loads(json_str)

type_map = {str: "string", int: "int", float: "float64", bool: "bool", list: "[]interface{}", dict: "map[string]interface{}"}

print("type User struct {")
for key, value in data.items():
    go_type = type_map.get(type(value), "interface{}")
    print(f"    {key.capitalize()} {go_type} `json:\"{key}\"`")
print("}")
EOF

# Output:
# type User struct {
#     Name string `json:"name"`
#     Age int `json:"age"`
#     Email string `json:"email"`
#     Active bool `json:"active"`
# }
```

---

## 8. Network Tools | 网络工具

### IP Lookup | IP 查询

**English:**
```bash
# Get public IP
curl -s ifconfig.me

# Get IP details
curl -s ipinfo.io

# Get IP location
curl -s "http://ip-api.com/json/"

# DNS lookup
nslookup google.com
dig google.com
```

---

### HTTP Request Test | HTTP 请求测试

**English:**
```bash
# GET request
curl -s https://api.github.com

# POST request
curl -X POST -H "Content-Type: application/json" -d '{"name":"test"}' https://httpbin.org/post

# With headers
curl -H "Authorization: Bearer token" https://api.example.com

# Check response time
curl -w "Time: %{time_total}s\n" -o /dev/null -s https://google.com

# Check HTTP status
curl -s -o /dev/null -w "%{http_code}" https://google.com
```

---

### Port Check | 端口检测

**English:**
```bash
# Check if port is open
nc -zv localhost 8080

# Scan multiple ports
nc -zv localhost 80 443 8080 3000

# Check remote port
nc -zv google.com 443
```

---

## 9. Color Tools | 颜色工具

### Color Conversion | 颜色转换

**English:**
```bash
# Color format conversion
python3 << 'EOF'
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    max_c, min_c = max(r, g, b), min(r, g, b)
    l = (max_c + min_c) / 2
    
    if max_c == min_c:
        h = s = 0
    else:
        d = max_c - min_c
        s = d / (2 - max_c - min_c)
        if max_c == r: h = (g - b) / d + (g < b) * 6
        elif max_c == g: h = (b - r) / d + 2
        else: h = (r - g) / d + 4
        h /= 6
    
    return round(h * 360), round(s * 100), round(l * 100)

# Example
hex_color = "#FF5733"
r, g, b = hex_to_rgb(hex_color)
h, s, l = rgb_to_hsl(r, g, b)

print(f"HEX: {hex_color}")
print(f"RGB: rgb({r}, {g}, {b})")
print(f"HSL: hsl({h}, {s}%, {l}%)")
EOF
```

---

## 10. Number Tools | 数字工具

### Base Conversion | 进制转换

**English:**
```bash
# Base conversion
python3 << 'EOF'
def convert_base(num, from_base, to_base):
    # Convert to decimal first
    if isinstance(num, str):
        decimal = int(num, from_base)
    else:
        decimal = num
    
    # Convert to target base
    if to_base == 10:
        return str(decimal)
    
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while decimal > 0:
        result = digits[decimal % to_base] + result
        decimal //= to_base
    
    return result or "0"

# Examples
print("Binary to Decimal:", convert_base("1010", 2, 10))  # 10
print("Decimal to Hex:", convert_base(255, 10, 16))  # FF
print("Hex to Binary:", convert_base("FF", 16, 2))  # 11111111
print("Decimal to Octal:", convert_base(64, 10, 8))  # 100
EOF
```

---

### Roman Numerals | 罗马数字

**English:**
```bash
# Roman numeral conversion
python3 << 'EOF'
def int_to_roman(num):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    result = ""
    for i, v in enumerate(val):
        while num >= v:
            result += syms[i]
            num -= v
    return result

def roman_to_int(roman):
    val = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = 0
    for i in range(len(roman)):
        if i > 0 and val[roman[i]] > val[roman[i-1]]:
            result += val[roman[i]] - 2 * val[roman[i-1]]
        else:
            result += val[roman[i]]
    return result

print("2024 →", int_to_roman(2024))  # MMXXIV
print("MMXXIV →", roman_to_int("MMXXIV"))  # 2024
EOF
```

---

## 11. QR Code Tools | 二维码工具

### QR Code Generator | 二维码生成器

**English:**
```bash
# Generate QR code with auto-install if needed
python3 << 'EOF'
import subprocess
import sys

def ensure_qrencode():
    """Ensure qrencode is installed, auto-install if not"""
    result = subprocess.run(['which', 'qrencode'], capture_output=True)
    if result.returncode == 0:
        return True
    
    print("📦 qrencode not found. Installing...")
    subprocess.run(['brew', 'install', 'qrencode'])
    
    # Verify installation
    result = subprocess.run(['which', 'qrencode'], capture_output=True)
    return result.returncode == 0

def generate_qr(text, output_file=None):
    """Generate QR code"""
    if output_file:
        subprocess.run(['qrencode', '-o', output_file, text])
        print(f"✅ QR code saved to {output_file}")
    else:
        subprocess.run(['qrencode', '-t', 'UTF8'], input=text.encode())

# Main
text = "https://example.com"  # Replace with actual content

if ensure_qrencode():
    print(f"Generating QR code for: {text}")
    generate_qr(text)
EOF
```

**中文:**
```bash
# 生成二维码（自动安装依赖）
python3 << 'EOF'
import subprocess

def ensure_qrencode():
    """确保 qrencode 已安装，未安装则自动安装"""
    result = subprocess.run(['which', 'qrencode'], capture_output=True)
    if result.returncode == 0:
        return True
    
    print("📦 qrencode 未安装，正在自动安装...")
    subprocess.run(['brew', 'install', 'qrencode'])
    
    result = subprocess.run(['which', 'qrencode'], capture_output=True)
    return result.returncode == 0

text = "https://example.com"
if ensure_qrencode():
    print(f"正在生成二维码: {text}")
    subprocess.run(['qrencode', '-t', 'UTF8'], input=text.encode())
EOF
```

---

### QR Code Reader | 二维码解析

**English:**
```bash
# Decode QR code with auto-install
python3 << 'EOF'
import subprocess

def ensure_zbar():
    """Ensure zbar is installed"""
    result = subprocess.run(['which', 'zbarimg'], capture_output=True)
    if result.returncode == 0:
        return True
    print("📦 zbar not found. Installing...")
    subprocess.run(['brew', 'install', 'zbar'])
    return True

if ensure_zbar():
    subprocess.run(['zbarimg', 'qrcode.png'])
EOF
```

---

## 12. Mock Data Generator | Mock 数据生成器

### Generate Test Data | 生成测试数据

**English:**
```bash
# Generate mock user data
python3 << 'EOF'
import random
import string
import json
from datetime import datetime, timedelta

def generate_name():
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_email(name):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
    return f"{name.lower().replace(' ', '.')}@{random.choice(domains)}"

def generate_phone():
    return f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_date(start_year=1990, end_year=2005):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_address():
    streets = ["Main St", "Oak Ave", "Pine Rd", "Maple Dr", "Cedar Ln"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    states = ["NY", "CA", "IL", "TX", "AZ"]
    return {
        "street": f"{random.randint(100, 9999)} {random.choice(streets)}",
        "city": random.choice(cities),
        "state": random.choice(states),
        "zip": f"{random.randint(10000, 99999)}"
    }

def generate_user():
    name = generate_name()
    return {
        "id": random.randint(1000, 9999),
        "name": name,
        "email": generate_email(name),
        "phone": generate_phone(),
        "birth_date": generate_date(),
        "address": generate_address(),
        "active": random.choice([True, False])
    }

# Generate multiple users
users = [generate_user() for _ in range(5)]
print(json.dumps(users, indent=2))
EOF
```

**中文:**
```bash
# 生成中文测试数据
python3 << 'EOF'
import random
import json

def generate_chinese_name():
    surnames = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴"]
    given_names = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军"]
    return f"{random.choice(surnames)}{random.choice(given_names)}"

def generate_phone_cn():
    prefixes = ["130", "131", "132", "133", "135", "136", "137", "138", "139",
                "150", "151", "152", "153", "155", "156", "157", "158", "159",
                "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
    return f"{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generate_id_card_cn():
    # 简化版身份证号生成
    area_codes = ["110101", "310101", "440101", "330101", "320101"]
    area = random.choice(area_codes)
    year = random.randint(1960, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    seq = random.randint(1, 999)
    return f"{area}{year}{month:02d}{day:02d}{seq:03d}"

def generate_address_cn():
    provinces = ["北京市", "上海市", "广东省", "浙江省", "江苏省"]
    cities = ["朝阳区", "浦东新区", "天河区", "西湖区", "鼓楼区"]
    streets = ["中山路", "人民路", "建设路", "解放路", "和平路"]
    return f"{random.choice(provinces)}{random.choice(cities)}{random.choice(streets)}{random.randint(1, 999)}号"

def generate_user_cn():
    name = generate_chinese_name()
    return {
        "id": random.randint(10000, 99999),
        "姓名": name,
        "手机": generate_phone_cn(),
        "身份证": generate_id_card_cn(),
        "地址": generate_address_cn(),
        "状态": random.choice(["活跃", "沉默", "流失"])
    }

# 生成多条数据
users = [generate_user_cn() for _ in range(5)]
print(json.dumps(users, indent=2, ensure_ascii=False))
EOF
```

---

### Generate Mock API Response | 生成 Mock API 响应

**English:**
```bash
# Generate REST API mock response
python3 << 'EOF'
import json
import random
from datetime import datetime, timedelta

def mock_api_response(endpoint, count=10):
    responses = {
        "/users": lambda: [
            {"id": i, "name": f"User {i}", "email": f"user{i}@example.com", "role": random.choice(["admin", "user", "guest"])}
            for i in range(1, count + 1)
        ],
        "/products": lambda: [
            {"id": i, "name": f"Product {i}", "price": round(random.uniform(10, 1000), 2), "stock": random.randint(0, 100)}
            for i in range(1, count + 1)
        ],
        "/orders": lambda: [
            {
                "id": f"ORD-{random.randint(10000, 99999)}",
                "user_id": random.randint(1, 100),
                "total": round(random.uniform(50, 500), 2),
                "status": random.choice(["pending", "processing", "shipped", "delivered"]),
                "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
            }
            for _ in range(count)
        ]
    }
    
    data = responses.get(endpoint, lambda: {"error": "Unknown endpoint"})()
    
    return {
        "endpoint": endpoint,
        "timestamp": datetime.now().isoformat(),
        "count": len(data) if isinstance(data, list) else 1,
        "data": data
    }

# Example usage
for endpoint in ["/users", "/products", "/orders"]:
    response = mock_api_response(endpoint, count=3)
    print(f"\n=== {endpoint} ===")
    print(json.dumps(response, indent=2)[:500] + "...")
EOF
```

---

## 13. Data Format Converter | 数据格式转换器

### CSV ↔ JSON ↔ XML ↔ YAML Conversion

**English:**
```bash
# Multi-format data converter
python3 << 'EOF'
import json
import csv
import io

def csv_to_json(csv_string):
    reader = csv.DictReader(io.StringIO(csv_string))
    return list(reader)

def json_to_csv(json_data):
    if not json_data:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=json_data[0].keys())
    writer.writeheader()
    writer.writerows(json_data)
    return output.getvalue()

def json_to_xml(json_data, root="root"):
    def dict_to_xml(d, parent="item"):
        xml = ""
        for key, value in d.items():
            if isinstance(value, dict):
                xml += f"<{key}>{dict_to_xml(value, key)}</{key}>"
            elif isinstance(value, list):
                for item in value:
                    xml += f"<{key}>{dict_to_xml(item, key) if isinstance(item, dict) else item}</{key}>"
            else:
                xml += f"<{key}>{value}</{key}>"
        return xml
    
    if isinstance(json_data, list):
        items = "".join(f"<item>{dict_to_xml(item)}</item>" for item in json_data)
        return f"<{root}>{items}</{root}>"
    return f"<{root}>{dict_to_xml(json_data)}</{root}>"

def json_to_yaml(json_data, indent=0):
    yaml = ""
    prefix = "  " * indent
    
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, (dict, list)):
                yaml += f"{prefix}{key}:\n{json_to_yaml(value, indent + 1)}"
            else:
                yaml += f"{prefix}{key}: {repr(value) if isinstance(value, str) else value}\n"
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, dict):
                yaml += f"{prefix}-\n{json_to_yaml(item, indent + 1)}"
            else:
                yaml += f"{prefix}- {item}\n"
    else:
        yaml += f"{prefix}{json_data}\n"
    
    return yaml

# Example data
csv_data = """name,age,city
Alice,30,New York
Bob,25,Los Angeles
Charlie,35,Chicago"""

# Convert CSV to JSON
json_data = csv_to_json(csv_data)
print("=== CSV to JSON ===")
print(json.dumps(json_data, indent=2))

# Convert JSON to XML
print("\n=== JSON to XML ===")
print(json_to_xml(json_data, "users"))

# Convert JSON to YAML
print("\n=== JSON to YAML ===")
print(json_to_yaml(json_data))
EOF
```

**中文:**
```bash
# 多格式数据转换
python3 << 'EOF'
import json

# CSV 转 JSON
csv_data = """姓名,年龄,城市
张三,28,北京
李四,32,上海
王五,25,广州"""

import csv, io
reader = csv.DictReader(io.StringIO(csv_data))
json_result = list(reader)
print("CSV → JSON:")
print(json.dumps(json_result, indent=2, ensure_ascii=False))

# JSON 转 CSV
output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=json_result[0].keys())
writer.writeheader()
writer.writerows(json_result)
print("\nJSON → CSV:")
print(output.getvalue())
EOF
```

---

## 14. Coordinate Converter | 坐标转换工具

### WGS84 ↔ GCJ02 ↔ BD09 Conversion

**English:**
```bash
# Coordinate system conversion (China specific)
python3 << 'EOF'
import math

# WGS84 (GPS) ↔ GCJ02 (China Mars coordinate) ↔ BD09 (Baidu coordinate)

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323

def out_of_china(lng, lat):
    return not (73.66 < lng < 135.05 and 3.86 < lat < 53.55)

def transform_lat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def transform_lng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def wgs84_to_gcj02(lng, lat):
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return mglng, mglat

def gcj02_to_bd09(lng, lat):
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return bd_lng, bd_lat

def bd09_to_gcj02(lng, lat):
    x = lng - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return gg_lng, gg_lat

def gcj02_to_wgs84(lng, lat):
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat

# Example: Beijing Tiananmen
wgs84 = (116.391243, 39.907511)  # GPS coordinate
gcj02 = wgs84_to_gcj02(*wgs84)   # China Mars coordinate
bd09 = gcj02_to_bd09(*gcj02)     # Baidu coordinate

print(f"WGS84 (GPS):     {wgs84}")
print(f"GCJ02 (Mars):    {gcj02}")
print(f"BD09 (Baidu):    {bd09}")
print(f"\nReverse BD09 → WGS84: {gcj02_to_wgs84(*bd09_to_gcj02(*bd09))}")
EOF
```

**中文:**
```bash
# 坐标系转换（中国特有）
# WGS84 (GPS原始坐标) ↔ GCJ02 (火星坐标/国测局坐标) ↔ BD09 (百度坐标)

python3 << 'EOF'
# 使用上面的代码...

# 示例：北京天安门
print("北京天安门坐标转换:")
wgs84 = (116.391243, 39.907511)  # GPS坐标
print(f"WGS84 (GPS原始): {wgs84}")
print(f"GCJ02 (高德/腾讯): {wgs84_to_gcj02(*wgs84)}")
print(f"BD09 (百度): {gcj02_to_bd09(*wgs84_to_gcj02(*wgs84))}")
EOF
```

---

## 15. IBAN Validator | IBAN 验证工具

### IBAN Validation & Parsing | IBAN 验证与解析

**English:**
```bash
# IBAN (International Bank Account Number) validator
python3 << 'EOF'
def validate_iban(iban):
    """Validate IBAN using checksum algorithm"""
    # Remove spaces and convert to uppercase
    iban = iban.replace(" ", "").upper()
    
    # Check basic format
    if len(iban) < 15 or len(iban) > 34:
        return {"valid": False, "error": "Invalid length"}
    
    if not iban[:2].isalpha():
        return {"valid": False, "error": "Country code must be letters"}
    
    if not iban[2:4].isdigit():
        return {"valid": False, "error": "Check digits must be numbers"}
    
    # Move first 4 characters to end
    moved = iban[4:] + iban[:4]
    
    # Replace letters with numbers (A=10, B=11, ..., Z=35)
    numeric = ""
    for char in moved:
        if char.isalpha():
            numeric += str(ord(char) - ord('A') + 10)
        else:
            numeric += char
    
    # Calculate mod 97
    checksum = int(numeric) % 97
    
    if checksum != 1:
        return {"valid": False, "error": f"Invalid checksum (mod 97 = {checksum})"}
    
    # Parse IBAN components
    country = iban[:2]
    check_digits = iban[2:4]
    
    # Country-specific BBAN parsing
    country_formats = {
        "GB": {"bank": (4, 8), "branch": (8, 12), "account": (12, 22)},
        "DE": {"bank": (4, 12), "account": (12, 22)},
        "FR": {"bank": (4, 9), "branch": (9, 14), "account": (14, 25)},
        "IT": {"bank": (4, 9), "branch": (9, 14), "account": (14, 27)},
        "ES": {"bank": (4, 8), "branch": (8, 12), "account": (12, 22)},
        "NL": {"bank": (4, 8), "account": (8, 18)},
        "BE": {"bank": (4, 7), "account": (7, 14)},
        "CH": {"bank": (4, 9), "account": (9, 21)},
    }
    
    result = {
        "valid": True,
        "iban": iban,
        "country": country,
        "check_digits": check_digits,
        "bban": iban[4:]
    }
    
    if country in country_formats:
        for key, (start, end) in country_formats[country].items():
            result[key] = iban[start:end]
    
    return result

# Example IBANs
test_ibans = [
    "GB82 WEST 1234 5698 7654 32",  # UK
    "DE89 3704 0044 0532 0130 00",  # Germany
    "FR14 2004 1010 0505 0001 3M02 606",  # France
    "IT60 X054 2811 1010 0000 0123 456",  # Italy
    "ES91 2100 0418 4502 0005 1332",  # Spain
    "INVALID IBAN",  # Invalid
]

for iban in test_ibans:
    result = validate_iban(iban)
    status = "✅ Valid" if result["valid"] else f"❌ {result.get('error', 'Invalid')}"
    print(f"\n{iban}")
    print(f"  Status: {status}")
    if result["valid"]:
        print(f"  Country: {result['country']}")
        print(f"  BBAN: {result['bban']}")
EOF
```

**中文:**
```bash
# IBAN 银行账号验证
python3 << 'EOF'
# 使用上面的 validate_iban 函数...

# 测试样例
test_ibans = [
    "GB82 WEST 1234 5698 7654 32",  # 英国
    "DE89 3704 0044 0532 0130 00",  # 德国
    "FR14 2004 1010 0505 0001 3M02 606",  # 法国
]

for iban in test_ibans:
    result = validate_iban(iban)
    status = "✅ 有效" if result["valid"] else f"❌ {result.get('error', '无效')}"
    print(f"\n{iban}")
    print(f"  状态: {status}")
    if result["valid"]:
        print(f"  国家: {result['country']}")
        print(f"  银行账号: {result['bban']}")
EOF
```

---

## 16. ASCII Art Generator | ASCII 艺术生成器

### Text to ASCII Art | 文字转 ASCII 艺术

**English:**
```bash
# Generate ASCII art with auto-install if needed
python3 << 'EOF'
import subprocess

def ensure_figlet():
    """Ensure figlet is installed, auto-install if not"""
    result = subprocess.run(['which', 'figlet'], capture_output=True)
    if result.returncode == 0:
        return True
    
    print("📦 figlet not found. Installing...")
    subprocess.run(['brew', 'install', 'figlet'])
    return True

def generate_ascii_builtin(text):
    """Generate ASCII art using built-in font (fallback)"""
    FONT = {
        'A': [' █████ ', '██   ██', '███████', '██   ██', '██   ██'],
        'B': ['██████ ', '██   ██', '██████ ', '██   ██', '██████ '],
        'C': [' ██████', '██     ', '██     ', '██     ', ' ██████'],
        'D': ['██████ ', '██   ██', '██   ██', '██   ██', '██████ '],
        'E': ['███████', '██     ', '█████  ', '██     ', '███████'],
        'F': ['███████', '██     ', '█████  ', '██     ', '██     '],
        'G': [' ██████ ', '██      ', '██  ████', '██    ██', ' ██████ '],
        'H': ['██   ██', '██   ██', '███████', '██   ██', '██   ██'],
        'I': ['███', '██ ', '██ ', '██ ', '███'],
        'J': ['    ██', '    ██', '    ██', '██  ██', ' ████ '],
        'K': ['██   ██', '██ ██  ', '████   ', '██ ██  ', '██   ██'],
        'L': ['██     ', '██     ', '██     ', '██     ', '███████'],
        'M': ['███   ███', '████ ████', '██ ███ ██', '██     ██', '██     ██'],
        'N': ['██    ██', '███   ██', '██ ██ ██', '██   ███', '██    ██'],
        'O': [' █████ ', '██   ██', '██   ██', '██   ██', ' █████ '],
        'P': ['██████ ', '██   ██', '██████ ', '██     ', '██     '],
        'Q': [' █████ ', '██   ██', '██ █ ██', '██  ██ ', ' ███ ██'],
        'R': ['██████ ', '██   ██', '██████ ', '██ ██  ', '██  ███'],
        'S': [' ██████', '██     ', ' █████ ', '     ██', '██████ '],
        'T': ['███████', '  ██   ', '  ██   ', '  ██   ', '  ██   '],
        'U': ['██   ██', '██   ██', '██   ██', '██   ██', ' █████ '],
        'V': ['██   ██', '██   ██', '██   ██', ' ██ ██ ', '  ███  '],
        'W': ['██     ██', '██     ██', '██  █  ██', '██ ███ ██', ' ██ █ ███ '],
        'X': ['██   ██', ' ██ ██ ', '  ███  ', ' ██ ██ ', '██   ██'],
        'Y': ['██   ██', ' ██ ██ ', '  ███  ', '  ██   ', '  ██   '],
        'Z': ['███████', '    ██ ', '  ██   ', ' ██    ', '███████'],
        ' ': ['   ', '   ', '   ', '   ', '   '],
        '0': [' █████ ', '██  ███', '██ █ ██', '███  ██', ' █████ '],
        '1': ['  ██', ' ███', '  ██', '  ██', '█████'],
        '2': [' █████ ', '██   ██', '    ██ ', '  ███  ', '███████'],
        '3': ['█████  ', '     ██', '  ████ ', '     ██', '█████  '],
        '4': ['██   ██', '██   ██', '███████', '     ██', '     ██'],
        '5': ['███████', '██     ', '██████ ', '     ██', '██████ '],
        '6': [' █████ ', '██     ', '██████ ', '██   ██', ' █████ '],
        '7': ['███████', '    ██ ', '   ██  ', '  ██   ', '  ██   '],
        '8': [' █████ ', '██   ██', ' █████ ', '██   ██', ' █████ '],
        '9': [' █████ ', '██   ██', ' ██████', '     ██', ' █████ '],
    }
    
    text = text.upper()
    lines = [''] * 5
    for char in text:
        if char in FONT:
            for i, line in enumerate(FONT[char]):
                lines[i] += line + ' '
        else:
            for i in range(5):
                lines[i] += '    '
    return '\n'.join(lines)

# Main
text = "HELLO"

if ensure_figlet():
    print(f"🎨 Generating ASCII art for: {text}")
    subprocess.run(['figlet', text])
EOF
```

**中文:**
```bash
# 生成 ASCII 艺术（自动安装依赖）
python3 << 'EOF'
import subprocess

def ensure_figlet():
    """确保 figlet 已安装，未安装则自动安装"""
    result = subprocess.run(['which', 'figlet'], capture_output=True)
    if result.returncode == 0:
        return True
    
    print("📦 figlet 未安装，正在自动安装...")
    subprocess.run(['brew', 'install', 'figlet'])
    return True

text = "Hello"
if ensure_figlet():
    print(f"🎨 正在生成 ASCII 艺术: {text}")
    subprocess.run(['figlet', text])
EOF
```

**Using different fonts | 使用不同字体:**
```bash
figlet -f slant "Hello World"
figlet -f banner "Hello World"
figlet -f block "Hello World"
showfigfonts  # List all available fonts
```

---

## 17. Unix Permissions | Unix 权限工具

### Chmod Calculator | Chmod 计算器

**English:**
```bash
# Chmod calculator and permission decoder
python3 << 'EOF'
def chmod_calculator(user_r=False, user_w=False, user_x=False,
                     group_r=False, group_w=False, group_x=False,
                     other_r=False, other_w=False, other_x=False):
    """Calculate chmod value from permission checkboxes"""
    user = (user_r * 4) + (user_w * 2) + (user_x * 1)
    group = (group_r * 4) + (group_w * 2) + (group_x * 1)
    other = (other_r * 4) + (other_w * 2) + (other_x * 1)
    return f"{user}{group}{other}"

def decode_chmod(mode):
    """Decode chmod value to permissions"""
    if isinstance(mode, str):
        mode = int(mode, 8) if mode.isdigit() else int(mode)
    
    permissions = {
        'user': {'read': bool(mode & 0o400), 'write': bool(mode & 0o200), 'execute': bool(mode & 0o100)},
        'group': {'read': bool(mode & 0o040), 'write': bool(mode & 0o020), 'execute': bool(mode & 0o010)},
        'other': {'read': bool(mode & 0o004), 'write': bool(mode & 0o002), 'execute': bool(mode & 0o001)},
    }
    
    # Generate symbolic notation
    def to_symbol(p):
        r = 'r' if p['read'] else '-'
        w = 'w' if p['write'] else '-'
        x = 'x' if p['execute'] else '-'
        return r + w + x
    
    symbolic = to_symbol(permissions['user']) + to_symbol(permissions['group']) + to_symbol(permissions['other'])
    
    return {
        'octal': oct(mode)[-3:],
        'symbolic': symbolic,
        'permissions': permissions,
        'explanation': {
            'user': f"Owner can {'read' if permissions['user']['read'] else ''} {'write' if permissions['user']['write'] else ''} {'execute' if permissions['user']['execute'] else ''}".strip(),
            'group': f"Group can {'read' if permissions['group']['read'] else ''} {'write' if permissions['group']['write'] else ''} {'execute' if permissions['group']['execute'] else ''}".strip(),
            'other': f"Others can {'read' if permissions['other']['read'] else ''} {'write' if permissions['other']['write'] else ''} {'execute' if permissions['other']['execute'] else ''}".strip(),
        }
    }

# Calculate from checkboxes
print("=== Calculate from permissions ===")
result = chmod_calculator(user_r=True, user_w=True, user_x=True,
                          group_r=True, group_x=True,
                          other_r=True)
print(f"chmod 755 = {result}")  # 755

# Decode permissions
print("\n=== Decode chmod values ===")
for mode in [755, 644, 777, 600, 700]:
    decoded = decode_chmod(mode)
    print(f"\nchmod {decoded['octal']} ({decoded['symbolic']})")
    for who, explanation in decoded['explanation'].items():
        print(f"  {who}: {explanation}")

# Common permission presets
print("\n=== Common Presets ===")
presets = {
    "Private file (600)": 0o600,
    "Private directory (700)": 0o700,
    "Public file (644)": 0o644,
    "Public directory (755)": 0o755,
    "Executable (755)": 0o755,
    "Full access (777)": 0o777,
}

for name, mode in presets.items():
    decoded = decode_chmod(mode)
    print(f"{name}: {decoded['symbolic']}")
EOF
```

**中文:**
```bash
# Chmod 计算器
python3 << 'EOF'
# 使用上面的 decode_chmod 函数...

print("=== 常用权限说明 ===")
presets = {
    "私有文件 (600)": 0o600,
    "私有目录 (700)": 0o700,
    "公开文件 (644)": 0o644,
    "公开目录 (755)": 0o755,
    "可执行文件 (755)": 0o755,
}

for name, mode in presets.items():
    decoded = decode_chmod(mode)
    print(f"{name}: {decoded['symbolic']}")
EOF
```

---

## 18. HMAC Calculator | HMAC 计算器

### HMAC (Hash-based Message Authentication Code)

**English:**
```bash
# HMAC calculator
python3 << 'EOF'
import hmac
import hashlib

def calculate_hmac(message, key, algorithm='sha256'):
    """Calculate HMAC for a message with a key"""
    alg = getattr(hashlib, algorithm)
    h = hmac.new(key.encode(), message.encode(), alg)
    return h.hexdigest()

def verify_hmac(message, key, signature, algorithm='sha256'):
    """Verify HMAC signature"""
    expected = calculate_hmac(message, key, algorithm)
    return hmac.compare_digest(expected, signature)

# Supported algorithms
algorithms = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_256', 'sha3_512']

message = "Hello, World!"
key = "secret-key-123"

print(f"Message: {message}")
print(f"Key: {key}")
print("\nHMAC signatures:")

for alg in algorithms:
    try:
        sig = calculate_hmac(message, key, alg)
        print(f"  HMAC-{alg.upper()}: {sig}")
    except AttributeError:
        pass

# Verification example
print("\n=== Verification ===")
signature = calculate_hmac(message, key, 'sha256')
print(f"Signature: {signature}")
print(f"Verify (correct key): {verify_hmac(message, key, signature, 'sha256')}")
print(f"Verify (wrong key): {verify_hmac(message, 'wrong-key', signature, 'sha256')}")
EOF
```

**中文:**
```bash
# HMAC 计算器
python3 << 'EOF'
import hmac
import hashlib

# 计算各种 HMAC
message = "重要消息"
key = "密钥123"

print(f"消息: {message}")
print(f"密钥: {key}")
print(f"\nHMAC-SHA256: {hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()}")
print(f"HMAC-MD5: {hmac.new(key.encode(), message.encode(), hashlib.md5).hexdigest()}")
EOF
```

---

## 19. AES Encryption/Decryption | AES 加密解密

### Symmetric Encryption | 对称加密

**English:**
```bash
# AES encryption/decryption using Python
python3 << 'EOF'
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
    import base64
    
    def aes_encrypt(plaintext, key=None, iv=None):
        """Encrypt text using AES-256-CBC"""
        if key is None:
            key = get_random_bytes(32)  # 256-bit key
        elif isinstance(key, str):
            key = key.encode().ljust(32, b'\0')[:32]
        
        if iv is None:
            iv = get_random_bytes(16)
        elif isinstance(iv, str):
            iv = iv.encode().ljust(16, b'\0')[:16]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = pad(plaintext.encode(), AES.block_size)
        encrypted = cipher.encrypt(padded)
        
        return {
            'ciphertext': base64.b64encode(encrypted).decode(),
            'key': base64.b64encode(key).decode(),
            'iv': base64.b64encode(iv).decode(),
        }
    
    def aes_decrypt(ciphertext, key, iv):
        """Decrypt AES-256-CBC encrypted text"""
        if isinstance(key, str):
            key = base64.b64decode(key)
        if isinstance(iv, str):
            iv = base64.b64decode(iv)
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(base64.b64decode(ciphertext)), AES.block_size)
        return decrypted.decode()
    
    # Example
    plaintext = "This is a secret message!"
    result = aes_encrypt(plaintext)
    
    print(f"Original: {plaintext}")
    print(f"Encrypted: {result['ciphertext']}")
    print(f"Key: {result['key']}")
    print(f"IV: {result['iv']}")
    
    decrypted = aes_decrypt(result['ciphertext'], result['key'], result['iv'])
    print(f"Decrypted: {decrypted}")

except ImportError:
    print("Install PyCryptodome: pip install pycryptodome")
    
    # Alternative using openssl CLI
    import subprocess
    
    def aes_encrypt_openssl(plaintext, password):
        """Encrypt using openssl CLI"""
        result = subprocess.run(
            ['openssl', 'enc', '-aes-256-cbc', '-base64', '-pass', f'pass:{password}'],
            input=plaintext.encode(),
            capture_output=True
        )
        return result.stdout.decode().strip()
    
    def aes_decrypt_openssl(ciphertext, password):
        """Decrypt using openssl CLI"""
        result = subprocess.run(
            ['openssl', 'enc', '-aes-256-cbc', '-base64', '-d', '-pass', f'pass:{password}'],
            input=ciphertext.encode(),
            capture_output=True
        )
        return result.stdout.decode().strip()
    
    # Example
    password = "my-secret-password"
    plaintext = "This is a secret message!"
    
    encrypted = aes_encrypt_openssl(plaintext, password)
    print(f"Encrypted: {encrypted}")
    
    decrypted = aes_decrypt_openssl(encrypted, password)
    print(f"Decrypted: {decrypted}")
EOF
```

**中文:**
```bash
# 使用 openssl 命令行进行 AES 加密
# 加密
echo "秘密消息" | openssl enc -aes-256-cbc -base64 -pass pass:密码123

# 解密
echo "U2FsdGVkX1..." | openssl enc -aes-256-cbc -base64 -d -pass pass:密码123

# 加密文件
openssl enc -aes-256-cbc -salt -in file.txt -out file.enc -pass pass:密码

# 解密文件
openssl enc -aes-256-cbc -d -in file.enc -out file.txt -pass pass:密码
```

---

## 20. Config File Converter | 配置文件转换器

### ENV ↔ JSON ↔ YAML ↔ TOML Conversion

**English:**
```bash
# Configuration file format converter
python3 << 'EOF'
import json

def env_to_dict(env_string):
    """Convert .env format to dict"""
    result = {}
    for line in env_string.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip().strip('"\'')
    return result

def dict_to_env(data):
    """Convert dict to .env format"""
    lines = []
    for key, value in data.items():
        if isinstance(value, str) and (' ' in value or value == ''):
            lines.append(f'{key}="{value}"')
        else:
            lines.append(f'{key}={value}')
    return '\n'.join(lines)

def dict_to_toml(data, section=None):
    """Convert dict to TOML format"""
    lines = []
    simple = {}
    tables = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            tables[key] = value
        else:
            simple[key] = value
    
    if section:
        lines.append(f'[{section}]')
    
    for key, value in simple.items():
        if isinstance(value, str):
            lines.append(f'{key} = "{value}"')
        elif isinstance(value, bool):
            lines.append(f'{key} = {str(value).lower()}')
        else:
            lines.append(f'{key} = {value}')
    
    for table_name, table_data in tables.items():
        lines.append(f'\n[{table_name}]')
        for key, value in table_data.items():
            if isinstance(value, str):
                lines.append(f'{key} = "{value}"')
            elif isinstance(value, bool):
                lines.append(f'{key} = {str(value).lower()}')
            else:
                lines.append(f'{key} = {value}')
    
    return '\n'.join(lines)

def dict_to_ini(data):
    """Convert dict to INI format"""
    lines = []
    simple = {}
    sections = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            sections[key] = value
        else:
            simple[key] = value
    
    # Default section
    for key, value in simple.items():
        lines.append(f'{key}={value}')
    
    # Named sections
    for section_name, section_data in sections.items():
        lines.append(f'\n[{section_name}]')
        for key, value in section_data.items():
            lines.append(f'{key}={value}')
    
    return '\n'.join(lines)

# Example
env_config = """
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=admin
DB_PASS="secret password"

# Redis configuration
REDIS_URL=redis://localhost:6379
DEBUG=true
"""

config_dict = env_to_dict(env_config)
print("=== Original ENV ===")
print(env_config)

print("\n=== As JSON ===")
print(json.dumps(config_dict, indent=2))

print("\n=== As TOML ===")
print(dict_to_toml(config_dict))

print("\n=== As INI ===")
print(dict_to_ini(config_dict))
EOF
```

**中文:**
```bash
# 配置文件格式转换
python3 << 'EOF'
# 环境变量转 JSON
env_str = """
HOST=localhost
PORT=3000
DEBUG=true
"""

config = {}
for line in env_str.strip().split('\n'):
    if '=' in line:
        k, v = line.split('=', 1)
        config[k.strip()] = v.strip()

import json
print("JSON 格式:")
print(json.dumps(config, indent=2))
EOF
```

---

## Trigger Words | 触发词

**English:**
```
Text statistics, case conversion, text diff, text sort
Base64 encode/decode, URL encode/decode, Hex encode/decode, JWT decode
Format JSON, format XML, format SQL, format HTML
Timestamp conversion, cron parser, date calculator
Regex test, regex patterns, regex generator
MD5 hash, SHA256 hash, SHA512 hash, RIPEMD hash
Password generator, password strength checker, BIP39 mnemonic
Generate UUID, generate ULID, generate NanoID, JSON to struct
QR code generator, ASCII art generator
Mock data generator, random data generator
CSV to JSON, JSON to CSV, XML converter, YAML converter
Coordinate converter, WGS84 to GCJ02, GCJ02 to BD09
IBAN validator, credit card validator, Luhn algorithm
Chmod calculator, file permissions, Unix permissions
HMAC calculator, HMAC-SHA256
AES encrypt, AES decrypt, symmetric encryption
Config converter, ENV to JSON, TOML converter
IP lookup, HTTP request test, port check
Color conversion, HEX to RGB, palette generator
Base conversion, Roman numerals, unit converter
```

**中文:**
```
文本统计, 大小写转换, 文本对比, 文本排序
Base64 编码/解码, URL 编码/解码, 十六进制编解码, JWT 解码
格式化 JSON, 格式化 XML, 格式化 SQL, 格式化 HTML
时间戳转换, Cron 解析, 日期计算
正则测试, 正则模式, 正则生成
MD5 加密, SHA256 哈希, SHA512 哈希
密码生成器, 密码强度检测, BIP39 助记词
生成 UUID, 生成 ULID, 生成 NanoID, JSON 转结构体
二维码生成, ASCII 艺术字
Mock 数据生成, 随机数据生成
CSV 转 JSON, JSON 转 CSV, XML 转换, YAML 转换
坐标转换, WGS84 转 GCJ02, GCJ02 转 BD09
IBAN 验证, 信用卡验证, Luhn 算法
Chmod 计算器, 文件权限, Unix 权限
HMAC 计算器, HMAC-SHA256
AES 加密, AES 解密, 对称加密
配置文件转换, ENV 转 JSON, TOML 转换
查询 IP, HTTP 请求测试, 端口检测
颜色转换, HEX 转 RGB, 调色板生成
进制转换, 罗马数字, 单位转换
```

---

## Quick Reference | 快速参考

| Task | Command |
|------|---------|
| Text stats | `python3 -c "import re; text='hello'; print(len(text))"` |
| Case convert | `python3 -c "print('hello world'.title())"` |
| Base64 encode | `echo -n "text" \| base64` |
| Base64 decode | `echo "encoded" \| base64 -d` |
| URL encode | `python3 -c "import urllib.parse; print(urllib.parse.quote('text'))"` |
| JSON format | `echo '{"key":"value"}' \| python3 -m json.tool` |
| Timestamp | `date +%s` |
| UUID | `uuidgen` |
| MD5 | `echo -n "text" \| md5` |
| SHA256 | `echo -n "text" \| shasum -a 256` |
| Password | `openssl rand -base64 12` |
| Public IP | `curl -s ifconfig.me` |
| QR Code | `echo "text" \| qrencode -t UTF8` |
| AES encrypt | `echo "text" \| openssl enc -aes-256-cbc -base64 -pass pass:key` |
| Chmod decode | `python3 -c "import stat; print(oct(0o755))"` |
| HMAC | `python3 -c "import hmac,hashlib; print(hmac.new(b'key',b'msg',hashlib.sha256).hexdigest())"` |

---

## Notes | 注意事项

**English:**
- Some commands differ between macOS and Linux (e.g., `date` command)
- AES encryption requires openssl (pre-installed on most systems)
- QR code generation requires `qrencode` (install: `brew install qrencode`)
- ASCII art with figlet: `brew install figlet`
- Network tools require internet connection
- BIP39 requires proper library for production use
- For Python-based tools, required packages: `pycryptodome`, `qrcode[pil]`, `pyzbar`

**中文:**
- 部分命令在 macOS 和 Linux 上有差异（如 `date` 命令）
- AES 加密需要 openssl（大多数系统已预装）
- 二维码生成需要 `qrencode`（安装：`brew install qrencode`）
- ASCII 艺术需要 figlet：`brew install figlet`
- 网络工具需要网络连接
- BIP39 生产环境需要使用专用库
- Python 工具依赖包：`pycryptodome`, `qrcode[pil]`, `pyzbar`
