slug: cn-timestamp-tool
name: 时间戳转换工具
description: "cn-timestamp-tool。纯Python标准库，无需API Key。"
keywords: timestamp, tool
version: "1.0.0"
author: 千策

# 时间戳转换工具

纯 Python 标准库实现的时间戳转换工具。

## 功能

- **时间戳 → 日期时间**：将 Unix 时间戳转换为可读日期时间
- **日期时间 → 时间戳**：将日期时间转换为 Unix 时间戳
- **当前时间戳**：获取当前 Unix 时间戳（秒/毫秒）
- **时区支持**：支持不同时区的转换

## 使用方式

```bash
# 当前时间戳（秒）
python3 cn_timestamp_tool.py now

# 当前时间戳（毫秒）
python3 cn_timestamp_tool.py now-ms

# 时间戳转日期时间
python3 cn_timestamp_tool.py to-datetime 1714214400

# 日期时间转时间戳
python3 cn_timestamp_tool.py to-timestamp "2024-04-27 14:30:00"

# 指定格式输出
python3 cn_timestamp_tool.py format 1714214400 "%Y年%m月%d日 %H:%M:%S"

# 带时区转换
python3 cn_timestamp_tool.py to-datetime 1714214400 -z Asia/Shanghai
```

## 技术说明

- 纯 Python 标准库（`datetime`、`time`、`argparse`、`zoneinfo`）
- 无外部依赖
- 默认时区 Asia/Shanghai

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
