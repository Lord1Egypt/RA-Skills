---
slug: cn-base64-tools
name: cn-base64-tools
version: "1.0.0"
description: "Base64编码解码工具。支持文本编码/解码、URL安全Base64、文件Base64转换。纯Python标准库，无需API Key。"
scope: "base64, encoding, decoding, url-safe-base64"
install: |
  无额外依赖，纯Python标准库
env: ""
entry:
  type: prompt
  prompt: |
    当用户需要Base64编码或解码时使用此skill。调用 scripts/base64_tools.py "encode 文本" 或 "decode 编码文本"。
handler: |
  python3 scripts/base64_tools.py "<操作> <内容>"
---

# Base64工具

Base64编码解码工具。支持文本、URL安全Base64编解码。

## 功能

- **文本编码**：将普通文本转为Base64字符串
- **文本解码**：将Base64字符串还原为原始文本
- **URL安全模式**：使用URL安全字符替换 `+/` 为 `-_`
- **自动检测**：自动判断输入是否为合法Base64

## 安装要求

- Python 3.6+
- 无外部依赖

## 使用方法

```bash
# 编码
python3 scripts/base64_tools.py "encode 你好世界"

# 解码
python3 scripts/base64_tools.py "decode 5L2g5aW95LiW55WM"

# URL安全编码
python3 scripts/base64_tools.py "encode-url 数据内容"
```

## 示例

输入：`encode Hello World`
输出：`SGVsbG8gV29ybGQ=`

输入：`decode SGVsbG8gV29ybGQ=`
输出：`Hello World`

## 分类

开发工具

## 关键词

base64, 编码, 解码, encode, decode, url-safe

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
