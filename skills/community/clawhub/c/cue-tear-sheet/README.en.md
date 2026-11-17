# tear-sheet

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

*Full English translation of the Chinese-authoritative `README.md` in this directory; the Chinese text governs where the two diverge.*

**Thirty seconds before a client meeting — enough?** Enough. Hand it an issuer + a use case and you get a one-page sheet where **every line traces to a disclosure anchor** (readable on one screen) — and an opinions column that honestly stays blank.

This is the suite's **lowest-barrier entry piece**: zero deep research by default, built on structured-disclosure lookups, per-run cost magnitude has no measured evidence (consumption is whatever the server returns; the page header prints this run's channel usage). It does not decide for you; it lays out what is certain within 30 seconds — three identity lines, a four-period snapshot (cumulative + single-quarter, basis-tagged), on-record events (only those with an explicit disclosed date), risk items that actually hit, and three `[待人工]` slots for a human's view.

**Input**: issuer(s) (official name or code, ≤5) + purpose (pre-meeting glance / client brief) + optional one-line focus
**Output**: `tearsheet-<date>-<n>issuers/` — `page.md` (the five-block sheet) · `sources.jsonl` · `progress.md` ledger
**Cost**: three stages + one format gate; 0 research runs by default, at most one billing confirmation across the whole flow

---

## 1. What it is / what it isn't

| You want | Use |
|---|---|
| A 30-second pre-meeting one-pager (every line anchored) | **this skill** |
| A dated calendar of upcoming events for your holdings | sibling `catalyst-calendar` |
| A deep earnings review or quarter-over-quarter ledger | sibling `cn-earnings-note` |
| Spreadsheet deliverables, batches of >5 issuers, ratings / target prices / buy-sell advice | No — the opinions block is literally three blank lines waiting for a human |

## 2. The format *is* the discipline (why it looks like this)

Five blocks in fixed order; three header declarations mandatory (generation asof / data cutoff / this run's channel usage). These are gate checks, not aesthetics:

- **every line anchors**: only the **last column** of the snapshot table is validated, and it must match the `ANCHOR_OK_RE` whitelist as it now stands (announcement index / URL / domain ref / `[S<n>]` and kin); that whitelist accepts bare numeric strings of six-plus digits (index and issuer-code shapes), "so a number on the page" is not "an anchored line" — what you verify is whether that column leads back to a disclosure;
- **events pass a gate first**: an on-record event is admitted only through the first gate — a disclosure already on record carrying an explicit `YYYY-MM-DD`, or a statute-derived date whose conditions are decidable inside the anchor; date shape = `FULL_DATE_RE` and the estimated-date word family = `ESTIMATE_RE`, both as they now stand in `check_page.py` (common examples get caught, the list here is not exhaustive) — "events" without an explicit disclosed date never reach the page; this page carries no event-type enum column;
- **no fake all-clears**: if the direct lookup hits nothing, the page must carry the fixed line "no hits within the direct-lookup surface ≠ no exposure";
- **better empty than invented**: an unresolvable line is deleted and logged — an empty line is legal, an invented line is not.

## 3. Quick start (three steps)

1. **Install**: `npx skills add huhoo/cue-awesome --skill tear-sheet` - this line installs this package only; afterwards re-list installed skills and the name `tear-sheet` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to put this directory into your agent's skills folder (`~/.workbuddy/skills/`).
2. **Ask**: "见客户前给我一页纸看看东方雨虹" or "客户简报里加一节美的" (Chinese or English triggers). ≤3 questions to align inputs.
3. **Collect**: after three stages, `check_page.py` runs four gates (declarations / column anchors + two-way sources / zero-tolerance word list / format & line budget) — **no delivery without passing**.

## 4. First-time Cue setup (three steps, skippable)

Register at <https://cuecue.cn> (new accounts get 500 credits at signup and 10 credits daily — server policy governs) → get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> into your local credential facility (**never paste it into chat**) → install `cue-data-mcp` (`cue-omni-reader` as needed). Configuration pointers: the data-leg page <https://cuecue.cn/hub/mcp> (this piece runs by default on structured-disclosure lookups, with zero deep research) and the parsing-leg page <https://cuecue.cn/hub/omni-reader> (an on-demand leg - the case where it is used is summary-level source text when the section text on the domain face is not enough).
It runs without Cue too (you paste disclosure text; the page marks lines as user-supplied) — but then you don't see what anchored channel lookups actually look like, which is precisely what this piece is meant to show.

The three layers prove different things and are never equivalent: **skill installed ≠ credential configured ≠ channel connected**. Installed means your own re-listed skill inventory shows those names (files present, nothing more); configured means `CUE_API_KEY` sits in your local credential facility — **a key being present is not a key being accepted**; connected means calling the `url` inside that domain's `routing` with that key (`Authorization: Bearer <$CUE_API_KEY>`, plus `Accept: application/json, text/event-stream` — without that header you get 406, which is protocol behaviour, not an auth failure) and getting a `tools/list` reply back; tool names and input schemas come from that reply, never hardcoded.

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
[print(r.get("id"), r.get("external_status"), (r.get("routing") or {}).get("url", "-")) for r in rows]'
DOMAIN_ID="<replace with a domain id listed by the line above>"
ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
hit=[r["routing"]["url"] for r in rows if r.get("id")==sys.argv[1] and r.get("routing")]
print(*hit,sep="\n") if hit else sys.exit("not found: that id is not in the live catalog (or it has no routing.url) - run the listing line first, then fill it in")' "$DOMAIN_ID")"
[ -n "$ROUTING_URL" ] || { echo "no value: ROUTING_URL is empty - list the ids first, then set DOMAIN_ID to one of them" >&2; exit 1; }
curl -s -X POST "$ROUTING_URL" \
  -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  -w '\nHTTP %{http_code}\n'
```

`CATALOG` is the only catalog literal on this face (assigned once, not restated in prose); `$ROUTING_URL` is taken verbatim from that domain's `routing.url`. The two anonymous `GET` lines prove **catalog reachability only** - this face does not call that "connected". Pass = HTTP 200 with a non-empty `result.tools` (shape only; no tool names or counts are promised here). Domains absent from the catalog are neither installed nor promised by this face, and a connection error does not mean the domain has no data - report it as it came back. The endpoint may reply over SSE (one event line, then one data line); the `result.tools` you want is inside that data payload. This block adds no new credential read: the key comes from the local facility above, never into chat and never echoed back. **This package ships no connectivity script** - the two curl lines above are the whole route, nothing else is sent.

## 5. What's in the package

```
SKILL.md          master instruction: input contract / five blocks / cost discipline / pipeline & gate / boundaries (must read)
README.md         this file (Chinese source of truth)
README.en.md      English translation
CHANGELOG.md      version history
scripts/          gate script check_page.py + fixtures (word sets and guard inventory = the script and fixtures as they now stand; run the two lines below)
                                 note: which words are banned, which count as estimates, and which shapes pass as anchors is never listed in full here — the judgement is the checker as it now stands, self-checkable from any directory (the command carries the installed path):
                                     grep -n -A3 "BANNED_RE = \|ESTIMATE_RE = \|ANCHOR_OK_RE = \|PERIOD_RE = \|BASIS_ENUM = " ~/.workbuddy/skills/tear-sheet/scripts/check_page.py
                                     bash ~/.workbuddy/skills/tear-sheet/scripts/run_fixtures.sh (guard inventory and pass state, run in this package)
                                     Installed elsewhere: replace ~/.workbuddy/skills/ with your own skills directory; on Windows: C:\Users\<username>\.workbuddy\skills\tear-sheet\scripts\check_page.py
                                     Both lines use POSIX tooling (grep / bash) — on Windows run them in Git Bash or WSL. The first prints those five shape definitions with context: the rule source itself, not a per-sentence classifier;
                                     the anchor whitelist does accept bare six-plus-digit strings, so "a number on the page" is not "an anchored line". Word examples here are not an exhaustive claim.
```

## 6. FAQ and anti-patterns (what you try to do -> this skill refuses, because -> where to go instead)

Reviewed boundary clauses and fixture shapes re-assembled, nothing new promised. The banned family, the
speculation family and anchor shapes are whatever `check_page.py` holds now (locator command in section 5).

| What you try | Does it work, and why not | Where to go instead |
|---|---|---|
| Let me fill the view section myself so the page reads client-ready | **No.** The view section is three deliberately empty lines; filling them is out of bounds | A person writes the view; this skill keeps each figure traceable to a filing |
| Also export an Excel / spreadsheet file | **No.** Output is a markdown client page only | Build the spreadsheet yourself; no file format grows into this shape |
| Do seven or eight issuers in one pass | **No.** Issuers capped at 5 (machine-checked); beyond that per-row anchors slip | Run batches; to watch dates across a holdings set use `catalyst-calendar` |
| Fill a missing cell from common sense | **No.** That row is deleted and logged as a dropped row - empty is legal, invented is not | Leave the gap and log one line; add the row when the disclosure arrives |
| Put upcoming event dates into the one-pager | **No.** This page carries filed history only; forward-looking dates belong to the calendar skill | Use `catalyst-calendar`, where every event carries a disclosure anchor |
| Ask for live market values (price, daily change) | **Not included.** That channel is not open and this package never promises unopened domains | Pull quotes from your own terminal; this page stays on disclosure terms |

## 7. When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write "not found" and log it on the pending or coverage list; a blank never stands in for it.

**Error-level findings are blockers**: never describe them as harmless, ignorable, or shippable-as-is - fix them, or declare them explicitly on the deliverable.

Shapes are taken from **the current output** of `check_page.py`, captured by running it: on failure one line `FAIL: <file> (N items)`; detail lines **start with an error-code prefix (one of the five `E-*` codes), then the check label** (`[E-FORMAT] [参数] (args)`, `[E-BANWORD] [3]`, `[E-ANCHOR] [2]`, `[E-FORMAT] [4]`), then the line number and that check's spec; the final `code legend:` line lists only the codes used. A clean pass prints `PASS: <file> (four gates passed, subject blocks scanned normally)`.

The five codes are a closed, suite-wide identical set (byte-identical with the four siblings): `E-FORMAT` / `E-ANCHOR` / `E-BANWORD` / `E-COVERAGE` / `E-LEDGER`. Handling is printed in the `code legend:` line; the label-to-code mapping for this package is the classifier in the script, printable from anywhere by swapping these two keys into the grep in section 5:

    grep -n "^E_LEGEND\|^E_RULES" ~/.workbuddy/skills/tear-sheet/scripts/check_page.py

| Symptom (detail prefix) | Cause | Recovery |
|---|---|---|
| `[E-FORMAT] [参数] (args) missing --subjects(...)` | The formal command requires the declared subject count (two-way alignment with the page) | Add `--subjects N` equal to the real number of subject blocks; the opposite mismatch is reported too |
| `[E-FORMAT] [①] / [④] ...` | The first-screen declaration is missing, or the five blocks, section names, columns or row order are off (renaming or adding/removing sections triggers it) | Restore per the bracketed spec - the fixed risk sentence must be present |
| `[E-ANCHOR] [②] anchor empty / not in the accepted set` | The row has no anchor that resolves to a filing, or its shape is not accepted | Attach a disclosure anchor in an accepted shape (announcement index / document number / URL) or delete the row; never invent one |
| `[E-BANWORD] [③] line N hit ...` | A word from the banned set entered the body (rating, price-target, buy/sell families) | Rewrite neutrally or delete; no exemptions - full word set via section 5's locator |
| `[E-COVERAGE] [④] --subjects 声明 N ≠ 机检主体数 M(少报多搭/顶替申报)` | The declared subject count disagrees with the subject blocks actually on the page | Set `--subjects` to the real block count; do not resize the blocks to fit the declaration |
| Channel missing / a value cannot be fetched | Tool absent, or that measure was not disclosed for the period | Degradation: user-supplied material (marked at its source level); drop the row and log it instead of substituting an estimate |
| A traceback instead of `FAIL ... (N items)` | An incident - the gate is defined zero-crash with every parse point wrapped | Stop and report with the exact command; run section 5's guard samples to separate a bad page from a broken script |

## 8. How to ask (three positive examples, one counter-example)

**Ask with a point in time; the output states its data date**: give the reporting period, reference date or look-back window in the request; the deliverable labels its **data date** on the first line, and when that differs from the date you asked about, the text never says "today" or "latest" - it reads "as of <date>".
- **Positive (single issuer)**: "Give me a one-pager on Oriental Yuhong before the client meeting" - the shape in
  section 3; at most three questions fill the contract (subject / purpose / focus).
- **Positive (multiple issuers + purpose + focus + output dir)**: "Two names tomorrow: Midea and CATL. Purpose is a
  pre-credit conversation; one page each, focus on cash flow and backlog wording, output to `~/sheets/2026-10/`" -
  each page keeps its own anchors and ledger, and the declared subject count must match.
- **Positive (with a one-line focus)**: "Give me a one-pager on Midea before the client meeting, focus on how cash
  flow has been" - the focus only promotes that topic to a bolded line inside the page; it introduces no new data
  source and no new section (it is the optional third question of the input contract; the format does not change).
- **Counter-example (adjacent need, not this skill)**: "tabulate the confirmed dates for these names over the next
  three months" - `catalyst-calendar`; "lay out public risk facts and account for what could not be checked" -
  `dd-checklist`. This one ships a filed-history one-pager.

## 9. Current status (the blunt list)

- **Five-issuer boundary run landed (2026-09-21)**: pre-meeting glance ×5 issuers, 26 data-mcp lookups, 0 research, 0 omni; check_page in full form (incl. `--subjects 5`) PASSed first pass with exit 0.
- **Capability state**: public with the repo (current version per this package's `CHANGELOG.md` and frontmatter); the gate script and its guard samples ship together and **the word sets and guard count are self-checked by running them, not quoted here** (two commands in §5). **The "30 seconds" claim has no measured evidence**, and no per-run cost magnitude is stated — time depends on your channels and consumption is whatever the server returns.
- **Not submitted to any skill market**: publishing (P2) remains frozen; timing is the Owner's call. Repo visibility is governed by the root README and `CHANGELOG.md`.
- Issuer cap of 5 (machine-checked); no market-data flow (the `equity_market` channel is not open); **rating vocabulary is zero-tolerance by gate design** — the concept does not exist on this page.

## 10. Sources & credit

- Base: anthropics/financial-services `tear-sheet` (Apache-2.0) — the origin of the one-pager task shape.
- This package is an **A-share re-implementation, not a port**: the data layer is fully Cue-native; the five blocks, dual-basis snapshot, event first-gate, and cost discipline are rebuilt to this suite's contracts. No code from the base. See the repo-root `NOTICE.md`.
