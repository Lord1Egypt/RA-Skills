---
name: docsforai
description: Crawl and read documentation websites using DocsForAI. Use when you need to learn a new library, framework, or tool by reading its official docs; when you want to look up how something works from documentation; when writing or debugging code that requires understanding of a specific SDK/API; when the user asks you to "read the docs", "check the documentation", or "learn how to use X". Supports VitePress, Docsify, Mintlify, Docusaurus, mdBook, MkDocs, Starlight, GitBook, Feishu Docs, and generic sites. Auto-detects framework type.
metadata:
  openclaw:
    requires:
      bins: ["docsforai"]
    install:
      - id: docsforai
        kind: uv
        package: docsforai
        bins: ["docsforai"]
        label: Install DocsForAI (PyPI)
---

# DocsForAI — Documentation Crawler Skill

Crawl any documentation website into structured, persistent Markdown files and read them on demand — so you always work from accurate, up-to-date documentation rather than training-data guesses.

**Source:** https://pypi.org/project/docsforai/ | https://github.com/dx2331lxz/DocsForAI | **Latest:** 0.6.0

---

## Install (one-time)

```bash
uv tool install docsforai   # recommended: isolated, no system Python pollution
pip install --break-system-packages docsforai  # fallback if uv unavailable
```

Verify: `docsforai --version`

---

## Core Principles

**Always use `multi-md` format.** It preserves the site's original chapter hierarchy as individual files, so you can navigate to exactly the section you need without loading the entire documentation into context.

**Output rule:** docsforai writes directly to `<output>/<site-name>/` — no extra subdirectory is created.

**Docs are persistent.** Once crawled, they live on disk across sessions. Check before crawling; never re-crawl what already exists.

---

## Workflow

### Step 1 — Check if docs already exist

Before doing anything else, check both the local filesystem and MEMORY.md:

```bash
ls ~/.openclaw/workspace/skills/docsforai/docs/
```

Also look up the **「已下载文档（DocsForAI）」** section in MEMORY.md for a record of previously crawled sites and their paths.

If the site folder already exists → skip to Step 3.

### Step 2 — Crawl (only if not already downloaded)

Always pass the skill's `docs/` directory as `-o`. DocsForAI creates `<site-name>/` inside it automatically.

```bash
docsforai crawl <URL> -f multi-md \
  -o ~/.openclaw/workspace/skills/docsforai/docs
```

Common examples:

| URL | Site name | Final path |
|---|---|---|
| https://vitepress.dev/guide | `vitepress` | `docs/vitepress/` |
| https://docs.pydantic.dev | `pydantic` | `docs/pydantic/` |
| https://docusaurus.io/docs | `docusaurus` | `docs/docusaurus/` |
| https://react.dev/learn | `react` | `docs/react/` |
| https://docs.python.org/3 | `python` | `docs/python/` |

After crawling completes, proceed to Step 2b.

#### Step 2b — Record to MEMORY.md (required)

Append a row to the 「已下载文档（DocsForAI）」section in MEMORY.md. Create the section if it doesn't exist yet:

```markdown
## 已下载文档（DocsForAI）

| Site | Local path | Crawled |
|---|---|---|
| vitepress | ~/.openclaw/workspace/skills/docsforai/docs/vitepress/ | 2026-04-02 |
```

Never overwrite existing rows — always append.

### Step 3 — Map the structure

Before reading any file, get a full picture of the directory tree:

```bash
find ~/.openclaw/workspace/skills/docsforai/docs/<site-name> -name "*.md" | sort
```

Scan the output. Identify which subdirectories and files correspond to the topic you need. This costs nothing and saves you from loading irrelevant chapters.

### Step 4 — Read on demand (the most important step)

**Load only what is directly relevant to the current task.** Follow this decision tree:

#### 4a. You need a quick orientation
Read the top-level index first:
```bash
read ~/.openclaw/workspace/skills/docsforai/docs/<site-name>/index.md
```

#### 4b. You know roughly what you need
Read the specific chapter file directly:
```bash
read ~/.openclaw/workspace/skills/docsforai/docs/<site-name>/guide/configuration.md
read ~/.openclaw/workspace/skills/docsforai/docs/<site-name>/reference/api.md
```

#### 4c. You need to find where something is documented
Search across all files for a keyword, then read only the matching file:
```bash
# Find which file covers a specific topic
grep -rl "defineConfig\|plugin\|vite" \
  ~/.openclaw/workspace/skills/docsforai/docs/<site-name>/ | head -10
```

#### 4d. You need to understand a full feature area
Read the section index, then follow up with the specific sub-pages you need:
```bash
# Read section overview
read ~/.openclaw/workspace/skills/docsforai/docs/<site-name>/guide/index.md

# Then read only the sub-pages that apply
read ~/.openclaw/workspace/skills/docsforai/docs/<site-name>/guide/routing.md
```

**Rules:**
- Never read the entire docs tree in one go
- Stop reading once you have enough to proceed
- If you read something and it's not what you needed, search more precisely rather than loading more files

---

## When to Consult Docs (decision guide)

Use this skill proactively whenever you are about to:

| Situation | Action |
|---|---|
| Use an API you haven't used in this session | Read the relevant API reference page |
| Write configuration for a framework | Read the configuration guide |
| Debug an unexpected behavior | Search docs for the error or behavior, read matching section |
| Use a CLI tool you're unfamiliar with | Read the CLI reference page |
| Implement a non-trivial feature | Read the feature's guide page before writing code |
| Upgrade a library version | Check migration or changelog docs first |

**Do not guess** at API signatures, config options, or CLI flags when the docs are available on disk. A 2-second read beats a hallucinated parameter.

---

## CLI Reference

```bash
# Standard crawl
docsforai crawl <URL> -f multi-md -o <output-dir>

# Force framework type (skip auto-detection)
docsforai crawl <URL> --type nextdocs -f multi-md -o <output-dir>
docsforai crawl <URL> --type mkdocs -f multi-md -o <output-dir>

# Polite crawling (for rate-sensitive sites)
docsforai crawl <URL> -f multi-md --concurrency 2 --delay 0.5 -o <output-dir>

# Limit pages (generic mode only)
docsforai crawl <URL> -f multi-md --max-pages 100 -o <output-dir>
```

## Supported Frameworks (auto-detected)

| Framework | Detection signal |
|---|---|
| VitePress | `.VPSidebar` CSS class / generator meta |
| Docsify | `$docsify` global variable — fetches raw `.md` source |
| Mintlify | `x-llms-txt` response header — single request for full content |
| Docusaurus | generator meta / `.theme-doc-sidebar-container` |
| mdBook | `#mdbook-sidebar` / `ol.chapter` |
| MkDocs | generator meta / `.md-nav--primary` (Material + default themes) |
| Starlight | `#starlight__sidebar` / `.sl-markdown-content` |
| GitBook | generator meta `GitBook` / sitemap-based discovery |
| NextDocs | `/_next/` assets + `.mdx-content` — sitemap discovery + sidebar fallback |
| Feishu Docs | `open.feishu.cn` domain — internal API |
| Generic | BFS link traversal — fallback for any other site |

## Tips

- **Mintlify sites** fetch everything in one request — near-instant
- **Cloudflare-protected sites** — DocsForAI auto-retries with system `curl`
- **Count total pages:** `find ~/.openclaw/workspace/skills/docsforai/docs/<site> -name "*.md" | wc -l`
- **Re-crawl to refresh:** delete the site folder first, then crawl again
