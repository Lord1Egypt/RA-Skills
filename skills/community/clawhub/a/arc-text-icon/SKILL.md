---
name: arc-text-icon
description: Generate upper-arc (上弧形) Chinese text icons for packaging, seals, badges, banners, or outer labels. Produces characters laid out along a circular arc with the text heads pointing outward (字头朝外), supports customizable text, font (黑体/宋体/楷体), color, stroke, arc curvature, font size, transparent or colored backgrounds. Triggers on requests like "上弧形文字"、"上弧形排版"、"弧形文字图"、"印章弧形字"、"packaging arc text"、"concentric arc characters".
---

# Arc Text Icon (上弧形文字图标)

Render Chinese (or any CJK/Latin) text along an upper-arc curve with characters standing upright on the arc tangent and text heads pointing outward. Output is suitable for outer packaging labels, gift box stickers, badges, seal decorations, banner headings, and similar design artifacts.

## Changelog

- **v1.0.2** (2026-07-14) - 三个隐藏 bug 修复：
  - **几何公式 bug**：`compute_positions` 调用方的 `cy` 修正——原本 `cy = y_top + r`（画布外），现改为 `cy = y_top`（弧顶位置）
  - **render facecolor bug**：transparent 模式下 `fig = plt.figure(facecolor='white')` 与 `savefig(transparent=True)` 冲突，导致输出为白底纯白图；现改为 `facecolor='none'`
  - **self_check 假成功 bug**：原 `self_check` 只检查 `alpha > 100`，导致纯白图（alpha=255 + RGB=255）也会报 1.12M 像素 PASS；现改为必须同时检查 `alpha > 128 AND RGB_max < 200`
- **v1.0.1** (2026-07-14) - 脱敏版：原示例文字替换为占位符"在此填入要生成的文字"（不显示具体内容）
- **v1.0.0** (2026-07-14) - 首版发布

## File Naming Convention (强制规范)

**Pattern**: `YYYY-MM-DD+vN+说明.png`

- `YYYY-MM-DD` 创作/发布日期（必填）
- `vN` 版本号 `v1, v2, v3 ...`（必填，从 v1 起递增）
- `说明` 简短文字描述（可省，例如"问候语"）

**Examples**:
- `2026-07-14+v1+问候语.png`
- `2026-07-14+v2.png`（纯版本号也可）
- `2026-07-14+v1+问候语_预览.png`（白底预览后缀 `_预览`）

**Rationale**: 当后续生成新版本图时，日期+版本号前缀确保不会与历史文件混淆。

When using `--out`, pass the full filename including date and version. The script auto-appends `_预览.png` for the white-bg variant.

## Quick Start

```bash
python3 scripts/render_arc_text.py \
  --text "在此填入要生成的文字" \
  --font-size 78 \
  --half-angle-deg 55 \
  --chord 1500 \
  --font kai \
  --color "#000000" \
  --canvas 1600 700 \
  --out 2026-07-14+v1+文字说明.png \
  --transparent
```

The script writes the **main PNG** (transparent or colored background per request) plus a **white-background preview PNG** (`my_icon_预览.png`) so the result is immediately visible in chat tools (some IM clients render transparent PNGs as blank).

## Hard Constraints (must verify before delivery)

Three checks must pass before sending any rendered image to the user:

1. **Strong-pixel self-check**: open the PNG with PIL and verify `nonzero alpha > 100` pixel count > 5000. Empty / near-empty output means geometry placed all characters off-canvas — re-verify the math.
2. **Coverage range**: non-transparent pixels should span `y ∈ [50, canvas_h-50]` and `x ∈ [50, canvas_w-50]`. Values clustered in a corner indicate `polar formula` direction error.
3. **White-bg preview**: always also write a `_预览.png` on a white background. Transparent PNGs render blank in many IM clients (Feishu/Telegram/Slack) and produce "看不到文字" complaints.

## Core Geometry (read this before tuning)

The arc is part of a circle with center `(cx, cy)` BELOW the canvas and radius `r`. The text lies on the upper arc — half-angle `θ` measured from vertical.

```
cx = canvas_w / 2
cy = y_top + r                    # r 是弧半径, y_top 是弧顶在画布的 y 坐标
chord = 2 * r * sin(half_angle)   # 弦水平投影宽 = 文字实际占据的水平宽度
h_arc = r * (1 - cos(half_angle)) # 中间高、两端低的高度差
y_chord = cy - h_arc              # 弦端点 y 坐标

对第 i 个字符 (i = 0..n-1):
  progress = (i + 0.5) / n                              # 等分, 不加 padding
  theta    = half_angle * (2 * progress - 1)            # 范围 [-half_angle, +half_angle]
  dx       = cx + r * sin(theta)                         # x 用 sin 拉开
  dy       = cy - r * (1 - cos(theta))                   # y 用 cos 上凸
  rotation = -degrees(theta)                             # 字头朝外, baseline 沿切线
```

**Common pitfall (v1–v20 历史教训):**

- ❌ `dx = cx + r * cos(theta)` — 所有字符 dx 相同, 全部堆在画布中央 (cos 是偶函数)
- ✅ `dx = cx + r * sin(theta)` — sin 拉开左右
- ❌ `rotation = +theta` — 字头朝圆心
- ✅ `rotation = -theta` — 字头朝外

**Another common pitfall:**

- ❌ `r = chord / (2 * sin(half_angle))` with `chord = text_width` — r 远大于画布高度, 圆心被推得极远
- ✅ 让 `r < canvas_h`, 由 `r = canvas_h * 0.7~0.9` 反算 `half_angle`

## Spacing (字中心间距 ≠ 弦长 / 字号)

The user's complaint "字距不够 / 文字有重叠" usually comes from this mistake:

- `matplotlib ax.text(fontsize=N)` actually renders character ink width ≈ `1.05 * N` (for CJK), not `N`
- 字中心间距 = `chord / (n-1)` 或 `chord / n` (per design)
- 避免重叠的条件: **字中心间距 > 字宽 + 5 px**

| 字号 (font_size) | 字宽 ≈ 1.05*N | 12 字推荐 chord | 12 字实际间距 (chord/11) | 是否安全 |
|---|---|---|---|---|
| 60 | 63 | 800 | 73 | ✓ |
| 70 | 74 | 900 | 82 | ✓ |
| 80 | 84 | 1100 | 100 | ✓ |
| 90 | 95 | 1200 | 109 | 边界 |
| 100 | 105 | 1400 | 127 | 边界 |
| 110 | 116 | 1500 | 136 | ✗ 重叠 |

**Default safe settings for 12 chars:** `font_size=78, chord=1500, half_angle=55°` → spacing 146 px vs 字宽 84 px → 间隙 62 px ✓

## Parameters

| Param | Default | Notes |
|---|---|---|
| `--text` | required | 字符串, 12 字左右最稳定 |
| `--font-size` | 78 | 见上表 |
| `--half-angle-deg` | 55 | 25° 平缓 / 45° 适中 / 55° 明显 / 70° 陡 |
| `--chord` | 1500 | 弦水平投影宽, 12 字推荐 1400-1600 |
| `--font` | kai | kai (AR PL UKai CN) / song (Noto Serif CJK) / hei (Noto Sans CJK) |
| `--color` | #000000 | 文字色 |
| `--stroke-color` | none | 描边色 (空=无描边) |
| `--stroke-width` | 2 | 描边粗细 |
| `--canvas` | 1600 700 | 画布宽高 |
| `--transparent` | flag | 透明底; 否则用 `--bg` 颜色 |
| `--bg` | #FFFFFF | 非透明时的底色 |

## Bundled Resources

- `scripts/render_arc_text.py` — CLI wrapper that takes all parameters, writes both transparent and white-bg versions, runs strong-pixel self-check, and refuses to write empty output (exit 1 with diagnostic).
- `references/params.md` — Extended parameter tuning guide with worked examples for 8/10/12/14 char strings, half-angle vs curvature mapping, and font selection guide.
- `assets/sample_fonts.txt` — Lists the CJK fonts available on this system with their role (楷体 / 宋体 / 黑体).

## Common Use Cases

1. **外包装贴纸 / Outer packaging label**: transparent bg, kai or hei, black or red text, 12-16 chars along half-angle 50-60°
2. **印章异形 / Seal-style**: red text + gold stroke, smaller font, 8-10 chars, half-angle 60-70°
3. **横幅标题 / Banner heading**: black-bg with white text, larger font, half-angle 25-35°
4. **礼品盒贴 / Gift box sticker**: gold text + no stroke, white bg, half-angle 45-55°

## Known Failure Modes

| Symptom | Root cause | Fix |
|---|---|---|
| Empty PNG (0 strong pixels) | `polar formula` placed all characters off-canvas | Verify `dy ∈ [50, canvas_h-50]` for all characters before render |
| Characters all stacked in one corner | `dx = cx + r*cos(theta)` (cos is even) | Use `dx = cx + r*sin(theta)` |
| Characters all tilted inward | `rotation = +theta` | Use `rotation = -theta` |
| "看不到文字" complaint | Only transparent PNG delivered | Always also write `_预览.png` on white bg |
| "字距不够" complaint | font_size too large for chord / n | Either shrink font_size or widen chord (see table) |
| Padding didn't change spacing | `progress_padding` formula was wrong | Use direct `(i+0.5)/n`, padding only adjusts end-margin, not inter-character spacing |

## Iteration Checklist

After every parameter change, verify:

1. `python3 -c "from PIL import Image; import numpy as np; im = Image.open('out.png'); a = np.array(im); print('pixels:', (a[...,-1]>100).sum() if a.shape[-1]==4 else 'no-alpha')"`
2. Open `_预览.png` in viewer, visually scan that:
   - All characters are visible
   - No two characters overlap
   - The arc shape is clearly upper-curved (middle higher than ends)
   - Character heads point outward, not inward
3. If any fails, re-check geometry math BEFORE rerendering