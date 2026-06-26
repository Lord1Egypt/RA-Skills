name: Hex解码器
version: "1.0.0"
description: "Hex十六进制编码解码工具。文本与十六进制互转，支持批量处理、颜色码解析，常用于调试和逆向工程。纯Python标准库，无需API Key。"
license: MIT-0
tags:
  - tools


# Hex解码器

Hex十六进制编码解码工具。开发调试好帮手。

## 功能

- **文本转Hex**：将普通文本转为十六进制字符串
- **Hex转文本**：将十六进制还原为原始文本
- **颜色码解析**：解析#RRGGBB颜色值
- **批量处理**：支持多行文本同时转换
- **格式化输出**：支持带空格/0x前缀的Hex输出

## 安装要求

- Python 3.6+
- 无外部依赖

## 使用方法

```bash
# 编码
python3 scripts/hex_decoder.py "encode Hello"

# 解码
python3 scripts/hex_decoder.py "decode 48656c6c6f"

# 颜色码解析
python3 scripts/hex_decoder.py "color FF5500"
```

## 示例

输入：`encode Hello`
输出：`48656c6c6f`

输入：`decode 48656c6c6f`
输出：`Hello`

## 分类

开发工具

## 关键词

hex, 十六进制, 编码, 解码, encode, decode

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
