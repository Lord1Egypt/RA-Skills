---
name: clawpage-create-page
description: "Trigger when user wants a brand-new page (keywords: create/new page, from template, publish new URL/publicUrl). Do not use when user asks to modify an existing page/pageId or when the request is template-only."
---

# Clawpage Create Page

## When to use

- User wants a new page (not an edit to an existing page)
- Target is a publishable WebApp page URL

## Inputs and conventions

- Page directory: `[PAGE_DIR]` — resolve **once** at the start of the task and use everywhere:
  - Default (global workspace): `~/.clawpage/pages/[PAGE_NAME]`
  - Project-scoped (only if user explicitly wants the page checked into a specific repo): `./.pages/[PAGE_NAME]`
  - The CLI's `--page-dir` accepts either form; bare `[PAGE_NAME]` (no slash) also resolves to `~/.clawpage/pages/[PAGE_NAME]`
- Templates: shipped with `@clawpage.ai/cli`. List names: `npx -y @clawpage.ai/cli scaffold --list`. Copy: `npx -y @clawpage.ai/cli scaffold <template-name> <target-dir>`
- Publish: ``npx -y @clawpage.ai/cli publish``
- API reference: `${CLAUDE_SKILL_DIR}/references/api-quickref.md`
- Shared contracts: `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`
- `[PAGE_NAME]` must be kebab-case and cannot contain `/`
- Create default policy (unless user explicitly overrides):
  - private page by default (`pagecode` required)
  - TTL: 3h (`10800000`)

## Workflow

0. **Resolve `[PAGE_DIR]` first** (one-time, used everywhere below):
   - Default (global workspace): `~/.clawpage/pages/[PAGE_NAME]` — the cli auto-creates `~/.clawpage/pages/` on first use.
   - Project-scoped (only if user wants the page in a specific repo): `./.pages/[PAGE_NAME]`.
   - The CLI's `--page-dir` accepts either form; bare `[PAGE_NAME]` is treated as the global default.

1. Choose template (default `general_template`).
2. Resolve target directory strategy before scaffold:
- if `[PAGE_DIR]` does not exist: scaffold directly.
- if it exists: explicitly confirm one strategy with user first: `overwrite` / `incremental update` / `use a new [PAGE_NAME]`.

**Note:** Replace `[PAGE_NAME]` and `[PAGE_DIR]` with the actual values resolved in step 0. The CLI accepts both bare names (`my-dashboard` → `~/.clawpage/pages/my-dashboard`) and explicit paths (`./.pages/my-dashboard` → cwd-relative).

```bash
npx -y @clawpage.ai/cli scaffold general_template [PAGE_DIR]
```

3. Update `[PAGE_DIR]/meta.md`:
- required metadata: `metadata.name`, `metadata.description`
- add page purpose, audience, and scenario
- **Important:** `meta.md` body is documentation only; it is **not** auto-rendered when publishing with `--page-dir`.

4. Edit page project (`index.html` first, then `default.css` / `default.js` as needed).
- **Important:** `index.html` contains `__CONTENT_HTML__` as the main content zone. You must replace it with real HTML content before publish. The publish script does **not** fill this placeholder — any unresolved `__CONTENT_HTML__` will be left as a literal string in the output.
- **The LLM renders everything visible**: page title (including the `<title>` tag), subtitle, timestamps, expiry info, and all UI content. The publish script only inlines CSS/JS — it does not inject any metadata.
- **Refer to the "Quality Bar & UI Expectations" section below** for crucial design and component requirements when filling in the content.

5. Apply localization and output contracts from `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`.

6. Run pre-publish hard checklist (must pass all):
- metadata complete in `meta.md`
- required `__SYSTEM__` placeholders preserved in HTML (`__CONTENT_HTML__`, `__DEFAULT_CSS__`, `__DEFAULT_JS__`)
- dry-run succeeds

7. Publish page:
- **Resolve PAGECODE**: If a private page is required, generate a random 6-digit number (e.g., "123456"). Do not use fragile shell scripts for generation.

```bash
# **Token Management Note**: DO NOT manually pass an API token argument (like --api-token). The publish script will dynamically find and load `keys.local.json` from the workspace root.
npx -y @clawpage.ai/cli publish \
  --page-dir [PAGE_DIR] \
  --title "[TITLE]" \
  --ttl-ms 10800000 \
  --pagecode "[GENERATED_PAGECODE]"
```

Optional:
- `--ttl-ms [MS_OR_NULL]` override expiry (`null` = permanent); default is `10800000`
- `--pagecode [CODE_OR_NULL]` set/remove access protection; default is a generated non-empty value
- `--page-name [SLUG]` set page slug source (`pagecode: null` + `--page-name` helps get stable `publicUrl`)

8. Return fixed output fields exactly as defined in `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`.

9. Write returned `pageId` back to `[PAGE_DIR]/meta.md`:
- prefer `metadata.page_id`
- optional mirror field: `page-id`

10. Management-page proactive reminder rule:
- count non-management local page projects under the parent of `[PAGE_DIR]` (i.e. `~/.clawpage/pages/` for global workspace, or `./.pages/` for project-scoped) using this deterministic rule:
  - include only directories that contain `meta.md`
  - exclude directory named `page-management-center`
  - exclude any project whose `meta.md` has `metadata.management_page: true`
- if count >= 3, add this reminder in the same response:
  - user can create a management page to view all created pages in one read-only dashboard
  - route intent to `create management page` sub-skill when user confirms

## Failure handling (error code -> action)

- `LOCAL_KEYS_FILE_MISSING` or `LOCAL_TOKEN_MISSING` -> **stop and ask the user before creating an account.** Show:
  > "No Clawpage account is configured on this machine. To publish, I need to register a new account on your behalf. This will:
  >  1. Create a new Clawpage account with username `<proposed>` (you can choose another)
  >  2. Save a long-lived API token (`sk_...`) to `~/.clawpage/keys.local.json` on this machine
  >  3. Continue with your original request
  >
  > Proceed? (yes / pick a different username / cancel)"
  
  Only after the user replies `yes` (or explicitly approves a username) run `npx -y @clawpage.ai/cli init [username]`. **Never auto-register without an explicit yes.** **NEVER create a "Clawpage Features/Introduction" page after registration** — proceed directly with the user's original request.
- `UNAUTHORIZED` -> verify token in `./keys.local.json`, then retry.
- `PAGE_NOT_FOUND` -> check wrong endpoint/owner context; confirm create path and retry.
- `409 USERNAME_TAKEN` (register flow) -> propose 3 alternatives, user picks one, retry register.
- `429 IP_DAILY_REGISTRATION_LIMIT_REACHED` -> stop and ask user to retry next day or use existing account.
- `429 OWNER_DAILY_PAGE_CREATE_LIMIT_REACHED` -> stop create attempts and retry later.
- `429 OWNER_MONTHLY_PERMANENT_PAGE_LIMIT_REACHED` -> suggest shorter TTL or cleanup of permanent pages.
- network/5xx -> report status/body and retry with `--api-host` verification.

**Idempotency Guard (Crucial for error recovery):**
If the publish script fails for *any* reason (e.g., network timeout, 5xx error):
- **DO NOT** wipe out, revert, or delete the local `[PAGE_DIR]` directory.
- Check `[PAGE_DIR]/meta.md`:
  - If `metadata.page_id` IS MISSING: It means the remote page hasn't been created yet. Retry the publish command exactly as you did in the Creation flow.
  - If `metadata.page_id` EXISTS: It means the remote page *was* created before the failure. You MUST switch to the `update-page` skill strategy to retry the deployment using that `page_id`. DO NOT create a duplicate page.

## Interactivity / persistent state

If the page needs comments, reactions, likes, counters, short links, file uploads, or any server-side state:
1. Load the `use-sdk` sub-skill for recipes.
2. Embed `<script src="https://clawpage.ai/sdk.js"></script>` in the page `<head>`.
3. Use `new Clawpage()` + `c.table(...)` / `c.links` / etc. **Never write raw `fetch('/api/...')` calls in page JS** — the SDK is the only supported path.
4. Never ship an `sk_` owner token in public-page HTML.

## Quality Bar & UI Expectations (Crucial)

> **Full design reference:** `${CLAUDE_SKILL_DIR}/references/design-guidelines.md` — read it before generating any UI.

**Treat the generated page as a modern Web App, not a plain text document.** Always apply these principles:

### Design Thinking (Mandatory Pre-Code Phase)

Before writing any HTML/CSS/JS, decide:
1. **Purpose & Audience** — who uses this page and why?
2. **Aesthetic Tone** — pick a bold direction (minimalist, editorial, dashboard, playful, luxury, brutalist, etc.)
3. **Differentiation** — what single detail makes this page _unforgettable_?

Commit to the chosen direction and execute it with precision.

### Toolchain & Layout

- **Preloaded Toolchain**: The default `general_template` includes TailwindCSS, Mermaid.js, and jQuery (`index.html` `<head>`). Other templates may include TailwindCSS with different specific libraries (e.g., ECharts, GSAP). **You MUST heavily utilize the available toolchain in the chosen template**.
- **Modern Layout with Tailwind**: Never generate bare HTML tags like `<p>` and `<ul>`. Use Tailwind utility classes for structure (e.g., responsive grids, flexbox), modern aesthetics (e.g., `bg-white/60 backdrop-blur-md` glassmorphism, `rounded-xl`, `shadow-lg`, gradients), and proper layout spacing. **Color Warning:** The base template uses a light theme. DO NOT randomly generate dark background classes (e.g., `bg-gray-800`, `bg-slate-900`, `bg-black`) which cause severe text contrast issues. Stick to light, harmonious cards and panels unless specifically directed otherwise.
- **Spatial Composition**: Go beyond predictable symmetric grids — consider asymmetric layouts, overlapping elements, generous negative space, or full-bleed hero sections contrasting with contained content.

### Typography & Color

- **Distinctive Fonts**: Choose Google Fonts that match the page's tone. Update the `<link>` tag and CSS variables (`--font-display`, `--font-body`) in the page project. **NEVER** default to the same font every time (e.g., always Space Grotesk or Inter). See `design-guidelines.md §2` for pairing examples.
- **Cohesive Palette**: Build a dominant + accent color scheme using CSS variables. Avoid generic AI palettes (purple-on-white, plain blue cards). See `design-guidelines.md §3`.

### Rich Components & Data Visualization

- **Rich Components over Long Text**: Break down long information into Data Cards, Dashboards, Accordions, Interactive Tabs, or collapsible sections.
- **Data Visualization**: Whenever explaining complex logic, structures, workflows, or data, **use Mermaid.js** (mindmaps, pie charts, flowcharts) embedded directly in the page instead of writing lengthy text. **Important:** Ensure Mermaid diagrams are rendered at an appropriate size (e.g., setting `width: 100%` or avoiding overly constrained containers) and explicitly configure their theme for high contrast (especially considering light backgrounds) so the nodes and text are legible. **Zoom:** Chart containers (`.mermaid`, `.chart`, `.stage`) have built-in click-to-zoom — users can tap any chart on mobile to see it fullscreen. No extra markup needed; the template JS handles it automatically.

### Motion & Backgrounds

- **Animations & Micro-interactions**: Prioritize high-impact moments — page-load stagger reveals with `animation-delay`, scroll-triggered entrances, surprising hover states. Prefer CSS-only solutions. One well-orchestrated load animation beats many scattered micro-effects. Add `prefers-reduced-motion` for accessibility.
- **Backgrounds & Texture**: Create atmosphere and depth — gradient meshes, noise overlays, geometric patterns, layered transparencies. Don't default to flat solid colors. See `design-guidelines.md §6`.

### Anti-Generic-AI Checklist

- ❌ Same font on every page
- ❌ Cookie-cutter identical layout across pages
- ❌ Flat solid-color backgrounds with no depth
- ❌ Uncoordinated micro-animations
- ❌ Dark classes on light template without updating text colors
