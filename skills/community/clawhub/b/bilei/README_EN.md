# Bilei.skill 💣→✅ (bilei-skill)

English ｜ [中文](README.md)

> **One sentence, 10 seconds to defuse a product category.**
>
> In an era of ads everywhere, check for landmines before you pay.
> Better to skip than to buy wrong.

Renovating your new home, you want a reliable air conditioner —

Every search returns pure praise, not a single negative.
The comparison reviewers are "you know what",
the feeds are flooded with GEO-poisoned posts by amateur accounts,
the few negatives get PR'd away, then buried by the algorithm.

Even a 17-year ad-industry veteran can't escape it. What about everyone else?

**Bilei is an anti-astro-turfing shopping advisor Skill:**

Give it a category and a budget.
It checks what PR can't touch — administrative penalties, inspection failures, recall notices —
digs up negative reviews scattered across complaint platforms and community corners,
grades the evidence by strength, runs quantitative trade-offs, and delivers a verdict first.

If no reliable option exists right now, it says "none right now" — no pushing.

**From power banks and cables to TVs, sofas and fridges — anything you'll keep for years can be vetted with it.**

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

## Install

Just two steps:

1. Open your agent (Claude Code / Cursor / Codex / WorkBuddy, etc.)
2. Say: **"Install this skill: https://github.com/zhashushu/bilei-skill"**

Or use the universal CLI installer (auto-detects your runtime):

```bash
npx skills add zhashushu/bilei-skill
```

Or manually: copy the whole folder into your agent's skills directory (e.g. `~/.claude/skills/`, `~/.workbuddy/skills/`). The folder name doesn't matter — rename it freely; what shows in the UI comes from `display_name` in SKILL.md.

## Usage

After installing, just say —

> "Defuse: living-room air conditioner, budget 5000, how to choose between a 1.5HP wall unit and a 3HP floor unit"
> "Robot vacuum under 3000, pets at home, mostly hair — check for landmines"
> "Is this dishwasher worth it? The salesperson says its 3-in-1 drying is an industry first — should I believe that?"
> "Does a 90-yuan cable deserve vetting too?" — Yes. The cheaper the product, the more fake specs. One sentence is all it takes.

## What it checks

1. **Mandatory certifications & standards** — does this category have them? Where to verify (China 3C: `cx.cnca.cn`; recalls: `samrdprc.org.cn`)
2. **Blacklist** — which brands/models were penalized, failed spot checks, or got recalled: model, authority, date, source, item by item
3. **Evidence grading** — official penalties/inspections > third-party tests > independent media benchmarks > user complaints > vendor claims/soft ads; every claim gets a grade
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
