# Apify-First Agent Install Note

For Codex, Claude, OpenClaw, Cursor, and custom agents:

1. Install the `beyond-seo` folder.
2. Configure only `APIFY_API_TOKEN` as the main token.
3. Restart the agent/runtime so the environment variable is loaded.
4. The skill should use Apify actors first for crawling, SERP, maps, trends, PageSpeed/Lighthouse, GSC/GA4-style connector/export workflows, and backlink/authority checks.

Do not place the token inside any Markdown, JSON, CSV, or report file.


---

# Install Beyond SEO in Different AI Agents

## Codex

1. Keep the folder name as `beyond-seo`.
2. Ensure `SKILL.md` is at the root of the folder.
3. `SKILL.md` includes YAML frontmatter for Codex-style skill discovery.
4. Add the full folder to the project or skills directory.
5. Tell Codex: "Use the Beyond SEO skill. Read SKILL.md first."

## Claude Projects

1. Upload the full `beyond-seo` folder or ZIP.
2. Add this project instruction:
   "Use Beyond SEO as the operating system for SEO, AEO/GEO, backlinks, local SEO, competitor research, keyword mapping, and reporting. Read SKILL.md first."

## OpenClaw

1. Add the folder to your skills or agent knowledge directory.
2. Register/alias it as `beyond-seo`.
3. Allow the agent to access the Markdown files and optional Python tools.
4. If Apify is available, expose `APIFY_API_TOKEN`.

## Cursor / Local Agents

1. Place the folder inside your repo.
2. Open `SKILL.md`.
3. Use the supporting modules as task-specific SOPs.
4. Install optional Python requirements only if using `/tools`.

## Optional Environment Variables

```text
APIFY_API_TOKEN
PAGESPEED_API_KEY
GSC_EXPORT_PATH
GA4_EXPORT_PATH
AHREFS_EXPORT_PATH
SEMRUSH_EXPORT_PATH
MOZ_EXPORT_PATH
SCREAMING_FROG_EXPORT_PATH
CUSTOM_SCRAPER_API_KEY
CUSTOM_SCRAPER_BASE_URL
```

## Optional Python Setup

```bash
pip install -r requirements.txt
```
