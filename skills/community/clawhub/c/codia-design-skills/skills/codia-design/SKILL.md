---
name: codia-design
description: Use when the user asks broadly to use Codia Design, needs Codia CLI setup/auth/account checks, needs help choosing the right Codia feature skill, or asks for a multi-step workflow across Codia image, PDF, SVG, credits, or usage tools.
---

# Codia Design

This is the compatibility router, setup, and workflow orchestration skill for Codia Design. In the normal root-pack install, the top-level `../../SKILL.md` file is the primary router. Keep this child skill available for older installs and `--full-depth` installs where `codia-design` is loaded as a separate top-level skill.

Use it to install or authenticate the local `codia-design` CLI, choose the right feature skill, and coordinate multi-step work. For a single clear operation, use the matching feature skill directly.

Use this skill when:

- The user asks broadly to use Codia, Codia Design, or Codia Design Skills and the exact tool is unclear.
- The user needs CLI setup, authentication, credits, usage, limits, or account troubleshooting.
- The task needs multiple Codia tools in sequence, such as generating assets and adapting them into final formats.

For focused one-step requests, prefer the matching feature skill listed in [Feature Skills](#feature-skills). This router should pick and sequence those skills; it should not duplicate every parameter table from the feature skills.

For common multi-step scenarios, prefer the matching workflow skill:

| Scenario | Workflow Skill |
|---|---|
| Product launch, ecommerce listings, product marketing asset packs | `codia-product-assets` |
| Campaign posters, launch graphics, social creative sets, multi-size adaptations | `codia-campaign-assets` |
| PDF/document to editable design data, PPTX deck, or both | `codia-document-deck` |

## Setup Check

Before running any Codia command, check whether the CLI is available.

macOS / Linux:

```bash
command -v codia-design
```

Windows PowerShell:

```powershell
Get-Command codia-design -ErrorAction SilentlyContinue
```

If `codia-design` is missing, install it automatically before continuing when the agent has permission to run global npm installs.

```bash
npm install -g @codia-ai/codia-design-cli
```

```powershell
npm install -g @codia-ai/codia-design-cli
```

Then verify:

```bash
codia-design --help
codia-design auth status
```

```powershell
codia-design --help
codia-design auth status
```

If the install command fails because the agent lacks permission to install global npm packages, tell the user to run the same `npm install -g ...` command manually, then continue after they confirm it is installed.

## Authentication

If `codia-design auth status` reports `connected: false`, run:

```bash
codia-design auth login --platform codex
```

The command opens Codia in the browser. The user logs in and authorizes the skill; the CLI stores the token locally in `~/.codia/design-skills/config.json`.

If browser login is unavailable in the target environment, bind an existing Codia Open API key directly:

```bash
codia-design auth set --api-key api_key_xxx
```

## Common Commands

```bash
codia-design credits
codia-design usage --page 1 --page_size 20
codia-design image-to-design --image ./screenshot.png --out result.json
codia-design pdf-to-design --pdf ./file.pdf --pages 0,1 --out result.json
codia-design pdf-to-ppt --pdf ./file.pdf --pages 0,1,2 --title "Deck" --poll --out deck.json
codia-design remove-bg --image ./product.png --download-dir ./outputs --out result.json
codia-design image generate --prompt "modern SaaS dashboard hero image" --download-dir ./outputs
codia-design image upscale --image ./image.png --download-dir ./outputs
codia-design image replace-bg --image ./product.png --prompt "clean white studio background" --download-dir ./outputs
codia-design svg create --image ./logo.png
```

Prefer local file paths when the user provides local assets. Image commands, background removal, image-to-design, and SVG create send local images directly to their target multipart endpoints; URL inputs still use JSON URL mode. Use `--out` for large responses.

Never print API keys or contents of `~/.codia/design-skills/config.json`.

## PDF Page Numbering

PDF page selection is zero-based across PDF APIs:

- `pdf-to-design --pages` is zero-based. Use `0` for the first page, `1` for the second page.
- `pdf-to-ppt --pages` is zero-based in the Task API. Use `0` for the first page, `1` for the second page.
- `usage --page` is account-history pagination, not PDF page selection. Pass `1` for the first result page; do not use `0` even though the current API normalizes it to `1`.

If a `pdf-to-ppt` result appears offset by one page, report it as a server-side conversion issue; do not add 1 to page numbers as a workaround.

For `pdf-to-ppt --poll`, the CLI downloads the returned `ppt_url` by default and validates that the file is an openable PPTX package. Use `--download-dir DIR` to choose the output directory, or `--no-download` only when the user explicitly wants JSON-only behavior. If the API returns an error, the returned URL cannot be downloaded, or the downloaded file is not a valid PPTX package, treat the command as failed and report the API/validation error directly. Do not rasterize the PDF locally or generate a substitute PPTX unless the user explicitly asks for a local fallback.

## Image Generation Defaults

For `codia-design image generate`, keep the first call simple. If the user does not specify model or size, run the command with just the prompt; the CLI defaults to `seedream_5` at `2560x1440`.

All image-output commands download returned image URLs by default and return local paths in `data.local_file` and `data.local_files`. This includes `image generate`, `remove-bg`, `image upscale`, `image replace-bg`, `image object-erase`, `image watermark-remove`, `image image-to-image`, `image remix`, and `image reframe`. Use `--download-dir DIR` when the user wants a specific location, or `--no-download` only for JSON-only workflows. When exact pixels matter, explain that providers may normalize requested sizes; Seedream 16:9 uses `2560x1440`, not `1920x1080`.

## Credits And Pricing

The CLI uses the public Open API v2 surface (`/v2/open/*`) and estimates credits from the server `open_api_v2` pricing table before making billable calls. After a billable command completes, it queries `codia-design credits`; if the remaining `available_credits` is below 2x the estimated cost, tell the user the estimate, remaining balance, and recommended 2x balance. This reminder must not block generation. Use `--estimate` to show the estimate without sending a request. Use `codia-design limits` or `https://codia.ai/api-reference#description/introduction` when the user needs the live pricing and limits table.

Key costs:

| Command | Credits |
|---|---:|
| `pdf-to-design` | 13/page |
| `pdf-to-ppt` | 13/page |
| `image-to-design` | 13/request |
| `remove-bg` | 13/request |
| `svg create` | 13/create |
| `image describe` | 5/request |
| `image layering` | 27/request |
| `image generate`, `image image-to-image`, `image remix`, `image reframe`, `image upscale` | varies by model/resolution |

## Feature Skills

For complete parameter tables, response schemas, and usage examples, use the matching feature skill. Each feature lives in its own `skills/<name>/SKILL.md` directory:

| Command | Skill | Response |
|---|---|---|
| product asset workflow | `codia-product-assets` | Multi-step image asset set |
| campaign asset workflow | `codia-campaign-assets` | Multi-step visual variants and sizes |
| document/deck workflow | `codia-document-deck` | Editable design data and/or PPTX |
| `image-to-design` | `codia-image-to-design` | VisualElement tree |
| `pdf-to-design` | `codia-pdf-to-design` | Multi-page VisualElement tree |
| `pdf-to-ppt` | `codia-pdf-to-ppt` | Asynchronous task (requires polling) |
| `remove-bg` | `codia-remove-bg` | Image URL |
| `svg` | `codia-svg` | SVG workflow |
| `image generate` | `codia-image-generate` | Image URL array |
| `image upscale` | `codia-image-upscale` | Image URL array |
| `image replace-bg` | `codia-image-replace-bg` | Image URL array |
| `image object-erase` | `codia-image-object-erase` | Image URL array |
| `image describe` | `codia-image-describe` | Text description |
| `image watermark-remove` | `codia-image-watermark-remove` | Image URL array |
| `image image-to-image` | `codia-image-image-to-image` | Image URL array |
| `image remix` | `codia-image-remix` | Image URL array |
| `image reframe` | `codia-image-reframe` | Image URL array |
| `image layering` | `codia-image-layering` | Layering DSL |
| `credits` | `codia-credits` | Balance object |
| `usage` | `codia-usage` | Usage record list |
| `auto-recharge` | `codia-auto-recharge` | Automatic recharge settings |
