# cn-research-brief

**Turn a batch of Chinese-language sources into one traceable research brief: every finding carries its own source line with a retrieval date, every gap is named, and every judgement is left to a human.**

Bullet points are not scarce; **what is scarce is a bullet you can trace back to one dated source**. Two hard gates do the work: a finding without an anchor never enters section two, and a gap that was not named never passes the machine check.

**Input**: a set of Chinese sources (web pages, announcements, reports, parsed documents) plus the subject and the retrieval window - or a question to be broken down
**Output**: a four-section brief (one-sentence conclusion / findings / gaps and definitions / sources) and the per-source lines behind it
**Cost**: a four-section contract plus one machine check; whether the channel legs (deep research / parsing) are switched on decides what this brief can contain - each path and what it lacks is written in sections 2 and 4
**Machine check**: `scripts/check_brief.py`, four lanes (format / anchors / banned verdict words / gap accounting), zero network; the counter-evidence matrix lives inside that script

---

## 1. Open it, do these three steps

| Step | Action | How | What happens if you skip it |
|---|---|---|---|
| 1 | **See the shape first** (30 seconds, no network, no billing) | `bash scripts/fixtures/run_fixtures.sh` - three tiers in one run: checker self-test, skeleton without a channel, and the skeleton failing on purpose. Last line reports 档数=3｜合期望=3｜不合=0｜不可判=0 | Neatly formatted is not the same as sourced; this tier shows the difference in half a minute |
| 2 | **Register sources, attach one per finding** | One source per line in section four: `- [S#] title (URL ｜ retrieval date YYYY-MM-DD)`; every finding line in section two ends with one `[S#]`. If two sources disagree, keep both lines - no merging, no averaging | A source line without a retrieval date fires `E-ANCHOR`; a finding without an anchor fires `E-ANCHOR` too, and fixing it afterwards costs more than attaching it now |
| 3 | **Pass the check, then hand it to a human** | `python3 -B scripts/check_brief.py <brief.md>`, fix what each `E-*` line names; the result is still a **draft** - whether and how to conclude is yours | Unnamed gaps, leaked verdict words and unmatchable anchors all travel with the draft into a decision; those three are format-level, the substance still needs the original text |

Decision documents, ratings, target prices and market-timing analysis are **not in these three steps** - this package is accountable only for laying out this set of sources faithfully, and only at the format level.

## 2. Install → connect the channel → produce

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill cn-research-brief` - this line installs this package only; afterwards re-list installed skills on your side and the name `cn-research-brief` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this directory into your host's supported skills location (`~/.workbuddy/skills/`).

The evidence legs here are two optional auxiliaries: `cue-research` (deep research, cross-source verification) and `cue-omni-reader` (parsing PDFs, pages and recordings into quotable text). The channel route:

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

`CATALOG` is the only catalog literal on this face (assigned once, not restated in prose); `$ROUTING_URL` is taken verbatim from that domain's `routing.url`. The three layers prove different things and are never equivalent: **skill installed != credential configured != channel connected**. The anonymous `GET` proves **catalog reachability** only - this face does not call that "connected"; the key is proven *accepted* once a `tools/list` reply comes back with it attached, pass = HTTP 200 with a non-empty `result.tools` (shape only; no tool names or counts are promised). The parsing leg is the MCP connection in your host: the same `tools/list` handshake - once connected, that reply should show these names: a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total), so one fixed count cannot judge both routes. Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this package neither self-certifies nor runs either for you. Domains absent from the catalog are neither installed nor promised here, and a connection error does not mean the domain has no data. The key comes from your local credential facility - never into chat, never echoed back; this block adds no new credential read. Parsing and deep-research spend follows the server reply; this package neither estimates nor pays it, and always asks before anything is spent. Configuration pointers: the data-leg page <https://cuecue.cn/hub/mcp> and the parsing-leg page <https://cuecue.cn/hub/omni-reader> (this package uses the data leg for catalog discovery and the parsing leg for remote body text; the deep-research skill `cue-research` is its own runner and ships its own script, and its credential is the same key); to obtain a key go to <https://cuecue.cn/hub/api-key>.

## 3. Offline sample: see the shape in 30 seconds

```bash
cd cn-research-brief
bash scripts/fixtures/run_fixtures.sh
# tier 1  checker self-test: the good sample passes, the four bad samples each fire their own lane
# tier 2  skeleton without a channel: scripts/make_outline.py lays sources.jsonl out as a fill-in skeleton
# tier 3  the skeleton through the checker: E-FORMAT is expected - the conclusion slot stays a placeholder on purpose
```

On your own material it is the same two commands:

```bash
python3 -B scripts/make_outline.py --sources your-sources.jsonl --out my-skeleton.md
python3 -B scripts/check_brief.py my-skeleton.md
```

Each source line needs three keys - `title`, `url`, `asof` (retrieval date, `YYYY-MM-DD`); `id` is optional and defaults to `S1`, `S2`... in line order. Lines that are not valid JSON, that miss a key, or whose date is not `YYYY-MM-DD` are **rejected and named line by line**, never skipped silently; if nothing is usable the script exits 1 - an empty list is not a skeleton, it is the absence of sources.

## 4. Dependencies and what each path costs

- `python3`: used by the checker and the skeleton generator; standard library only, no network, sends no requests.
- The two channel auxiliaries (`cue-research` / `cue-omni-reader`) are optional: without them nothing errors, but the cost is stated in the same sentence - **what you lose is the cross-source evidence layer**, so this package can only lay your existing sources out as a shaped skeleton with the conclusion slot left empty (the gap is evidence density, not formatting). Whether or not they are installed, the package asks before spending anything.
- A connected channel is not the same as data in hand: figures follow the actual reply; truncated or summary-only responses are named in section three rather than filled in from common sense.

## 5. The four lanes and self-checks

| Lane | Code | What it holds |
|---|---|---|
| 1 format | `E-FORMAT` | The four header declarations word for word; four sections present and ordered; the one-sentence conclusion must be a real sentence - a placeholder fires |
| 2 anchors | `E-ANCHOR` | Every finding ends with `[S#]`; that number exists in section four; every source line carries both a URL and a retrieval date |
| 3 verdict words | `E-BANWORD` | Ratings, target prices, buy/sell and trend claims are zero-hit unless tagged `[待人工]` on the same line; hedged numbers never stand in for figures |
| 4 gaps and counts | `E-COVERAGE` | Anything written as not-found must be named item by item in section three, matched by item **coreference**: annotations and punctuation are stripped first, then a literal match, one side fully containing the other (shorter side ≥ 4 characters), or a Chinese-character overlap ratio ≥ 0.6 counts as the same item — so the same gap phrased differently does not turn the card red. An item named in section three with no coreferential line in the body fires too (both directions; the bare words "not retrieved" somewhere in the section do not count as naming); an empty source section means there is no provenance at all |

```bash
python3 -B scripts/check_brief.py --help                              # four lanes, no network
python3 -B scripts/check_brief.py --selftest                           # good passes, four bad each fire
python3 -B scripts/check_brief.py scripts/fixtures/good-brief.md       # should PASS
python3 -B scripts/check_brief.py scripts/fixtures/bad-no-anchor.md    # should FAIL: finding without an anchor
python3 -B scripts/check_brief.py scripts/fixtures/bad-missing-section.md  # should FAIL: section three absent
python3 -B scripts/check_brief.py scripts/fixtures/bad-rating-word.md  # should FAIL: verdict word untagged
python3 -B scripts/check_brief.py scripts/fixtures/bad-unsourced.md    # should FAIL: not one source line
python3 -B scripts/check_brief.py scripts/fixtures/good-brief.md --quiet   # summary line only
```

**Take every count from the script's own report line** (`FAIL: ... (N items)` and the `扫过 N 行，发条 0 条` line under `PASS:`); this file does not restate them - a restated count becomes a second source of truth.

## 6. What is in the package

```
SKILL.md                     the contract: scope / inputs / four steps / four sections / channel and fallback / red lines (read first)
README.md / README.en.md     this file (Chinese authoritative / English companion)
CHANGELOG.md                 version history
scripts/check_brief.py       the four-lane machine check (stdlib; the full rule set lives in the script, this file only points)
scripts/make_outline.py      the no-channel skeleton generator (lays sources out; fills in no conclusions)
scripts/fixtures/            one good sample, four bad samples, a source sample, and the offline three-tier runner
```

## 7. FAQ and anti-patterns

| What you try to do | Accepted? | Because |
|---|---|---|
| "Turn these three reports into a bullet list" | yes | multi-source, one bullet one source is exactly the use |
| "Just summarise this one announcement" | no | one source is a retelling, not a cross-checked brief - the cheap-looking shortcut pretends a comparison happened |
| "Give me the conclusion first, sources later" | no | a conclusion that later sources cannot support is an invention; the checker fires `E-ANCHOR` / `E-FORMAT` |
| "Add a target price while you are at it" | no | verdicts belong to humans; writing one fires `E-BANWORD` unless the same line carries `[待人工]` |
| "Even without the channel, just hand me a finished brief" | you get a skeleton | what is missing is the cross-source layer, not formatting; the skeleton failing the check is the reminder that this step was not done |
