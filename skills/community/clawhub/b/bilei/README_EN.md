# Bilei.skill 💣→✅ (bilei-skill)

English ｜ [中文](README.md)

> **Before you buy anything, check the negative data PR can't touch, then decide whether to pay.**
>
> Better to skip than to buy wrong.

## Install

Pick one:

1. Tell your agent (Claude Code / Cursor / Codex / WorkBuddy, etc.): **"Install this skill: https://github.com/zhashushu/bilei-skill"**
2. Universal CLI (auto-detects your runtime):

```bash
npx skills add zhashushu/bilei-skill
```

3. With the ClawHub CLI already installed (published slug `bilei`):

```bash
clawhub install bilei
```

Or copy the whole folder into your agent's skills directory (e.g. `~/.claude/skills/`, `~/.workbuddy/skills/`). The folder name doesn't matter; the name in the UI comes from `display_name` in SKILL.md.

## One real run: air fryer (2026-11-17)

The ask was 「想买个空气炸锅，帮我避雷」. The skill checked 17 public sources and did not push a model.

| Verdict | Why it would not name one | L1 |
|---|---|---|
| No single model you can order outright | The high-scoring reviews are from 2022; whether it is still on sale, and what you would actually pay, had no reliable source | 合肥荣事达 RS-B821: the knob turns, but it was not wired. 合市监处罚〔2026〕56号, fine 76.14 万元 |

Recommendation strength cannot exceed evidence strength.

The same screen also listed: knob turns but is not wired; coating migration may be over the limit; claimed capacity is not actual capacity; mechanical-knob temperature off by 10–20°C; electrical safety / hot housing; coating peeling and after-sales disputes.

## How this differs from a normal AI recommendation

- L1 penalties, inspections and recalls come first. A hit on the exact model knocks that model out.
- L3 splits into L3a (borrowed from a user, or self-purchased), L3b (vendor-sent or commissioned) and L3c (paid custom). SGS, TÜV and 华测 samples default to L3b, and are not graded L2.
- A press release counts as one source, however many times it is reposted.
- If no reliable option is left, it says none right now.

## Light edition and heavy edition

| Edition | Fit | How it works | Repo |
|---|---|---|---|
| Light (this repo) | See whether anything in the category is buyable now | Single agent, no orchestration | This repo |
| Heavy | Full audit over ¥2000, and for safety-critical categories | Evidence / quantitative comparison / verdict / price intel, role-isolated; price lookup happens after the verdict | [bilei-team-skill](https://github.com/zhashushu/bilei-team-skill) |

If this run was useful, star the repo, and name the next category in an issue.

---

Renovating your new home, you want a reliable air conditioner —

Every search returns pure praise, not a single negative.
The comparison reviewers are "you know what",
the feeds are flooded with GEO-poisoned posts by amateur accounts,
the few negatives get PR'd away, then buried by the algorithm.

Even a 17-year ad-industry veteran can't escape it. What about everyone else?

---

## The story behind it

I've worked in new media for 17 years (among the first wave of content creators on Weibo) and co-founded an MCN over a decade ago. I've placed soft and hard ads of every size for clients — I'm basically a human ad-detector myself.

Yet this year, while renovating my new home, I discovered that searching Douyin, Xiaohongshu, Bilibili, Zhihu and SMZDM for home appliances turned up nothing objective. The reviewers are "you know what", the feeds are flooded with GEO-poisoned posts, the few negatives get PR'd away and buried by algorithms — no negatives at all, pure praise.

Such an information cocoon is terrifying — even an industry insider can't buy an objective product. So I asked myself: what cannot be tampered with? Administrative penalties can't be PR'd away. Negative reviews get buried by algorithms for human readers, but AI can collect them far more easily.

This skill is built on that idea: use penalties, inspection notices and recalls — data PR can't touch — as the foundation, let AI gather the scattered negatives, grade the evidence, then talk recommendations.

**I know exactly where the ad money goes — so this skill only trusts what PR cannot touch.**

---

## News background: GEO poisoning is not a conspiracy theory — CCTV's 3·15 Gala confirmed the industry

Think "no objective reviews" is an illusion? CCTV's 2026 3·15 Gala exposed the whole chain:

- A reporter bought a "GEO optimization system" and **invented from scratch** a fake smart band (Apollo-9) with absurd selling points like "quantum-entanglement sensing" and "black-hole battery life"; the system auto-generated 10+ promotional posts and published them across platforms;
- **Just 2 hours later**, an AI model recommended the nonexistent product as a "standard answer";
- A GEO vendor's own words: "We can rank top-3 on any platform"; "A few million to plant some poison — why not?"

That's one real reason you can't find objective reviews: **the truth isn't absent — its weight is diluted by mass-produced soft ads.**

📎 Source: [CCTV News — 3·15 Gala: "Are AI models being poisoned? Brainwashing AI has become an industry"](https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=12967278106578155767)

---

## Usage

After installing, just say —

> "Defuse: living-room air conditioner, budget 5000, how to choose between a 1.5HP wall unit and a 3HP floor unit"
> "Robot vacuum under 3000, pets at home, mostly hair — check for landmines"
> "Is this dishwasher worth it? The salesperson says its 3-in-1 drying is an industry first — should I believe that?"
> "Does a 90-yuan cable deserve vetting too?" — Yes. The cheaper the product, the more fake specs. One sentence is all it takes.

## What it checks

1. **Mandatory certifications & standards** — does this category have them? Where to verify (China 3C: `cx.cnca.cn`; recalls: `samrdprc.org.cn`)
2. **Blacklist** — which brands/models were penalized, failed spot checks, or got recalled: model, authority, date, source, item by item
3. **Evidence grading** — L1 official penalties / inspections / recalls > L2 tests with no commercial tie > L3 media or creator tests (L3a borrowed from a user or self-purchased, L3b vendor-sent or commissioned, L3c paid custom) > L4 user complaints > L0 vendor claims. A model-level L1 primary source knocks that model out; a reprint alone, with no original document, is not enough to exclude it by itself
4. **Source profiling** — for every cited reviewer: who pays them (paid testing / vendor samples / commissions / self-purchased); conflict of interest discounts opinions, never facts
5. **Astro-turfing detection** — 10 links may trace back to 1 press release; near-duplicate posts are treated as GEO poisoning
6. **Quantitative trade-off** — premiums must go through the script (`scripts/premium_decision.py`): TCO/EAC, critical failure rate p\*, premium ROI, fair-price ceiling. No mental math
7. **Verdict first** — one recommendation + budget pick + quality pick + search terms / direct links / SKU path + on-arrival verification steps

## Three disciplines

1. **Recommendation strength ≤ evidence strength** — which never exceeds source strength
2. **Never fabricate** — say "not found" when it's not found; say "none right now" when nothing is reliable
3. **Verify first, write later** — prices, certifications, inspections and recalls are always looked up live, never from memory

## Quantitative engine

`scripts/premium_decision.py` (zero dependencies, standard library only, Python 3.8+) turns the "budget pick vs quality pick" debate into numbers:

```bash
python3 scripts/premium_decision.py selftest
python3 scripts/premium_decision.py all --input case.json --format both
```

## File structure

```
bilei-skill/
├── SKILL.md                        # Main skill file (single agent, no orchestration dependencies)
├── references/
│   └── source-credibility.md       # Evidence grades L1–L4, seven source archetypes, poisoning signals
└── scripts/
    └── premium_decision.py         # Premium-vs-risk calculator
```

## Honest words about accuracy

How accurate is it? Let's be upfront:

**Model capability accounts for only 30% of result accuracy; the other 70% depends on each vendor's search optimization.** If the sources are heavily poisoned, results will suffer — a polluted information pool is beyond any model, no matter how strong.

In my tests, the built-in search of the **DeepSeek** and **Gemini** clients returned somewhat higher-quality results.

That's why this skill stakes everything on data PR can't touch — penalties, inspection notices, recall announcements, plus negatives gathered from the corners: positive voices can be bought, but negative traces are hard to erase.

## Disclaimer

- Outputs are based on public information at query time; prices and promotions expire — re-verify before ordering.
- Meeting national quality standards is a floor, not a guarantee of greatness; the final purchase decision should fit your own scenario.
- Recommendation strength is always capped by evidence strength; when evidence is lacking, this skill would rather tell you "not found".

## License

MIT
