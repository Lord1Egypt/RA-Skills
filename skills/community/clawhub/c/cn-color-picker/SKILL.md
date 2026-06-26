name: 颜色选择器
version: "1.0.0"
description: "颜色选择与转换工具。支持HEX/RGB/HSL/HSV格式互转、调色板生成、渐变色预览。纯Python标准库，无需API Key。"
license: MIT-0
tags:
  - tools


# 颜色选择器

颜色选择与转换工具。设计师和前端开发者的颜色助手。

## 功能

- **格式互转**：HEX ↔ RGB ↔ HSL ↔ HSV
- **调色板生成**：基于一个主色生成5色和谐调色板
- **渐变色预览**：生成两色之间的10级渐变
- **颜色解析**：自动识别输入格式并转换

## 安装要求

- Python 3.6+
- 无外部依赖

## 使用方法

```bash
# HEX转RGB
python3 scripts/color_picker.py "hex2rgb #FF5500"

# RGB转HSL
python3 scripts/color_picker.py "rgb2hsl 255,85,0"

# 生成调色板
python3 scripts/color_picker.py "palette #3366FF"

# 渐变色
python3 scripts/color_picker.py "gradient #FF0000 #0000FF"
```

## 示例

输入：`hex2rgb #FF5500`
输出：`RGB: (255, 85, 0)`

输入：`palette #3366FF`
输出：5个和谐配色方案的HEX值

## 分类

设计工具

## 关键词

颜色, 调色板, HEX, RGB, HSL, HSV, color, palette, gradient

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
