# Typography Guide for Car Advertisements

## Font Pairing Recommendations

### Primary Pairing (Recommended)
**Chinese**: 思源黑体 Source Han Sans / Noto Sans SC
- Headline: Bold (700)
- Subtitle: Light (300)
- Body: Regular (400)

**English**: Montserrat
- Headline: Extra Bold (800)
- Subtitle: Light (300)
- Body: Medium (500)

### Alternative Pairings

**Luxury/Premium**:
- Chinese: 方正兰亭黑
- English: Playfair Display + Lato
- Character: Elegant, high contrast

**Sporty/Dynamic**:
- Chinese: 汉仪旗黑
- English: Bebas Neue + Roboto
- Character: Condensed, impactful

**Tech/Modern**:
- Chinese: 阿里巴巴普惠体
- English: Inter + Space Grotesk
- Character: Geometric, clean

## Size Hierarchy (1080x1920px)

### Large Format (Hero)
```
Headline:     80-100px  (Bold)
Subtitle:     32-40px   (Light)
Slogan:       48-56px   (Medium)
Details:      20-24px   (Regular)
Logo:         100-150px width
```

### Medium Format (Social)
```
Headline:     60-80px   (Bold)
Subtitle:     24-32px   (Light)
Slogan:       36-48px   (Medium)
Details:      16-20px   (Regular)
Logo:         80-120px width
```

### Small Format (Banner)
```
Headline:     40-60px   (Bold)
Subtitle:     18-24px   (Light)
Slogan:       28-36px   (Medium)
Details:      14-16px   (Regular)
Logo:         60-80px width
```

## Text Effects

### Shadow Treatment
```
Text Shadow for Readability:
- Offset: 2-4px
- Blur: 4-8px
- Color: rgba(0,0,0,0.3-0.5)

Premium Alternative:
- Gradient overlay on text
- Subtle inner shadow
- Slight letter-spacing (tracking)
```

### Gradient Text
For headline emphasis on complex backgrounds:
```css
/* White to light gray gradient */
background: linear-gradient(180deg, #fff 0%, #e0e0e0 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

## Layout Patterns

### Pattern A: Center Stack
```
┌─────────────────┐
│                 │
│    [LOGO]       │ ← Top center
│                 │
│    HEADLINE     │ ← Large, centered
│    subtitle     │ ← Smaller, below
│                 │
│    [CAR]        │
│                 │
│    slogan       │ ← Bottom center
│                 │
└─────────────────┘
```
**Best for**: Single model focus, clean aesthetic

### Pattern B: Asymmetric
```
┌─────────────────┐
│  HEADLINE       │ ← Left aligned
│  subtitle       │
│                 │
│         [CAR]   │ ← Right aligned car
│                 │
│  slogan         │ ← Bottom left
│  [LOGO]         │
└─────────────────┘
```
**Best for**: Dynamic feel, luxury positioning

### Pattern C: Editorial
```
┌─────────────────┐
│   HEADLINE      │ ← Top, large
│                 │
│   [CAR]         │ ← Full width
│   [CELEBRITY]   │ ← Overlapping
│                 │
│   subtitle      │ ← Bottom
│   slogan        │
└─────────────────┘
```
**Best for**: Celebrity endorsements, lifestyle campaigns

## Chinese Typography Specifics

### Font Size Adjustments
Chinese characters need more breathing room:
- Increase line-height by 20-30%
- Use generous letter-spacing for light weights
- Avoid ultra-thin strokes (<100 weight) at small sizes

### Character Count Guidelines
- Headline: 2-6 characters ideal
- Subtitle: 8-15 characters
- Slogan: 10-20 characters
- More characters = larger size needed

### Punctuation
- Use full-width Chinese punctuation
- Avoid punctuation in headlines when possible
- Periods can be replaced with visual breaks

## Accessibility

### Contrast Requirements
- Minimum: 4.5:1 for normal text
- Preferred: 7:1 for headlines
- Test against both light and dark gradient areas

### Readability at Distance
- Headline should be readable at 3m distance on phone screen
- Test by viewing at actual size from arm's length
- If unclear, increase weight or add text shadow

## Common Mistakes to Avoid

1. **Too many fonts**: Stick to 1-2 typefaces
2. **Poor contrast**: White text on light gradients
3. **Overcrowding**: Too much text competing with car
4. **Wrong scale**: Text too small relative to car
5. **Inconsistent alignment**: Mixing center and left align
6. **Ignoring safe zones**: Text too close to edges

## Implementation Notes

### Web Fonts (if generating HTML)
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&family=Montserrat:wght@300;500;800&display=swap" rel="stylesheet">
```

### Local Fonts (if using PIL)
```python
# Download and reference local font files
headline_font = ImageFont.truetype("fonts/NotoSansSC-Bold.otf", 80)
subtitle_font = ImageFont.truetype("fonts/NotoSansSC-Light.otf", 32)
```
