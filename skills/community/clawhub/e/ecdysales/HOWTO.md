# How to Use Ecdysales Lite 🏷️

**Turn your product photos into listing-ready images with one command.**

## What does it do?

You have a photo of a product. You want to sell it online. Ecdysales takes that photo and adds:

- 💰 A **price tag** (yellow sticker, top-right corner)
- 🔲 A **watermark** (subtle tiled pattern so nobody steals your image)
- 🏷️ Your **brand logo** (bottom-right corner)

That's it. Photo in, listing-ready image out.

## Before & After

**Your photo:**
```
┌─────────────────────┐
│                     │
│   📷 plain product  │
│      photo          │
│                     │
└─────────────────────┘
```

**After Ecdysales:**
```
┌─────────────────────┐
│          [$299] 💰  │
│ ░░░░░░░░░░░░░░░░░░░ │
│ ░░ 📷 product  ░░░░ │
│ ░░   photo     ░░░░ │
│ ░░░░░░░░░░░░░░░░░░░ │
│                [🏷️] │
└─────────────────────┘
```

## Install (one time)

1. Make sure you have [ImageMagick](https://imagemagick.org/) installed
   - **Mac:** `brew install imagemagick`
   - **Ubuntu/Debian:** `sudo apt install imagemagick`
   - **Windows:** download from imagemagick.org

2. Or just run the setup script:
   ```bash
   ./scripts/setup.sh --install
   ```

## Use it

### Basic — add everything

```bash
./scripts/run.sh my-photo.jpg '$299'
```

⚠️ **Use single quotes around the price!** The `$` sign means something special to your terminal. Single quotes keep it safe:
- ✅ `'$299'`
- ❌ `"$299"` — your terminal will eat the `$2`

### Just the price tag (no watermark, no logo)

```bash
./scripts/run.sh my-photo.jpg '$299' --sticker-only
```

### Keep the watermark but skip the logo

```bash
./scripts/run.sh my-photo.jpg '$299' --no-logo
```

### Process a whole folder of photos

Create a text file with prices (`prices.txt`):
```
shoes.jpg '$89'
jacket.jpg '$150'
watch.jpg '$450'
```

Then run:
```bash
./scripts/run.sh --batch ./my-photos prices.txt
```

Your processed images land in the `output/` folder.

## Options

| What you want | Command |
|---------------|---------|
| Everything (watermark + logo + price) | `./scripts/run.sh photo.jpg '$99'` |
| Price tag only | `./scripts/run.sh photo.jpg '$99' --sticker-only` |
| No logo | `./scripts/run.sh photo.jpg '$99' --no-logo` |
| No watermark | `./scripts/run.sh photo.jpg '$99' --no-watermark` |
| Batch process a folder | `./scripts/run.sh --batch ./photos prices.txt` |
| Use the latest photo you received | `./scripts/run.sh --latest '$99'` |

## Where do my images go?

Processed images go into the `output/` folder, next to the scripts.

## Can I change the logo?

Yes! Replace `assets/logo.png` with your own logo. Keep it a PNG with a transparent background for best results.

## Can I change the watermark?

Yes! Replace `assets/watermark-pattern.png` with your own pattern. It tiles automatically across the image.

## Customizing the look — Config files

Three JSON files control how each layer looks. Edit them to change the default style without passing command flags every time.

### `config/sticker-config.json` — the price tag

```json
{
  "reactive": false,
  "fill": "#FFD700",
  "stroke": "#000000",
  "strokeWidth": 4,
  "textColor": "#000000",
  "font": "Helvetica-Bold",
  "fontSize": 48,
  "widthRatio": 0.2,
  "heightRatio": 0.125,
  "cornerRadius": 20,
  "padding": 30,
  "position": "top-right"
}
```

**Two modes:**

**Fixed mode** (`reactive: false`) — sticker wraps around the text at a fixed font size.
- `fontSize` controls text size (e.g. `48`)
- Sticker size depends on the price text ("$50" is smaller than "$1,500")

**Reactive mode** (`reactive: true`) — sticker scales to a fraction of the image, font auto-sizes to fit.
- `widthRatio` = fraction of image width (e.g. `0.2` = 1/5)
- `heightRatio` = fraction of image height (e.g. `0.125` = 1/8)
- `fontSize` must be `"auto"`
- Sticker is always the same size regardless of price text

**Example — fixed mode, big red sticker:**
```json
{
  "reactive": false,
  "fill": "#E53935",
  "textColor": "#FFFFFF",
  "fontSize": 64,
  "position": "top-left"
}
```

**Example — reactive mode, always 1/4 width × 1/6 height:**
```json
{
  "reactive": true,
  "fill": "#1E88E5",
  "textColor": "#FFFFFF",
  "fontSize": "auto",
  "widthRatio": 0.25,
  "heightRatio": 0.167,
  "position": "bottom-right"
}
```

| Setting | Description |
|---------|-------------|
| `reactive` | `true` or `false` — switches between modes |
| `fill` | Background color (hex, e.g. `#FFD700` for gold) |
| `stroke` | Border color (hex) |
| `strokeWidth` | Border thickness (px) |
| `textColor` | Price text color (hex) |
| `font` | Font name (must be installed on your system) |
| `fontSize` | Text size (px) — use `"auto"` in reactive mode |
| `widthRatio` | Sticker width as fraction of image — reactive only |
| `heightRatio` | Sticker height as fraction of image — reactive only |
| `cornerRadius` | Rounded corners (px) |
| `padding` | Inner space around text (px) — fixed only |
| `position` | `top-left`, `top-right`, `bottom-left`, `bottom-right`, `random` |

### `config/watermark-config.json` — the background pattern

```json
{
  "opacity": 25,
  "enabled": true
}
```

| Setting | Description |
|---------|-------------|
| `opacity` | How visible: `0` = invisible, `100` = solid. Default `25`. |
| `enabled` | `true` = apply watermark, `false` = skip it |

**Example — heavy watermark:**
```json
{ "opacity": 50, "enabled": true }
```

**Example — no watermark:**
```json
{ "opacity": 25, "enabled": false }
```

### `config/logo-config.json` — your brand logo

```json
{
  "size": 15,
  "opacity": 80,
  "position": "bottom-right",
  "enabled": true
}
```

| Setting | Description |
|---------|-------------|
| `size` | Logo width as % of image width (`1`-`100`) |
| `opacity` | Transparency: `0` = invisible, `100` = solid |
| `position` | `top-left`, `top-right`, `bottom-left`, `bottom-right`, `random` |
| `enabled` | `true` = show logo, `false` = skip it |

**Example — big logo, top-left:**
```json
{ "size": 25, "opacity": 100, "position": "top-left", "enabled": true }
```

### Config validation

If you mess up a config, the script tells you exactly what's wrong:

```
❌ Sticker config error:
  reactive: true but widthRatio=0 and heightRatio=0. Set both > 0 (e.g. 0.2 and 0.125).
Fix: edit config/sticker-config.json
```

Common mistakes:
- `reactive: true` but `widthRatio` or `heightRatio` is `0`
- `reactive: false` but `fontSize` is `"auto"` (needs a number)
- `opacity` outside `0`-`100`
- Invalid hex color (must start with `#`)

## What image formats work?

Any format ImageMagick supports: JPG, PNG, WEBP, HEIC, BMP, TIFF, and more.

## It's free?

Yes. Open source. Use it, modify it, sell the images it makes. No strings attached.

## AI Agent Integration

Ecdysales ships with a `SKILL.md` file that teaches AI agents how to use it automatically. When an agent sees `$price:` with an attached image, it runs the processor and returns the result — no manual commands needed.

See `SKILL.md` for agent instructions and integration details.

---

*Built with ImageMagick. No AI, no cloud, no account needed. Just your photos and a price tag.*
