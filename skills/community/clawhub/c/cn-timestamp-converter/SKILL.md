---
slug: cn-timestamp-converter
name: 时间戳转换器
version: "1.2.1"
author: 千策
---

# 时间戳转换器

Unix时间戳转可读日期。开发调试必备。

## 功能

- **时间戳→日期**：将Unix时间戳转为可读日期
- **秒/毫秒自动识别**：10位秒级 vs 13位毫秒级自动判断
- **时区支持**：UTC自动转换，显示本地时间
- **当前时间戳**：不传参数时自动获取当前时间戳

## 安装要求

- Python 3.6+
- 无外部依赖（纯标准库）

## 使用方法

```bash
# 时间戳转日期（10位秒级）
python3 scripts/timestamp_converter.py "1745800000"

# 时间戳转日期（13位毫秒级，自动识别）
python3 scripts/timestamp_converter.py "1745800000000"

# 不传参数，获取当前时间戳
python3 scripts/timestamp_converter.py
```

## 输出格式

```json
{
  "unix": 1745800000,
  "utc": "2025-04-28T07:46:40+00:00",
  "local": "2025-04-28 15:46:40",
  "readable": "2025年04月28日 15:46:40"
}
```

## 分类

开发工具

## 关键词

时间戳, timestamp, 日期转换, 时区, datetime, unix

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
