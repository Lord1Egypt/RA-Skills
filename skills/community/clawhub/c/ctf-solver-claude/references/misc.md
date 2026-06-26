# CTF MISC 子技能

## 总体流程

```
识别文件/数据类型 → 选择对应解法 → 解码/提取/分析 → 获取 flag
```

---

## Phase 1：第一眼判断

```bash
file <attachment>          # 文件类型（可能与扩展名不符）
xxd <file> | head -20      # 查看 magic bytes
strings <file> | grep -i flag
binwalk <file>             # 嵌套文件检测
binwalk -e <file>          # 自动提取嵌套文件
exiftool <file>            # 元数据（图片/PDF等）
```

**常见 Magic Bytes**：
| 开头 | 类型 |
|------|------|
| `FF D8 FF` | JPEG |
| `89 50 4E 47` | PNG |
| `50 4B 03 04` | ZIP |
| `25 50 44 46` | PDF |
| `37 7A BC AF` | 7z |
| `1F 8B` | GZIP |

---

## Phase 2：编码 / 解码

### 2.1 Base 系列

```python
import base64, codecs

data = "SGVsbG8gV29ybGQ="

# Base64
print(base64.b64decode(data))

# Base32
print(base64.b32decode(data))

# Base16 (hex)
print(bytes.fromhex("48656c6c6f"))

# Base85 / Ascii85
print(base64.b85decode(data))

# 多层嵌套：循环解码直到出现 flag
result = data.encode()
for _ in range(20):
    try:
        result = base64.b64decode(result)
        if b'flag' in result.lower():
            print(result)
            break
    except:
        break
```

### 2.2 凯撒 / ROT

```python
# ROT13
import codecs
print(codecs.decode("synt{uryyb}", 'rot_13'))

# 暴力枚举所有位移
text = "synt{uryyb}"
for shift in range(26):
    result = ''.join(chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
                     if c.isalpha() else c for c in text.lower())
    if 'flag' in result:
        print(shift, result)
```

### 2.3 维吉尼亚密码

```python
# 在线工具：https://www.dcode.fr/vigenere-cipher
# 或 quipqiup.com 自动分析
```

### 2.4 其他编码速查

```python
# Morse
# ... 搜索 "CTF morse decoder"

# 二进制转文本
bits = "01100110 01101100 01100001 01100111"
print(''.join(chr(int(b, 2)) for b in bits.split()))

# 八进制
print(''.join(chr(int(o, 8)) for o in "146 154 141 147".split()))

# URL 编码
from urllib.parse import unquote
print(unquote("%66%6c%61%67"))

# HTML 实体
# &#102;&#108;&#97;&#103; → flag

# Unicode
print("\u0066\u006c\u0061\u0067")
```

---

## Phase 3：隐写术（Steganography）

### 3.1 图片隐写

```bash
# 安装工具
pip install stegano --break-system-packages
apt-get install -y steghide outguess 2>/dev/null

# LSB 隐写（PNG/BMP）
python3 -c "
from PIL import Image
img = Image.open('image.png')
pixels = list(img.getdata())
bits = ''
for p in pixels[:1000]:
    for channel in (p if isinstance(p, tuple) else [p]):
        bits += str(channel & 1)
# 每8位转一个字符
print(''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)))
"

# zsteg（PNG/BMP 多通道 LSB）
gem install zsteg 2>/dev/null || pip install zsteg 2>/dev/null
zsteg image.png -a    # 全自动扫描

# steghide（JPEG，可能有密码）
steghide extract -sf image.jpg -p ""
steghide extract -sf image.jpg -p "password"

# stegsolve（GUI，用 java）
# 替代：python PIL 查看各通道
python3 -c "
from PIL import Image
img = Image.open('image.png')
r, g, b = img.split()[:3]
r.save('red.png'); g.save('green.png'); b.save('blue.png')
"

# exiftool 检查元数据
exiftool image.jpg | grep -i "comment\|description\|flag"
```

### 3.2 音频隐写

```bash
# 安装 sox, audacity
apt-get install -y sox 2>/dev/null

# 查看频谱图（Sonic Visualiser / Audacity）
# 高频/低频段常隐藏摩尔斯码

# DTMF 解码
pip install dtmf --break-system-packages
python3 -m dtmf audio.wav

# LSB in WAV
python3 -c "
import wave, struct
w = wave.open('audio.wav', 'rb')
frames = w.readframes(w.getnframes())
bits = ''.join(str(b & 1) for b in frames[:8000])
print(''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)[:100]))
"
```

### 3.3 文件隐写

```bash
# 文件末尾附加数据
tail -c 200 file.jpg       # 查看末尾字节
binwalk -e file.jpg        # 提取附加文件
foremost -i file.jpg -o output/  # 文件雕刻

# ZIP 注释
python3 -c "
import zipfile
z = zipfile.ZipFile('file.zip')
print(z.comment)
"
```

---

## Phase 4：流量分析

```bash
# 工具：tshark（wireshark CLI）
apt-get install -y tshark 2>/dev/null

# 基础分析
tshark -r traffic.pcap -Y "http" -T fields -e http.request.uri -e http.file_data 2>/dev/null
tshark -r traffic.pcap -Y "tcp" | head -50

# 提取 HTTP 对象
tshark -r traffic.pcap --export-objects http,./exported/ 2>/dev/null

# 找 flag 字符串
strings traffic.pcap | grep -i "flag{"
strings traffic.pcap | grep -E "[A-Z]+CTF\{"

# 提取 TCP 流（重组）
tshark -r traffic.pcap -q -z follow,tcp,ascii,0 2>/dev/null | head -100

# DNS 隐写（数据外带）
tshark -r traffic.pcap -Y dns -T fields -e dns.qry.name 2>/dev/null | sort -u
```

---

## Phase 5：内存取证

```bash
# 安装 volatility3
pip install volatility3 --break-system-packages

# 基础命令
vol -f memory.dmp windows.info         # 系统信息
vol -f memory.dmp windows.pslist       # 进程列表
vol -f memory.dmp windows.cmdline      # 命令行参数（常含 flag）
vol -f memory.dmp windows.filescan     # 扫描文件
vol -f memory.dmp windows.dumpfiles --virtaddr 0x... # 提取文件

# grep flag
strings memory.dmp | grep -i "flag{"
strings memory.dmp | grep -E "[A-Z]+CTF\{"
```

---

## Phase 6：压缩包密码

```bash
# 安装 john / hashcat
apt-get install -y john 2>/dev/null

# ZIP 密码爆破
zip2john challenge.zip > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

# 7z 密码
7z2john challenge.7z > hash.txt
john hash.txt

# CRC 碰撞（ZIP 小文件 < 5 字节）
python3 -c "
import zipfile, struct, zlib
z = zipfile.ZipFile('file.zip')
info = z.infolist()[0]
crc = info.CRC
size = info.file_size
# 枚举所有可能的 size 字节内容
for i in range(256**size):
    data = i.to_bytes(size, 'big')
    if zlib.crc32(data) & 0xFFFFFFFF == crc:
        print(data)
        break
"

# 已知明文攻击（bkcrack）
# git clone https://github.com/kimci86/bkcrack
# 需要知道 zip 内某文件的明文片段（≥12字节）
```

---

## Phase 7：密码学

```python
# RSA（已知 p, q 分解）
from Crypto.Util.number import inverse, long_to_bytes
p, q, e, c = ..., ..., ..., ...
n = p * q
phi = (p-1) * (q-1)
d = inverse(e, phi)
m = pow(c, d, n)
print(long_to_bytes(m))

# RSA 小公钥指数攻击（e=3, 无填充）
import gmpy2
m, is_perfect = gmpy2.iroot(c, e)
print(long_to_bytes(int(m)))

# XOR
key = b'\x42'
ct = bytes.fromhex("...")
print(bytes(b ^ key[0] for b in ct))

# 多字节 XOR 爆破
for k in range(256):
    pt = bytes(b ^ k for b in ct)
    if b'flag' in pt.lower():
        print(k, pt)
```

---

## Phase 8：二维码 / 条形码

```bash
pip install qrcode Pillow zxing --break-system-packages
python3 -c "
import zxing
reader = zxing.BarCodeReader()
barcode = reader.decode('qrcode.png')
print(barcode.parsed)
"
# 或在线工具：https://zxing.org/w/decode.jspx
```

---

## 常用在线工具

- CyberChef: https://gchq.github.io/CyberChef/ （万能编解码）
- dcode.fr: https://www.dcode.fr/ （各种密码）
- StegOnline: https://stegonline.georgeom.net/
- Forensically: https://29a.ch/photo-forensics/
