# Codia Design Skills

Codia Design Skills gives local AI agents a reliable way to call Codia Open API from normal project work. After installation, an agent can inspect screenshots, convert PDFs into design data, generate or edit images, remove backgrounds, create SVG assets, export PDFs to PPT, and check account usage through the local `codia-design` command.

This repository is for agent skills. The skill files teach Codex, Claude Code, Cursor, and other agents when to use Codia, which workflow to choose, and how to call the runtime safely. The runtime CLI is installed separately and performs the authenticated API requests on the user's machine.

You normally do not need to paste CLI commands into the agent. Ask for the outcome you want, provide local file paths or URLs, and let the agent pick the matching Codia skill.

## Quick Start

### Preferred (npx skills)

Install the Codia Design root skill pack from GitHub with `npx skills`:

```bash
npx -y skills add https://github.com/codia-ai/codia-design-skills.git -g -y
```

The default install creates one top-level `codia-design-skills` skill. Workflow and feature instructions live inside the pack under:

```text
SKILL.md
skills/<workflow-or-feature>/SKILL.md
```

The root skill handles routing and reads the relevant child `SKILL.md` file when a task needs specific parameters, model choices, or multi-step sequencing. Do not use `--full-depth` for normal installs unless you intentionally want every child skill installed as a separate top-level skill.

For a hands-off setup flow, give [AGENT_INSTALL.md](AGENT_INSTALL.md) to your agent and ask it to install Codia Design Skills.

## Use In An Agent

After installing the skill pack, start a new agent session or ask the agent to reload skills. Then describe the task in normal language. The agent will load the `codia-design-skills` root router, choose the right child workflow or feature instructions, check whether the `codia-design` CLI is installed, verify authentication, run the needed command, and report local output files or returned URLs.

Example agent requests:

```text
Use Codia to convert ./screenshot.png into editable design JSON and save it under ./outputs.
Use Codia to convert pages 0-4 of ./proposal.pdf into a PPT and also extract editable design data.
Use Codia to create a product launch asset pack from ./product.png with a white-background tile, a lifestyle scene, and a 16:9 banner.
Use Codia to generate a campaign poster, adapt it to 1:1, 4:5, and 9:16, and save all outputs in ./outputs.
Use Codia to remove the background from ./product.png and return a transparent PNG.
Use Codia to check my credits and recent usage.
```

Give the agent the source file path, desired page range, target sizes or aspect ratios, output directory, and any visual constraints that matter. For PDFs, page numbers are zero-based in Codia PDF APIs, so page `0` means the first page.

### Skill Routing

The top-level `codia-design-skills` skill is the router, setup, and workflow orchestration entry point. It is useful when the request is broad, account setup is needed, or several Codia tools must be chained together.

Common multi-step requests are handled by workflow instructions such as `codia-product-assets`, `codia-campaign-assets`, and `codia-document-deck`. Focused one-step requests are handled by feature instructions such as `codia-image-generate`, `codia-pdf-to-ppt`, `codia-remove-bg`, `codia-image-upscale`, `codia-image-reframe`, and `codia-credits`.

## Available Skills

### codia-design-skills

Root router, runtime setup, account check, feature routing, and multi-step workflow orchestration for the Codia Design Skills pack.

Triggers: use Codia, Codia Design, setup Codia, Codia auth, product launch asset pack, PDF to design and PPT, campaign variants

### codia-design

Compatibility router and setup instructions for users who install the child skills as separate top-level skills with `--full-depth`.

Triggers: use Codia, Codia Design, setup Codia, Codia auth, route Codia tools

### codia-product-assets

Creates coherent product launch or ecommerce asset packs from product photos, including listing images, store banners, catalog tiles, marketplace visuals, and product scene variations.

Triggers: product launch asset pack, ecommerce images, product listing images, store banner, product marketing images, marketplace visuals

### codia-campaign-assets

Creates campaign posters, launch graphics, hero images, social creative sets, controlled variants, and multi-size adaptations.

Triggers: campaign poster, marketing visual, launch graphic, social creative set, hero image, multi-size assets

### codia-document-deck

Converts PDFs, screenshots, reports, documents, or existing marketing files into editable design data, PPTX slides, or both.

Triggers: PDF to design and PPT, document to deck, PDF to editable design, report to slides, screenshot to design

### codia-image-generate

Generates new images from text prompts for posters, campaign visuals, product concepts, backgrounds, icons, and visual drafts.

Triggers: generate image, make a poster, create campaign visual, product launch visual, visual draft, background image

### codia-image-image-to-image

Creates a new image from one or more reference images while preserving or transforming visual direction.

Triggers: transform this image, restyle image, reference-based generation, create variants from image, image-to-image

### codia-image-remix

Creates controlled visual variations from an existing image while keeping the core concept recognizable.

Triggers: remix image, make variants, campaign alternatives, different mood, same style variations

### codia-image-reframe

Adapts an image into new aspect ratios and layouts for social, ads, banners, posters, thumbnails, and packaging.

Triggers: resize for social, adapt to 9:16, make banner, reframe poster, change aspect ratio

### codia-image-upscale

Increases resolution and improves final asset quality for generated images, product photos, graphics, and delivery files.

Triggers: upscale, make HD, increase resolution, sharpen, final delivery, improve quality

### codia-remove-bg

Removes image backgrounds and returns transparent-background assets for products, portraits, and isolated subjects.

Triggers: remove background, transparent PNG, cutout, isolate product, extract subject

### codia-image-replace-bg

Replaces an image background with studio, lifestyle, ecommerce, or campaign scenes.

Triggers: replace background, white studio background, lifestyle scene, ecommerce background, product scene

### codia-image-object-erase

Removes unwanted objects, props, defects, clutter, or distractions from images the user is allowed to edit.

Triggers: remove object, erase prop, clean clutter, remove defect, remove bystander

### codia-image-watermark-remove

Removes watermarks or overlays only from user-owned or otherwise authorized images.

Triggers: remove watermark, clean overlay, authorized watermark removal

### codia-image-describe

Describes and analyzes image content, style, layout, visible details, and visual intent.

Triggers: describe image, inspect image, summarize image, extract visual details, caption image

### codia-image-to-design

Converts screenshots, posters, UI mockups, and images into editable Codia design data.

Triggers: image to design, screenshot to design, editable design JSON, turn mockup into design data

### codia-image-layering

Converts an image into Codia layering DSL for structured editable reconstruction.

Triggers: image layers, layering DSL, structured design data, editable reconstruction

### codia-pdf-to-design

Converts selected PDF pages into editable Codia design data.

Triggers: PDF to design, extract PDF pages, editable PDF design, PDF layout reconstruction

### codia-pdf-to-ppt

Converts selected PDF pages into a downloadable PPTX deck and validates the downloaded PowerPoint file.

Triggers: PDF to PPT, PDF to PowerPoint, convert PDF pages to slides, make deck from PDF

### codia-svg

Vectorizes logos, icons, and images into SVG through the asynchronous Codia SVG workflow.

Triggers: vectorize image, logo to SVG, icon to SVG, create SVG

### codia-credits

Checks current Codia Open API credit balance before or after agent work.

Triggers: Codia credits, credit balance, quota left, enough credits

### codia-usage

Inspects Codia Open API usage records and recent task costs.

Triggers: Codia usage, usage records, billing history, recent cost, task consumption

### codia-auto-recharge

Reads or updates Codia Open API automatic recharge settings.

Triggers: auto recharge, quota top-up, recharge threshold, recharge limit

## Install The Runtime

### Automatic CLI bootstrap

The agent will check whether `codia-design` is available before calling Codia APIs. If the command is missing and the agent is allowed to run global npm installs, it may install the runtime automatically.

Manual install:

```bash
npm install -g @codia-ai/codia-design-cli
```

Windows PowerShell:

```powershell
npm install -g @codia-ai/codia-design-cli
```

Update an existing install:

```bash
npm install -g @codia-ai/codia-design-cli@latest
```

Run without installing globally:

```bash
npx -y @codia-ai/codia-design-cli --help
```

## Connect An API Key

Use browser login when it is available:

```bash
codia-design auth login --platform codex
```

Or bind an API key directly:

```bash
codia-design auth set --api-key api_key_xxx
```

The CLI stores local auth state in:

```text
~/.codia/design-skills/config.json
```

Do not commit this file, print it in chat, or include it in a package archive.

## Verify Access

Run these checks after installing the skill and runtime:

```bash
codia-design --version
codia-design --help
codia-design auth status
codia-design credits
```

For command-specific guidance, run `codia-design <command> --help`, `codia-design image --help`, or `codia-design image <command> --help`.

## Optional Direct CLI Reference

These commands are mainly for manual debugging, local verification, or cases where an agent asks you to approve the exact command it plans to run.

```bash
codia-design image-to-design --image ./screenshot.png --out result.json
codia-design pdf-to-design --pdf ./file.pdf --pages 0,1 --out result.json
codia-design pdf-to-ppt --pdf ./file.pdf --pages 0,1,2 --title "Deck" --poll --out deck.json
codia-design image generate --prompt "modern product launch visual" --model seedream_5 --size 2560x1440 --download-dir ./outputs
codia-design image replace-bg --image ./product.png --prompt "clean white studio background" --model nano_banana_2 --download-dir ./outputs --out replace-bg.json
codia-design image upscale --image ./photo.png --model codia_image_v2 --download-dir ./outputs --out upscale.json
codia-design remove-bg --image ./product.png --download-dir ./outputs --out remove-bg.json
codia-design svg create --image ./logo.png --out svg-task.json
codia-design usage --page 1 --page_size 20
```

Image-output commands download returned images by default. Pass `--download-dir DIR` to choose the local output directory; the JSON response will include `data.local_file` or `data.local_files` next to the remote URL fields. Use `--no-download` only when a JSON-only response is required.

The CLI calls the public Open API v2 surface (`/v2/open/*`). Billable commands estimate the `open_api_v2` credit cost before running, then query `codia-design credits` after the operation completes. If the remaining `available_credits` is below 2x the estimated cost, the CLI prints a reminder to stderr but does not block generation. Pass `--estimate` to show the estimate without sending the request. Common fixed prices are `pdf-to-design` 13 credits/page, `pdf-to-ppt` 13 credits/page, `image-to-design` 13 credits/request, `remove-bg` 13 credits/request, `image describe` 5 credits/request, `image layering` 27 credits/request, and `svg create` 13 credits/create. Image generation and several edit tools vary by model and resolution. Use `codia-design limits` or the API reference at `https://codia.ai/api-reference#description/introduction` for the live pricing and limits table.

PDF page numbering is zero-based across PDF APIs:

- `pdf-to-design --pages` is zero-based. Use `0` for the first page.
- `pdf-to-ppt --pages` is zero-based. Use `0` for the first page.

`pdf-to-ppt` follows the task workflow in the public API reference: local files are uploaded to `POST /v2/open/uploads` first, then the CLI creates `operation: "pdf_to_ppt"` with `POST /v2/open/tasks`, polls `GET /v2/open/tasks/:task_id`, and downloads `result.ppt_url`. The API expects NotebookLM-style image-only PDFs; report API errors directly and do not generate local substitute PPTX files unless explicitly requested.

## Security

Before publishing, packaging, or opening a pull request, scan for obvious secrets:

```bash
rg -n --hidden -S \
  -g '!.git' -g '!node_modules' -g '!dist' \
  '(CODIA_API_KEY|api_key_[A-Za-z0-9_-]+|Authorization: Bearer|BEGIN (RSA|EC|OPENSSH) PRIVATE KEY)' .
```

No output means this rule set did not find a matching plaintext secret. It is not a complete security audit.

Read [SECURITY.md](SECURITY.md) for credential handling rules, local file permissions, and runtime bootstrap policy.

## Version

Current public skills release: `v0.1.1`

Requires CLI: `@codia-ai/codia-design-cli >=0.1.1`

The runtime CLI is distributed separately through the `@codia-ai/codia-design-cli` npm package.
