---
slug: cn-password-generator
name: 安全密码生成器
description: "安全的随机密码生成器。支持自定义长度、字符类型（大小写字母、数字、特殊符号）、排除相似字符、批量生成。纯Python标准库，无需API Key。"
keywords: 密码, 生成密码, 随机密码, 安全, password, generator, 强密码
version: "1.0.0"
author: 千策
---

# 安全密码生成器

安全的随机密码生成器，纯Python标准库实现，无需API Key，开箱即用。

## 功能

- 随机密码生成（默认16位）
- 自定义字符类型：大写、小写、数字、特殊符号
- 排除相似字符（0O1lI等），避免混淆
- 批量生成多个密码
- 纯标准库，零依赖

## 使用示例

```
生成一个16位密码
生成10个20位强密码
生成不含特殊符号的12位密码
```

## 技术实现

调用 `scripts/password_generator.py` 生成密码，支持参数：
- 长度（默认16）
- 字符类型开关（大写/小写/数字/特殊符号）
- 排除相似字符（--exclude-similar）
- 生成数量

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
