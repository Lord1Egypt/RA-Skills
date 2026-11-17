---
name: abonten-lead-skill
description: "Turn photos of offline posters, signboards, flyers, and billboards into a traceable business-lead pipeline: extract visible details, research public business contacts and decision-makers with a bounded TreeBased search, and prepare a Notion dashboard and outreach. Use when the user provides physical-advertising images or asks for ALS/offline lead generation. Do not use for private-person discovery, data-broker enrichment, or unsolicited outreach."
---

# Abonten Lead Skill (ALS)

ALS turns imperfect street-level photos into useful, evidence-backed business leads. It separates what is visible from what is researched, keeps provenance for every important fact, and leaves external communication under the user's control.

## Operating contract

- Treat every image as evidence. Do not invent, silently autocorrect, or complete unreadable names, digits, URLs, or handles.
- Keep the raw transcription and the normalized value side by side. Record the source image and, when useful, the crop or region where the value appeared.
- Use public business information and public professional contact paths only. Do not use people-finder sites, leaked datasets, private accounts, or personal home addresses.
- Label facts, verified findings, and hypotheses separately. An apparent lack of online presence is a research observation, not proof that a company needs the user's service.
- Preserve existing Notion data. Never delete or overwrite manual notes merely to make records uniform.
- Creating or updating a Notion dashboard is an external write and requires a clear target. Sending email or messages requires an explicit send instruction plus a final recipient/message preview.

## Choose the mode

Use the smallest mode that satisfies the request:

1. **Intake** — inspect images and extract/deduplicate businesses.
2. **Research** — enrich selected leads with public web evidence and decision-maker or professional contact paths.
3. **Dashboard** — create or update a Notion database, or produce an importable fallback.
4. **Outreach** — draft calls/emails, or send an explicitly approved batch.

If the user supplies images without a mode, perform Intake and prepare a Research/Dashboard queue. Ask for the user's offer before ranking fit or drafting personalized outreach. Do not send anything by default.

## Workflow

### 1. Intake the images

- Enumerate every supplied image or local file and inspect it at its available resolution.
- Do not reject a photo because the sign is cropped, angled, blurry, or partly out of frame. Inspect likely text regions separately and keep a lead when enough evidence remains.
- Use vision/OCR and targeted crops. Re-read uncertain text at least once; if it is still uncertain, retain the ambiguity (for example, 8/B, not a guess).
- If one image contains several businesses, create separate candidate leads and link them to the same source image.

Extract, when visible:

- business or brand name;
- raw text and offer/product/service;
- phone, WhatsApp, email, website, QR-code destination, or social handle;
- address, neighborhood, landmarks, city, and country;
- call to action, dates, opening hours, and any other useful context.

For each value, store source_image, source_region when available, raw_value, normalized_value, and confidence (high, medium, or low). Keep an unresolved_questions note for anything that needs research or user confirmation.

### 2. Normalize and deduplicate

- Use business name plus location, phone, website, or social handle to form an identity match.
- Keep alternate spellings, aliases, and every supporting image; do not discard evidence just because two captures look similar.
- Normalize phone numbers only when the country or market is known. Preserve the exact printed number and never guess a missing country code.
- Mark a record possible_duplicate when identity is plausible but not proven. Merge only when the evidence supports the merge.

### 3. Research with TreeBased search

When research is requested, read [references/treebased-search.md](references/treebased-search.md) before searching. Start with the strongest seed in the image (exact name, phone, domain, handle, or location), then branch outward to corroborate identity, official footprint, public professional roles, social accounts, and business need signals.

Use the environment's approved research/search routing. Cite each material finding with its source URL and access date. Prefer official business pages, verified company profiles, reputable directories, professional profiles, registries, and credible news or job pages. Never present a guessed email pattern, an unverified phone number, or an assumed CEO as a fact.

For each lead, return:

- identity status: confirmed, probable, or unresolved;
- public contact paths, tagged as general_business, role_based_business, or professional_social;
- decision-maker name and role only when a public source supports them;
- evidence URLs and the claim each source supports;
- an evidence-based need/fit hypothesis, clearly marked as a hypothesis;
- the next best action and the reason for it.

Use a bounded search budget. Normally stop after identity and a usable business contact are corroborated, or after roughly 6–10 targeted queries / two unproductive branches. Extend the search only for a high-value lead or when the user asks for deeper research. A missing decision-maker is a valid result.

### 4. Build the dashboard

When the user asks for Notion output, read [references/notion-dashboard.md](references/notion-dashboard.md).

- If a Notion connector is available and the destination is clear, preview the records and then upsert them using a stable identity key.
- If the destination is unclear, show the proposed schema and ask where the database should live before creating pages.
- If Notion is unavailable, produce a clean CSV/Markdown/JSON fallback with the same fields and source links.
- Keep New capture, Research queue, Verified contacts, Outreach queue, and Do not contact states distinct.
- Do not mark a lead verified merely because OCR found a phone number.

### 5. Prepare or send outreach

When drafting or sending messages, read [references/outreach.md](references/outreach.md).

- Personalize from observed or cited facts; do not imply a relationship, referral, or research finding that did not happen.
- Prefer a public business address, role-based email, main line, or professional social account. Treat a private-looking number or personal account as out of scope.
- Show a complete preview containing recipient, channel, subject/opening, body, evidence used, and opt-out language.
- Send only after the user explicitly approves the exact batch or clearly instructs ALS to send it. Log the channel, timestamp, source, and any opt-out; never contact a Do not contact lead.

## Output format

Return a compact summary and a lead table. Include:

- images processed and candidate businesses found;
- duplicates merged and records left unresolved;
- researched leads, verified contact paths, and missing decision-makers;
- dashboard status (created, updated, preview only, or fallback file);
- outreach status (drafted, awaiting approval, sent, or skipped);
- source links for researched claims.

Use the field definitions in the referenced documents so an intake-only run can be continued later without reprocessing the images.
