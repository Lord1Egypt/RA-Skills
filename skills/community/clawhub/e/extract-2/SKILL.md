---
name: extract
description: >-
  Reverse-engineer the design taste of any website. Given a URL, captures DOM data
  and screenshots via Playwright (MCP if available, standalone fallback if not),
  then runs a 4-step analysis pipeline to produce {domain}.md + {domain}.json with
  practical design tokens (colors, typography, spacing, radii, shadows, grid, motion)
  AND taste DNA (Trigger → Decision → Reason → Evidence → Trade-off explaining WHY
  the design works, with confidence scoring). Supports multi-page crawl for system-level
  signals and comparative mode for two-site delta analysis. Use whenever the user wants
  to extract a site's design system, study a competitor's visual language, port an
  aesthetic to a new project, or generate design guidance for an AI coding agent.
  Triggers on '/extract <url>', 'analyze the design of X', 'what makes X's site good',
  'extract design tokens from X', 'give me X's design DNA', 'build something in the
  style of X', 'I want my app to feel like X', 'compare the design of X and Y',
  '/extract <url1> vs <url2>'. Output rejects AI slop ('clean', 'modern', 'user-friendly')
  in favor of concrete px/hex values and restraint trade-offs. Do NOT use for scraping
  data, summarizing page content, or tasks unrelated to visual design.
compatibility: >-
  Works with or without Playwright MCP. If MCP is connected (mcp__playwright__* tools
  available), uses it for faster capture. If not, falls back to a bundled standalone
  Playwright script (Node.js) — zero MCP setup required. Playwright npm package must
  be available: npx playwright install chromium (one-time, ~100MB).
metadata:
  version: "1.0.0"
  author: Built from PRD, adapted from senlindesign/taste-skill (MIT)
  license: MIT
---

# Extract — Reverse-Engineer a Website's Design DNA

This skill turns a URL into two files:

- **`./{domain}.md`** — human-readable. Two sections:
  - **Design Map** — practical tokens (colors, type scale, spacing, radii, shadows, grid, motion)
  - **Taste DNA** — 3–4 opinionated trade-offs (Trigger → Decision → Reason → Evidence → Trade-off) with confidence scores
  - **Delta** (comparative mode only) — agreements vs divergences between two sites
- **`./{domain}.json`** — structured, machine-parseable. Same data, for downstream tools and for `/graft`.

The pipeline rejects generic descriptions like "clean and modern". A finished report should read like a senior designer explaining *why* this particular page made *these particular* choices — and what plausible alternatives it rejected.

## When to activate

Trigger this skill whenever the user wants to study a website's design. Catch all of these:

- Explicit: `/extract <url>` or `/extract <url1> vs <url2>`
- Natural language: "analyze the design of vercel.com", "what makes Stripe's site so good", "extract the design tokens from linear.app", "give me the design DNA for are.na"
- Mimicry intent: "I want my dashboard to feel like Linear", "build me a landing page in the style of <url>", "port this site's design to my project"
- Comparative: "compare the design of X and Y", "how does X's design differ from Y's"
- Any mention of a URL in connection with visual/design topics

When in doubt, activate. The cost of a wasted invocation is small; the cost of generating generic design advice when this skill could have produced specific, evidence-backed analysis is large.

Do NOT activate for: "extract data from a website" (scraping), "summarize the content of <url>" (not design), "deploy this site" (unrelated).

---

## Phase 0 — Parse URL and Setup

### Step 1 — URL

Extract the URL(s) from the user's message. Accept these forms:
- `/extract https://linear.app`
- `/extract https://stripe.com vs https://vercel.com` → comparative mode
- "analyze the design of vercel.com" (add `https://` if missing)
- A bare URL anywhere in the prompt

If no URL provided, ask for one. If it's clearly not a URL (file path, etc.), ask if they meant a hosted page.

Resolve common short forms: `linear.app` → `https://linear.app`, `www.stripe.com` → `https://www.stripe.com`.

### Step 2 — Extract domain for file naming

From the URL, extract the hostname and strip any `www.` prefix:
- `https://linear.app` → `linear.app`
- `https://www.stripe.com` → `stripe.com`
- `https://vercel.com/home` → `vercel.com`

Store as `{domain}`. All output files use this: `{domain}.md`, `{domain}.json`. **Never** use the generic name `taste.md` — it collides across runs.

### Step 3 — Setup questions

If the user already specified export target AND crawl scope, skip. Otherwise, ask once:

> Two quick questions before I start:
>
> **Export target** — which tool are you building with?
> 1. Cursor → `.cursor/rules/{domain}-taste.mdc`
> 2. Windsurf → `.windsurf/rules/{domain}-taste.md`
> 3. Claude Code → CLAUDE.md (appends Design Taste section)
> 4. GitHub Copilot → `.github/copilot-instructions.md` (appends)
> 5. Bolt → `.bolt/prompt`
> 6. Antigravity → GEMINI.md
> 7. v0 by Vercel → `taste-tokens.css` + instructions
> 8. Figma Make → `taste-figma.css` + instructions
> 9. Lovable → print text to paste in Project Knowledge
> 10. Skip → keep `{domain}.md` + `{domain}.json` only
>
> **Crawl scope** — this page only, or explore 2–3 linked pages?
> 1. This page only → faster, focused on exactly what you gave me
> 2. Explore linked pages → I'll visit 2–3 nav pages and merge the data
>
> **Comparative mode** (if single URL given) — analyze alone, or also compare against a second URL?

Store answers. Defaults: export = "skip", crawl = "single". Do not ask again.

---

## Phase 1 — Capture Page Data

### Detect capture method

Check if Playwright MCP tools are available:

**If MCP is available** (`mcp__playwright__browser_navigate`, `mcp__playwright__browser_evaluate`, etc. respond):
→ Use MCP path (faster, lower token cost).

**If MCP is NOT available:**
→ Use the bundled fallback script. Run:
```bash
node extract/references/capture-fallback.mjs --url <url> --domain <domain> [--crawl] [--compare <url2>]
```
If `playwright` is not installed, first run: `npx playwright install chromium`
The fallback script produces the same data shape as MCP capture — downstream analysis doesn't care which was used.

### MCP Capture Path

Run these steps in order. If any step errors, stop and report — do not continue with degraded data.

1. **Resize viewport** to 1440×900:
   ```
   mcp__playwright__browser_resize  width=1440  height=900
   ```

2. **Navigate** to URL (fresh context — `--isolated` flag ensures no cookies/login state leak):
   ```
   mcp__playwright__browser_navigate  url=<URL>
   ```

3. **Wait for hydration** (3 seconds):
   ```
   mcp__playwright__browser_wait_for  time=3
   ```
   If page still looks skeleton-like after 3s, wait another 3s. If still incomplete after 6s total, note it in output.

4. **Take screenshots**:

   4a. Viewport screenshot (1440×900, primary visual reference):
   ```
   mcp__playwright__browser_take_screenshot  type=jpeg  filename={domain}-viewport.jpeg
   ```

   4b. Full-page screenshot:
   ```
   mcp__playwright__browser_take_screenshot  type=jpeg  filename={domain}-fullpage.jpeg  fullPage=true
   ```

5. **Run DOM extractor** — inject `references/extract-dom.js` via evaluate:
   ```
   mcp__playwright__browser_evaluate  function=<contents of extract-dom.js>
   ```
   This returns the complete DOM data snapshot (colors, typography, spacing, radii, shadows, grid, cards, images, buttons, motion, navLinks).

6. **Motion/interaction capture** — hover over interactive elements to capture transition deltas:

   6a. Identify 1–2 nav links and 1–2 buttons from the DOM data.
   
   6b. For each target element:
   - Record computed `transition`, `transform`, `backgroundColor`, `color`, `boxShadow`, `opacity` BEFORE hover
   - Execute hover via `mcp__playwright__browser_click` or mouse move
   - Wait 400ms for transition to complete
   - Record the same properties AFTER hover
   - Note which properties changed and by how much
   - Move mouse away, wait 200ms to reset

7. **Error detection** — before proceeding, check:
   - If the page has a password field → stop: "URL resolves to a login page. Use the public marketing page."
   - If the screenshot shows a Cloudflare/bot verify page → stop: "Bot detection block. Try a different page on the same domain."
   - If the page body is mostly empty → warn: "Page may be incompletely rendered."

### Multi-page crawl (if crawl scope = "explore")

After primary capture:
1. From `navLinks` in the DOM data, filter out login/auth/checkout paths
2. Sort remaining links by path length (shorter = more likely to be a main section)
3. Pick 2 additional same-domain pages
4. Repeat the full capture (steps 1–6) for each
5. Merge data across pages:
   - Values appearing on **2+ pages** → tagged as `[system]` signal (higher confidence)
   - Values on **1 page only** → tagged as `[local]` (lower confidence, still captured)

### Comparative mode

If a second URL was provided:
1. Complete the entire capture phase for the primary URL first
2. Then repeat the entire capture phase independently for the second URL
3. Both datasets are passed to the analysis pipeline

---

## Phase 2 — Analysis Pipeline (4 Steps)

Run these steps **sequentially**. Each step reads only the prior step's output plus its reference file. Do not preload all steps at once — this keeps each step focused and prevents context contamination.

### Step 1 — Measure

**Read:** `references/step1-measure.md`
**Input:** DOM data + screenshots from Phase 1
**Output:** ~20 measurement categories, every value cited with exact px/hex/ratio. No adjectives, pure measurement.

### Step 2 — Pattern

**Read:** `references/step2-pattern.md`
**Input:** Step 1 output
**Output:** 5–8 systematic patterns, each with Pattern / Evidence / Design Goal. This is where repeated behaviors get named.

### Step 3 — Taste

**Read:** `references/step3-taste.md`
**Input:** Step 1 + Step 2 output
**Output:** 3–4 taste principles, each with Trigger / Decision / Reason / Evidence / Trade-off / Confidence. At least one must be a Restraint trade-off.

### Step 4 — Observer (Quality Gate)

**Read:** `references/step4-observer.md`
**Input:** Steps 1–3 output + original URL(s) + screenshots
**Output:** Final `{domain}.json` + `{domain}.md` + export format file (if not "skip") + comparative Delta section (if applicable).

This step validates the entire pipeline output, runs the anti-slop grep, checks evidence chains, and produces the final files.

---

## Phase 3 — Anti-Slop Enforcement

**Read:** `references/anti-slop-wordlist.md`

This is a mechanical check, not a mental scan. After Step 4 generates the output files:

1. Run a literal grep against `{domain}.md` for every banned term
2. If any hit is a **genuine positive descriptor** (not in a quoted foil), rewrite that passage
3. Replace the vague term with a specific measurement or trade-off
4. Re-run the grep
5. Repeat until 0 genuine-descriptor hits

Also validate:
- Both `Design Map` and `Taste DNA` sections are present in the `.md`
- `{domain}.json` parses as valid JSON
- All required schema fields are populated

---

## Phase 4 — Export

**Read:** `references/export-formats.md`

Generate the export file matching the user's selection from Phase 0, Step 3. The export draws from `{domain}.json` and includes:
1. Token block (exact values)
2. Taste directives (principles as imperatives)
3. Anti-patterns (restraints as "Never/Avoid" bullets)

Anti-slop rules apply to export files too.

---

## Known Limitations

- **Login pages**: Pages behind login return the login form, not the target page. Use the public marketing page.
- **Cloudflare/bot blocks**: Some sites show a verification page. Try a different page on the same domain, or provide a direct URL to a specific page.
- **SPA hydration**: Heavy SPAs (Figma, Notion) may still be hydrating after the 6s wait window. Flagged as a caveat, not silently ignored.
- **CSS custom properties**: Variable names are lost in computed style extraction — only resolved values are captured.
- **Viewport dependency**: All measurements are from a 1440×900 viewport. Mobile layouts are not captured (but mobile design systems usually share the same tokens).
- **Hover states**: Only 1–2 nav links and 1–2 buttons are hovered. Sites with complex hover menus or reveal-on-hover content may have interaction taste that's missed.
