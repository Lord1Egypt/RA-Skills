# Background Remover

AI-powered ai background remover image generation, backed by the Neta talesofai API. Provide a text prompt and receive a direct image URL in seconds.

---

## Install

**Via npx skills:**
```bash
npx skills add BarbaraLedbettergq/background-remover-claw-skill
```

**Via ClawHub:**
```bash
clawhub install background-remover-claw-skill
```

---

## Usage

```bash
# Basic — uses default prompt
node backgroundremoverclaw.js

# Custom prompt
node backgroundremoverclaw.js "product photo, white background removed, transparent PNG"

# Specify size
node backgroundremoverclaw.js "floating sneaker" --size portrait

# Reference an existing image by UUID
node backgroundremoverclaw.js "remove background" --ref <picture_uuid>

# Pass token inline
node backgroundremoverclaw.js "studio shot cutout" --token YOUR_NETA_TOKEN
```

The script prints a single image URL to stdout on success.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--token` | string | — | Neta API token (overrides env/file) |
| `--ref` | picture_uuid | — | Reference image UUID for inherit_params |

### Size dimensions

| Name | Width × Height |
|------|---------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

---

## Token setup

The script resolves `NETA_TOKEN` in this order:

1. `--token` CLI flag
2. `NETA_TOKEN` environment variable

```
NETA_TOKEN=your_token_here
```

---

## Examples

```bash
# Square cutout (default)
node backgroundremoverclaw.js "remove background, transparent cutout, clean edges"

# Portrait product shot
node backgroundremoverclaw.js "isolated product, no background" --size portrait

# Landscape banner crop
node backgroundremoverclaw.js "floating object transparent" --size landscape
```

## Example Output

![Generated example](https://oss.talesofai.cn/picture/9499b2c5-0f8a-4c48-ae9a-1400c3b15e95.webp)
