---
name: color-toolkit
description: 专业颜色工具集，支持颜色编码转换、对比度计算、智能颜色推荐、HTML预览生成。适用于UI设计、无障碍开发、配色方案生成等场景。
author: wUwproject
version: 1.0.1
tags:
  - color
  - color-conversion
  - contrast
  - accessibility
  - design
  - wcag
---

# Color Toolkit - 专业颜色工具集

## 概述

Color Toolkit 是一个通用的颜色处理工具包，提供：
- **颜色编码转换**：HEX ↔ RGB ↔ HSL ↔ HSV ↔ CMYK 全支持
- **对比度计算**：WCAG 2.1、APCA、CIELAB ΔE*ab、CIEDE2000 四种算法
- **智能颜色推荐**：根据用户描述生成配色方案
- **HTML预览生成**：实时预览颜色效果

## 触发场景

当用户请求以下操作时自动加载：
- "转换颜色"、"颜色格式转换"、"HEX转RGB"等
- "计算对比度"、"颜色对比"、"无障碍对比"等
- "推荐颜色"、"配色方案"、"根据描述生成颜色"等
- "生成颜色预览"、"显示颜色"、"预览HTML"等

## 核心功能

### 1. 颜色编码转换

```
输入格式支持：
- HEX: #FF5733, #F53
- RGB: rgb(255, 87, 51), 255, 87, 51
- HSL: hsl(11, 100%, 60%), 11, 100, 60
- HSV: 11, 100, 60
- CMYK: 0, 66, 100, 0

输出格式：
- HEX: #FF5733
- RGB: RGB(r=255, g=87, b=51)
- HSL: HSL(h=11.0, s=100.0, l=60.0)
- HSV: HSV(h=11, s=100, v=60)
- CMYK: CMYK(c=0, m=66, y=100, k=0)
```

### 2. 对比度计算（四种算法）

| 算法 | 用途 | 评估标准 |
|------|------|----------|
| WCAG 2.1 | 无障碍标准 | ≥4.5:1 (AA) / ≥7:1 (AAA) |
| APCA | 现代对比度 | ≥45 Lc (可读) / ≥75 Lc (优秀) |
| CIELAB ΔE*ab | 精确色差 | ≤2 (不可辨) / ≤10 (微小) |
| CIEDE2000 | 专业色差 | ≤1 (完美) / ≤2 (接近) |

### 3. 智能颜色推荐

**输入**：用户描述（中文/英文）
**处理**：LLM解析语义 → 提取关键词 → 映射到色彩空间
**输出**：
- 主色（1个）
- 辅助色（2-3个）
- 强调色（1个）
- 背景/文字色建议

### 4. HTML预览生成

生成的HTML包含：
- 颜色色块展示
- 渐变效果预览
- 对比度示例
- 文本可读性测试
- 无障碍合规提示

## 使用方式

### 方式一：直接对话（推荐）

```
用户：请帮我转换颜色 #3498db 到所有格式
用户：计算 #000000 和 #ffffff 的对比度
用户：推荐一套科技感的配色方案
用户：生成这个颜色的预览页面
```

### 方式二：CLI调用

```bash
# 颜色转换
python color_toolkit.py convert "#3498db"

# 对比度计算
python color_toolkit.py contrast "#000000" "#ffffff" --algorithm wcag2

# 颜色推荐
python color_toolkit.py recommend "科技感 蓝色"

# HTML预览
python color_toolkit.py preview "#3498db" --output preview.html
```

## 输出格式

### 颜色转换结果示例

```json
{
  "input": "#3498db",
  "result": {
    "hex": "#3498db",
    "rgb": {"r": 52, "g": 152, "b": 219},
    "hsl": {"h": 204.0, "s": 69.8, "l": 53.1},
    "hsv": {"h": 204, "s": 76, "v": 86},
    "cmyk": {"c": 76, "m": 31, "y": 0, "k": 14},
    "luminance": "0.215",
    "grayscale": 130,
    "temperature": "冷色",
    "family": "蓝色系"
  }
}
```

### 对比度计算结果示例

```json
{
  "color1": "#000000",
  "color2": "#ffffff",
  "algorithms": {
    "wcag2": {
      "value": "21.00:1",
      "level": "AAA级",
      "pass": true
    },
    "apca": {
      "value": 106.3,
      "level": "优秀",
      "pass": true
    },
    "cielab": {
      "value": "100.00 ΔE",
      "level": "极大差异",
      "pass": true
    },
    "ciede2000": {
      "value": "100.00 ΔE00",
      "level": "极大差异",
      "pass": true
    }
  }
}
```

### 颜色推荐结果示例

```json
{
  "request": "科技感 蓝色",
  "palette": {
    "primary": {"hex": "#0066FF", "name": "科技蓝"},
    "secondary": [
      {"hex": "#00D4FF", "name": "电光青"},
      {"hex": "#1A1A2E", "name": "深空灰"}
    ],
    "accent": {"hex": "#00FF88", "name": "信号绿"},
    "background": "#0A0A14",
    "text": "#FFFFFF"
  },
  "preview_url": "palette_preview.html"
}
```

## 技术实现

### 依赖
- Python 3.8+
- 仅使用标准库（math, re, random, dataclasses, typing）

### 文件结构

```
color-toolkit/
├── SKILL.md              # 本说明文档
├── color_toolkit.py      # 核心模块
├── cli.py                # CLI入口
├── preview_generator.py  # HTML预览生成
└── color_recommender.py  # 智能推荐
```

## 注意事项

1. **输入验证**：HEX格式支持3位和6位简写
2. **边界处理**：RGB值自动裁剪到0-255范围
3. **性能**：颜色转换无外部依赖，毫秒级响应
4. **无障碍**：WCAG对比度是UI设计的必备检查项

## 示例对话

```
用户：#FF5733 是什么颜色？
助手：
- **HEX**: #FF5733
- **RGB**: RGB(r=255, g=87, b=51)
- **HSL**: HSL(h=11, s=100%, l=60%)
- **色系**: 暖色 / 橙红系
- **亮度**: 0.384（较高）
- **预览**: [生成HTML预览]

用户：计算这个颜色和白色的对比度
助手：
- **WCAG 2.1**: 3.97:1 (大文本AA级) ⚠️
- **APCA**: 58.2 Lc (良好)
- **结论**: 小文本可能不符合AA标准，建议增加对比度

用户：给我一套春天主题的配色
助手：
- **主色**: #4CAF50 (生机绿)
- **辅助**: #E8F5E9 (浅芽绿), #FF9800 (迎春黄)
- **强调**: #E91E63 (桃花粉)
- **预览**: [生成春意盎然的HTML预览]
```
