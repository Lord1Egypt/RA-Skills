slug: cn-color-tool
name: 颜色转换工具
description: "cn-color-tool。纯Python标准库，无需API Key。"
keywords: color, tool
version: "1.0.0"
author: 千策

# 颜色转换工具

纯 Python 标准库实现的颜色格式转换工具。

## 功能

- **HEX → RGB**：十六进制颜色码转 RGB 元组
- **RGB → HEX**：RGB 转十六进制颜色码
- **RGB → HSL**：RGB 转 HSL
- **HSL → RGB**：HSL 转 RGB
- **颜色预览**：输出适合终端显示的颜色信息

## 使用方式

```bash
# HEX 转 RGB
python3 cn_color_tool.py hex2rgb "#FF5733"

# RGB 转 HEX
python3 cn_color_tool.py rgb2hex 255 87 51

# RGB 转 HSL
python3 cn_color_tool.py rgb2hsl 255 87 51

# HSL 转 RGB
python3 cn_color_tool.py hsl2rgb 11 100 60

# 完整转换（显示所有格式）
python3 cn_color_tool.py convert "#FF5733"

# HEX 转 HSL（一步到位）
python3 cn_color_tool.py hex2hsl "#FF5733"
```

## 技术说明

- 纯 Python 标准库（`colorsys`、`argparse`）
- 无外部依赖
- HSL 中 H 范围 0-360，S/L 范围 0-100

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
