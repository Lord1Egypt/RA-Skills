# ClawHub Skill SEO Log

Tracking description changes, tag updates, and search ranking results for the `fleece` skill on ClawHub.

---

## v1.0.0 — Initial publish (2026-05-18)

**Description:**
> Fleece credit card research CLI. Provides live US credit card data via Brave Search — full reports, earning rates, transfer partners, statement credits, recent news, card comparisons, portfolio analysis, ROI estimates, and profile-based recommendations. Install with `pip install fleece-cli`. Use whenever you need current credit card information.

**Tags:** `latest`

**Search results:**
| Query | Rank | Score |
|---|---|---|
| `credit card` | #13 | 0.701 |

**Issues identified:**
- Generic name "Fleece" gives no signal to vector search
- Description truncated in results — key terms buried
- No categorical tags
- Zero results for conversational queries like "what card should I use for dining"

---

## v1.1.0 — Keyword-rich description + tags (2026-05-18)

**Changes:**
- Rewrote description to front-load issuer names (Chase, Amex, Citi, Capital One, Bilt) and reward types (points, miles, cash back, annual fees, welcome bonuses, transfer partners)
- Added "Use this skill when..." section with 8 natural-language trigger phrases near top of SKILL.md body
- Added 14 categorical tags

**Tags:** `latest, credit-cards, rewards, points, miles, travel, finance, research, amex, chase, citi, capital-one, brave-search, wallet, transfer-partners`

**Search results:**
| Query | Rank | Score |
|---|---|---|
| `credit card research` | **#1** | 0.817 |
| `credit card redemption` | **#1** | 0.782 |
| `credit card` | #13 | 0.702 |
| `what card should I use for dining` | — | no results |

---

## v1.1.1 — Conversational query language (2026-05-18)

**Changes:**
- Rewrote description opening to directly mirror user query phrasing:
  > "What credit card should I use for dining, travel, groceries, or gas?" — Fleece answers this with live data...
- Added `recommendations`, `dining`, `groceries`, `gas` tags

**Rationale:** Vector search scores on embedding similarity — starting the description with the exact question users ask maximizes cosine similarity for that query bucket.

**Tags:** `latest, credit-cards, rewards, points, miles, travel, finance, research, amex, chase, citi, capital-one, brave-search, wallet, transfer-partners, recommendations, dining, groceries, gas`

**Search results:**
| Query | Rank | Score |
|---|---|---|
| `credit card research` | **#1** | 0.817 |
| `credit card redemption` | **#1** | 0.782 |
| `what card should I use for dining` | — | no results (below threshold) |

**Note:** ClawHub has a minimum score threshold (~0.6–0.7). Conversational queries fall below it for all skills — not specific to fleece. Vector index update lag (~minutes) observed between publish and ranking change.

---

## v1.2.0 — MCC command added (2026-05-18)

**Changes:**
- Added `fleece mcc` command (offline MCC code lookup + wallet cross-reference)
- Added `mcc`, `merchant-category` tags

**Tags:** added `mcc, merchant-category`

---

## v1.2.1 — Claude skill for MCC published (2026-05-18)

**Changes:**
- Added `fleece-mcc.md` Claude Code skill
- No description change

---

## v1.3.0 — MCC-enriched workflows across all skills (2026-05-18)

**Changes:**
- Added merchant lookup as an explicit trigger phrase in agent SKILL.md:
  > "What card should I use at Costco?", "Which card earns the most at gas stations?", "What MCC is a pharmacy?"
- Added MCC workflow table to agent SKILL.md mapping common codes to typical card bonuses (5411 groceries, 5812 restaurants, 5541 gas, 4511 airlines, 7011 hotels, 4111 transit, 5912 drugstores)
- **fleece-wallet**: added post-gap-analysis MCC flow (`fleece mcc <code> --wallet`)
- **fleece-rates**: added MCC precision tip (5812 vs 5814 vs 5411 distinctions)
- **fleece-recommend**: added MCC-informed spending profile workflow
- **fleece-compare**: added MCC-precise comparison example

**Rationale:** MCC lookup answers "what card should I use at [merchant]?" with precision. Cross-referencing wallet gaps with MCC codes turns vague category gaps into specific merchant-level card recommendations. Adding merchant phrasing to trigger phrases broadens the query surface the skill matches.

**Tags:** unchanged from v1.2.1

---

## v1.4.0 — Profile system added (2026-05-18)

**Changes:**
- Added `fleece profile` command (show/set/unset/fields — no API key needed)
- `fleece wallet`, `fleece roi`, and `fleece recommend` now auto-inject profile context
- Added `fleece-profile.md` Claude Code skill
- Added `profile` tag
- Agent SKILL.md: added "Spending profile" trigger phrase and profile setup section

**Tags:** added `profile`

---

## v1.5.0 — Profile section in agent SKILL.md (2026-05-18)

**Changes:**
- Expanded agent SKILL.md with full profile documentation: setup workflow, field list, auto-injection behaviour for wallet/roi/recommend
- No description change

**Rationale:** Adding profile as a trigger phrase ("Save my spending habits", "Remember I spend $600/month on dining") broadens the query surface to match users who want to personalise their research experience.

**Tags:** unchanged from v1.4.0

---

## v1.6.0 — skills.sh / Vercel Agent Skills registry (2026-05-19)

**Changes:**
- Fixed SKILL.md frontmatter: removed embedded quotes from description (broke YAML parsing — ClawHub and skills.sh CLI silently failed to parse)
- Added `metadata` block (`author: chenyuan99`, `version: "1.5.0"`) matching skills.sh format
- Added root-level `SKILL.md` and `skills/fleece/SKILL.md` for `npx skills add chenyuan99/fleece`
- Distributed to 6 additional platforms: Gemini CLI, GitHub Copilot, Cursor, Windsurf (via `install.sh` flags and dedicated files)
- `npx skills add chenyuan99/fleece` now installs across **55+ agents** including Claude Code, Cursor, Copilot, Gemini CLI, Windsurf, Cline, Codex, Warp, Kiro, Continue, Junie

**Rationale:** The skills.sh / Vercel Agent Skills registry is platform-agnostic and installs to 55+ agents in one command. This is the highest-leverage distribution channel — broader reach than ClawHub, GitHub stars, or individual platform files. The YAML quote fix was the only blocker.

**Key lesson:** Embedded quotes in YAML frontmatter description (`"What credit card..."`) silently break parsing in both ClawHub's vector indexer and the skills.sh CLI. Always use plain unquoted text for the description field.

**Tags:** unchanged from v1.5.0

---

## Observations & lessons

1. **Description is the primary ranking signal** — ClawHub's vector search indexes the frontmatter `description` field. The body content appears to have lower weight. Front-load the highest-value keywords.

2. **Conversational queries hit a threshold floor** — queries phrased as full sentences ("what card should I use for...") return 0 results across all skills, suggesting the registry-wide similarity is below ClawHub's cutoff for this query type. Not a fleece-specific problem.

3. **Intent buckets explain everything about the `credit card` ranking** — this deserves a full explanation.

   ClawHub uses vector search: queries and skill descriptions are both converted into embedding vectors, and skills are ranked by cosine similarity (how close the vectors are in meaning). The word "credit card" alone is semantically dominated by the **payment intent** — *"give my agent a credit card to spend with"* — because that's the majority use case on ClawHub. The top results (`CreditClaw`, `CashClaw`, `Chase Bank`, `Shop Paper`) all say some variation of *"Give your Claw Agent a credit card — spend anywhere."*

   Fleece serves a completely different intent: **research** — *"help me find the best rewards card, compare fees, analyze my wallet."* These two meanings of "credit card" live in different regions of the embedding space. Our description is semantically distant from the payment cluster no matter how many times we say "credit card."

   **Analogy:** searching "Python" on a coding forum returns programming results; searching "Python" on a nature forum returns snakes. Same word, different intent, different vector neighborhood. We cannot rank #1 for "credit card" without misrepresenting what Fleece does — and we shouldn't try.

   **The right strategy is owning our intent bucket:**

   | Query | Intent | Our rank | Score |
   |---|---|---|---|
   | `credit card` | Give agent a payment card | #13 | 0.713 |
   | `credit card research` | Find best rewards card | **#1** | 0.827 |
   | `credit card redemption` | Redeem points/miles | **#1** | 0.786 |

   Users searching "credit card research" or "credit card redemption" are exactly our audience. Users searching "credit card" generally want payment capability — not our product. Ranking #1 in the right buckets is more valuable than ranking #5 in the wrong one.

4. **Tags are for filtering, not ranking** — adding tags didn't move needle on search scores but helps with tag-based browsing.

5. **Index update lag** — ClawHub rebuilds vector embeddings asynchronously after publish. The `inspect` summary field reflects the old content until the rebuild completes. Wait ~5–10 minutes before testing ranking changes.
