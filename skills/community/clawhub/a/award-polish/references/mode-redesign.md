# Mode 2: Redesigning an existing website

This file is guidance for the redesign mode inside this skill. It does not replace what the user asked for. When the user and this file disagree, follow the user.

Goal: raise the experience to award level without breaking what exists. Inside this mode, keep existing features, links, and data unless the user asks to change them.

## Step 1: understand the current state (no rebuild, no feature re-inventory)

- Pull the latest code, read the code and any existing log.
- Open the live URL and take one screenshot at 375px and one at desktop width.
- **Check live speed first**: `curl -sI <url>` for cache-control and CDN hit headers (x-vercel-cache, cf-cache-status), `curl -o /dev/null -s -w '%{time_starttransfer}' <url>` for time to first byte, three times each on the home and core pages. If nothing is cached and TTFB is over 0.8 s, that is fatal: find the cause (on one content site the 404 page read request headers, turning 215 prerendered pages into per-request rendering at 1.4 s TTFB), fix it separately, ship it separately on the user's go-ahead, then start polishing.
- Write a current-state audit in the log (borrowing the taste skill's redesign protocol):
  - Brand: primary and accent colors, fonts, radius, logo use.
  - Information architecture: page tree, main navigation, main conversion paths.
  - Keep: signature interactions, a recognizable first screen, the copy voice.
  - Remove: AI clichés, broken layouts, dead links, cheap stock photos, anything that slows it down.
  - Current readings of the three dials (with design-taste-frontend installed): the redesign starts from these.
  - Search baseline: ranking pages, each page's title, description, canonical, hreflang, structured data types, H1, share card. Run `scripts/seo_keep.py --base <live> --new <live> --pages <pages…> --files /robots.txt /sitemap.xml` against the live site itself first (expect 0 differences) to confirm the script works and the page list is right; write the page list in the log, and before every release run live against local.
- Then write three lists in the log:
  - **Must keep**: domain, routes, product name, logo (unless a new logo is part of the request), existing features, core flow, constraints the user set.
  - **Can change**: visuals, layout, motion, copy voice, images, interaction details.
  - **Already broken**: fix first.
- Decide the depth:
  - "Polish", "improve": keep the current style and raise it.
  - "Redesign", "new visuals", "start over": new visuals, keeping features, routes and content.
  When unsure, keep the style and raise it, and say so in the log.
- The feature list only guards against **breaking things during the redesign**. When features are done, this skill does not add big ones unless the user asks.
- **Two kickoff records for this redesign** (part of the kickoff record, including when a review or the reference study has not happened yet):
  - Anchor set screenshots: the current home and core pages, one image per screen (`layout_check.py --slices 8`), one set at 1440 and one at 375, in `refs/anchor/`. The scores can wait for the first review; the screenshots cannot, because once code changes they cannot be retaken.
  - "What each score looks like": for all ten items, what 6, 7, 8 and 9 look like, written about this product's own things (pages, buttons, data). Before the reference study, write from the product; add reference examples afterwards.
- **Write the state and to-do so work can start directly**: save the search baseline with `seo_keep.py --base <site> --new <site> --pages <pages…> --dump refs/seo-baseline.json` (a relative path inside the repo or the working directory; absolute paths and `..` are refused), copy each page's title and description verbatim into the log with canonical and structured data types (just writing "present" does not count), and state that these fields may not shrink in the redesign; to-dos come in three levels, fatal, experience, polish, each with location, problem and fix.

## Step 2: study award sites, find the gaps

- Pick references following `reference-study.md`.
- When the depth is "redesign, new visuals", also make 2-3 first-screen direction mockups first; a small review narrows them and work starts after the user picks (see `mode-new.md` step 2). For plain polish, keep the current direction without candidates.
- Put our home and core pages next to theirs, write "where we fall short" for each of the 10 items, and sort the gaps into a to-do list, biggest first.
- Pick 4-6 signature moments from the core flow and add them to the list.
- Settle (or keep) the spacing scale, accent color, radius and fonts, write them in the log, and unify the whole site on them.

## Where to start a redesign (for polish depth, in this order, stop when enough)

1. Type: lowest risk, biggest gain.
2. Whitespace and rhythm: open up section spacing and even out the vertical rhythm.
3. Color: lower saturation, unify neutrals, keep the brand accent.
4. Motion: add fitting micro-interactions to existing components.
5. Restructure the first screen and key sections.
6. Replace whole blocks: only when the existing block cannot be saved.

## Two written checks for redesigns (before every release; any failure blocks it)

- **Preservation check**: list every changed URL, main navigation label, form field name and anchor. Inside this redesign it stays empty unless the user approved a change. Run search fields with `seo_keep.py --base <live> --new <local production build>`; release only at 0 differences. H1 text counts as a search field: the redesign changes how it is set, not the words. A reviewer suggestion to reword the H1, title, or description waits for the user.
- **Brand check**: the existing brand accent, fonts and logo use are all still there (unless the user approved a change).

## Step 3: enter the iteration loop

Go straight into the shared iteration loop in SKILL.md, fixing the latest full issue list in one go each batch.

Redesign specifics:

- **When to ship**: `release.md`. With real users on the site, use its "staged updates", and every batch must be fully working.
- **Pull the main branch before every batch**: the user or other tools commit there too (halfway through one polish, the user merged a change on main that duplicated the polish branch). Merge new commits into the polish branch first. Inside this skill, when both sides changed the same thing, keep main's copy. If the user wants the other copy, follow the user. Afterwards the preservation check uses the new live site as its base.
- **When the user adds directions one after another, merge them**: the later one usually adds to the earlier one. When unsure, write a merged full version in the log and follow it.

## When the site already has real users

- **Keep user data compatible**: localStorage keys and shapes, account state, favorites and history must survive the redesign without loss or errors. If the shape changes, write a migration and test it with real old data.
- **Keep search ranking**: inside this redesign, routes stay. Compare every page's title, description, structured data, sitemap, and canonical before and after. Those fields do not shrink unless the user approves it.
- **Preview before going live**: verify on the host's preview deploy (Cloudflare or Vercel preview URLs) in the live environment, then switch; click through the core flow right after. If it breaks, follow `release.md`, which asks the user before rolling back to the previous deploy.
- **CDN caching**: CDNs keep serving old pages and old CSS; after release confirm with `wait_live.py` per `release.md`, purging caches if needed.
- **Follow the project's own quality gates inside this redesign**: review scores, file fingerprints, and audit records in a content pipeline block edits to reviewed sources. Inside this skill, a display-only change (a cover image, an internal link, or button text) and a change to body text both go through that same review. The other route is an explicit yes from the user for that one change, recorded in the log with the change and the approval.
- **Pages behind a login**: reviewer subagents cannot pass a login wall. Inside this skill, look for a demo mode or a test account first. If there is none, ask the user how to proceed and wait. This skill does not sign in with the user's real account.
