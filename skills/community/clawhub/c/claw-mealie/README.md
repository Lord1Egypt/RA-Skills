# Mealie for OpenClaw

Turn recipe links, photos, PDFs, and notes into recipes in [Mealie](https://mealie.io)—then use them to plan meals and build shopping lists, all through OpenClaw.

- **Import recipes from websites**, or let OpenClaw read images, PDFs, and pasted text into a structured recipe.
- **Keep the details that matter:** ingredients, instructions, quantities, timings, and source attribution, with original files attached when wanted.
- **Manage your kitchen:** find and edit recipes, organize collections, schedule meals, and add ingredients to shopping lists.
- **Access the full advertised API:** the helper discovers your instance's endpoints and schemas rather than relying on a fixed endpoint list. Token permissions still apply.

The Python helper uses only the standard library. Mealie's server-side AI is optional, not required.

## Requirements

- OpenClaw with Python 3 available where commands execute.
- A reachable Mealie instance and an API token.
- For photos and scanned PDFs: image/document tools available to your OpenClaw agent. Text-based PDF extraction optionally uses Poppler's `pdftotext`.

## Install

### 1. Install the skill

```sh
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/Lanjelin/openclaw-mealie.git ~/.openclaw/workspace/skills/mealie
```

This uses OpenClaw's default workspace. If your agent uses a different workspace, install into that workspace's `skills/mealie` directory. To share the skill across agents instead, use `~/.openclaw/skills/mealie` (or `$OPENCLAW_STATE_DIR/skills/mealie` with a custom state directory). Choose one location; a workspace copy takes precedence over a shared copy. Review an existing installation before replacing it.

### 2. Connect Mealie

In Mealie, open your profile's **API Tokens** page (`/user/profile/api-tokens`) and create a token. Use an account with only the permissions you need.

Add these values to **`~/.openclaw/.env`**, or `$OPENCLAW_STATE_DIR/.env` for a custom state directory:

```dotenv
MEALIE_URL=https://mealie.example.com
MEALIE_API_TOKEN=your-mealie-api-token
```

Replace the example values. Use your instance's canonical URL, including any installation prefix, but **do not append `/api`**. Edit an existing `.env` without removing other entries. Keep it outside this repository and protect it:

```sh
chmod 600 ~/.openclaw/.env
```

Adjust the path if you use a custom state directory. No `openclaw.json` entry is required. Restart the OpenClaw Gateway and start a fresh session after updating `.env`.

### 3. Check the skill

```sh
openclaw skills info mealie
```

The skill should be eligible with no missing requirements. If variables are missing, check that `.env` belongs to the Gateway's state directory. Existing process environment values take precedence over `.env`.

## Try it

Ask OpenClaw:

> Import this recipe into Mealie: https://publisher.example/recipe

> Turn this attached recipe photo into a Mealie recipe and keep the original as an attachment.

> Import the recipe from this PDF. Ask me about anything you can't read rather than guessing.

> Plan three dinners using my saved recipes, then add their ingredients to my shopping list.

The skill instructs the agent to check for duplicates, preserve source details, and verify the saved result. Photos and PDFs are read using OpenClaw's available tools before import; uploading an attachment alone does not create recipe ingredients or instructions.

## Update

```sh
git -C ~/.openclaw/workspace/skills/mealie pull --ff-only
```

Use your actual install path if different, then start a fresh OpenClaw session.

## Advanced usage

The helper supports API discovery, JSON requests, multipart uploads, downloads, and recipe imports. See [the workflow reference](./references/workflows.md) for commands and examples, or [SKILL.md](./SKILL.md) for the agent instructions.

To use it directly from a terminal, first export `MEALIE_URL` and `MEALIE_API_TOKEN` into that shell. The helper reads its process environment; it does **not** load `.env` itself.

```sh
python3 ~/.openclaw/workspace/skills/mealie/scripts/mealie.py endpoints --search recipes
python3 ~/.openclaw/workspace/skills/mealie/scripts/mealie.py describe GET /api/recipes
```

## Good to know

- **Sandboxed agents:** Gateway `.env` values are not automatically forwarded into containers. Python, credentials, files, and network access must be available in the execution environment; use approved sandbox configuration rather than disabling isolation.
- **Ingredient scaling:** imported ingredient lines may remain text. Structured quantities and food/unit mappings need review before reliable scaling or shopping-list aggregation.
- **Import limits:** protected websites may not scrape, scans need vision/OCR, and unreadable details need clarification. Not every source field is guaranteed to survive Mealie's normalization.
- **Optional server AI:** requires Mealie configuration and may send source content to an external provider or incur costs.
- **Credentials:** never commit or share your token. Revoke any token that has been exposed. Administrative and destructive operations require appropriate intent and permissions.

Developed against Mealie v3.28.0. API discovery follows your instance's live schema; it does not imply that every endpoint has been tested.

## Development

Run the local regression suite without a Mealie server or real token:

```sh
python3 -B -m unittest discover -s tests -v
```

Documentation: [Mealie API](https://docs.mealie.io/documentation/getting-started/api-usage/) · [OpenClaw skills](https://docs.openclaw.ai/tools/skills) · [OpenClaw environment](https://docs.openclaw.ai/help/environment)

## License

[MIT](./LICENSE) © 2026 Lanjelin.
