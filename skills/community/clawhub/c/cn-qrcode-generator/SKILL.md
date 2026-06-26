---
slug: cn-qrcode-generator
name: 二维码生成工具
version: "1.0.0"
author: 千策
---

# 二维码生成器

输入URL或文本，生成PNG二维码。

## 功能
- 输入URL/文本，生成二维码
- 自定义尺寸（默认300px）

## 用法
python3 scripts/qrcode_generator.py "https://example.com"
python3 scripts/qrcode_generator.py "Hello World"

## 依赖
- Python 3.7+
- certifi（SSL证书验证）

## 数据来源
使用 qrserver.com 公开API生成二维码，无需API Key。

## 版本
- v1.2.0: 文档优化，更新依赖说明

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
