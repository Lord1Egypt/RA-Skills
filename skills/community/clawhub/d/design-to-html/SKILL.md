---
name: design-to-html
description: Convert visual design mockups/images to pixel-perfect HTML/CSS code through iterative refinement. Use when user wants to: (1) Convert a design image/screenshot to HTML code, (2) Generate web pages from visual mockups, (3) Create HTML that matches a design pixel-by-pixel, (4) Iteratively improve HTML to match visual design. Triggers on phrases like "convert design to HTML", "from image to code", "pixel-perfect HTML", "design mockup to code".
metadata:
  openclaw:
    requires:
      env: []
    primaryEnv: null
---

# Design to HTML

Convert visual design images to pixel-perfect HTML/CSS through iterative refinement with automated visual comparison.

## Workflow

```
Input: Design image (PNG/JPG)
Output: HTML/CSS code + comparison report

Process:
1. Analyze design → Generate initial HTML
2. Render HTML → Compare with original
3. Generate diff report → Optimize HTML
4. Repeat 5 times or until 95% match
5. Output final code + report
```

## Step 1: Initialize

**Command**: `/design-to-html <image-path> [--threshold 95] [--iterations 5]`

**Actions**:
1. Load design image
2. Extract dimensions (width, height)
3. Analyze visual structure (layout, colors, fonts, spacing)
4. Generate initial HTML/CSS

**Example prompt**:
```
Analyze this design mockup and generate HTML/CSS code that recreates it.

Design dimensions: {width}x{height}px
Key elements detected:
- Layout type: [grid/flex/block]
- Primary colors: [list]
- Font styles: [list]
- Spacing patterns: [list]

Generate complete HTML with inline CSS.
```

## Step 2: Render & Compare (Iteration Loop)

Run comparison script for each iteration:

```bash
node scripts/compare.js <original-image> <html-file> <output-dir> <iteration>
```

**Script outputs**:
- `rendered_<n>.png` - HTML screenshot
- `diff_<n>.png` - Visual difference map
- `report_<n>.json` - Comparison metrics

**Comparison metrics**:
- `matchScore` - Pixel similarity percentage
- `diffPixels` - Number of mismatched pixels
- `issues` - List of detected problems

## Step 3: Generate Diff Report

**Report structure** (passed to model):
```json
{
  "iteration": 2,
  "matchScore": 78.5,
  "diffPixels": 21500,
  "issues": [
    {
      "type": "color",
      "location": {"x": 100, "y": 200, "w": 50, "h": 30},
      "description": "Button background color mismatch: expected #FF5733, got #FF5722",
      "severity": "medium"
    },
    {
      "type": "spacing",
      "location": {"x": 150, "y": 100, "w": 200, "h": 50},
      "description": "Padding mismatch: expected 20px, got 15px",
      "severity": "high"
    }
  ]
}
```

## Step 4: Optimize HTML

**Model prompt template**:
```
## Iteration {iteration}/{maxIterations}

**Current match score**: {matchScore}%
**Target**: {threshold}%

**Issues detected**:
{issuesFormatted}

**Visual difference**: See diff_{iteration}.png

**Previous HTML**:
```html
{previousHtml}
```

**Optimization instructions**:
1. Fix color mismatches (use exact hex values)
2. Correct spacing/padding issues
3. Adjust layout positioning
4. Match font sizes and weights

Output optimized HTML code only.
```

## Step 5: Final Output

**Completion criteria**:
- Match score ≥ threshold (default 95%)
- OR completed max iterations (default 5)

**Output package**:
- `final.html` - Final HTML/CSS code
- `comparison_report.md` - Iteration history
- `rendered_final.png` - Final screenshot
- `diff_final.png` - Final comparison
- `timeline/` - All iteration screenshots

## Scripts

### render.js
Render HTML to PNG screenshot using Puppeteer.

```bash
node scripts/render.js <html-file> <output-image> [--width 1920] [--height 1080]
```

### compare.js
Pixel-level comparison using pixelmatch.

```bash
node scripts/compare.js <original> <rendered> <diff-output> [--threshold 0.1]
```

### analyze.js
Analyze design image structure.

```bash
node scripts/analyze.js <image-file> <output-json>
```

### pipeline.js
Run full iteration pipeline.

```bash
node scripts/pipeline.js <original-image> [--threshold 95] [--iterations 5] [--output-dir ./output]
```

## Setup

Install dependencies:

```bash
cd ~/.openclaw/skills/design-to-html
npm install
```

**Dependencies**:
- puppeteer - HTML rendering
- pixelmatch - Pixel comparison
- pngjs - PNG processing
- sharp - Image analysis

## Examples

### Simple button design
```
Input: button.png (200x50px)
Iterations: 3
Final score: 96.2%
Time: ~25s
```

### Card component
```
Input: card.png (400x300px)
Iterations: 5
Final score: 91.8%
Time: ~45s
```

### Full page layout
```
Input: landing-page.png (1920x1080px)
Iterations: 5
Final score: 87.5%
Time: ~90s
```

## Tips

1. **Higher threshold** → More iterations, better accuracy
2. **Larger images** → More diff pixels, harder to reach threshold
3. **Complex layouts** → May need manual tweaks after automation
4. **Color precision** → Use exact hex values from design
5. **Font matching** → Specify exact font-family, size, weight

## Limitations

- Requires Node.js + Puppeteer (headless Chrome)
- May struggle with:
  - Complex gradients
  - SVG icons
  - Custom fonts (not web-safe)
  - Animations/transitions
- Best for static, flat designs