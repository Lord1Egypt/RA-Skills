# 字体文件目录

本目录用于存放自定义字体文件（.ttf, .otf 格式）。

## 使用说明

1. 将字体文件放入此目录
2. 在调用 text_to_image 时指定 font_path 参数

## 示例

```python
from scripts.txt2img import text_to_image

text_to_image(
    text="使用自定义字体",
    output_path="output.png",
    font_path="assets/fonts/your-font.ttf"
)
```

## 推荐字体

- **中文字体**: 思源黑体、微软雅黑、苹方字体
- **英文字体**: Arial、Helvetica、Roboto、DejaVu Sans