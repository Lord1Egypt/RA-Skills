# Restructuring Progress Tracker

String the multiple announcements of one A-share major asset restructuring onto a single timeline: mark each progress node (trading halt, preliminary plan, draft, inquiry, review meeting, approval, implementation), record what changed at each step (consideration, payment method, performance commitments, lock-up), and source every step to its own announcement with a retrieval date. Gaps are named item by item, in both directions.

**What it does not do**: no ratings, no target prices, no buy/sell timing, no probability guesses on approval, no valuation judgements. Those slots stay `[待人工]` for a human.

## 1. Start here: three steps today

| Step | Do | Output |
|---|---|---|
| 1 | Collect the announcements for one deal (at least two) | A list: disclosure date, node, title, link |
| 2 | Order them into a timeline, one factual line each | Section 3, "Progress timeline" |
| 3 | Compare adjacent announcements, write "before → after" | Section 4, "Changes per step", two anchors per line |

Then run `python3 scripts/check_tracker.py <draft>.md` and fix whatever comes back red.

## 2. Install → connect → produce

```bash
# 1. Install
npx skills add huhoo/cue-awesome --skill cn-restructuring-tracker

# 2. List the catalog, take this group's routing URL
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000

# 3. Confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# 4. Lay the announcement list out as a skeleton, then read each source to fill it
python3 scripts/make_outline.py announcements.jsonl --out tracker.md
```

## 3. Offline samples

`scripts/fixtures/` holds one complete good sample and five bad ones, each failing exactly one lane:

```bash
bash scripts/fixtures/run_fixtures.sh
```

Five tiers: criterion self-test / good plus five bad run one by one / skeleton generation / skeleton must go red on its placeholder lines / five boundary shapes. Runs in 30 seconds, zero network, zero billing, zero credentials.

## 4. Dependencies and the cost of each path

- Dependency: `python3` (standard library only, no third-party packages).
- **With a channel**: you can fetch the announcements and read what changed between steps — the only form of this piece that carries value.
- **Without a channel**: it can only lay an existing list out as a skeleton, leaving the conclusion and the changes as placeholders. **The cost, stated plainly: no source text means no changes, and no changes means the core value of this tracker is zero** — what remains is a table waiting to be filled. The skeleton goes red on its placeholder lines by design, not by fault.

## 5. Boundaries and non-promises

- **Boundary against `ma-restructuring-terms-cn`**: that piece is a **clause read** — one restructuring document broken into eight verbatim cards. This piece is **cross-period tracking** — several announcements for the same deal strung onto a timeline. A timeline with fewer than two rows is clause-read work, and the checker names that piece for you.
- Not promised: whether the deal will succeed, where the price goes, whether the consideration is high or low, the odds of approval.
- Not promised: anything the announcements do not disclose. What was not obtained is written as not obtained.

## 6. When something goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| "timeline has only N rows" | Only one announcement in hand | Switch to `ma-restructuring-terms-cn`, or collect the rest |
| "change line has only 1 anchor" | The change points at one place | Anchor the before and after values separately |
| "section 6 is missing an item" | Body says not obtained, section 6 omits it | Add it to section 6 |
| "section 6 lists an extra item" | Section 6 names it, body never says it | Add the body line, or drop the section 6 item |
| "node not in the register" | Used a word like "review meeting held" | Use one of the eight registered nodes, or put the fact in the line |
| "dates out of order" | Timeline reversed | Re-sort ascending by date |

## 7. How to ask

- "Where does this restructuring stand now?"
- "How many times have the consideration and lock-up changed since the halt?"
- "What changed in the draft versus the preliminary plan?"
- "String these announcements into one timeline"

## 8. Capability boundary

- Input: several announcements for one deal (`ma-restructuring-document`, `announcement-doc`), or already-parsed documents (`parsed-doc`).
- Output: one cross-period tracker (`change-brief`), seven sections, every step sourced.
- Not done here: clause reads (go to `ma-restructuring-terms-cn`), ratings and target prices, buy/sell advice, approval odds.

## 9. Resources

- `SKILL.md` — full specification (seven-section contract, five machine checks, sourcing discipline)
- `scripts/check_tracker.py` — the five checks; `--selftest` runs the bundled fixtures
- `scripts/make_outline.py` — zero-channel fallback: lays an announcement list out as a skeleton
- `scripts/fixtures/` — one good sample, five bad ones, `run_fixtures.sh`
- `CHANGELOG.md` — version history
