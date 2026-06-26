slug: cn-color-converter
name: 颜色格式转换器
version: "1.0.0"
description: |
  Color Converter skill.
  自动生成，无人工审查。
metadata: {"openclaw": {"emoji": "🔧"}}

# 颜色格式转换器


在不同颜色格式之间转换：HEX、RGB、RGBA、HSL、HSLA、CMYK。

## 功能

- HEX → RGB/HSL 转换
- RGB → HEX/HSL/CMYK 转换
- HSL → HEX/RGB 转换
- 颜色预览（输出ASCII预览）

## 使用方法

```bash
# HEX转RGB
python3 cn_color_converter.py "#FF5733"

# RGB转HEX
python3 cn_color_converter.py "rgb(255, 87, 51)"

# HEX转HSL
python3 cn_color_converter.py "#3498db" --hsl

# 颜色预览
python3 cn_color_converter.py "#E74C3C" --preview

# 调色板生成
python3 cn_color_converter.py "#3498db" --palette 5
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `color` | 输入颜色（位置参数） | 必填 |
| `--rgb` | 输出RGB格式 | False |
| `--hex` | 输出HEX格式 | False |
| `--hsl` | 输出HSL格式 | False |
| `--cmyk` | 输出CMYK格式 | False |
| `--preview` | 显示颜色预览 | False |
| `--palette` | 生成调色板数量 | 0 |

## 示例

```bash
# 基本转换
python3 cn_color_converter.py "255, 87, 51"
python3 cn_color_converter.py "hsl(120, 60%, 50%)"

# 生成5色渐变调色板
python3 cn_color_converter.py "#3498db" --palette 5
```

## 依赖

- Python 3.x（内置）

## 注意事项

- 支持格式：#RGB、#RRGGBB、rgb(r,g,b)、hsl(h,s%,l%)

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
