# PPTX 常用模式参考

## Table of Contents
- [EMU 单位速查](#emu)
- [预设形状 ID](#shapes)
- [对角线连接器 XML](#connector)
- [淡入过渡 XML](#transition)
- [文字框多段落](#textbox)
- [典型脚本结构](#template)

---

## EMU 单位速查 {#emu}

| 描述 | EMU |
|------|-----|
| 1 磅 (pt) | 12700 |
| 1 英寸 | 914400 |
| 1 厘米 | 360000 |
| 16:9 幻灯片宽度 | 12192000 |
| 16:9 幻灯片高度 | 6858000 |
| 4:3 幻灯片宽度 | 9144000 |
| 4:3 幻灯片高度 | 6858000 |

```python
from pptx.util import Pt, Emu, Inches, Cm
Pt(12)        # 12磅
Inches(1)     # 1英寸
Cm(2.5)       # 2.5厘米
Emu(914400)   # 直接指定 EMU
```

---

## 预设形状 ID {#shapes}

`slide.shapes.add_shape(shape_type_id, left, top, width, height)`

| ID | 形状 |
|----|------|
| 1  | 矩形 (rect) |
| 5  | 圆角矩形 (roundRect) |
| 9  | 椭圆 / 圆形 (ellipse) |
| 13 | 三角形 (triangle) |
| 17 | 六边形 (hexagon) |
| 24 | 右箭头 (rightArrow) |

完整列表见 `pptx.enum.shapes.MSO_SHAPE_TYPE`。

---

## 对角线连接器 XML {#connector}

通过 `pptx_helpers.diag_connector()` 生成，内部结构：

```xml
<p:cxnSp xmlns:p="..." xmlns:a="..." xmlns:r="...">
  <p:nvCxnSpPr>
    <p:cNvPr id="{id}" name="conn{id}"/>
    <p:cNvCxnSpPr/><p:nvPr/>
  </p:nvCxnSpPr>
  <p:spPr>
    <a:xfrm [flipH="1"]>
      <a:off x="{left_emu}" y="{top_emu}"/>
      <a:ext cx="{width_emu}" cy="{height_emu}"/>
    </a:xfrm>
    <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
    <a:ln w="{width_emu}">
      <a:solidFill><a:srgbClr val="{RRGGBB}"/></a:solidFill>
      <a:round/>
    </a:ln>
  </p:spPr>
</p:cxnSp>
```

`flipH="1"` 规则：`(x2 < x1) XOR (y2 < y1)` 为真时加入，控制连线斜向。

---

## 淡入过渡 XML {#transition}

```xml
<p:transition xmlns:p="..." xmlns:a="..." spd="med" advClick="1">
  <p:fade/>
</p:transition>
```

- `spd`：`slow` | `med` | `fast`
- `advClick="1"`：点击前进，`advTm="3000"` 可自动前进（毫秒）
- 插入位置：必须在 `<p:cSld>` 之后，用 `cSld.addnext(elem)` 插入

其他过渡效果：`<p:wipe dir="l"/>` 左划、`<p:push dir="l"/>` 推入、`<p:zoom/>` 缩放。

---

## 文字框多段落 {#textbox}

```python
from pptx.util import Pt, Emu
from pptx.enum.text import PP_ALIGN

shp = slide.shapes.add_shape(1, left, top, width, height)
tf = shp.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = Emu(55000)
tf.margin_top  = tf.margin_bottom = Emu(28000)

for i, line in enumerate(text.split('\n')):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = p.space_after = Pt(0)
    run = p.add_run()
    run.text = line
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    run.font.bold = True
```

---

## 典型脚本结构 {#template}

```python
#!/usr/bin/env python3
from pptx import Presentation
from pptx.util import Emu
from pptx.dml.color import RGBColor
from pptx_helpers import bg_rect, h_line, textbox, add_fade_transition

SW, SH = 12192000, 6858000   # 16:9

prs = Presentation()
prs.slide_width  = Emu(SW)
prs.slide_height = Emu(SH)
layout = prs.slide_layouts[6]   # blank（无占位符）

def draw_skeleton(slide):
    bg_rect(slide, RGBColor(0x06,0x0D,0x1E), SW, SH)
    # ... 骨架元素

def draw_layer_a(slide):
    pass  # 第一组数据

def draw_layer_b(slide):
    pass  # 第二组数据

# 多幻灯片渐进展示（WPS 兼容）
for show_a, show_b in [(False, False), (True, False), (True, True)]:
    s = prs.slides.add_slide(layout)
    draw_skeleton(s)
    if show_a: draw_layer_a(s)
    if show_b: draw_layer_b(s)
    add_fade_transition(s)

prs.save('output.pptx')
print('✓ Saved: output.pptx')
```
