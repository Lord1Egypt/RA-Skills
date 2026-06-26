# Art Director

> On-aesthetic image generation for brands that tell stories with images.

A ClawHub skill for any publication, brand, newsletter, essay, or longform piece that needs images to feel like *yours* — consistent with your visual identity, specific to the piece they accompany, and doing real editorial work rather than sitting there as decoration.

Wraps `nano-banana-pro` (Gemini) for the underlying image generation. What this skill adds on top:

- **A persistent brand aesthetic** (`aesthetic.md`) — write your visual identity once, and every image you generate carries it.
- **Per-image art direction thinking** — structured guidance in `SKILL.md` teaches the calling agent how to turn a topic into a proper brief (metaphor over literal, tone over description, art language over tech language).
- **An iteration loop** — `batch` command for generating 10–20 images against the current aesthetic so you can see what it does and doesn't produce, then tune.

Battle-tested at [OffworldNews.AI](https://offworldnews.ai), an experimental publication built around autonomous agents.

---

## What this looks like

One brief, nine shipped aesthetics. Same image brief run through each preset — nine different arguments from the same subject.

| Documentary | Product-photo | Conceptual-illustration |
|:---:|:---:|:---:|
| ![Documentary](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-documentary.png) | ![Product photo](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-product-photo.png) | ![Conceptual](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-conceptual.png) |
| Observed, photographic | Studio photography, seamless | Painterly, metaphor-forward |
| **Schematic** | **Orbital** | **Editorial-collage** |
| ![Schematic](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-schematic.png) | ![Orbital](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-orbital.png) | ![Editorial collage](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-editorial-collage.png) |
| Ink linework, paper, exploded-view | Flat vector, mid-century poster | Torn paper, halftone, analog |
| **Product-render** | **Synthwave** | **Phosphor** |
| ![Product render](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-product-render.png) | ![Synthwave](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-synthwave.png) | ![Phosphor](https://raw.githubusercontent.com/MachinesOfDesire/art-director/main/examples/booth-phosphor.png) |
| 3D render, architectural | Chrome, neon, after-midnight | Green CRT, scan lines, low-bit |

See [`SKILL.md`](SKILL.md) for the full brief and how to construct your own.

---

## Install

```bash
openclaw skill install art-director
openclaw skill install nano-banana-pro   # dependency
```

Set your Gemini API key (nano-banana-pro reads this):
```bash
export GEMINI_API_KEY="..."
```

Copy a starting aesthetic preset:
```bash
python3 art_director.py install --preset documentary
```

Edit `aesthetic.md` to describe your brand. Then:

```bash
python3 art_director.py generate \
  --brief "a single candle in a dark library, high contrast, photographic grain" \
  --output first-test.png
```

---

## The two-layer model

Every image generation is:

```
brand aesthetic (aesthetic.md)  +  per-image brief  →  final prompt
```

**`aesthetic.md`** holds your palette, composition defaults, rendering medium, tone, constraints, and reference anchors. Written once by the operator. Stable across every image.

**The brief** is written per-image by whoever is requesting the image — an agent, a writer, a human operator. Contains the specific argument, metaphor, and tonal shift for this one piece.

The skill merges them. Operators own the aesthetic. Agents own the brief. Neither has to know the other to do their job well.

---

## Presets

Nine starting points ship in `presets/`:

| Preset | Feel | Good for |
|---|---|---|
| `documentary` | Desaturated photography, observed, natural light, feature-magazine | Publications, brands that want quiet authority |
| `conceptual-illustration` | Painterly, metaphor-first, traditional-media texture | Essays, criticism, culture, opinion |
| `product-render` | 3D renders, architectural composition, single-accent palette | SaaS, infrastructure, developer tools, product marketing |
| `product-photo` | Real photography, seamless backdrops, quiet product reverence | Premium consumer brands, D2C, lifestyle publications |
| `schematic` | Precise ink linework, orthographic / exploded-view, paper texture | Engineering, manuals, technical docs, data-heavy content |
| `editorial-collage` | Torn-magazine scraps, halftone dots, analog composition | Features, culture mags, longform with editorial bite |
| `synthwave` | 80s retrofuturist, neon magenta/cyan, chrome, VHS texture | Indie games, music brands, podcasts, retro-tech |
| `phosphor` | Monochrome CRT, scan lines, low-bit pixel, green/amber/duotone | Indie games, retro-computing, terminal-aesthetic publications |
| `orbital` | Flat vector poster, cosmic geometry, mid-century palette, print texture | Science writing, culture brands, poster-design sensibility |

Or start blank:
```bash
python3 art_director.py install --preset blank
```

---

## Commands

### `install` — set up your aesthetic
```bash
python3 art_director.py install --preset <name>
# --force   overwrite existing aesthetic.md
# --target  custom path (default: ./aesthetic.md)
```

### `generate` — one image
```bash
python3 art_director.py generate \
  --brief "<per-image brief>" \
  --output "<filename.png>" \
  --resolution 2K
```
- `--resolution` — `1K` (draft), `2K` (default), `4K` (final)
- `--aesthetic` — path to aesthetic file (default: `$AESTHETIC_PATH` or `./aesthetic.md`)

### `batch` — iterate on your aesthetic
```bash
python3 art_director.py batch \
  --briefs briefs.txt \
  --outdir ./iteration-01/
```
`briefs.txt` is plain text, one brief per line. Blank lines and `#`-prefixed comments are ignored. Generates one image per line into `--outdir`, numbered `01.png`, `02.png`, …

Use this to stress-test a fresh aesthetic before you commit to it.

### `check-nano` — verify setup
```bash
python3 art_director.py check-nano
```
Confirms nano-banana-pro, `uv`, and `aesthetic.md` are all in place.

---

## Configuration

All optional:

| Variable | Purpose | Default |
|---|---|---|
| `GEMINI_API_KEY` | Gemini API key (required for generation; read by nano-banana-pro) | — |
| `OUTPUT_DIR` | Where generated images land | `.` |
| `AESTHETIC_PATH` | Where to look for the brand aesthetic file | `./aesthetic.md` |
| `NANO_BANANA_SCRIPT` | Override the path to nano-banana-pro's `generate_image.py` | auto-detected |

---

## How to get to "this looks like us"

1. `install --preset <closest>` — pick the preset that's least wrong
2. Write 10–20 briefs for pieces your brand would actually publish. Save them to `briefs.txt`.
3. `batch --briefs briefs.txt --outdir ./v1/` — generate against the current aesthetic
4. Review the 20 images side by side. Note which feel on-brand, which feel generic, which feel off.
5. Edit `aesthetic.md` — sharpen the palette that worked, remove the rendering choices that didn't, add constraints for the clichés you saw slip through.
6. `batch --briefs briefs.txt --outdir ./v2/` — regenerate
7. Compare v1 and v2 side by side. Keep what improved, revert what didn't.
8. Repeat. You'll reach "this looks like us" within a couple of evenings.

Aesthetic configs don't get good by being specified exhaustively up front. They get good by iteration.

---

## What this skill is not

- Not a text-to-image tool. Those exist. If you just want a description rendered, use one.
- Not a decorative image generator. If your piece doesn't have an argument the image should carry, this skill won't save you.
- Not a portrait generator. No identifiable real or synthetic people. Use abstraction, silhouette, hands, shadow.
- Not a typography tool. No text rendered into the image. Ever.

---

## Companion: Creative Director agent (forthcoming)

The Art Director skill is a capability. The matching *agent template* — a creative-director persona with taste, history, and working voice that uses this skill — is planned as a separate ClawHub offering. Ship order: skill first (this), agent template later (once install data tells us what a packageable persona actually needs).

---

## License

MIT-0 (MIT No Attribution) — the [mandatory license](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md) for all ClawHub skills. Use, modify, redistribute, ship commercially — no attribution required. Contributions welcome at the homepage linked in `SKILL.md`.
