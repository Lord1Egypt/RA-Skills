---
name: amazon-product-analysis
description: "Turn an Amazon product link into an evidence-based short-form video script — extract listing selling points, mine real buyer language from reviews, then produce a shot-by-shot script once the user picks a content direction (product-demo / narrative / direct-response). Trigger this skill when the user drops an amazon.com or amzn.to product link and mentions short video, UGC/ad video, social content, or asks 'what kind of video would work for this product' / 'write me a video script', even if they never say the word 'skill'. This version focuses on listing + review insight and does not scrape competing viral videos for teardown (see 'Known limitations' below), and does not generate the video itself (video synthesis is a future iteration — if asked to 'just produce the video' or 'analyze similar viral videos', explain the current scope instead of forcing it)."
---

# Amazon Product → Social Video Script

## Why it's designed this way

Before, picking a topic and writing copy for a UGC/ad video was mostly guesswork — a marketer would guess what might go viral based on gut feeling, then have AI generate copy directly from that guess. This skill exists to remove the guesswork: let the AI first lay out everything that's actually verifiable (what the product says about itself, what buyers say about it), and only bring a human in once, at the point where a real judgment call is needed — which brand tone / channel strategy to lean into. Information gathering and analysis is work the AI should own end-to-end; picking a direction is the value judgment that actually belongs to a human.

So the whole flow has two phases: **Steps 1-2 are information gathering — don't interrupt the user for confirmation partway through.** There are exactly two points in the whole flow where you stop and wait for a user reply — **Step 3 (pick a content direction)** and **the end of Step 4 (pick a video-generation path)**. Don't stop anywhere else. If you hit a minor snag before Step 3 (e.g. a review page loading slowly), work around it yourself instead of interrupting the user over it.

## Overall flow

### Step 0: Confirm the input

Check whether the link is a valid Amazon product page (`amazon.com/dp/...`, `amazon.com/gp/product/...`, or an `amzn.to` short link). If the user gave a search-results or category page instead of a specific product page, ask which product they mean first — everything downstream is built around a single product.

### Step 1: Pull the listing, extract selling points

Open the product link: if the current environment has gstack installed, prefer its `/browse` skill (a headless browser is more stable — Amazon's anti-bot detection is aggressive). Without gstack, fall back to whatever browser-automation tool you have available (a built-in browser tool, a headless-browser MCP, etc.). **Do not** hit the page with a bare `fetch`/`WebFetch` HTTP request — an unrendered request without JS execution is much more likely to trip Amazon's anti-bot detection and return a CAPTCHA page or get rate-limited.

Extract:
- Title
- The five bullet points, verbatim
- Price, star rating, number of ratings
- Category
- Key information from the A+ content / rich media description (if it loads)

Produce a **product selling-points summary** (keep it in context — no need to write it to a file yet).

**Price sanity check**: opening Amazon this way can sometimes get geolocated to a non-US shipping address (this has actually happened — auto-detected as India, price shown in INR). If the scraped price isn't in USD, flag it clearly in the summary as "price not verified against the US storefront" — don't treat it as the real price and let it leak into the script or brief downstream.

### Step 2: Pull reviews, mine authentic buyer language

**Only use the review module embedded in the product page itself — don't navigate to the separate "see all reviews" page** (URL shaped like `/product-reviews/ASIN`). The embedded review section on the product page typically already has 8-10 curated reviews (mix of positive and negative), plus Amazon's own "Customers say" AI summary (which lists positive/negative mention counts by dimension, including the negative percentage per dimension) — none of this requires login, and it's usually enough to work with. **The full reviews list page can hit an Amazon login wall depending on account/network conditions** — if that happens, never suggest the user log into their Amazon account, and never have the agent attempt to log in on the user's behalf (that's an account-security boundary this skill shouldn't touch). A smaller review sample is preferable to going anywhere near the login flow to get more. If the embedded reviews + AI summary genuinely have thin negative coverage, say so plainly in the output — "negative review sample is limited; the full reviews list requiring login was not accessed" — don't pretend the coverage was thorough when it wasn't.

Use the browser tool selected in Step 1 to open the product page and pull as much review text as you can, both positive and negative — complaints in negative reviews are often the most direct entry point (e.g. "thought it would fit my big dog but it was too small" flips directly into a "made for large breeds" hook in the video).

Don't just do word-frequency counting — that's not useful. Pull out **complete phrases you could drop straight into copy**: how buyers describe the experience, a before/after change, a pleasant surprise, or a disappointment, in their own words. Tag each one as either "validates a selling point" or "surfaces an unresolved pain point / common concern."

Watch for any review that is itself **a small story with a beginning, middle, and end** (e.g. "my kid nagged me about this for a week after seeing an influencer post it, I finally caved and bought it") — a review like that doesn't need a narrative framework bolted on; it's already the skeleton of a narrative-style script, and it's more authentic and easier to judge for audience resonance than a story invented from scratch. Flag these when you find them — in Step 3 you can offer the specific story itself as a standalone "narrative" option rather than a generic "we could also do narrative."

Produce a **list of high-signal review language**.

### Step 3: Summarize insight, ask the user to pick a direction

Roll up the Step 1-2 output into a short **content strategy brief**, then tell the user which viable video directions you're seeing (these usually fall into product-demo / narrative / direct-response, but the exact labels should match what you actually found — don't force it into those three buckets. For example, if Step 2 surfaced a review that's already a self-contained story, present that specific story as the narrative option instead of vaguely saying "narrative is possible"), and ask them to pick one.

This is one of the two points in the whole flow where you stop and wait for a reply — everything before this that you could figure out on your own, figure out on your own; don't repeatedly ask "should I keep going?" or "does this look right?" along the way.

### Step 4: Produce the script for the chosen direction

Generate a shot-by-shot script. Recommended format per shot:
- Timestamp / shot number
- Visual description
- Voiceover / caption copy
- What this line is based on (which Step 1 selling point / which Step 2 buyer quote it maps to) — **every line needs to trace back to a specific piece of evidence from an earlier step, never invented from nothing.** This is this skill's core value over just asking a model to "write me a UGC video script."

**Keep each shot in the 5-10 second range** — don't cut shots by feel. This isn't an aesthetic preference, it's a production constraint: mainstream image-to-video models (e.g. Seedance) generate clips in roughly 5-10 second increments. A shot shorter than 5 seconds doesn't map cleanly onto a generation call later (either you waste generation capacity, or it gets forced to merge with an adjacent shot, breaking the intended cut). A shot longer than 10 seconds usually can't be generated at all and has to be split later anyway — meaning the shot design work gets redone for nothing. Design shots against this production ceiling up front rather than reworking it at generation time.

If the user needs multiple markets/languages, ask which language version to produce at this step and adjust pain points and wording accordingly — buyers in different markets often care about different things; don't just translate one script and call it done (there's no dedicated multi-market review analysis yet — for now this relies on manually reminding the model to localize).

Once the script is done, **ask the user how they want to generate the video next**: shot-by-shot generation (each shot generated as its own 5-10s clip, then stitched together), or converting key shots into keyframe images first to lock the visual style before doing image-to-video (higher consistency, one extra confirmation round). This only hands the "what's next" choice to the user — this skill does not do video generation itself. **Don't call any video-generation API here** — once you've asked, this round of the task is done; the user takes that answer to whatever host platform they use (e.g. Seedance inside Doubao) to actually generate it.

## Output

Recommend creating a working folder per product (named after a short English product name or the ASIN), containing:
- `insights.md` — the Step 1-3 rollup (selling-points summary + review-language list + content strategy brief)
- `script.md` — the final Step 4 script

## Dependencies

- **A browser-automation tool (required, either one)**:
  - If gstack is available: prefer its `/browse` skill. If a `$B` command fails with `Executable not found in $PATH: "bun"`, run `export PATH="$HOME/.bun/bin:$PATH"` and retry — bun lives in `~/.bun/bin`, which isn't always on the current shell's PATH.
  - Without gstack: use whatever browser-automation tool your agent environment provides (a built-in browser tool, a headless-browser MCP, etc.) — anything that can execute JS and read text/screenshots works. Avoid a bare, non-rendering HTTP request against Amazon.

## Out of scope for this version (future iteration)

- **Video generation itself**: this version only produces the script. If asked to "just produce the finished video," explain the current scope rather than improvising a video-generation path. The near-term direction has already been decided (weighed three options — a hosted service, a self-built gateway, or bring-your-own-key — and picked the lowest-engineering one): **once the script is done, video generation is left to whatever generation capability the host platform already has** (e.g. its built-in Seedance model). This skill doesn't call any video-generation API. If cross-platform reuse or cost/quota control becomes necessary later, a self-built gateway (reusing the "key stays server-side, thin client calls it" pattern from other projects) is worth considering then — no need to over-engineer this up front.
- **Systematic multi-language/multi-market analysis**: currently Step 4 only reminds the model to manually account for localization; there's no dedicated per-country review scraping and pain-point analysis yet.
- **Searching/tearing down viral social videos**: an earlier version of this skill added a step to search TikTok/YouTube Shorts for viral videos in the same category and analyze their opening hooks and narrative structure. In practice, outside of Douyin (untested in this skill), every other platform only exposes page-level metadata (title, description, view count) — no way to actually see the footage or understand the audio, so analysis depth was shallow and the cost wasn't cheap either (TikTok search is also blocked outright for headless browsers). So this step is skipped for now, in favor of the more solid and more reliably accessible "listing + reviews" sources. Before reviving this step, read "Known limitations" below — that's the direct reason it was skipped, and it needs solving first.

## Capabilities worth adding (easier to solve than the video problem, just not done yet)

- **Product images aren't downloaded/analyzed yet**: Step 1 currently only pulls text (`$B text`/`$B data`). The listing's image gallery — lifestyle shots, size-comparison images, selling-point infographics (a lot of key selling points are baked into images, so text-only scraping misses them) — is untouched. This is different from the video problem: images can be pulled with `$B media --images` or `scrape images`, downloaded, and read directly with the Read tool (when Claude is in the loop, just read the image directly — no need to route through OCR/a vision model). It's genuinely readable content, and much cheaper than video. Worth adding into Step 1 once prioritized.

- **Reference-image source for video generation**: not a Step 1 requirement (Step 1 uses the real listing images directly when it needs to look at something — there's no "user upload" option there). This matters for a future iteration that adds image-to-video synthesis — what image should be used to keep the product's on-screen appearance consistent with the real product? Two sources: ① the real listing images pulled from the product link, ② images the user uploads themselves. This has to be a user choice, not a default, because a purely AI-generated appearance can diverge from the real product (a genuine negative review mined in Step 2 — "Green is much much darker and less vibrant than the product images" — is a live example of exactly this failure mode: a mismatch between video and real product just manufactures the next version of that same complaint). When video generation is added, ask the user to pick a source at that step — don't fold it into the current Step 0-4 flow as a second pause point; Step 3 is deliberately the only pause point in the current design, and adding another would break that constraint.

## Known limitations (recorded for later, not something to solve right now)

- **Amazon's embedded listing video is metadata-only, no content access**: it streams from a `blob:` URL, so `/browse` can't retrieve the actual video file, and there's no caption/transcript track. Only title, cover image, duration, and accompanying text are accessible — no way to see the footage or understand the audio.
- **YouTube Shorts is similarly metadata-only**: title, description, view/like/comment counts, tags, publish date, and creator are all readable, but there's no way to download the video file or transcribe the actual footage/audio.
- **TikTok's search page blocks headless browsers outright** — currently completely inaccessible, not even metadata comes through.
- **Douyin is theoretically the only platform with "download-level" access** (via a `douyin-video`-style skill, which can pull the watermark-free video file plus caption and engagement data) — but this hasn't actually been tested inside this skill; it's an untested assumption about reusing an existing capability, not a verified one.
- Reviving the "viral video analysis" step with real content understanding (footage + audio transcription) would require adding download plus vision/speech-transcription capability — `/browse` alone can't get there.
