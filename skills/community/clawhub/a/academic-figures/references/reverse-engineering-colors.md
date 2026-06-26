# Reverse-Engineering Chart Colors from Reference Images

When a user says "match the colors/style of this chart," do NOT eyeball it.
Extract exact pixel values programmatically. This technique was used to
derive the `glm` theme for `academic-figures`.

## Step 1: Get the dominant colors

```python
from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('reference.png')
arr = np.array(img)
pixels = arr[:, :, :3].reshape(-1, 3)

# Round to nearest 16 for grouping similar shades
rounded = (pixels // 16 * 16).astype(int)
colors = Counter(map(tuple, rounded))

for color, count in colors.most_common(20):
    r, g, b = color
    hex_c = f'#{r:02X}{g:02X}{b:02X}'
    pct = count / len(pixels) * 100
    print(f'{hex_c} RGB({r:3d},{g:3d},{b:3d}) {pct:5.1f}%')
```

**How to interpret results:**
- The largest cluster (~70-80%) is the background
- The 2nd and 3rd largest colored clusters are the bar fill colors
- Small percentages of black are text/hatch lines

## Step 2: Separate background from bar fills

Background is usually the single most common color. For publication charts
it's white `#FFFFFF` or near-white `#F0F0F0`.

Bar fill colors appear as distinct hue clusters. Filter by saturation:
```python
# Only keep colored pixels (skip white/gray/black)
for color, count in colors.most_common(50):
    r, g, b = color
    mx, mn = max(color), min(color)
    if mx - mn > 15 and 30 < mx < 235:  # has color saturation
        print(f'Bar fill candidate: #{r:02X}{g:02X}{b:02X}')
```

## Step 3: Detect hatching

Hatching creates alternating bright/dark bands WITHIN a bar. Scan brightness
along a single column through the bar interior:

```python
# Find a dense colored column (bar interior)
col_counts = colored_mask.sum(axis=0)
densest_x = np.argmax(col_counts)

# Scan brightness vertically
brightness = arr[:, densest_x, :3].mean(axis=1)
# Count transitions between light and dark
median_b = np.median(brightness[colored_mask[:, densest_x]])
above = brightness > median_b
transitions = np.sum(np.abs(np.diff(above.astype(int))) > 0)
# transitions > 8 in a single bar = hatching present
```

For diagonal hatching: transitions appear in BOTH horizontal scans (along a
row) and vertical scans (along a column). For horizontal-only hatching:
transitions only in vertical scans.

## Step 4: Extract hatch line color

Sample the darkest pixels within a bar region:
```python
# Within a known bar area, find the darkest pixels
bar_region = arr[y_start:y_end, x_start:x_end, :3]
dark_mask = bar_region.mean(axis=2) < 50  # brightness < 50
dark_pixels = bar_region[dark_mask]
hatch_color = dark_pixels.mean(axis=0)  # usually [0, 0, 0] = black
```

## Worked example: GLM-5.2 blog fig6

```
Background:  #F0F0F0  (80.9%, off-white)
Blue fill:   #70A0D0  ( 2.1%, dusty blue)
Orange fill: #D09050  ( 8.2%, sandy orange)
Hatch lines: #000000  ( 3.7%, pure black)
Ratio text:  #C03030  ( 0.3%, muted red)

Hatch pattern: diagonal (/), every ~30px horizontal, ~22px vertical
Hatch on: ALL bars (both series, both tall and short)
```
