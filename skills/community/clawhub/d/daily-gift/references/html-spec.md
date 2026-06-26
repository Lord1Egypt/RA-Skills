# H5 Gift HTML Spec

This file defines the output contract for generated H5 gifts.

The goal is smooth delivery across OpenClaw contexts:

- best case when hosted preview is configured: send a hosted URL that opens directly in-channel, such as a Telegram Web App button
- strong local fallback: immediate Canvas presentation
- universal fallback: send a single HTML file through a file-capable channel

## Core Output Rule

Every final H5 gift should be generated as a single HTML file.

That means:

- one `.html` file
- no required external asset folder
- no dependency on a local dev server
- no dependency on private infrastructure

It does **not** mean every byte must be inlined.

For final gifts, use this external-resource policy:

- JavaScript libraries: CDN allowed
- Fonts: CDN allowed
- Images and custom visual assets: must be inline

## External Resource Policy

### JavaScript Libraries

CDN use is allowed for stable public libraries such as:

- p5.js
- Three.js
- GSAP

Rules:

- pin exact versions, never use `@latest`
- prefer stable public CDNs such as `jsdelivr`, `cdnjs`, or `unpkg`
- add integrity hashes when practical
- only include libraries the gift actually needs

### Fonts

CDN-hosted fonts are allowed.

Good sources:

- Google Fonts
- stable public font CDNs

Rules:

- prefer a small number of font requests
- do not depend on obscure or fragile font hosts

### Images And Custom Assets

These must be embedded inline.

Use:

- base64 `data:` URIs
- inline SVG where appropriate

Rich H5 gifts may use multiple composited sprites or transparent PNG layers, but those custom assets must still be embedded inline in the final HTML.

Do not rely on:

- external image URLs
- temporary object storage links
- third-party image hosts

## Required

- single-file HTML output
- all essential images embedded inline, ideally as `data:` URIs
- include `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- work as a standalone file when opened directly
- keep the result mobile-friendly even if Canvas is later used for desktop display
- if using CDN libraries or fonts, lock versions and use stable public sources
- provide a lightweight loading state when CDN resources may take a moment to resolve
- before delivery, open the generated HTML in a browser testing environment using `profile="openclaw"` and verify that the page renders, the core interaction works, important content is reachable, bottom-fixed UI remains accessible, and text is readable
- if browser self-test cannot complete even with `profile="openclaw"`, do one manual source review for obvious layout or interaction problems and include an explicit warning in delivery that browser self-test was skipped

## Strongly Recommended

- keep the final file reasonably small, ideally under `200KB` before CDN-loaded libraries and fonts
- prefer CSS animation over heavy JavaScript animation when the effect allows it
- keep the number of moving parts low
- include one clear focal point on first render
- make the first interaction immediately understandable
- when a gift can be done well without CDN libraries, prefer the simpler path

## Visual Quality Floor

The templates under `{baseDir}/assets/templates/` represent the minimum visual quality bar, not the ceiling.

That means the final gift should usually show:

- deliberate composition rather than default centered blocks
- typography chosen for the mood, not whatever default font loads first
- text containers, borders, textures, shadows, or surfaces that help the words feel placed rather than pasted
- enough atmosphere to feel complete when the concept calls for it, such as star fields, light particles, rain, glow, grain, depth layers, or other scene-setting details
- motion that feels intentional and tuned, not abrupt or obviously placeholder

Use richer visual tools when they materially improve the craft:

- `three.js`
- `p5.js`
- `GSAP`
- other stable visual libraries with pinned versions

Do not add libraries for decoration alone. Use them when they help the gift reach a level of polish, immersion, or object-feeling that simpler code would miss.

The gift should not feel:

- rushed
- flat
- like a quick demo
- like generic component layout with emotional copy dropped into it
- obviously less polished than the nearest relevant template

Whenever the user's prior interaction suggests a clear visual preference, bias the palette, typography, density, and atmosphere toward that preference.

## Motion And Physical Feeling

When the gift concept implies a physical object such as a box, drawer, card, envelope, cabinet, shelf, or folded note:

- the object should visibly open, close, pull, slide, flip, lift, or otherwise behave like the thing it claims to be
- transitions should use spring-like easing rather than flat linear motion
- elements should feel like they have weight, friction, resistance, or momentum
- prefer CSS spring-style motion, tuned keyframes, or `GSAP` for object motion over simple opacity fades

A box that does not open is not a box.

A drawer that does not pull is not a drawer.

If the metaphor implies physics, deliver physics.

## Delivery Strategy

Preferred display order:

1. Generate the final single HTML file.
2. Save it under the gifts output folder.
3. Run the mandatory browser-based functional self-test on that HTML file using `profile="openclaw"`.
4. If browser self-test cannot complete, do one manual HTML review for obvious issues and prepare an explicit delivery warning that browser self-test was skipped.
5. Run `{baseDir}/scripts/deliver-gift.sh <html-file> workspace/daily-gift/setup-state.json` to resolve the delivery path from setup state.
6. If the script returns `delivery_mode = hosted_url`, send that URL first.
7. When the active channel supports it, wrap the hosted URL in the lightest open affordance available, such as a Telegram Web App button or equivalent in-app web container.
8. If the script returns `delivery_mode = local_file` and OpenClaw Canvas is available and enabled, present the file there for the smoothest local interactive experience.
9. If the script returns `delivery_mode = local_file` and Canvas is unavailable, send the HTML file itself when the channel supports file delivery.

Do not assume Canvas exists in every runtime context, and do not assume public hosting is always configured.

## Optional Hosting Guidance

Hosted preview should improve delivery friction, not become a hard dependency.

Recommended default:

- `surge`

Why `surge` is the simplest default:

- email-based setup
- no credit card requirement
- one-time login with locally stored credentials
- one-command deploy flow that works well for single-page gifts

Suggested deployment shape:

- copy the generated HTML into a temporary directory as `index.html`
- deploy that directory
- return the resulting HTTPS URL

Implementation note:

- keep the skill's runtime contract provider-agnostic even if `surge` is the default recommendation
- use `scripts/deliver-gift.sh` as the runtime entry point that reads setup-state hosting config before calling `scripts/deploy.sh`
- if deployment fails, fall back to Canvas or direct HTML file delivery

## Output Path Convention

Recommended output location:

- `workspace/gifts/YYYY-MM-DD-<slug>.html`

If multiple gifts are generated in one day, append a short suffix.

## Cleanup Strategy

- keep generated HTML gift files for the most recent `30` days by default
- older HTML files may be deleted to keep the workspace light
- deleting old HTML files should not delete gift-history records or other metadata

## Forbidden

- no external image URLs for critical rendering
- no `@latest` for CDN libraries
- no unauthenticated runtime dependency on private or fragile resources
- no required resources that need login or API auth just to render the gift
- no required API calls or fetches during page load
- no localStorage requirement for normal viewing
- no assumption that a separate server is running

## Important Nuance

Authoring templates may use development-time helpers or external references while being designed.

The final delivered gift should still be robust as a single HTML artifact:

- CDN libraries and fonts are acceptable when pinned and stable
- images and custom assets must still be embedded inline
