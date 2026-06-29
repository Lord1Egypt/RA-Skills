---
name: fix-broken-links
description: 'Scan web files for broken hyperlinks and weak SEO anchor text, then interactively replace, strip, or skip each dead URL. Use when asked to find or fix broken links, check for dead links or 404s, audit hyperlinks, validate URLs, or flag generic anchor text ("click here", "read more") in HTML, Markdown, JS/TS, JSON, CSS, SQL, or template files.'
metadata:
  tags: 'links, seo, html, markdown, url-validation'
---

# Fix Broken Links

Scans web files for broken hyperlinks and reports them. For each broken URL the
skill tries common spelling variations, optionally hands the link to the GitHub
Copilot CLI for suggested replacements, and presents an interactive fix menu.
Generic anchor text (`click here`, `read more`, etc.) is flagged as an SEO issue.

## When to Use This Skill

- User asks to "find broken links", "fix broken links", or "check for dead links / 404s"
- User wants to audit or validate the hyperlinks in edited or changed files
- User wants generic anchor text (`click here`, `here`, `read more`) flagged for SEO
- User wants link checking across HTML, Markdown, JS/TS, JSON, CSS, SQL, or templates

## Prerequisites

- `curl` — HTTP status checks (the script exits quietly if absent)
- `grep`, `sed` — link extraction (standard on any POSIX system)
- Bash 4+ for `scripts/link-fix.sh`; on Windows use Git Bash or WSL, or run the
  PowerShell 7+ port `scripts/link-fix.ps1`
- `jq` — optional; lets the bash script parse a JSON payload piped on stdin
- `git` — optional; used to discover changed files when no paths are passed (falls
  back to a full repo scan)
- `copilot` (GitHub Copilot CLI) — optional; powers agent-suggested replacements.
  Without it, only verified spelling variations are offered.

## How It Works

The script has two modes:

- **With file paths** (passed as command-line arguments): it checks each link,
  looks up replacement candidates, and presents the interactive fix menu.
- **With no file arguments**: it discovers changed files via `git` (or scans the
  repo) and simply lists the broken links — no replacement lookups and no prompts.

Links are found by scanning each file for `http(s)://` URLs, so the same logic
covers every format that embeds absolute URLs.

## Step-by-Step Workflow

### 1. Choose the script for the platform

| Platform | Command |
| --- | --- |
| POSIX / Git Bash / WSL | `bash scripts/link-fix.sh <files...>` |
| Windows PowerShell 7+ | `pwsh scripts/link-fix.ps1 <files...>` |

### 2. Run against the target files

Pass one or more web files to get the full repair flow (lookup + interactive menu):

```bash
bash scripts/link-fix.sh docs/guide.md index.html
```

```powershell
pwsh scripts/link-fix.ps1 docs/guide.md index.html
```

Run with no arguments to report broken links in changed files only (no prompts):

```bash
bash scripts/link-fix.sh
```

### 3. Resolve each broken link

For each broken URL the interactive menu offers:

| Key | Action |
| --- | --- |
| `r` | Replace with the suggested URL (a working variation, or an agent-proposed alternative) |
| `1`–`9` | Replace with a numbered alternative |
| `d` | Strip the link wrapper, keeping the visible text as plain text |
| `c` | Enter a custom replacement URL |
| `s` | Skip |

## Supported Source Types

| Source | Examples matched |
| --- | --- |
| HTML | `<a href>`, `<img src>`, `<script src>`, `<link href>`, `<iframe src>` |
| Markdown | `[text](url)`, `[text][ref]`, bare `<url>` |
| JS / TS / Vue / Svelte | `fetch()`, `XMLHttpRequest.open()`, jQuery, axios, `href:`/`url:` props |
| JSON / JSONL | any string value that is an absolute URL |
| CSS | `url(...)` |
| SQL | URL literals in query strings |
| Templates | Jinja2, ERB, EJS, Handlebars, Pug |

The `d` (remove) action understands HTML `<a>` wrappers and Markdown `[text](url)`
links specifically, keeping the visible text. Other source types support
`r` (replace) and `c` (custom) via literal URL substitution.

## Features

- **Self-contained core**: bash and PowerShell ports — no runtime to install
- **Format-agnostic link scan**: extracts every `http(s)` URL, covering HTML,
  Markdown, JS/TS, JSON, CSS, SQL, and templates at once
- **Automatic URL healing**: tries www, https, and trailing-slash variations
- **Agent-assisted suggestions**: optionally hands the broken link to the Copilot
  CLI for replacement candidates; if the CLI is missing or errors, it offers none
- **SEO audit**: flags anchor text that is too generic to benefit search ranking
- **Large-file guard**: prompts before checking files with more than 50 links
- **Interactive fix menu**: replace with suggestion, enter custom URL, strip tag
  keeping text, or skip

## Example Output

```text
  Checking 2 link(s) in docs/guide.md ...
    BROKEN (404) https://example.com/old-page

------------------------------------------------------------
  SEO anchor issues (consider descriptive link text)
    docs/guide.md: <a href="https://example.com/old-page">click here</a>

============================================================
  fix-broken-links report
============================================================

  [1] docs/guide.md
    URL : https://example.com/old-page
    HTTP: 404

    r  Replace -> https://example.com/docs/install
    1  Replace -> https://example.com/docs/getting-started
    d  Remove link, keep text
    c  Custom replacement URL
    s  Skip
  > r
    replaced

  1 file(s) updated:
    docs/guide.md
```

With no file arguments (or when a file carries no checkable links) the script
stops after the broken-link list — the menu above is skipped.

## File Structure

```
fix-broken-links/
├── SKILL.md            This file
└── scripts/
    ├── link-fix.sh     Bash implementation
    └── link-fix.ps1    PowerShell 7+ port
```

## Limitations

- Only checks absolute `http://` and `https://` URLs; relative paths require a running server
- Dynamic links generated at runtime from database queries are not detectable from source alone
- When `copilot` suggestions are enabled, broken URLs are sent to the Copilot service as prompt input
- Agent-suggested replacements are model proposals and are not verified live; confirm each before accepting
- The `d` (remove) action targets HTML and Markdown link syntax; bare URLs in code are best handled with `r` or `c`

## Troubleshooting

| Issue | Solution |
| --- | --- |
| `curl not found` | Install `curl`; the script exits quietly without it |
| No replacement suggestions offered | Install the `copilot` CLI, or use `c` to enter a custom URL |
| PowerShell script blocked | Run with `pwsh -File scripts/link-fix.ps1` or adjust the execution policy |
| Bash script not executable | Run via `bash scripts/link-fix.sh` or `chmod +x scripts/link-fix.sh` |
