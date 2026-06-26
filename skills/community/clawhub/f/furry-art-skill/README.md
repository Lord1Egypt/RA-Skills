# Furry Art Generator

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art](https://www.neta.art/open/).

Generate stunning **furry art generator ai** images from a text prompt — powered by the Neta talesofai API. Get back a direct image URL in seconds.

---

## Install

```bash
# Via npx skills
npx skills add omactiengartelle/furry-art-skill

# Via ClawHub
clawhub install furry-art-skill
```

---

## Usage

```bash
# Basic — uses built-in default prompt
node furryart.js

# Custom prompt
node furryart.js "red fox warrior in armor, fantasy setting, detailed fur"

# Specify size
node furryart.js "wolf mage casting spells" --size portrait

# Reference an existing image for style inheritance
node furryart.js "same character, different pose" --ref <picture_uuid>
```

The script prints the final image URL to stdout and progress info to stderr.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--token` | string | — | Override the API token for this run |
| `--ref` | picture_uuid | — | Inherit style/params from an existing image |

### Size dimensions

| Name | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Default prompt

When no prompt is provided, the skill uses:

> anthropomorphic animal character, furry art style, detailed fur texture, expressive eyes, vibrant colors, clean linework, digital illustration

---

## Example output

```
Submitting: "red fox knight in enchanted forest" [square 1024×1024]
Task: abc123-def456-...
Waiting… attempt 3/90 [PENDING]
https://cdn.talesofai.cn/artifacts/abc123.png
```

## Example Output

![Generated example](https://oss.talesofai.cn/picture/7312ff44-8e15-4c55-b3dd-f6c1b248834e.webp)

---

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
