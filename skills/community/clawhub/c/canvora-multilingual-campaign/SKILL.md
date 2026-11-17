---
name: multilingual-campaign
version: 1.0.1
description: Turn one Canvora generation into a native multilingual campaign — generate once, convert per language with layout-preserving localization. 150+ languages including RTL (Arabic, Hebrew, Urdu) and CJK. Use when the user wants social visuals in multiple languages, localized campaigns, translated posts, or content for LATAM/MENA/European/Asian markets.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"🌍","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# Multilingual Campaign Creation

The canonical flow: **generate the campaign once, then convert it per language.** Canvora's localization is an image-to-image conversion of the finished visuals — layout, colors, fonts, and imagery stay exactly the same; only the text changes language. Design effort happens once, in the master; every language inherits it. Setup, credits, and general CLI usage: see the `canvora` skill. Design execution belongs to the pipeline — don't art-direct slide by slide, but do carry through any overall look the user has stated (see the `instagram-carousel` skill's rule; it applies here too).

## The flow

```bash
# 1. Generate the master once (any language — usually the user's primary market)
#    Without --json the first stdout line is the bare id (progress goes to stderr)
ID=$(canvora generate --idea "..." --format instagram_post --brand $BRAND_ID | head -1)
canvora status "$ID" --json    # poll until completed before localizing

# 2. Convert per language (one call per language; confirm the list with the user first)
#    A multi-visual master is 3+ outputs per language — fire and poll, don't --wait
ES=$(canvora localize $ID --language es | head -1)
canvora status "$ES" --json    # repeat every ~30s until completed
AR=$(canvora localize $ID --language ar | head -1)
canvora status "$AR" --json
```

`| head -1` captures the id from `generate` and `localize` alike — same idiom both times, nothing to remember, and no `jq` needed. Keep `--wait` only where the step really is 1-2 visuals (a single-image master). Above that, poll: most harnesses kill a shell command at 120s while the conversion carries on server-side, and re-running after a timeout starts a second, separate job. See the `canvora` skill's "Long runs" section.

`localize` converts ALL visuals in the generation (10 credits per visual per language — a 6-slide deck into Spanish = 60; always confirm languages with the user before running). To convert only ONE visual out of a multi-visual generation, use `canvora edit <outputId> --prompt "Translate all visible text into Spanish" --yes` instead.

A campaign is one generation plus one call per language, so **add up the whole plan — master + (visuals × 10 × languages) — and run `canvora credits --json` once before you start.** Running dry on the third language leaves a half-localized campaign with the earlier languages already paid for. State that total in the same message as the run: announce it, don't ask permission (the language list is the thing you confirm, not the price).

## Briefing the master so conversions survive

- **Short text:** translations expand (German/Portuguese commonly +20–35%). Keep master slide text ≤20 words per slide — overflow in the converted versions is the #1 multilingual failure.
- **Pin what shouldn't move:** brand names, product names, campaign hashtags stay in the source language — say so in the brief ("keep 'Acme' and '#AcmeLaunch' untranslated").
- **Language precision at conversion time:** "Brazilian Portuguese" (`pt-BR`) vs "Portuguese"; Simplified vs Traditional Chinese. Pass what the user's market actually means.
- **RTL check:** Arabic/Hebrew/Urdu conversions mirror text direction automatically; still eyeball reading order on multi-column layouts before shipping.

## When NOT to localize (the exception)

If a market needs different *content* — a different hook for Brazil than for Germany, market-specific examples or CTAs — that is not a conversion job. Run a separate `canvora generate` per market with its own brief. Language is auto-detected from the brief (a Spanish idea yields a natively Spanish generation), or force it with `--language`. Treat this as the exception: same message everywhere → localize; different message per market → separate generations.

## Delivery

- Poll each localization to completion; group results by language, outputs sorted by `sortOrder` within each.
- **Captions are not visuals:** write each language's caption natively (the agent's job) — never translate the master caption literally.

## Campaign patterns

- **Market test:** master → localize into 3 candidate markets → post all → double down where engagement is highest. Cheap enough to treat languages as A/B variants.
- **The multilingual flex post:** one design in 4+ languages side-by-side is itself strong social content ("same post, four markets, three minutes").
- **Agency onboarding:** brand kit per client once → every campaign ships in all their market languages by default.

## Quality checklist

- [ ] Master generated once; languages produced via `localize` (not regeneration)
- [ ] Master slide text ≤20 words; brand/product names pinned untranslated
- [ ] Language list confirmed with the user before converting
- [ ] RTL outputs reviewed for reading order
- [ ] Per-language captions written natively; outputs sorted by `sortOrder`
