---
name: blackboard
version: 1.0.2
description: >
  根据关键词生成深色海报风格插图（竖版 9:16），类似"保姆级教程"封面图风格。
  特点：深灰/黑色背景、白色细边框、大字居中中文、高对比度配色（青柠绿+珊瑚红）、
  **手写马克笔字体风格**（厚笔触、不规则边缘、真实马克笔质感）、
  顶部品牌区、中部标题区、底部标签语，悬挂于白色砖墙。
  触发场景：用户说"生成一张海报"、"做个封面图"、"这种风格的图怎么做"、
  "生成黑底白字的设计图"，或上传参考图要求生成类似风格。
---

# 黑板海报生成器

## 工作流

1. 理解用户意图 → 提取主题、品牌、色调关键词
2. 构建结构化提示词（深色海报 + 马克笔字体）
3. 调用 image_synthesize 生成图片
4. 发给用户图片 + 提示词文本

---

## 构图结构（五段式）

```
+------------------------------------------+
|  [品牌区]   [图标]   [品牌名]           |  ← 顶部灰/白色条
+------------------------------------------+
|                                          |
|           [大字主标题 - 白马克笔]         |  ← 中部主标题
|       [副标题词1 - 青柠绿马克笔]          |
|       [副标题词2 - 珊瑚红马克笔]          |
|           [补充词 - 青柠绿马克笔]          |
|                                          |
+------------------------------------------+
|          [底部标签语 - 白马克笔]          |  ← 底部说明
+------------------------------------------+
```

---

## 核心提示词模板

```
[VERTICAL 9:16 POSTER - DARK BACKGROUND]
Portrait orientation, 9:16 aspect ratio.

[BACKGROUND & FRAME]
Dark charcoal grey background (#1a1a1a), thin white border around edges.
Poster hangs on white brick wall, held by [N] small black clips at top.
Two thin strings connecting clips to wall.

[TOP BRAND ZONE - optional]
Top strip area:
- Left: '[品牌英文名]' in bold white sans-serif font
- Center: [品牌图标描述] (small icon/logo)
- Right: '[品牌名]' in bold white sans-serif font

[MAIN HEADLINE ZONE - centered, HANDWRITTEN MARKER STYLE]
Line 1 (large, bold white handwritten marker): '[主标题 - 中文]'
Line 2a (medium, lime green #ADFF2F handwritten marker): '[关键词/亮点1]'
Line 2b (medium, coral red #FF6B6B handwritten marker): '[关键词/亮点2]'
Line 3 (small, lime green handwritten marker): '[补充信息]'

[BOTTOM TAG ZONE]
Bold white handwritten marker text, centered: '[底部标签语]'

[TEXT STYLE - CRITICAL]
All Chinese text rendered in BOLD HANDWRITTEN MARKER STYLE:
- Thick marker strokes, uneven line weight like real marker on dark surface
- Slight imperfections, natural hand-drawn wobble
- Characters appear to be written with a broad-tip white/chalk marker
- NOT clean sans-serif font — must look like actual hand-lettering
- High contrast on dark background, centered alignment
- Minimalist design, no clutter
```

---

## 配色方案

| 用途 | 颜色名称 | 提示词关键词 |
|------|---------|-----------|
| 背景 | 深炭灰 | dark charcoal grey #1a1a1a |
| 主文字 | 白/马克笔白 | bold white marker, chalk white |
| 强调色1 | 青柠绿 | lime green #ADFF2F marker |
| 强调色2 | 珊瑚红 | coral red #FF6B6B marker |
| 品牌区 | 浅灰 | light grey strip |

---

## 构图变体

### 变体A：极简大字体（推荐）
无品牌区，整个海报只有主标题，大字马克笔撑满画面，底部一行小字标签语

### 变体B：双品牌对比
顶部两个品牌LOGO并列，中间大字马克笔，中间关键词分色

### 变体C：数字+标签
大数字居中（珊瑚红马克笔），单位白马克笔，解释白马克笔小字

### 变体D：人物+主题
顶部小头像，中部大字白马克笔，底部标签语白马克笔

---

## 调用格式

```python
image_synthesize(
  requests=[{
    "prompt": "完整英文提示词（见上方模板组装）",
    "output_file": "/workspace/[英文主题]_poster.png",
    "aspect_ratio": "9:16",
    "resolution": "2K"
  }]
)
```

## 输出规则

- 文件路径：`/workspace/[英文主题]_poster.png`
- aspect_ratio **必须为 `"9:16"`**（竖版海报）
- 生成后用 `message` tool 发给用户（channel=feishu）
- 附上**完整英文提示词**供用户保存复用
- 中文字由 AI 生成，仅供参考；正式使用建议叠加精准字体文字

## 参考资源

- 配色与风格参考：`references/style-guide.md`
- 构图模板库：`references/layout-templates.md`
