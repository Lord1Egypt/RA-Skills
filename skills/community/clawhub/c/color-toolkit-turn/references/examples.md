# 输出示例

> 本文件展示 color-toolkit 各功能的输出格式示例。

## 颜色转换

输入 `#3498db`：

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

## 对比度计算

计算 `#000000` 和 `#ffffff` 的对比度：

```json
{
  "color1": "#000000",
  "color2": "#ffffff",
  "algorithms": {
    "wcag2": {"value": "21.00:1", "level": "AAA级", "pass": true},
    "apca": {"value": 106.3, "level": "优秀", "pass": true},
    "cielab": {"value": "100.00 ΔE", "level": "极大差异", "pass": true},
    "ciede2000": {"value": "100.00 ΔE00", "level": "极大差异", "pass": true}
  }
}
```

## 颜色推荐

输入"科技感 蓝色"：

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
