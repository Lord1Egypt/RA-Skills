---
name: digital-product-builder
description: Build and launch zero-cost digital products on Gumroad, itch.io, and DriveThruRPG. Use when: creating cover images or product art without external AI image services, generating product listing copy cheaply, building downloadable asset packs (TTRPG tokens, design kits, templates), or setting up a new digital storefront. Uses Python Pillow for images ($0, no login, no browser needed) and Groq for copy (~$0.01/product). Works on Linux, macOS, and Windows-WSL. Includes platform size presets, font discovery, and a catalog of common blockers with proven fixes.
---

# Digital Product Builder

Build and ship digital products for Gumroad, itch.io, and DriveThruRPG without spending money on image generators or expensive AI models.

**Stack:** Python Pillow for images ($0) + Groq for copy (~$0.01/product) + Claude main session for orchestration only.

---

## Quick Start

```bash
# Check Pillow
python3 -c "from PIL import Image, ImageDraw, ImageFont; print('Pillow ready')" 2>/dev/null || echo "Not installed"

# Install if missing (try each until one works)
pip3 install Pillow
# or: pip install Pillow
# or: python3 -m pip install Pillow
```

---

## Image Generation — Pillow

**Never use the browser tool for image generation.** Pillow is faster, crash-free, and requires no login or external service.

### Find available fonts (run this first)
```python
import os
font_dirs = [
    '/usr/share/fonts',                          # Linux
    '/System/Library/Fonts',                     # macOS
    'C:/Windows/Fonts',                          # Windows
    os.path.expanduser('~/.fonts'),
]
fonts = []
for d in font_dirs:
    if os.path.exists(d):
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith(('.ttf', '.otf')):
                    fonts.append(os.path.join(root, f))
print('\n'.join(fonts[:20]))
```

### Common font paths (Ubuntu/Debian)
```
/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf
/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf
/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
```

### Common font paths (macOS)
```
/System/Library/Fonts/Helvetica.ttc
/System/Library/Fonts/Georgia.ttf
/Library/Fonts/Arial.ttf
```

### Safe fallback (always works, no font file needed)
```python
font = ImageFont.load_default()  # basic but guaranteed
```

### Platform cover sizes
| Platform | Size | Notes |
|----------|------|-------|
| itch.io | 630×500px | Required for browse visibility |
| Gumroad | 1280×720px | 16:9 |
| DriveThruRPG | 900×700px | Landscape or portrait |
| Social preview (OG/Twitter) | 1200×630px | Standard |

### Cover image boilerplate
```python
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 630, 500
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

img  = Image.new("RGB", (W, H), (20, 20, 40))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(SERIF_BOLD, 36)
gold = (201, 168, 76)

# Border
draw.rectangle([10,10,W-10,H-10], outline=gold, width=4)

# Centered title
b = draw.textbbox((0,0), "Your Title", font=font)
draw.text(((W-(b[2]-b[0]))//2, (H-(b[3]-b[1]))//2), "Your Title",
          fill=gold, font=font)

img.save("/path/to/output.png", "PNG", optimize=True)
print(f"Saved ({os.path.getsize('/path/to/output.png')//1024}KB)")
```

### Radial gradient (dark-to-light effect)
```python
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

center = (230, 180, 80)   # bright centre
edge   = (60,  30,  10)   # dark edge
for step in range(30, 0, -1):
    t  = step / 30
    c  = lerp(center, edge, t)
    r  = int(radius * step / 30)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
```

### RGBA transparency (for compositing)
```python
img  = Image.new("RGBA", (W, H), (20, 20, 40, 255))
draw = ImageDraw.Draw(img, "RGBA")
# ... draw with alpha ...
# Flatten to RGB before saving PNG
bg = Image.new("RGB", (W, H), (20, 20, 40))
bg.paste(img, mask=img.split()[3])
bg.save(out_path, "PNG")
```

### ZIP bundle
```python
import zipfile
with zipfile.ZipFile("product.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme_text)
    for fp in file_list:
        z.write(fp, f"subfolder/{os.path.basename(fp)}")
```

---

## Copy Generation — Groq

**API key location:** Store your Groq API key in `~/.openclaw/workspace/dashboard/.env` as `GROQ_API_KEY=your_key_here`

### Node.js call pattern
```javascript
const https = require('https');
const GROQ_KEY = process.env.GROQ_API_KEY;

const body = JSON.stringify({
  model: "llama-3.3-70b-versatile",
  messages: [{ role: "user", content: YOUR_PROMPT }],
  max_tokens: 600,
  temperature: 0.7
});

const req = https.request({
  hostname: 'api.groq.com',
  path: '/openai/v1/chat/completions',
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${GROQ_KEY}`,
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body)
  }
}, res => {
  let d = '';
  res.on('data', c => d += c);
  res.on('end', () => console.log(JSON.parse(d).choices[0].message.content));
});
req.write(body);
req.end();
```

### Listing copy prompt template
```
Write a product listing for [PLATFORM]. Plain language. No em dashes.
No filler phrases ("elevate," "perfect for," "streamline your workflow").

Product: [NAME]
What it is: [DESCRIPTION]
Price: [PRICE]
Format: [FILE FORMAT]

Write: title (under 60 chars), tagline (1 sentence), description
(3 short paragraphs), what's included (5 items max), 5 search tags.
```

### De-AI-ify checklist (always run before saving copy)
- Remove em dashes — use periods or commas instead
- Remove: "elevate," "enhance," "seamlessly," "perfect for," "streamline"
- Break up long bullet lists into short paragraphs
- If it sounds like a press release, rewrite it

---

## Platform Playbooks

### itch.io
- New product: Dashboard → Create new project → Downloadable
- Cover image: **630×500px required** — no cover = invisible in browse
- Pricing: fixed price or "pay what you want" with minimum
- Upload: ZIP file for multi-file products
- Tags: use specific terms (e.g. "ttrpg tokens" not just "game")

### Gumroad
- New product: Products → New Product → Digital
- Cover: 1280×720 recommended
- Description editor may require manual paste — automation sometimes blocked
- Set Discover category in product settings for marketplace visibility
- Configure payout threshold in account settings

### DriveThruRPG
- Free publisher account at drivethrurpg.com/publishers
- Cover: 900×700px
- Categories for tokens: Accessories > Tokens/Maps
- Revenue: 70% creator / 30% DTRPG
- Payout: PayPal, $10 minimum

---

## Common Blockers & Fixes

| Blocker | Fix |
|---------|-----|
| Bing Image Creator requires MS account | Use Pillow — no external services needed |
| ideogram.ai / external generators blocked by Cloudflare | Use Pillow |
| Browser crashes during canvas rendering | Don't use browser for images. Pillow only. |
| Can't save canvas to file from browser JS | Pillow writes directly to disk |
| `file://` URLs blocked in browser tool | Serve via `python3 -m http.server PORT` |
| Gumroad editor blocks automation | Paste listing copy manually |
| `require is not defined` in browser evaluate | Use exec + node script instead |
| itch.io "invalid token" on email verify | Safe to ignore if account is already live |

---

## Cost Per Product

| Item | Tool | Cost |
|------|------|------|
| Cover image | Pillow | $0 |
| Asset sheets / bundles | Pillow | $0 |
| Product listing copy | Groq llama-3.3-70b | ~$0.01 |
| Orchestration | Claude main session | minimal |
| **Total per product** | | **< $0.05** |

No sub-agents needed. Do everything inline in the main session.

---

## Example Products Built With This Skill

- NPC Dialogue & Quest Text Packs — itch.io, $9
- TTRPG Character Token Pack — DriveThruRPG, $7.99
- Newsletter Creator Visual Kit — Gumroad, $12
