# cn-customer-concentration

**For one company, produce a six-section customer-concentration ledger: period-level totals, per-customer shares, related-party and dependency facts, every data row carrying both its period and its basis and anchored to a `[S#]`; a customer the disclosure did not name is not named by the ledger; every gap is written out as "not retrieved".**

Bullet points are not scarce; **what is scarce is a "how much of this company's revenue comes from how many customers" line you can trace back to one source that carries a period, a basis and a retrieval date**. The difference is not layout but three hard gates: a share without a period never enters a data row, an anonymous customer that gets named fires red, and per-customer shares summing above the period total fires red.

**Input**: one company (name or ticker) plus a batch of disclosure material (annual reports / prospectuses / enquiry replies / announcements) - or a question to be broken down
**Output**: a six-section ledger (one-line concentration summary / period totals / per-customer detail / related-party and dependency facts / gaps and definitions / sources)
**Cost**: a six-section contract plus one machine check; whether the channel legs (announcement search / text parsing) are switched on decides the "per-customer share" layer - what each path lacks and which to take is written in sections 2 and 4
**Machine check**: `scripts/check_concentration.py`, five lanes (format / anchors / red lines / two-way gap naming / scope boundary), zero network; the counter-evidence matrix lives inside that script

**This is not the same thing as `prospectus-digest-cn` or `cn-supply-chain-map` (this sentence is why the package exists)**: `prospectus-digest-cn` reads **one prospectus** and digests eight items verbatim into a quick card, with customer and supplier concentration being just one of them; this package produces a **cross-period customer-dependency ledger** - multiple periods, multiple disclosures, how the shares move, which customers enter and leave the top five. `cn-supply-chain-map` draws the **chain structure** (who sits in which link, and the upstream/downstream relations); this one asks **which customers the revenue comes from, and in what proportion**. This package **does not judge customer quality and does not judge the size of the risk**. The `集中度口径：` header line is the machine-checkable entry to that boundary - writing "prospectus" or "supply chain" gets you named and sent to the corresponding package.

---

## 1. Open it, do these three steps

| Step | Action | How | What happens if you skip it |
|---|---|---|---|
| 1 | **See the shape first** (30 seconds, no network, no billing) | `bash scripts/fixtures/run_fixtures.sh` - five tiers in one run: checker self-test, good and bad samples one by one, skeleton without a channel, the skeleton failing on purpose, boundary forms one by one. Last line reports 档数=5｜不合=0｜不可判=0 | Neatly formatted is not the same as sourced; this tier shows the difference in half a minute |
| 2 | **Register sources, attach one per row** | One source per line in section 6: `- [S#] title (URL ｜ retrieval date YYYY-MM-DD)`; every total row and every customer row ends with one `[S#]`. If two sources disagree, keep both lines - no merging, no averaging | A source line without a retrieval date fires `E-ANCHOR`; a data row without an anchor fires `E-ANCHOR` too, and fixing it afterwards costs more than attaching it now |
| 3 | **Pass the check, then hand it to a human** | `python3 -B scripts/check_concentration.py <ledger.md>`, fix what each `E-*` line names; the result is still a **draft** - what this concentration means, and how good the customers are, is yours | Unnamed gaps, leaked judgement words and anonymous customers named on its behalf all travel with the ledger into a human's judgement; those are format-level, the substance still needs the original text |

Judging customer quality and the size of the risk, ratings and target prices, buy/sell and timing advice are **not in these three steps** - this package is accountable only for laying this company's customer dependency out faithfully as a cross-period ledger, and only at the format level.

## 2. Install → connect the channel → produce

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill cn-customer-concentration` - this line installs this package only; afterwards re-list installed skills on your side and the name `cn-customer-concentration` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this directory into your host's supported skills location (`~/.workbuddy/skills/`).

The evidence legs here are two optional auxiliaries: `cue-data-mcp` (locating announcements and annual reports, the data leg) and `cue-omni-reader` (turning PDFs and pages into quotable text, the parsing leg). The channel route:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
[print(r.get("id"), r.get("external_status"), (r.get("routing") or {}).get("url", "-")) for r in rows]'
DOMAIN_ID="<replace with one of the domain ids listed above>"
ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
hit=[r["routing"]["url"] for r in rows if r.get("id")==sys.argv[1] and r.get("routing")]
print(*hit,sep="\n") if hit else sys.exit("not retrieved: that id is not in the live catalog")' "$DOMAIN_ID")"
[ -n "$ROUTING_URL" ] || { echo "failed: ROUTING_URL is empty" >&2; exit 1; }
curl -s -X POST "$ROUTING_URL" \
  -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  -w '\nHTTP %{http_code}\n'
```

`CATALOG` is the only literal catalog entry on this face (assigned once, never re-copied into prose); `$ROUTING_URL` is taken live from the domain's `routing.url` field - do not hardcode a hostname or path here. What each layer proves is not equivalent: **skill installed ≠ credentials configured ≠ channel connected**. An anonymous `GET` proves only that the catalog is reachable; a keyed call whose `tools/list` returns proves that key is accepted, passing meaning HTTP 200 with a non-empty `result.tools` (recognised by shape only - no tool names listed, no counts promised). The parsing leg goes through the host MCP: once connected, the tools listed by the host should include `parse`, `get_parse_status` and `read_result` - their presence proves only that they are exposed, not that parsing works. A domain absent from the catalog response is neither installed nor promised here; a connection error does not mean the domain has no data, report it as it is. The key comes from local credential infrastructure, never into chat and never echoed in the terminal. Consumption is whatever the server returns; ask before spending.

## 3. Offline sample: see the shape in 30 seconds

```bash
cd cn-customer-concentration
bash scripts/fixtures/run_fixtures.sh
# tier 1  checker self-test: the good sample passes, the seven bad samples each fire their own lane
# tier 2  good and seven bad samples one by one: each reports its own exit code and code set, never merged into one total
# tier 3  skeleton without a channel: scripts/make_outline.py lays sources.jsonl out as a fill-in skeleton
# tier 4  the skeleton through the checker: E-FORMAT is expected - the concentration summary stays a placeholder on purpose
# tier 5  boundary forms one by one: scope written as prospectus names the sibling package / scope written as supply chain names the other one /
#         an unrecognised scope value is a format red / a judgement word is red / a factual statement is not red /
#         a hedging word is red / an anonymous customer named is red / a share above the total is red
```

The same two commands when you start on your own:

```bash
python3 -B scripts/make_outline.py --sources your-sources.jsonl --out my-skeleton.md
python3 -B scripts/check_concentration.py my-skeleton.md
```

Source rows need three keys: `title` / `url` / `asof` (retrieval date `YYYY-MM-DD`); `id` is optional and defaults to `S1`, `S2`... in row order. Malformed JSON lines, lines missing a key, and lines whose date is not `YYYY-MM-DD` are **not accepted and are named one by one** - never silently skipped. With no usable row at all it exits 1: an empty list does not produce a skeleton, that is "no source", not "to be filled".

## 4. Dependencies and what each path costs

**Primary route (channel available)**: annual reports and prospectuses are located through the data leg, and the body text of long attachments and multi-page PDFs comes back through the parsing leg. With both legs on, this package can deliver the layer where "every share traces back to one source carrying a period, a basis and a retrieval date"; lose a leg and you lose that layer - without the data leg the disclosures must be supplied by you, and without the parsing leg the original sentence inside an attachment stops at "not retrieved".

**Degraded (no channel)**: `scripts/make_outline.py` lays an existing source list out as a fill-in skeleton. **The cost is stated in the same sentence**: what is missing is exactly the announcement-search and text-parsing layer, so the skeleton has only a shape and no reconciled concentration facts - section 2 keeps one total placeholder row, section 3 one per-customer placeholder row, section 4 one dependency-fact placeholder row, the concentration summary stays a placeholder, and the checker fires `E-FORMAT` by design. A skeleton is not a ledger; do not deliver it as one.

## 5. Boundaries and non-promises

- No judging customer quality and no judging the size of the risk: judgements such as risk controllable / severely dependent / high-quality customer / moat all go to `[待人工]`; ratings, target prices, buy/sell and timing advice likewise;
- **Judgement word family, zero hits**: risk controllable / risk not large / risk small / risk very low / risk very high / risk extremely large / severely dependent / excessively dependent / highly dependent / high-quality customer / benchmark customer / large-customer endorsement / high customer quality / deeply bound / bound to a leader / moat / strong stickiness / full order book / earnings certainty; hedging words (about / around / roughly) must not stand in for a number;
- **Narrowing (written in so nobody widens it later)**: a bare "dependent" is not caught - "the company is somewhat dependent on its top five customers" is a factual statement from the annual report and is recorded as usual; only "severely / excessively / highly dependent" are caught. A bare "concentration" is not caught; only verdict forms such as "risk controllable" are;
- Reading a single prospectus and digesting eight items goes to `prospectus-digest-cn`; drawing the upstream/downstream chain goes to `cn-supply-chain-map`;
- **An anonymous customer must not be named**: where the disclosure writes "Customer 1" or "the Nth customer", the bracketed note may only be of the "unnamed / anonymous / undisclosed / not named" kind; a company name inside the bracket fires red - if the disclosure did not name it, the ledger cannot name it on its behalf;
- Not retrieved means writing "not retrieved" as it is; filling in from industry convention is forbidden, and so is writing "no such item" as a substitute;
- Do not use this package for a single-source case - that is a paraphrase; its use is reconciling multiple periods and multiple sources;
- Domain and tool names follow the live catalog; this package lists no fixed set, promises no count, and promises nothing about whether a domain is open or how real-time a file is.

## 6. When something goes wrong

| Symptom | Where it comes from | Recovery |
|---|---|---|
| Several rows say "not retrieved" | The material has only disclosure titles; the body is in an attachment | Bring up the parsing leg for the original sentence; if it will not come up, keep the gap named - do not fill it in |
| The data leg will not connect | Missing credentials, or the domain is not live | Self-check per section 2; the skeleton still renders, at the cost stated in section 4 |
| `E-ANCHOR` fires | A data row has no anchor, or the anchor has no matching row in section 6, or a source row lacks a URL / retrieval date | Fill in by the line numbers named; whatever cannot be filled goes into the section-5 gap list - do not delete rows to make the count work |
| `E-COVERAGE` fires | The body says "not retrieved" but section 5 does not list it, or section 5 lists it and the body has no such statement | Both directions must match; a rephrasing of the same thing is not red (the check matches by coreference), only a genuine omission is |
| `E-SCOPE` fires | The `集中度口径：` header was written as "prospectus" or "supply chain" | Go to the corresponding package, or narrow the question to "how many customers this company's revenue depends on, and in what proportion" |
| `E-BANWORD` fires | A rating / target price / buy-sell call was written, or a judgement word such as "risk controllable" or "high-quality customer", or a hedging word standing in for a number | Rewrite as a neutral statement, or tag the same line `[待人工]`; values are copied from the source, and a mismatched basis goes into section 5 |
| `E-FORMAT` fires (shape) | A data row lacks a period or a basis, an anonymous customer's bracket holds a company name, or per-customer shares sum above the period total | Add the period and basis; put the anonymous customer back to "unnamed in the disclosure"; copy shares from the source, do not invent them |
| A factual line is wrongly red | The line reads "somewhat dependent", a factual statement | The check matches by word family (only "severely / excessively / highly" qualify); a bare "dependent" is not red; if it still fires, look for another judgement phrase on the same line |

## 7. How to ask (good and bad)

- Good: "how many customers does this company's revenue depend on, and in what proportion", "how has the top-five total share moved over the past few years", "who is the largest customer, and is it a related party", "what changed in the customer structure between 2023 and 2024".
- Bad: "is the customer-concentration risk large", "is this company worth buying", "what is the target price", "are its customers good" - judging customer quality and risk size is not in this package and goes to `[待人工]`; reading a single prospectus goes to `prospectus-digest-cn`, drawing the supply chain goes to `cn-supply-chain-map`.

## 8. Capability boundaries (honest list)

This package does not judge customer quality or the size of the risk (that is a judgement slot, `[待人工]`); it does no valuation modelling or financial forecasting; it does not name anonymous customers on the disclosure's behalf, and does not fill gaps from industry convention; it does not persist your files - the ledger is handed back to you when it is done. Availability and freshness of the disclosures themselves follow the live catalog; nothing is promised for a domain that is not open.

## 9. Resources

- `SKILL.md`: the six-section contract, the data-row shape and the red-line text (the Chinese face is authoritative)
- `README.en.md`: this English face; where the two conflict, the Chinese face wins
- `CHANGELOG.md`: version and changes
- `scripts/check_concentration.py`: five machine-check lanes (zero network)
- `scripts/make_outline.py`: zero-channel skeleton generator (fills in no conclusions)
- `scripts/fixtures/run_fixtures.sh`: offline five-tier runner (zero network, zero billing)
