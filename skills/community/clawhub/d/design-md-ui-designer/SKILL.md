---
name: design-md-ui-designer
description: Use when designing or improving web, app, extension, community, course, video-ideation, marketing landing, SEO content hub, or public policy-page UI with a DESIGN.md-backed design system, high-end media assets, responsive screenshots, accessibility checks, trust-building conversion copy, and high-quality AI-generated raster imagery when useful. Trigger when the user mentions DESIGN.md, design.md, designdotmd.directory, UI design skill, landing page, conversion page, Pages UI polish, community media, video ideation assets, design tokens, visual redesign, or gpt-image-2-2026-04-21 as designer.
---

# DESIGN.md UI Designer

Use this skill to turn a UI task into a durable design system plus verified
screens. It is especially useful for CWS public pages, extension UIs, landing
pages, dashboards, apps, communities, courses, video ideation boards, and
product pages where visual quality and repeatable iteration matter.

For any new product, extension, app, skill, course, template, or community that
needs a public surface, design the Cloudflare Pages landing system as part of
the product, not as an afterthought. The public surface must include a high-end
landing page plus privacy, support, reviewer or verification, and source or
transparency pages when applicable. Do not ship several products with the same
thumbnail, hero, screenshot framing, icon motif, or visual signature.

## Core Workflow

1. Read the current UI first: source files, live URL when relevant, screenshots,
   brand/product context, and existing assets.
2. Create or update a repo-local `DESIGN.md` before broad visual edits when the
   product does not already have one.
3. Keep `DESIGN.md` compact and agent-usable: YAML tokens for exact values,
   markdown rationale for how to apply them.
4. Implement UI changes using the design tokens and existing framework patterns.
5. Verify with real rendered screenshots at mobile, tablet, and desktop widths.
6. Run accessibility and layout checks: image loading, focus states, contrast,
   no horizontal overflow, no text clipping, no incoherent overlap.
7. For public/reviewer pages, verify claims are true, links work, and the first
   viewport clearly signals the product.
8. Verify Cloudflare Pages SEO and deployment readiness: canonical HTTPS Pages
   URLs, title and meta description, social preview image, sitemap,
   robots.txt, security headers, and `SoftwareApplication` JSON-LD for apps and
   extensions.
9. For marketing landings, run the conversion landing workflow before visual
   polish: first traffic source, one reader, trust reason, share moment, offer,
   proof receipts, SEO article cluster, and honest monetization boundary.
10. Run the critic score gate. Do not ship low-trust public pages, CWS media, or
   extension UI that fails the score threshold.

## DESIGN.md Contract

Prefer this structure:

```markdown
---
version: "alpha"
name: Product Design System
description: One sentence about the product surface.
colors:
  primary: "#111827"
  accent: "#1D4ED8"
typography:
  h1:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 780
    lineHeight: 1.04
    letterSpacing: 0
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 8px
  md: 16px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
---

## Overview
## Colors
## Typography
## Layout
## Elevation
## Shapes
## Components
## Do's and Don'ts
```

Rules:

- Tokens are normative; prose explains intent and usage.
- Keep font sizes stable across viewports; do not scale text with viewport width.
- Use 0 letter spacing unless the product has an explicit typography reason.
- Use cards only for repeated items, modals, and framed tools.
- Avoid nested cards, decorative blobs, generic gradients, and purely
  atmospheric assets.
- Use product-relevant images or real screenshots where users need to inspect
  the product.
- For CWS listing screenshots, use actual extension UI with sanitized fixture
  data, never generated product mocks.
- Each product must have a distinct design identity: icon motif, hero art,
  screenshot framing, promo layout, palette role, and visual signature.

## Cloudflare Pages Product Landing Contract

For every public product surface, create or maintain:

- homepage landing page with a first-viewport product signal, concrete workflow
  evidence, real screenshots or rendered app state, clear free MVP or install
  path, and no exaggerated outcome claims;
- privacy page that matches implementation and permissions exactly;
- support page with product-specific issue paths and contact/diagnostic detail;
- reviewer, verification, or test page with reproducible smoke-test steps when
  the product is reviewable, installable, or submitted to a marketplace;
- source, transparency, or release page when a source archive, policy packet, or
  reviewer artifact is part of the trust story;
- SEO baseline: title, description, canonical, social preview card,
  sitemap, robots, security headers, and structured data where relevant.

Use Cloudflare Pages URLs as canonical public URLs for marketplace submissions.
Do not leave GitHub Pages, localhost, preview URLs, or stale dashboard URLs as
canonical after a Cloudflare Pages deployment exists.

High-end landing pages must feel like a specific product solving a specific
problem. Avoid SaaS-template filler, generic AI-gradient heroes, duplicated
thumbnail systems, fake UI mockups, and vague "boost productivity" copy. The
first viewport should show either the product itself, the artifact it creates,
or the real workflow state users came for.

## Marketing Landing Conversion Workflow

Use this workflow for paid or monetizable product landings, Chrome extension
public pages, skill-pack pages, launch pages, and SEO hubs. Load
`references/marketing-landing.md` when the task involves offer positioning,
trust building, article thumbnails, pricing, or a conversion critique.

Before designing the page, write a compact launch brief:

- first traffic source: exact post, search query, marketplace listing,
  newsletter, community, partner, or profile that will send qualified visitors;
- one reader: the concrete operator who arrives and what painful moment made
  them search, click, or share;
- share moment: the exact page artifact, result, article, checklist, or
  before/after insight the visitor would send to someone else;
- trust reason: why a skeptical buyer should believe the claim now, using real
  screenshots, dataset scope, source archive, reviewer guide, named public
  evidence, or transparent boundaries;
- free MVP path and paid path: what is free today, what may be monetized, how
  updates are delivered, and what is deliberately not promised.

The page structure should be evidence-first, not template-first:

- hero: literal product or offer name, one specific use case, visible product
  state or artifact, one CTA, and no unverifiable outcome promise;
- proof strip: permissions, privacy, source/date, dataset size, version,
  reviewer path, or benchmark facts instead of vague badges;
- included/workflow section: what the buyer receives or can do, with stable
  update policy and deliverable boundaries;
- persona/use-case section: 3-4 concrete readers and the situation where the
  product is worth sharing;
- trust receipts: real artifacts, public screenshots, source links, test gates,
  reviewer instructions, or release notes. Do not invent testimonials, logos,
  revenue numbers, review speed, or buyer identities;
- content hub: 3-9 SEO articles or playbooks when education is needed. Give
  each article a video-style thumbnail, search-intent title, internal links,
  and a concrete operator task;
- pricing/FAQ/final CTA: answer refund, delivery, compatibility, updates,
  privacy, affiliation, and support questions without hiding risk.

Third-party brand usage must stay honest. Blog/editorial thumbnails may use a
third-party product/community name as a topic cue when the article is actually
about that ecosystem and the user has asked for it. Do not use official logos,
brand marks, or endorsement-like placement in landing heroes, CWS assets,
product proof, or marketplace media unless rights are explicit. Keep a visible
non-affiliation boundary on relevant pages.

## Image Generation

When generated raster imagery is needed, use the `imagegen` skill/tool. The
required designer preference is `gpt-image-2-2026-04-21` when the host exposes
model selection. If model selection is not exposed, use the available image tool
and record that limitation.

For UI/UX redesigns, run a holistic screen-look exploration before committing to
large visual edits:

1. Capture the current UI exactly as users see it in the browser at desktop and
   mobile widths. Include the full first viewport and the primary working
   surface; for extensions, capture popup, options, store, and support pages
   when relevant.
2. Summarize the visible product truth from those screenshots: what the user can
   do, what evidence is visible, what feels crowded or generic, and where trust
   is lost.
3. Feed the screenshot context and summary into `gpt-image-2-2026-04-21` for
   full-screen design look candidates when model selection is available. Ask for
   complete viewport compositions, not isolated components or decorative hero
   art.
4. Generate or describe 2-3 candidate directions, then choose the strongest one
   against the critic score gate before editing code.
5. Build from the selected candidate using repo-native components, real product
   screenshots/assets, and `DESIGN.md` tokens. Treat generated UI looks as
   direction, not factual product evidence.
6. Re-capture the same viewports after implementation and compare against the
   original screen: hierarchy, density, interaction clarity, overflow, and trust.

Use a concrete art direction before generation:

- product truth: what real product state or workflow the image supports
- composition: target size, focal object, negative space, crop safety, thumbnail
  legibility, and where text will sit if text is overlaid in HTML/CSS
- visual identity: palette, material, lighting, icon/object language, and how it
  follows `DESIGN.md`
- exclusions: no generic blobs, fake UI screenshots, unreadable pseudo-text,
  unrelated metaphors, or atmospheric stock-style filler

Use generated imagery for:

- landing-page hero art
- promo tiles
- empty-state art
- design exploration
- background product context
- distinct marketplace thumbnails when they are not used as product evidence

Do not use generated imagery as fake product UI evidence, policy proof, or CWS
screenshots.

For CWS promo tiles and public review pages, prefer generated bitmap art only
when it improves trust and still points back to the real product. Pair promo art
with real screenshots where reviewers need to inspect functionality.

## Community And Video Media Workflow

Use this stricter workflow for Skool/community covers, course thumbnails, post
cards, proof cards, short-form video concepts, Manim scenes, and video
ideation boards. These assets are public traffic surfaces, not decorative
extras.

1. Name the first traffic source before designing: exact community, profile,
   search query, post format, or partner loop where the first qualified viewers
   will come from.
2. Name the share moment: the exact point where the viewer would send the asset
   to a friend, tag someone, save it, or repost it.
3. Build the asset around real product truth: the real community activity,
   template, proof artifact, lesson, app state, or creator-owned example.
4. Draft at least 7 video or media candidates before selecting one. Each
   candidate needs hook, audience, proof artifact, incentive, CTA, privacy
   boundary, share trigger, and kill/iterate decision.
5. Use generated imagery only when it adds a concrete, ownable visual system.
   Do not use generic AI gradients, fake dashboards, stock course covers,
   unreadable pseudo-text, or reused sibling-product thumbnails.
6. For Manim or motion assets, validate aspect ratio, duration, fps, thumbnail,
   first-frame clarity, captions/metadata, and source ownership before treating
   the file as publishable.
7. Mark weak drafts as `prototype_only` or `rework`; do not present them as
   launch-ready media.

High-end community/video media must score at least `90/100` overall and no
category can be below `9/10`:

- traffic fit
- share trigger
- product truth
- visual distinction
- thumbnail and crop readability
- motion or composition quality
- privacy and rights safety
- incentive clarity
- conversion path quality

Block finalization when the score is below threshold. A working render, prompt,
or thumbnail is not enough. Iterate or kill the candidate.

For marketing landings and SEO hubs, also score the launch brief and content
system. Block finalization if the combined landing score is below `90/100` or
if traffic source, share moment, proof integrity, pricing boundary, or article
cluster quality scores below `9/10`.

## Critic Score Gate

Score every changed public page, extension popup, CWS screenshot, promo tile,
hero, and media asset before final delivery. Use a 0-10 score for each category
and record the scores in the task summary or repo log for release work.

Block finalization if any category is below `8/10`:

- product clarity: the first viewport or asset immediately tells what the
  product is and what the user can do
- visual trust: typography, spacing, palette, imagery, and hierarchy feel
  intentional and credible rather than default, low-effort, or generic
- evidence integrity: screenshots show real UI with sanitized data; generated
  images are not misrepresented as product evidence
- responsive polish: mobile, tablet, and desktop have no clipping, overlap,
  awkward crop, tiny unreadable text, or horizontal overflow
- accessibility: contrast, focus states, readable type sizes, controls, and
  tappable targets meet practical review expectations
- claim alignment: visible text and media only describe shipped, reproducible
  behavior
- conversion path quality: first action is specific, honest, free or reviewable
  when the MVP is rough, and tied to the product's share or proof moment
- uniqueness: the visual system is materially distinct from sibling products
  and current marketplace competitors

When the score is below threshold, iterate visually before shipping. Improve the
design system, regenerate or replace weak assets, refine layout density, and run
screenshots again. Do not excuse weak visuals as "only policy pages"; CWS
reviewer pages and store assets must build product trust.

## Verification Gate

Before finalizing UI work, capture or inspect rendered screenshots for:

- 320px or 360px mobile
- 390px mobile
- 768px tablet
- 1280px or wider desktop

Check:

- no broken images
- no horizontal overflow
- no text clipped inside buttons/cards/nav
- keyboard focus is visible
- tap targets are comfortable
- first viewport has the required brand/product signal
- claims match real product behavior
- critic score gate is recorded and all categories are at least `8/10`
- all Cloudflare Pages canonical URLs, policy URLs, support URLs, and reviewer
  URLs resolve to the correct product
- public pages pass SEO and security-header checks when the repo provides them
- product thumbnails, promo images, and hero assets are unique across sibling
  products

For Chrome extensions, combine this skill with `chrome-extension-cws-shipper`.
For submitted or pending-review marketplace items, do not alter the submitted
package or CWS dashboard draft just to improve design; prepare the improved
Cloudflare Pages surface and carry design changes into the next submitted
version unless the marketplace reports a blocker.

## Source Notes

Use `references/source-notes.md` for the source-derived principles behind this
workflow and links to the design.md, DESIGN.md directory, and Codex use-case
references.
