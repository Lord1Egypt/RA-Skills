---
name: ai-creative-studio
description: Turn one brief into a complete US-market creative package — ad copy, social posts, video hooks, image prompts and a reusable brand voice kit for TikTok, Instagram, Meta, YouTube and email. Built for US founders, DTC brands, agencies and solo marketers who need on-brand content in minutes.
version: 1.0.5
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    envVars:
      - name: OPENAI_API_KEY
        required: false
        description: Optional. Used only when the runtime should call an image or copy API instead of returning prompts.
      - name: REPLICATE_API_TOKEN
        required: false
        description: Optional. Optional token for hosted image/video generation models.
    emoji: "\u2728"
    homepage: https://github.com/rapidworker1
---

# AI Creative Studio

**One brief in. A full creative package out.** Hooks, ad copy, captions, scripts,
image prompts, a brand voice card, and a 30-day content calendar — all in US
English, all on-brand, all ready to ship.

Use this skill when someone asks for:

- social posts or captions for TikTok, Instagram, Facebook, LinkedIn, X, Threads
- Meta / Google / TikTok ad copy (primary text, headlines, descriptions, CTAs)
- UGC video hooks, scripts, shot lists, or creator briefs
- product photo / hero image / thumbnail prompts and art direction
- email subject lines, preview text, and launch sequences
- a brand voice card or messaging framework for a US audience
- a content calendar, launch plan, or repurposing matrix

---

## Why this exists

Most AI output for marketing is generic. This skill runs a **repeatable
production pipeline** instead of one-shot prompting:

1. **Brief normalization** — pull product, audience, offer, proof, tone, channels
   out of a messy request. Ask at most 3 questions if a required field is missing.
2. **Message spine** — one core promise, three proof pillars, one objection
   handled.
3. **Channel-native output** — a TikTok hook does not look like a LinkedIn post.
   Each channel gets its own format, length, and CTA.
4. **Brand voice lock** — a reusable voice card so every future request stays
   consistent.
5. **Compliance pass** — no unsubstantiated claims (no "cures", no fake
   statistics, no "guaranteed results"), no fake testimonials, no competitor
   trademarks used as keywords.

## Quickstart

**Input** (one of these is enough):

```text
Launch a $39 insulated dog bottle for US weekend hikers.
Tone: practical, a little blunt. Not hype.
```

**Run:**

```bash
python3 scripts/creative_brief.py --brief brief.yaml --out campaign/
```

This writes `campaign/brief.normalized.json`, `campaign/creative_pack.md`
(the full deliverable), and `campaign/prompt_set.json` (image/video prompts
ready for any generator).

**Then paste `campaign/creative_pack.md` back to the agent** and ask for the
variants you need ("give me 10 more TikTok hooks under 6 words").

### Brief file format

```yaml
product: "Insulated dog bottle (HydroFlask-class)"
audience: "US weekend hikers, 25-40, buy outdoor gear on Amazon and REI"
offer: "$39 + free shipping over $50, 30-day trial"
proof:
  - "18/8 stainless, keeps ice 24h"
  - "12,000 reviews, 4.7 stars"
tone: "practical, blunt, zero hype"
channels: [tiktok, instagram, meta_ads, email]
brand_voice: "Like a hiking buddy, not a billboard"
competitors: ["Yeti Rambler", "Hydro Flask Wide Mouth"]
cta: "Tap the link and try it for 30 days"
```

---

## Output contract

Every creative pack contains exactly these sections, in this order:

| Section | What it contains |
| --- | --- |
| **1. Message spine** | Core promise, 3 proof pillars, 1 objection handled, 1 CTA |
| **2. Brand voice card** | 5 voice traits, do/don't list, banned phrases, 3 sample lines |
| **3. Hook bank** | 15 hooks split by platform, sorted by strength signal |
| **4. Ad copy** | Meta (primary/headlines/description/CTA), Google (RSA + PMax assets), TikTok (primary text + CTA) |
| **5. Social posts** | Per-platform posts with hashtags, alt text, and pinned comment |
| **6. UGC scripts** | 3 scripts: problem → demo → proof → CTA, with shot list and on-screen text |
| **7. Image & video prompts** | Generation-ready prompts with camera, light, lens, aspect ratio, negative prompts |
| **8. Email sequence** | 4 emails: welcome, feature, proof, offer — with subject line + preview text |
| **9. 30-day calendar** | Date, channel, format, hook ID, CTA, asset checklist |
| **10. Compliance notes** | Claims to verify, trademarks to clear, disclaimers to add |

## Channel rules that matter in the US

- **TikTok / Reels**: hook in the first 2 seconds, 7–15 words, captions on, 9:16.
- **Instagram feed**: 4:5 image, caption under 125 characters before "more", 3–5 hashtags max.
- **Meta ads**: primary text 125 characters minimum of value before the CTA, 3–5 headlines, one CTA.
- **LinkedIn**: no emoji walls, no "🚀🚀🚀", professional but human, 1200–1800 characters.
- **X**: under 280 characters, one idea, link last.
- **Email**: subject line 30–45 characters, preview text 40–90 characters, one CTA per send.
- **Google RSA**: 15 headlines, 4 descriptions, 90 characters per headline.
- **US spelling and references** by default; say "cancel anytime", "free shipping", "30-day trial" only when the offer actually says so.

## Guardrails (hard rules)

- **No fake social proof.** Never invent reviews, star ratings, customer counts, awards, or press mentions. Use only proof the brief supplies.
- **No unsubstantiated claims.** Flag every health, income, or performance claim in *Compliance notes* and mark it `VERIFY`.
- **No competitor trademark use.** Competitors may be referenced as comparison, never in keywords, hashtags, or ad copy.
- **No impersonation.** Do not generate likenesses of real people, real brands' creative systems, or "in the style of <living artist>" work.
- **No NSFW, no sensitive-category ad copy** (health claims, credit offers, political content).
- **One offer per deliverable.** Price, discount, and CTA must match the brief exactly.

## Files in this bundle

```
references/
  brand-voice.md          Voice card template + 40 traits library
  channel-specs.md        US platform specs, hook patterns, CTA bank
  campaign-playbook.md    Launch sequence, testing plan, budget split, metrics
templates/
  brief.yaml              Input brief template
  social-posts.md         Post scaffolds per platform
  ad-copy.md              Ad copy scaffolds (Meta, Google, TikTok)
scripts/
  creative_brief.py       Normalize brief -> creative pack + prompt set
```

## Workflow

1. Load `templates/brief.yaml`, fill it from the user's request.
2. Run `scripts/creative_brief.py`.
3. Deliver `creative_pack.md` as the answer; keep `prompt_set.json` for the user's generator of choice.
4. Offer follow-ups in one line: "Want 10 more hooks, a 30-day calendar, or A/B variants of the primary text?"

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Script missing `python3` | Use `python` instead, or install Python 3.10+ |
| Brief feels thin | Ask the 3 highest-leverage questions: audience, offer, proof |
| Output too generic | Add 2 competitor names + 1 banned-phrase to the brief |
| Copy too long | Platform limits are in `references/channel-specs.md` |

## Related

- [`b2b-lead-research-agent`](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) — find the US accounts to run this creative against.
- [`ai-trading`](https://clawhub.ai/rapidworker1/skills/ai-trading) — research the tickers of public competitors before writing comparisons.
- **[Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite)** — one Windows kit that sets up all three workflows in a single folder. The desktop app is a separate download from the publisher's GitHub release, with a published SHA-256 so you can check the file before you unpack it; no skill bundle carries an installer.

---

*Content generated with this skill is a starting draft. Verify every claim, price, and statistic before publishing.*
