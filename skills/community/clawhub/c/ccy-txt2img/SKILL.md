---
name: ccy-txt2img
description: 本地离线图片生成技能。支持文本转图片、基础图形绘制（点线面圆等）、颜色填充与描边、简单图片合成，以及基于中文/英文描述的规则驱动智能绘制。仅依赖 Pillow，输出 PNG/JPEG。
---

# ccy-txt2img

本技能用于**本地离线生成简单图片**。仅依赖 Pillow，不调用外部 API。

## 什么时候使用

- 把中文/英文文本渲染成 PNG/JPEG
- 生成简单示意图、海报底图、流程草图、几何图形
- 根据简单中文/英文描述规则化绘图
- 用 scene JSON 精确绘制点、线、矩形、圆、文字、图标和图片图层

## 快速路径

技能目录：`skills/ccy-txt2img/`

### 文本转图片

```python
from scripts.txt2img import text_to_image

text_to_image(
    "你好，OpenClaw\n支持中文换行",
    "output.png",
    width=800,
    height=400,
    font_size=32,
    align="center"
)
```

### 描述驱动绘图

```python
from scripts.smart_draw import smart_draw

smart_draw(
    "白色背景，一个蓝色圆，一个红色矩形，一条黑线，写上：你好，开发点点",
    "smart.png"
)
```

也可以直接走 CLI：

```bash
python3 skills/ccy-txt2img/scripts/smart_draw.py \
  --prompt "现代办公室场景，有办公桌、电脑和椅子，写上：Factory Office" \
  --out office.png \
  --width 900 --height 600
```

渲染 scene JSON：

```bash
python3 skills/ccy-txt2img/scripts/smart_draw.py --scene scene.json --out scene.png
```

如需查看 prompt 解析出的 scene：加 `--print-scene`。

### scene 精确绘制

```python
from scripts.smart_draw import render_scene

scene = {
    "canvas": {"width": 800, "height": 600, "background": "#ffffff"},
    "layers": [
        {"type": "rect", "x": 60, "y": 60, "w": 200, "h": 120, "fill": "#E6F4FF", "stroke": "#1677ff", "stroke_width": 3},
        {"type": "circle", "cx": 420, "cy": 140, "r": 70, "fill": "#FFF1F0", "stroke": "#ff4d4f", "stroke_width": 3},
        {"type": "text", "text": "中英文字测试 Hello", "x": 60, "y": 260, "w": 680, "h": 120, "font_size": 30, "color": "#111111"}
    ],
    "output": {"path": "scene.jpg", "format": "JPEG"}
}

render_scene(scene)
```

## 能力边界

- 这是规则/程序化绘图，不是 Stable Diffusion / DALL·E 类真实图片生成。
- 适合简洁、可控、低成本的示意图和文字图。
- 自然语言理解基于关键词，复杂构图建议直接使用 scene JSON。

## 主要脚本

- `scripts/txt2img.py`
  - `text_to_image(...)`：保存文字图片
  - `render_text_image(...)`：内存渲染文字图层
  - `create_code_image(...)`：生成简易代码截图风格图片
- `scripts/smart_draw.py`
  - `smart_draw(...)`：描述转图片
  - `parse_description(...)`：描述转 scene
  - `render_scene(...)`：scene 渲染
  - CLI：`--prompt/--scene --out`，支持 `--width --height --background --print-scene`
- `examples.py`：示例脚本

## 验证

```bash
python3 -m compileall -q skills/ccy-txt2img/scripts
python3 skills/ccy-txt2img/examples.py
```

## 实用建议

- 中文文本优先使用系统 NotoSansCJK / 文泉驿字体；也可传 `font_path`。
- JPEG 不支持透明背景；需要透明时输出 PNG。
- 批量/并发生成时可以放心使用 `smart_draw`，文字图层在内存渲染，不再依赖固定临时文件。
