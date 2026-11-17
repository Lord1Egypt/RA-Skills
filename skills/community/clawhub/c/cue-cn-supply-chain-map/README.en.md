# cn-supply-chain-map

**For an industry or a company, produce a six-section supply-chain map: upstream, midstream and downstream, each link naming a representative company and its position in the chain, every row anchored to one dated source, every gap named, nothing filled in from convention.**

Bullet points are not scarce; **what is scarce is a "who sits where in the chain" line you can trace back to one dated source**. The difference is not layout but two hard gates: a company without a position bracket never enters a link row, and a gap that was not named never passes the machine check.

**Input**: an industry or a company plus a batch of material (announcements / annual reports / industry material packs / news) - or a question to be broken down
**Output**: a six-section map (one-line chain summary / upstream / midstream / downstream / gaps and definitions / sources)
**Cost**: a six-section contract plus one machine check; whether the channel legs (announcement search / text parsing) are switched on decides the "representative company and its position" layer - what each path lacks and which to take is written in sections 2 and 4
**Machine check**: `scripts/check_chain.py`, five lanes (format / anchors / red lines / two-way gap naming / scope boundary), zero network; the counter-evidence matrix lives inside that script

**This is not the same thing as `sector-overview` (this sentence is why the package exists)**: that one does the **industry cycle panorama** - volume, price, capacity, structure and trend for an industry; this one does the **chain structure** - who sits in which link, and what the upstream/downstream relations are. This package **does not judge the cycle, does not judge good or bad, and does not pick stocks**. The `链条口径：` header line is the machine-checkable entry to that boundary - writing `景气` gets you named and sent to the other package.

---

## 1. Open it, do these three steps

| Step | Action | How | What happens if you skip it |
|---|---|---|---|
| 1 | **See the shape first** (30 seconds, no network, no billing) | `bash scripts/fixtures/run_fixtures.sh` - five tiers in one run: checker self-test, good and bad samples one by one, skeleton without a channel, the skeleton failing on purpose, boundary forms one by one. Last line reports 档数=5｜不合=0｜不可判=0 | Neatly formatted is not the same as sourced; this tier shows the difference in half a minute |
| 2 | **Register sources, attach one per row** | One source per line in section 6: `- [S#] title (URL ｜ retrieval date YYYY-MM-DD)`; every link row in the three layers ends with one `[S#]`. If two sources disagree, keep both lines - no merging, no averaging | A source line without a retrieval date fires `E-ANCHOR`; a link row without an anchor fires `E-ANCHOR` too, and fixing it afterwards costs more than attaching it now |
| 3 | **Pass the check, then hand it to a human** | `python3 -B scripts/check_chain.py <map.md>`, fix what each `E-*` line names; the result is still a **draft** - how to read this chain is yours | Unnamed gaps, leaked recommendation words and unmatchable anchors all travel with the map into a human's judgement; those three are format-level, the substance still needs the original text |

Ratings and target prices, buy/sell and timing advice, and industry-cycle calls are **not in these three steps** - this package is accountable only for laying this chain out faithfully as a structure map, and only at the format level.

## 2. Install → connect the channel → produce

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill cn-supply-chain-map` - this line installs this package only; afterwards re-list installed skills on your side and the name `cn-supply-chain-map` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this directory into your host's supported skills location (`~/.workbuddy/skills/`).

The evidence legs here are two optional auxiliaries: `cue-data-mcp` (locating announcements and annual reports, the data leg) and `cue-omni-reader` (turning PDFs and pages into quotable text, the parsing leg). The channel route:

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

`CATALOG` is the only catalog literal on this face (assigned once, not restated in prose); `$ROUTING_URL` is taken verbatim from that domain's `routing.url`. The three layers prove different things and are never equivalent: **skill installed != credential configured != channel connected**. The anonymous `GET` proves **catalog reachability** only - this face does not call that "connected"; the key is proven *accepted* once a `tools/list` reply comes back with it attached, pass = HTTP 200 with a non-empty `result.tools` (shape only; no tool names or counts are promised). The parsing leg is the MCP connection in your host: **once connected**, the tools your host lists should show these names - a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total), so one fixed count cannot judge both routes. Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the local-file route by one real local-file parse (remote-only cannot read local files); this package neither self-certifies nor runs either for you. Domains absent from the catalog are neither installed nor promised here, and a connection error does not mean the domain has no data. The key comes from your local credential facility - never into chat, never echoed back; this block adds no new credential read. Parsing and search spend follows the server reply; this package neither estimates nor pays it, and always asks before anything is spent. Configuration pointers: the data-leg page <https://cuecue.cn/hub/mcp> and the parsing-leg page <https://cuecue.cn/hub/omni-reader> (this package may use both - the data leg locates announcements and annual reports, the parsing leg retrieves body text from long attachments and PDFs); to obtain a key go to <https://cuecue.cn/hub/api-key>.

## 3. Offline sample: see the shape in 30 seconds

```bash
cd cn-supply-chain-map
bash scripts/fixtures/run_fixtures.sh
# tier 1  checker self-test: the good sample passes, the six bad samples each fire their own lane
# tier 2  good and six bad samples one by one: each reports its own exit code and code set, never merged into one total
# tier 3  skeleton without a channel: scripts/make_outline.py lays sources.jsonl out as a fill-in skeleton
# tier 4  the skeleton through the checker: E-FORMAT is expected - the chain summary stays a placeholder on purpose
# tier 5  boundary forms one by one: 景气 names the sibling package / an unrecognised scope value is a format red / a recommendation word is red / a factual "受益于" line is not red / a hedging word is red
```

On your own material it is the same two commands:

```bash
python3 -B scripts/make_outline.py --sources your-sources.jsonl --out my-skeleton.md
python3 -B scripts/check_chain.py my-skeleton.md
```

Each source line needs three keys - `title`, `url`, `asof` (retrieval date, `YYYY-MM-DD`); `id` is optional and defaults to `S1`, `S2`... in line order. Lines that are not valid JSON, that miss a key, or whose date is not `YYYY-MM-DD` are **rejected and named line by line**, never skipped silently; if nothing is usable the script exits 1 - an empty list is not a skeleton, it is the absence of sources.

## 4. Dependencies and what each path costs

**Primary route (channel on)**: the data leg locates announcements and annual reports, the parsing leg retrieves body text from long attachments and multi-page PDFs. With both legs on, this package can deliver the layer where every link's representative company and its position return to one dated original; whichever leg is missing is the layer that is missing - without the data leg, announcements and reports can only come from you directly; without the parsing leg, sentences inside attachments stop at "not retrieved".

**Fallback (zero channel)**: `scripts/make_outline.py` lays your existing material list out as a fill-in skeleton. **The cost is stated in the same sentence**: what is missing is exactly the announcement-search and text-parsing layer, so the skeleton has shape but no weighed chain structure - each of the three layers keeps one `代表公司：未取到` slot, the chain summary stays a placeholder, and the checker fires `E-FORMAT` by design. A skeleton is not a map; do not deliver it as one.

## 5. Boundaries and non-promises

- No cycle calls, no good/bad calls, no stock picking: industry volume, price and structure go to `sector-overview`; ratings, target prices, buy/sell and timing advice are always `[待人工]`;
- **Recommendation word family is zero-hit**: 受益标的 / 受益股 / 核心标的 / 弹性标的 / 首选标的 / 龙头 / 潜力股 / 值得关注 / 建议关注 / 重点推荐 / 推荐关注 / 布局良机 / 上车 - a supply-chain map is a factual "who sits where" picture, not a stock list;
- **The narrowing (written down so nobody widens it later)**: a bare `受益` is not caught - "受益于硅料降价" is a causal statement, not a recommendation; only the forms that make a company the recommended object (`受益标的` / `受益股`) are caught. A bare `关注` is not caught; only `值得关注` / `建议关注` / `推荐关注` are;
- Not retrieved means writing "not retrieved" as it is; never fill in from industry convention, and never write "no such item" in its place;
- Do not use this package for a single source - that is a retelling; multi-source cross-checking is what it is for;
- Domains and tool names follow the live catalog; this package lists no fixed set, promises no counts, and promises nothing about whether a domain is open or how fresh its files are.

## 6. When something goes wrong

| Symptom | Where it comes from | Recovery |
|---|---|---|
| Many lines say "not retrieved" | You only have announcement titles; the body is in an attachment | Turn on the parsing leg for the original sentences; if it will not start, keep the gap named and do not fill it in |
| The data leg will not connect | Credential missing or the domain is not live | Self-check per section 2; the skeleton still works, and the cost is the sentence in section 4 |
| `E-ANCHOR` fires | A link row has no anchor, or the anchor has no matching line in section 6, or a source line lacks a URL / retrieval date | Fill in by the line numbers named; anything you cannot fill goes into the section 5 gap list - do not delete lines to make it green |
| `E-COVERAGE` fires | The body says not-retrieved but section 5 does not list it, or section 5 lists it but the body has no such statement | Both directions must line up; the same gap phrased differently is not red (matched by item coreference), only a real miss is |
| `E-SCOPE` fires | The `链条口径：` header says `景气` | Switch to `sector-overview`, or narrow the question to "which links are on this chain and who is in each" |
| `E-BANWORD` fires | A rating / target price / buy-sell call, a recommendation word such as `龙头` or `受益标的`, or a hedging word standing in for a figure | Rewrite as a neutral statement or tag `[待人工]` on the same line; figures follow the source, and mismatched definitions go to section 5 |
| `E-FORMAT` fires (position) | A link row names a company but has no position bracket, or the bracket is empty | Fill in its position in the chain; if you cannot, change the row to `代表公司：未取到` and name it in section 5 |
| A factual line is flagged | The line is "受益于硅料降价" | The checker matches word families (only `受益标的` / `受益股` fire); a bare `受益` does not; if it still fires, check whether the same line carries another recommendation phrase |

## 7. How to ask (good and bad)

- Good: "what are the upstream links on this chain and who is in each", "where does this company sit in the chain and who are its suppliers and customers", "who supplies a module maker", "which segments does this chain pass through from raw material to end market".
- Bad: "how is the industry cycle", "is it worth buying", "what is the target price", "who is the leader" - cycle calls go to `sector-overview`; buy/sell and timing, target prices and stock picking are not here, they are `[待人工]`.

## 8. Capability boundaries (honest list)

Market-price and fund-flow figures are outside this package (that domain follows the live catalog; if it is not open, nothing is promised); this package does no valuation modelling or financial forecasting; it does not judge which link earns more or which company is stronger (that is a cycle and competitive-position question, which belongs to `sector-overview` or a single-company research package); and it does not persist your files - the map is handed back to you when it is done.

## 9. Resources

- `SKILL.md`: the six-section contract, the link-row shape and the red lines (the Chinese face is authoritative)
- `README.md`: the Chinese face; this file is its English companion, and the Chinese face wins on conflict
- `scripts/check_chain.py`: the five-lane machine check (zero network)
- `scripts/make_outline.py`: the no-channel skeleton generator (fills in no conclusions)
- `scripts/fixtures/run_fixtures.sh`: the offline five-tier runner (zero network, zero billing)
