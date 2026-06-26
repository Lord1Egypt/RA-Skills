---
name: clawpage-update-page
description: "Trigger when user wants to modify an existing page/project/pageId (keywords: update existing page, revise, page-id, 基于旧页面). Do not use for brand-new pages or template-only changes."
---

# Clawpage Update Page

## When to use

- User wants to modify an existing page (structure, style, interaction, or content)
- User mentions reusing an existing page/project

## Paths and conventions

- Page directory: `[PAGE_DIR]` — resolve **once** at the start:
  - Default (global workspace): `~/.clawpage/pages/[PAGE_NAME]`
  - Project-scoped: `./.pages/[PAGE_NAME]` (only if the existing page lives in a project repo)
  - Listing existing pages: `ls ~/.clawpage/pages/` (default) or `find ./.pages -mindepth 2 -maxdepth 2 -name meta.md` (project-scoped)
- Page files: `meta.md`, `index.html`, `default.css`, `default.js`
- Publish: ``npx -y @clawpage.ai/cli publish``
- API reference: `${CLAUDE_SKILL_DIR}/references/api-quickref.md` (`PATCH /api/pages/<pageId>`)
- Shared contracts: `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`
- `[PAGE_NAME]` must be kebab-case and cannot contain `/`

## Matching strategy (two-phase)

1. Determine where the page lives. Default scan locations: `~/.clawpage/pages/` (global workspace) and `./.pages/` (project-scoped). If the user specified a different location in this or the preceding turn (e.g. `/tmp/clawpage-pages`), use that instead. If neither default has the page and the user didn't specify, ask before scanning other directories — cross-project scans can match the wrong page.

Then read metadata only first:

```bash
find ~/.clawpage/pages ./.pages -mindepth 2 -maxdepth 2 -name meta.md 2>/dev/null | while read -r f; do
  echo "== $f ==";
  sed -n '1,24p' "$f";
done
```

2. Read full `meta.md` only for shortlisted candidates.

## Update workflow

1. Edit `index.html` first.
2. Update `default.css` / `default.js` as required.
3. **Identify PAGE_ID**: Use `read_file` to read `[PAGE_DIR]/meta.md` and extract `metadata.page_id` from the YAML frontmatter. Do not use fragile shell scripts for extraction.

4. If semantics changed, sync `meta.md` metadata and notes.

5. Apply localization and output contracts from `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`.

6. Run pre-publish hard checklist (must pass all):
   - metadata complete in `meta.md`
   - required `__SYSTEM__` placeholders preserved in HTML (`__CONTENT_HTML__`, `__DEFAULT_CSS__`, `__DEFAULT_JS__`)
   - dry-run succeeds

7. Publish update:
   **Note:** Replace `[PAGE_DIR]` / `[PAGE_ID]` / `[TITLE]` with real values. The CLI accepts bare names (`my-dashboard`) and absolute / cwd-relative paths.

```bash
# **Token Management Note**: DO NOT manually pass an API token argument (like --api-token). The publish script will dynamically find and load `keys.local.json` from the workspace root.
npx -y @clawpage.ai/cli publish \
  --page-dir [PAGE_DIR] \
  --page-id "[PAGE_ID]" \
  --title "[TITLE]"
```

Optional:
- `--ttl-ms [MS_OR_NULL]` modify expiry (`null` = permanent, omitted = unchanged)
- `--pagecode [CODE_OR_NULL]` set/remove access protection
- `--page-name [SLUG]` rename page

8. Return fixed output fields exactly as defined in `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`.

## If `page-id` is missing

- tell user the local page is not yet bound to a remote `pageId`
- optionally create once, write back `pageId`, then continue update workflow
- when this fallback create is used, apply create default policy unless user explicitly overrides:
  - private page (`pagecode` required)
  - `ttlMs=10800000` (3h)

## Failure handling (error code -> action)

- `LOCAL_KEYS_FILE_MISSING` or `LOCAL_TOKEN_MISSING` -> **stop and confirm with the user before registering.** This is an "update" workflow — the user expects to modify an existing page, not create an account. Show:
  > "I can't find a Clawpage account on this machine. Update normally requires a token. Options:
  >  1. Register a new account now (creates `~/.clawpage/keys.local.json`)
  >  2. Cancel — you may have a token elsewhere or want to switch accounts first
  >
  > Which?"
  
  Only proceed with `npx -y @clawpage.ai/cli init` if the user explicitly chooses option 1. **NEVER create a "Clawpage Features/Introduction" page after registration** — proceed with the original update request.
- `UNAUTHORIZED` -> verify token in `./keys.local.json`, then retry.
- `PAGE_NOT_FOUND` -> verify `pageId` ownership/existence; if unbound, create first and write back `pageId`.
- `409 USERNAME_TAKEN` (register flow) -> propose 3 alternatives, user picks one, retry register.
- `429 IP_DAILY_REGISTRATION_LIMIT_REACHED` -> stop and ask user to retry next day or use existing account.
- `429 OWNER_DAILY_PAGE_CREATE_LIMIT_REACHED` -> stop create attempts and retry later.
- `429 OWNER_MONTHLY_PERMANENT_PAGE_LIMIT_REACHED` -> suggest shorter TTL or cleanup of permanent pages.
- network/5xx -> report status/body and retry with `--api-host` verification.

**Idempotency Guard (Crucial for error recovery):**
If the publish script fails for *any* reason (e.g., network timeout, 5xx error):
- **DO NOT** wipe out, revert, or delete the local `[PAGE_DIR]` directory.
- Check `[PAGE_DIR]/meta.md`:
  - If `metadata.page_id` IS MISSING: It means the remote page hasn't been created yet. You MUST switch to the `create-page` skill strategy to retry the deployment.
  - If `metadata.page_id` EXISTS: It means the remote page *was* created before or you are updating successfully. Retry the `update-page` publish command exactly as before.

## Adding interactivity to an existing page

If the edit introduces server-state features (comments, likes, counters, uploads, short links, stats):
1. Use the `use-sdk` sub-skill.
2. Add `<script src="https://clawpage.ai/sdk.js"></script>` if not already present.
3. Use the SDK (`new Clawpage()`, `c.table(...)`, `c.links`, etc.) — raw `fetch('/api/...')` is forbidden in page JS.
4. If the existing page has raw `fetch('/api/...')` calls, migrate them to the SDK as part of the edit.

## Quality Bar & UI Expectations (Crucial)

> **Full design reference:** `${CLAUDE_SKILL_DIR}/references/design-guidelines.md` — read it before generating any UI.

**Treat the updated page as a modern Web App, not a plain text document.** Always apply these principles:

### Update-Specific: Design Consistency

- **Preserve existing design language** — maintain the current page's font choices, color palette, layout patterns, and animation style unless the user explicitly requests a style change.
- If the user requests a visual overhaul, run the full Design Thinking phase from `design-guidelines.md §1`.

### Toolchain & Layout

- **Keep WebApp behavior**, do not regress an interactive page into an article-only page.
- **Preloaded Toolchain**: Rely heavily on the available preloaded toolchain. `general_template` provides TailwindCSS, Mermaid.js, and jQuery. Other templates provide TailwindCSS and possibly specific libraries (e.g., GSAP, ECharts). Check the `<head>` of `index.html` to see what is available.
- **Modern Layout**: Use Tailwind utility classes for modern aesthetics (e.g., responsive grids, flexbox, glassmorphism `bg-white/60 backdrop-blur-md`, `rounded-xl`, `shadow-lg`). Do not output bare HTML tags without styling. **Color Warning:** The base template uses a light theme. DO NOT randomly generate dark background classes (e.g., `bg-gray-800`, `bg-slate-900`, `bg-black`) which cause severe text contrast issues. Stick to light, harmonious cards and panels unless specifically directed otherwise.
- **Spatial Composition**: Maintain or enhance the page's spatial structure — asymmetric layouts, negative space, full-bleed sections where appropriate.

### Typography & Color

- **Distinctive Fonts**: When adding new sections, match the page's existing font choices. If fonts are generic defaults, consider upgrading them per `design-guidelines.md §2`.
- **Cohesive Palette**: Extend the existing color scheme consistently. Use CSS variables for new colors. See `design-guidelines.md §3`.

### Rich Components & Data Visualization

- **Rich Components**: Prioritize modular panels, data cards, state areas, accordions, and interaction blocks over raw text paragraphs.
- **Data Visualization**: Use Mermaid.js (mindmaps, pie charts, flowcharts) for complex logic/structure instead of long text explanations. **Important:** Ensure Mermaid diagrams are rendered at an appropriate size (e.g., setting `width: 100%` or avoiding overly constrained containers) and explicitly configure their theme for high contrast (especially considering light backgrounds) so the nodes and text are legible.

### Motion & Backgrounds

- **Animations & Micro-interactions**: Add engaging CSS animations (fade-in, slide-up keyframes) and interactive hover states in `default.css` to make the page feel premium. Prioritize page-load stagger and scroll-triggered entrances. Include `prefers-reduced-motion` for accessibility.
- **Backgrounds & Texture**: Enhance atmosphere with depth techniques (gradient meshes, noise, geometric patterns) — see `design-guidelines.md §6`.

### Anti-Generic-AI Checklist

- ❌ Regressing an interactive page to plain text
- ❌ Adding new sections with mismatched fonts or colors
- ❌ Flat solid-color backgrounds with no depth
- ❌ Dark classes on light template without updating text colors
