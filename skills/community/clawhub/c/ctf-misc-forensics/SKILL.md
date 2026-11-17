---
name: ctf-misc-forensics
description: "Misc杂项与流量取证助手：pcap流量分析、文件取证、隐写、编码谜题、内存/磁盘取证的识别与还原。遇到 misc、流量、pcap、取证、隐写、编码、内存镜像、磁盘镜像类题目时使用。"
---

# CTF Misc 与流量取证

从流量、文件、内存、磁盘中还原隐藏数据。

## 环境约定

- `$PY` = 64 位解题 Python（含 Pillow/numpy/pyzbar/dnspython/python-magic/pycryptodome/volatility3）。
  环境不确定时先运行 ctf-router 技能的 `scripts/env-check.py` 自检。
- **tshark**（Wireshark 自带）：流量分析主力；复杂协议人工配合 Wireshark GUI。
- **volatility3**：内存取证，`$PY -m volatility3 -f mem.dmp <plugin>`。
- **Linux 专属工具**（binwalk/foremost/strings/john/7z）：Windows 走 WSL
  （`wsl -d <distro> -- bash -lc "<cmd>"`，文件路径换 `/mnt/c/...`）；
  Linux/macOS 直接系统包管理器安装。

## 通用第一步（任何未知文件）

```powershell
$PY -c "import magic; print(magic.from_file('file'))"   # 真实类型
$PY -c "print(open('file','rb').read(32))"              # 魔数
# WSL/Linux 内：
strings -n 8 file | grep -iE 'flag|ctf'
binwalk file
7z x file -oout/
```

## 流量取证（tshark 速查）

```powershell
# 协议分布概览
tshark -r c.pcap -qz io,phs
# 提取 HTTP 传输的文件
tshark -r c.pcap --export-objects http,./http_out
# 追踪单条 TCP 流
tshark -r c.pcap -qz follow,tcp,raw,0
# DNS 隧道/编码：看查询名
tshark -r c.pcap -Y dns -T fields -e dns.qry.name
# USB 键盘/鼠标：8字节 HID 报告
tshark -r c.pcap -Y usb -T fields -e usb.capdata
# TLS 解密：有 keylog 时
tshark -r c.pcap -o tls.keylog_file:keys.log -Y http
```

- USB 键盘：byte0=修饰键（Shift=0x02），byte2=keycode，写脚本映射还原击键。
- USB 鼠标：相对位移累加成轨迹，可还原手写/画图。
- 包间隔编码：两种不同间隔（如 10ms/100ms）= 二进制 0/1。
- TCP flag 隐蔽信道：6 个 flag 位编码 0-63 → base64 字符。
- NTLMv2：从 NTLMSSP_AUTH 提 challenge+NTProofStr+blob 交给 hashcat。
- pcap 损坏：`pcapfix` 修复（Linux 包）。

## 内存取证（volatility3）

```powershell
$PY -m volatility3 -f mem.dmp windows.info        # 识别系统
$PY -m volatility3 -f mem.dmp windows.pslist      # 进程
$PY -m volatility3 -f mem.dmp windows.cmdline     # 命令行
$PY -m volatility3 -f mem.dmp windows.netscan     # 网络连接
$PY -m volatility3 -f mem.dmp windows.filescan | findstr flag
$PY -m volatility3 -f mem.dmp windows.dumpfiles --physaddr 0x...
# 兜底：直接正则扫镜像
$PY -c "import re; d=open('mem.dmp','rb').read(); print(re.findall(rb'flag\{[^}]+\}', d))"
```

## 磁盘取证（WSL/Linux）

```bash
fls -r image.dd            # 列文件（含删除）
icat image.dd <inode>      # 按 inode 恢复
foremost -i image.dd -o carved/
```

## 隐写速查

- PNG：zsteg（`gem install zsteg`，Linux）、位平面（numpy 抽 bit0-2）、IEND 后附加数据、
  改 IHDR 高度 + 暴破 CRC
- JPEG：steghide（Linux）、DCT 系数、缩略图
- 音频：频谱图（隐藏图像）、倒放、DTMF、LSB
- PDF：exiftool 元数据、`%EOF` 后数据、嵌入对象
- 视频：逐帧合成（numpy max）、多流容器（ffprobe 列流）
- Unicode：U+E0000 Tags 块减 0xE0000、变体选择符 U+E0100 偏移

## 编码谜题

```powershell
$PY -c "import base64; print(base64.b64decode('<s>'))"
$PY -c "import base64; print(base64.b32decode('<s>'))"
$PY -c "print(bytes.fromhex('<hex>').decode())"
# 字符集识别：A-Za-z0-9+/=→Base64；A-Z2-7=→Base32；0-9a-f→Hex
# 嵌套压缩：循环 7z 解压直到无压缩包
```

## 何时换技能

- 还原出密文/密钥后要破密码 → Crypto 技能。
- 提取出二进制要分析 → 逆向技能。
- 其实是 Web 备份/源码审计 → Web 技能。

## 深度知识库（按需读取）

本技能目录 `references/` 下两套参考文件（只读复用）：

| 目录 | 内容 |
|---|---|
| references/ctf-misc/ | 编码、pyjail/bashjail、游戏/自定义 VM、DNS |
| references/ctf-forensics/ | 取证全集：流量（network*.md）、USB/蓝牙（peripheral-capture.md）、磁盘内存（disk-*.md）、Windows（windows.md）、隐写（stego*.md）、信号硬件（signals-and-hardware.md） |
