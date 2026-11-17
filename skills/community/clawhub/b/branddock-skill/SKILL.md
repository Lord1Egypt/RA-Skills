---
name: branddock-on-brand
description: Work on-brand with Branddock, the brand memory and brand check for AI. Use this skill whenever you create, rewrite or review content for a brand that uses Branddock (social posts, emails, blogs, ads, web copy, scripts) — it makes you fetch the real brand context first, write with it, score every output with the F-VAL brand check, and leave publishing to the human.
---

# Branddock — brand memory and brand check

Branddock holds a brand's complete DNA (voice, personas, products, competitors, guidelines) and can measure how on-brand any text is: the F-VAL score (0–100, with concrete findings). Your job with this skill: never write "generic AI" content for a Branddock brand. Fetch the brand first, write with it, verify with the score, and let the human approve.

## When to use this skill

- Any content task for a brand that has a Branddock workspace: writing, rewriting, reviewing, translating, brainstorming in brand voice.
- Any question about the brand itself ("how do we sound?", "who are our personas?", "what does our brand say about X?").
- Checking whether an existing text (from any source) fits the brand.

Not needed for: content explicitly unrelated to the brand, or pure technical/code tasks.

## How you connect (pick the first that is available)

1. **MCP connector** (preferred): tools from the `Branddock` connector (`https://branddock.app/mcp`). If the tools are listed in your session, use them directly.
2. **REST API** (for scripts/automation): base `https://branddock.app/api/v1`, header `Authorization: Bearer bd_live_...` (workspace-locked API key, created in Branddock under Settings → API & Connectors).
3. **Neither available?** Tell the user: add the connector URL `https://branddock.app/mcp` in your AI's connector settings and log in with your Branddock account — or create an API key in Settings → API & Connectors. Don't improvise brand knowledge without a connection.

## The workflow (always this order)

### 1. Know the brand — before writing anything

- Call `get_brand_context` once per conversation (per brand). It returns the full brand DNA: voice and tone rules, do's & don'ts, personas, products, competitors, style notes and the brand's content language.
- Multiple brands on one account? Call `list_brands` first and pass the right `brand` (workspace id or exact name) to every tool call.
- Ground every brand statement in this context. If the context doesn't answer something, say so — never invent brand facts, slogans, product claims or persona details.

### 2. Create with the brand, not next to it

- Write in the brand's **content language** (it is in the context), unless the user explicitly asks otherwise.
- Apply the voice rules literally: vocabulary to use and to avoid, tone dimensions, anti-patterns. Personas from the context are your audience definitions — pick the one the user names, or ask.
- For substantial deliverables (posts, blogs, campaigns) prefer generating **through Branddock** (`generate_on_brand`) over writing inline: the full brand pipeline runs server-side, the result lands scored in the user's Branddock library, and the user keeps one place to review. Inline writing is fine for quick drafts and rewrites — then score it (step 3).
- Rewriting an existing text (email, reply, external copy)? Use `rewrite_on_brand` — nothing is stored, costs 1 credit.

### 3. Verify — score before you present

- Score your result with `score_against_brand` (free, unlimited). You get a composite 0–100, a per-pillar breakdown, the brand's threshold and concrete findings.
- **Below the threshold?** Revise using the findings (they tell you what is off-brand) and rescore. Maximum two revision rounds — if it still scores low, present your best version *with* the score and findings, honestly. Never hide a low score.
- Mention the score when you deliver: "F-VAL 84, above the threshold" is part of the answer, not decoration.

### 4. The human approves — always

- You never publish, schedule or send anything yourself. Everything you make is a proposal.
- Content generated through Branddock waits in the user's library for review; inline drafts are handed to the user with their score. Say what the next step is ("review it in Branddock" / "want me to adjust?").

## Tool map (MCP names)

**Know the brand (free):** `get_brand_context` · `get_brand_md` · `list_brands` · `list_personas` · `list_products` · `list_competitors` · `search_knowledge` · `get_deliverable_content`
**Guard & follow (free):** `score_against_brand` · `get_strategy_status` · `get_seo_status`
**Make (costs credits — see below):** `generate_on_brand` · `rewrite_on_brand` (1) · `generate_web_page` (5) · `generate_long_form_seo` (80) · `generate_campaign_strategy` (80)

**API-key only — NOT available over the MCP connector:** `generate_image` (2) · `generate_video` (20) · `import_brand_data`. Over the connector (route 1 above) these tools do not exist; don't try to call them. Need on-brand imagery or video? Tell the user it runs through a Branddock API key (route 2) or in the Branddock app itself.

## REST equivalents (when using an API key)

```bash
# Full brand context
curl https://branddock.app/api/v1/brand-context \
  -H "Authorization: Bearer bd_live_..."

# Score a text against the brand
curl https://branddock.app/api/v1/score \
  -H "Authorization: Bearer bd_live_..." \
  -H "Content-Type: application/json" \
  -d '{"content": "... (min. 50 tekens) ..."}'
```

Generation endpoints mirror the MCP tools (`/generate`, `/seo-generate`, `/webpage-generate`, `/image-generate`, `/video-generate`).

## Credits, costs and honesty

- Reading brand context and scoring are **always free** — use them liberally; that is the point of Branddock.
- Generating costs credits (numbers above). Before starting an expensive generation (long-form SEO or a campaign strategy, 80 credits; video, 20), tell the user the cost and expected duration (SEO ≈ 7–8 minutes, async — poll with `get_seo_status`).
- Never claim autonomy the product doesn't have: Branddock's own rule is "you approve" — no "autopilot" language, ever.

## When something fails

- **401 / unauthorized**: the connector session or API key is invalid — ask the user to reconnect (connector) or check the key.
- **Credits exhausted**: say so plainly; the user can top up in Branddock (Settings → Billing). Free tools keep working.
- **Brand not found**: call `list_brands` and use an id or exact name from that list.
- **A tool call needs the user's permission** (chat clients ask per tool): explain that read/score tools are safe to always-allow; generation tools are worth approving per use.

## First prompts that work well

- "Haal mijn merkcontext op en vat samen hoe mijn merk klinkt."
- "Schrijf een LinkedIn-post over [onderwerp] voor persona [naam] en scoor hem met de merk-check."
- "Herschrijf deze e-mail in onze merkstem en laat de score zien: [tekst]"
