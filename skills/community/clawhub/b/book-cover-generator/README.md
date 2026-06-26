# Book Cover Generator

Generate stunning book covers from text descriptions using AI — perfect for indie authors, self-publishers, and KDP creators. Describe your book's genre, mood, characters, and setting, and receive professional-quality cover art ready for Kindle, ebook, and print-on-demand publishing.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
# Via npx skills
npx skills add omactiengartelle/book-cover-generator

# Via ClawHub
clawhub install book-cover-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node bookcovergenerator.js "<description>" --token YOUR_TOKEN [--size <size>] [--ref <uuid>]
```

### Examples

```bash
# Fantasy novel cover
node bookcovergenerator.js "A lone wizard standing at the edge of a cliff overlooking a dragon-filled valley, epic fantasy, dramatic stormy sky, oil painting style" --token "$NETA_TOKEN"

# Romance novel cover
node bookcovergenerator.js "Two silhouettes embracing on a moonlit beach, soft warm tones, romantic atmosphere, cinematic lighting" --token "$NETA_TOKEN"

# Thriller cover
node bookcovergenerator.js "A shadowy figure in a rain-soaked city alley, neon reflections, dark and suspenseful mood, photorealistic" --token "$NETA_TOKEN"

# Non-fiction business book
node bookcovergenerator.js "Clean minimalist design, bold typography space, ascending graph motif, professional corporate blues and whites" --token "$NETA_TOKEN"

# Landscape size
node bookcovergenerator.js "Sci-fi spaceship battle above a ringed gas giant, cinematic, highly detailed" --token "$NETA_TOKEN" --size landscape

# With style reference
node bookcovergenerator.js "Dark gothic castle on a stormy night" --token "$NETA_TOKEN" --ref abc123-uuid-here
```

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--token` | string | — | Neta API token (required) |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size Dimensions

| Size | Dimensions | Best For |
|------|-----------|----------|
| `portrait` | 832 × 1216 | Standard book covers, KDP, Kindle |
| `square` | 1024 × 1024 | Social media, thumbnails |
| `landscape` | 1216 × 832 | Wide banners, panoramic scenes |
| `tall` | 704 × 1408 | Phone wallpapers, tall formats |

## Output

Returns a direct image URL. Download or open it in your browser to save the generated cover.

## Tips for Great Book Covers

- **Be specific about genre**: "dark fantasy", "cozy mystery", "literary fiction" help set the tone
- **Describe the mood**: "eerie", "hopeful", "tense", "whimsical"
- **Mention art style**: "oil painting", "watercolor", "photorealistic", "illustrated", "minimalist"
- **Leave room for text**: add "with space for title text at top" or "negative space for typography"
- **Specify lighting**: "golden hour", "dramatic side lighting", "soft diffused light"

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
