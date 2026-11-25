# 避雷选品团.skill 💣→✅ (bilei-team-skill)

[中文](README.md) ｜ English

> **Four roles working together, decided by evidence. If it cannot be found, say so.**
> This is the **multi-agent heavy edition** of [避雷.skill](https://github.com/zhashushu/bilei-skill) — everyday quick answers use the lite edition (轻快版); big-ticket items and safety-critical categories use this edition. If there is no reliable option, say there is none right now (目前没有).

## Install

Open the agent you are using (Claude Code / Cursor / Codex / WorkBuddy, and others) and tell it: **「帮我安装这个 skill：https://github.com/zhashushu/bilei-team-skill」**

Or use the general-purpose CLI installer:

```bash
npx skills add zhashushu/bilei-team-skill
```

You can also do it by hand: put the whole folder into your agent's skills directory (for example `~/.claude/skills/` or `~/.workbuddy/skills/`). The folder name can be anything. The skill name shown in the UI is `display_name` in SKILL.md.

## How this differs from a generic AI recommendation

- Administrative penalties, failed sampling inspections, and recall notices come first. A model-level L1 primary document removes that model from recommendation.
- An SGS / TÜV send-in test is recorded as L3b. A lab logo does not raise it to L2.
- Reprints of the same press release count as 1 source, however many times it is republished.
- The four roles stay isolated: the evidence role may not recommend, and the numbers role may not conclude. The price-intelligence role is sent out only after the verdict.
- If there is no reliable option, say there is none right now.

## Lite / heavy (轻快版 / 重型版)

| | [避雷.skill](https://github.com/zhashushu/bilei-skill) lite | **避雷选品团.skill (this repo)** heavy |
|---|---|---|
| Form | Single agent, no orchestration dependency | Multi-agent collaboration (4 roles) |
| Cost | About one tenth | Full manuals loaded × 4 lines |
| Fits | Everyday shopping, quick questions, low-priced small items | Big-ticket items over ¥2000, safety-critical categories, a full audit trail |

**Which to use**: Use 避雷.skill day to day. For an air conditioner, a water heater, a child safety seat, an e-bike — purchases where one mistake is costly — or when you want a full audit report that can be checked line by line, switch to this edition.

## How to start

Give it a category or a need. For example: 「想买个扫地机器人」, 「3000 以内 4K 显示器剪辑用」, 「这型号值不值得买」.

If this page is useful, a star on the repo is welcome, and so is an issue naming the next category.

## It sends four roles to work

1. **Anti-poisoning and quality investigator** (also gathers professional-review evidence) — checks national standards / 3C / sampling / recalls / penalties / soft-ad poisoning, and deliberately collects teardowns and instrumented measurements. For each model it gives a **source-interest audit**: who paid (paid test / send-in test / affiliate / a reader lent the unit), and whether the usable layer is facts or opinions. Facts only. No recommendations.
2. **Technical and market comparison officer** — first screens gating specs (protocol / compatibility / interface generation: the hidden yes-or-no issues that decide everything), then compares parameters on the same basis, and quantifies the premium %, TCO/EAC, and quality-price ratio (QPR). Numbers only. No conclusions.
3. **Lead adjudicator** (the main loop itself) — cross-checks, applies a veto, prices both tracks, and sets the recommendation level by evidence strength: **the strength of a recommendation cannot exceed the strength of the evidence**.
4. **Price intelligence officer** — sent out only after the verdict (looking up the price first would bias the vote): historical lows, landed price by channel, national subsidies and price protection, and when to buy. Ships a Manmanbuy comparison script that does not require a login.

**Role isolation is the core design**: the evidence role may not recommend, the numbers role may not conclude, and the price role must wait for the verdict. That closes off the confirmation bias of liking a product first and then looking for reasons.

## Built-in category layer

Gating specs, key metrics, and vertical-source files for 13 categories, plus four fallback questions for categories outside the table, plus rules of their own for non-physical goods (services / software / insurance / courses). Changing category does not mean changing the rules.

## Baseline abilities shared with the single-agent edition (filled in at v6.1)

- **Standards check**: look up mandatory national standards and certification, whether a stricter standard exists (the comparison must give the indicator numbers), and state which standard the conclusion follows. Without evidence that a standard is followed, a model cannot be the first choice.
- **Manufacturer audit**: four modes (in-house / contract manufacturing / badge engineering), plus a lookup of the contract factory's record by factory name. Pure contract manufacturing or badge engineering drops one level.
- **Source blocklist**: an official list shipped in the package, plus a user blocklist that is kept when the skill is updated. The list comes first, with a feature-based fallback. One sentence is enough to add or remove an entry.
- **Resale retention**: recent Xianyu sales → used price / markdown / retention rate, as an extra item in the comparison.
- **Version check**: one check for a newer version when the skill runs. It adds a single line at the end and does not interrupt the main flow.

> Stronger abilities that belong to this edition only (budget tiers, three-layer output, a share edition, and a seven-class source-credibility audit) stay as they are.

## Three rules (the same line as 避雷.skill)

1. **Recommendation strength ≤ evidence strength**, and the strength of the evidence cannot exceed the strength of the source.
2. **Do not invent data** — if it cannot be found, write that it cannot be found. If there is no reliable option, say there is none right now.
3. **A conflict of interest cuts the opinion layer, not the fact layer** — for a paid review source, drop its conclusion and keep its teardown photos and measured data.

## Quantitative scripts

- `scripts/premium_decision.py` — premium-versus-risk calculator (no dependencies, Python 3.8+): TCO/EAC, critical failure rate p\*, premium ROI, fair-price ceiling, QPR
- `scripts/manmanbuy_price.py` — Manmanbuy price comparison without login (physical goods only): one command returns the deal price, the mall, the date, and the price label
- `scripts/custom_blocklist.py` — the user's own source blocklist (add / remove / list / check / path). The list is stored at `~/.bilei/user-blocklist.md` and is kept when the skill is updated
- `scripts/check_update.py` — version check (fallback across sources + 24h cache + silent on failure)

```bash
python3 scripts/premium_decision.py selftest   # self-test
```

## Files

```
bilei-team-skill/
├── SKILL.md                        # skill entry (four-line parallel dispatch + budget tiers)
├── references/
│   ├── agent1_blacklist.md         # anti-poisoning and quality investigator manual
│   ├── agent2_quant.md             # comparison officer manual
│   ├── agent3_verdict.md           # lead adjudicator manual
│   ├── agent4_price_intel.md       # price intelligence officer manual
│   ├── category_profiles.md        # 13-category adaptation layer
│   ├── output_template.md          # three-layer output template (layer 0 / 1 / 2 + share edition)
│   ├── cases.md                    # failure cases (where the rules came from)
│   ├── changelog.md                # full changelog
│   ├── case_example.json           # sample input for the quantitative script
│   ├── manufacturer-audit.md       # manufacturer / supply-chain audit (in-house / contract / badge)
│   └── source-blocklist.md         # official source blocklist (shipped with the package)
└── scripts/
    ├── premium_decision.py         # premium-versus-risk calculator
    ├── manmanbuy_price.py          # Manmanbuy comparison without login
    ├── custom_blocklist.py         # user source blocklist
    └── check_update.py             # version check
```

## A plain statement on accuracy

Same as 避雷.skill: **model ability is only 30%; the other 70% depends on each company's search tuning and the source ecosystem.** Once sources are polluted, no model's output can be saved. In practice, the search built into the DeepSeek / Gemini clients is slightly better. That is why this edition insists on data public relations cannot scrub — administrative penalties, sampling notices, and recall announcements. Positive voices can be bought as traffic; negative traces are hard to erase.

## Disclaimer

- Output is based on public information at the time of the search. Prices and promotions go stale. Check again before you order.
- Passing a national quality requirement is only the floor. It does not mean the product is good to use. Make the final decision for your own situation.
- Every recommendation is limited by the evidence. When the evidence is not enough, this skill will tell you it cannot be found (查不到).

## License

MIT
