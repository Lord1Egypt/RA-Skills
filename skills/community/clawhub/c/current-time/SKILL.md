---
name: current-time
version: 1.0.0
description: |
  获取当前时间的工具。返回格式化的日期时间和时区信息。
  
  USE FOR:
  - "现在几点了", "当前时间"
  - "今天是几号", "什么日期"
  - 获取带时区的时间信息

author: changsheng0804
license: MIT
homepage: https://github.com/changsheng0804/workbuddy-skills
tags: [time, date, utility]

metadata:
  openclaw:
    emoji: 🕐
    requires:
      bins: ["date"]

---

# 当前时间工具

快速获取当前日期时间，支持多时区显示。

## 使用场景

✅ **适用**：
- 用户询问当前时间
- 需要时间戳用于日志记录
- 需要确认日期进行日程安排

## 快速开始

```
用户：现在几点了
AI：[执行] → 返回格式化时间
```

## 执行流程

1. **获取系统时间**
   ```bash
   date +"%Y年%m月%d日 %H:%M:%S %Z"
   ```

2. **格式化输出**
   - 日期：YYYY年MM月DD日
   - 时间：HH:MM:SS
   - 时区：显示当前时区

## 输出格式

```
当前时间：2026年04月14日 18:05:32 CST
```

## 示例

**用户**：今天星期几？

**AI**：
```bash
date +"今天是%Y年%m月%d日，星期%u"
```

**输出**：今天是2026年04月14日，星期2
