# ac-buying-consultant ❄️

**AI skill that turns any agent into a professional AC buying consultant.**

Guides first-time and repeat buyers through every decision — room sizing, AC type selection, efficiency ratings, refrigerant choice, and feature prioritisation — producing a personalised, actionable recommendation they can take to any showroom.

---

## What it does

1. Collects room dimensions, climate zone, occupancy, insulation, sun exposure, budget, and ownership status through a structured conversation.
2. Calculates the correct cooling capacity (BTU / tonnage) using an industry-standard heat load method with adjustments for ceiling height, occupants, room type, sun exposure, and climate.
3. Recommends the right AC type (split, window, portable, cassette, or ducted) based on the user's specific constraints.
4. Presents specs in three tiers: **Non-Negotiable → Strongly Recommended → Optional** — so users know exactly where to spend and where to save.
5. Explains efficiency ratings in the user's local standard (BEE/ISEER for India, SEER2/Energy Star for USA, EU Energy Label for Europe, etc.).
6. Flags refrigerant types to avoid (R22, R410A) and recommends R32 as the current standard.
7. Provides country-specific model tier suggestions only when requested.
8. Closes with professional installation and maintenance reminders.

---

## Skill type

**Pure instruction-based.** No APIs, no external tools, no environment variables. The agent's reasoning + the SKILL.md instructions = the entire product.

---

## Who it's for

- First-time AC buyers who are overwhelmed by specs
- Buyers upgrading from an old unit and unsure what has changed
- Anyone in a hot or humid climate who needs a properly sized unit
- Developers building home improvement or consumer electronics advisors

---

## Key design decisions

- **Capacity is calculated before any spec is discussed.** This is intentional — wrong sizing is the most expensive mistake in AC buying.
- **Brand-neutral by default.** The skill avoids brand recommendations unless the user explicitly asks, preventing any appearance of bias.
- **Budget-honest.** If a budget is insufficient for the correct unit, the skill says so clearly instead of recommending a compromise that will cost more long-term.
- **Climate-aware.** The skill adjusts BTU calculations and efficiency targets based on the user's actual climate, not generic rules of thumb.

---

## Files

```
ac-buying-consultant/
├── SKILL.md     ← Agent instructions (this is the skill)
└── README.md    ← This file
```

---

## Usage

Install via [ClawHub](https://clawhub.io) or drop the `SKILL.md` into your agent's skill directory. No configuration required.

---

## License

MIT