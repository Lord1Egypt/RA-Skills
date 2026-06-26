# Academic Figures — Pitfalls

## matplotlib not found in Hermes venv

The hermes-agent runs in its own venv (`~/.hermes/hermes-agent/venv/`), NOT the system python. If `gen_figure.py` fails with `ModuleNotFoundError: No module named 'matplotlib'`, install into the correct venv:

```bash
which python3
python3 -m pip install matplotlib numpy
```

Do NOT use `pip3 install --break-system-packages` — that installs into `/usr/lib/python3/`, which the hermes agent doesn't use.

## CJK font detection in venv

If `--cjk` flag fails to find fonts, check:
```bash
fc-list :lang=zh | head -5
```
If fonts exist but CJK rendering shows boxes, the venv's matplotlib cache may be stale. Clear it:
```bash
python3 -c "import matplotlib; print(matplotlib.get_cachedir())"
rm -rf <that_path>
```

## White background is MANDATORY (zero tolerance)

This skill generates **publication-quality figures for journal submissions** (Nature, Lancet, Science). All output MUST use white background (`facecolor='white'`).

**NEVER add a dark/black theme.** Dark backgrounds are only for presentation slides or tech blogs — NOT academic publications. This rule was violated once (v1.5.0 dev) and the user corrected it firmly. The `save_kwargs["facecolor"]` is hardcoded to `'white'` and must not be changed.

If a user asks for a dark-themed chart, redirect them to the `data-viz` or `creative` skills instead.

## Hatching: ALL bars must have patterns

When `--hatch` is enabled, **every** bar series gets a hatching pattern — not just the second series. The original GLM-5.2 blog figures (the design reference) show hatching on both short and tall bars. This was corrected by the user: "高、矮柱状图都是有斜纹的".

`HATCH_PATTERNS` has NO `None` entry — the first item is `'//'` so even the first series gets hatched. Different patterns (`//`, `\\`, `||`, `--`, `++`, `xx`) distinguish series even in black-and-white print.

**Hatch line color = black (`edgecolor='black'`)**, NOT a darkened version of the fill color. The original reference uses pure black `#000000` hatch lines on colored fills. Do not use `_darken_color()` for this — it produces inconsistent contrast on light fills like yellow.

## Color saturation: prefer muted/elegant over vibrant

The user explicitly rejected vibrant/saturated colors (`#2563EB`, `#F97316`) as "油腻俗气" (greasy/tacky). Publication figures should use **muted, low-saturation tones** — the aesthetic is 素雅 (elegant/underated).

The `glm` theme uses pixel-extracted colors from the GLM-5.2 blog:
- Blue: `#70A0D0` (dusty blue, NOT `#2563EB`)
- Orange: `#D09050` (sandy/khaki orange, NOT `#F97316`)
- Green: `#30B080` (muted teal-green)

When creating new themes or adjusting colors, keep saturation low. A good rule: if a color looks like it belongs on a startup landing page, it's too saturated for an academic figure.

## How to extract exact colors from a reference image

When a user provides a reference image and asks you to match its color scheme, do NOT guess — extract pixel data:

```python
from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('reference.png')
arr = np.array(img)
# Round to nearest 16 for grouping, find dominant non-white/black colors
pixels = arr[:, :, :3].reshape(-1, 3)
rounded = (pixels // 16 * 16).astype(int)
colors = Counter(map(tuple, rounded))
# Top colors by frequency → actual fill colors used in the chart
```

For hatching detection: scan brightness along a single column through a bar interior. Alternating bright/dark bands = hatching. Check both horizontal and vertical directions to determine if lines are diagonal.

See `references/reverse-engineering-colors.md` for a complete worked example.

## Composite figures: tight_layout conflict

Composite charts (`-t composite`) use GridSpec internally and call `fig.add_subplot()` directly. The main `plt.tight_layout()` call is **skipped** for composite/diagram types (signaled by the generator returning the string `"composite"` or `"diagram"`). If you add new self-managed chart types, ensure they return a sentinel string from the generator function so `main()` skips both `apply_base_style()` and `tight_layout()`.

## Diagram coordinate system

The diagram type uses an arbitrary coordinate space (not data coordinates). Block positions (`x`, `y`, `w`, `h`) are in abstract units. The axis limits auto-expand to fit all blocks with 1-1.5 units padding. Arrow connection points are calculated at block edges (midpoint of the facing edge). For complex layouts, plan block positions on paper first.
