# Clawnoter Obsidian

Save web articles and links into Obsidian from OpenClaw.

Clawnoter Obsidian is an OpenClaw skill for people who want a lightweight way to collect useful links, extract webpage content, and store the result inside a local Obsidian vault.

## What This Skill Does

- Saves a webpage into your Obsidian vault
- Downloads article images into an `images/` folder
- Stores article metadata in YAML frontmatter
- Supports an optional `page_comment`
- Includes first-run vault discovery and path configuration

## Install From ClawHub

This skill is primarily distributed through ClawHub.

If you want the easiest path, install it directly with:

```bash
clawhub install clawnoter-obsidian-save
```

After installation, the skill will be available to your OpenClaw agent.

## GitHub Repository

This repository is mainly for:

- source code
- issue tracking
- collaboration
- version history

For normal users, the recommended installation path is still ClawHub rather than manual copying from GitHub.

## How It Connects To OpenClaw

This repository does not need a separate service or plugin host.

To work inside OpenClaw, it only needs:

1. The skill to be installed into OpenClaw through ClawHub
2. `python3` available on the local machine
3. Access to a local writable Obsidian vault
4. Network access to fetch webpage content

Once installed, OpenClaw can invoke the skill when the user asks to save a link or article into Obsidian.

The runtime entrypoint for article saving is:

```bash
python ./scripts/save_article.py "<url>" "<save_path>" "[page_comment]"
```

`download_images.py` is an internal helper and is no longer meant to be called directly.

## First Run Experience

On the first real use, the skill will:

1. Introduce Clawnoter
2. Ask whether the user wants local Obsidian or iCloud Obsidian
3. If local Obsidian is selected, scan common local vault locations first
4. Ask the user to confirm the vault to use
5. Ask for an optional subfolder such as `Articles` or `ReadLater`
6. Save the configuration to:

```text
~/.obsidian-save-article-config.json
```

## Example Usage

Users can trigger it with prompts like:

- `保存到 Obsidian：https://example.com/article`
- `帮我保存这个链接到 Obsidian：https://example.com/article`
- `保存到 Obsidian：https://example.com/article page_comment：之后可以再展开`
- `查看保存路径`
- `重新配置`

## What Gets Saved

Typical saved content includes:

- Article title
- Original URL
- User `page_comment`
- Main article body
- Successfully downloaded images

The generated note is organized for Obsidian and includes YAML frontmatter plus the article body in a callout block.

## Runtime Requirements

- `python3`
- Network access to the target webpage
- A local writable Obsidian vault

## Optional Browser Fallback

The skill works without extra Python packages for its base path:

- `Jina`
- raw HTML fallback
- image downloading

For a stronger third-layer browser-rendered fallback on complex pages like WeChat or X, users can optionally install:

```bash
pip install playwright
playwright install chromium
```

If `playwright` is not installed, the skill will skip browser fallback automatically and continue with the base extraction path.

## Notes And Limits

- Primary fetch path uses `https://r.jina.ai/<URL>`
- If Jina fails, the skill falls back to raw HTML fetch plus local conversion
- If raw HTML extraction is still low quality, the skill falls back again to a local browser-rendered capture
- Login-required or heavily JavaScript-rendered pages may not extract cleanly
- Some images may fail to download, but article saving should still continue
