# cue-lead-pieces

**More than a third of the "verbatim quotes" a filing-reading agent pastes do not match the source; with this skill, 95%+ trace back word for word to the source page, and the ones that don't are flagged or put back automatically.**

The agent thinks; Cue perceives. Uses **Cue Omni Reader** to parse a listed company's own filings (A-share annual, interim and ad-hoc reports from cninfo; US 10-K / 10-Q / 8-K from SEC EDGAR) into text with source PDF page numbers, turns them into **traceable lead pieces** (object · why now · suggested action · verbatim evidence with source and page), and checks every quote in an agent's answer against the source page. Optionally, **Cue data-MCP** lists filings and **cue-research** adds context to "why now".

**English companion of `README.md` (Chinese primary; repo-local reference — channel pages do not resolve relative links).** beta · Python standard library · No usage telemetry

**Comparison demo image (bare agent vs agent + this skill): lives in this package's assets directory in the repository (GitHub renders it); the channel package does not ship images, so the distributed files do not contain it — read the numbers' scope and limits under "Delivery and verification" below.**

The image is a measurement, not an illustration: the same agent, the same question, the same public filings, 24 listed companies. **These numbers were measured with the local parsing path; the Omni parsing path has not yet been measured at this scale** (Omni page alignment was measured on 2 A-share filings only, see below). Scope and limits are under "Delivery and verification" below. (The image text is Chinese.)

## What it solves

| Your problem | What this skill delivers |
|---|---|
| The agent's "quote" looks real, but it isn't on that page | `verify` checks every quote against the cited source and page (±1), with a verdict and the nearest real text |
| Wrong page, edited wording, table cells rewritten as a sentence | `verify --fix` corrects the page or swaps in the original sentence or table rows; the draft is kept |
| Words or numbers that are nowhere in the source | Marked as not in the source; `--fix` drops them and warns which signal lost its evidence |
| Finding credit-deterioration signals in hundreds of pages is slow | `brief` returns the source catalog, lead pieces and paste-ready verbatim evidence in one call |
| Quote pages must match the real page and tables must read as tables | Cue Omni Reader's `grounded` result carries the source PDF page of every segment; `ingest` stores text per page and keeps tables as tables |

## What each Cue channel does here

| Channel | Use in this skill | Not configured (no error, degraded) |
|---|---|---|
| `cue-omni-reader` (primary parser) | Parses every filing; `detail="grounded"` gives source PDF pages, `cue.py ingest` stores text per page | `cue.py local` local fallback parser (PyMuPDF / pdftotext / EDGAR page breaks), labeled `local` in the catalog |
| `cue-data-mcp` (optional) | `disclosure_cn` / `disclosure` domains list filings and announcement ids to check and complete the list | `cue.py fetch` lists filings from the public cninfo / SEC EDGAR index (zero credit) |
| `cue-research` (optional, at most once) | Adds industry, peer or event context to "why now", in the explanation only, never as quote evidence | Not launched; the explanation relies on the filings only |

Omni parsing and cue-research consume credits: before launching, the agent tells you how many files and which kinds, and waits for your consent; it relays only the billing facts the service returns and never estimates rates. You may send only annual / interim reports through Omni and announcements through the local fallback.

## First-time Cue setup (three steps, optional)

Register at <https://cuecue.cn> (new accounts get 500 credits at signup and 10 credits daily — server policy governs) → get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> into your local credential facility (**never paste it into chat**) → install the three skills this package uses: `cue-omni-reader` is the parsing leg, add `cue-data-mcp` to list filings, add `cue-research` (at most once, optional) for "why now" background. All three ship in Cue's official skill collection (sensedeal); one command, two forms - whole set `npx skills add sensedeal/cue-skills` (it lists the skills published in that collection; pick what to install), or one at a time `npx skills add sensedeal/cue-skills --skill cue-omni-reader` (swap the last name for `cue-data-mcp` or `cue-research` to install just that one). Configuration pointers, no restated steps: the primary parser `cue-omni-reader` has its page at <https://cuecue.cn/hub/omni-reader>; `cue-data-mcp` has its data-leg page at <https://cuecue.cn/hub/mcp>; the deep-research skill `cue-research` is its own runner (it ships its own script); this package does not route it through the data-leg page; its credential is the same key - get one at <https://cuecue.cn/hub/api-key>. What each one does and which fallback runs when it is not opened are the three rows of the table above.

   Afterwards check three separate things, because they are not the same fact: **skill installed ≠ credentials configured ≠ channel connected**.
   - installed: list your installed skills again and the names from the command above show up (this only proves the files landed, not that data flows);
   - credentials configured: the `CUE_API_KEY` from the previous step exists in your local credential facility - never paste its value into chat and do not echo it in a terminal;
   - connected: connect to the target domain with that key following the `url` inside its own `routing` (`Authorization: Bearer <$CUE_API_KEY>`, plus `Accept: application/json, text/event-stream` - missing that header gives a 406, protocol behaviour, not an authentication failure; the key from the layer above merely being present says nothing about whether it is accepted - that becomes judgeable only here) **and** `tools/list` returns. How to ask: send a JSON-RPC `tools/list` request to the address that domain's `routing` gives you. What counts as passing: HTTP 200 and a non-empty `result.tools` in the body (verbatim shape `{"result":{"tools":[...]}}`, tool names and input schemas inside it) - **the tool list follows that response's current values; this package promises no specific set of tools and hardcodes no tool names**. An anonymous `GET` of the `CATALOG` defined in the block returning on the spot proves only that the **catalog is reachable** - this package does not call that "connected": it yields each domain's `external_status` and the live domains' `routing`, and a domain missing from it stays uninstalled and unpromised here. A connection error is not "the domain has no data": report it as-is and retry only what the error marks as retryable.

   ```bash
   CATALOG="https://cuecue.cn/api/mcp-catalog"
   curl -s "$CATALOG" | python3 -c 'import json,sys
   rows=json.load(sys.stdin)["data"]["domains"]
   [print(r.get("id"), r.get("external_status"), (r.get("routing") or {}).get("url", "-")) for r in rows]'
   DOMAIN_ID="<replace with one of the ids listed by the line above>"
   ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
   rows=json.load(sys.stdin)["data"]["domains"]
   hit=[r["routing"]["url"] for r in rows if r.get("id")==sys.argv[1] and r.get("routing")]
   print(*hit,sep="\n") if hit else sys.exit("Not found: that id is not in the catalog response (or its routing has no url field) - run the line above and pick one of the ids listed")' "$DOMAIN_ID")"
   [ -n "$ROUTING_URL" ] || { echo "Fetch failed: ROUTING_URL is empty - run the line above, then set DOMAIN_ID to one of the ids listed" >&2; exit 1; }
   curl -s -X POST "$ROUTING_URL" \
     -H "Authorization: Bearer $CUE_API_KEY" \
     -H "Accept: application/json, text/event-stream" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
     -w '\nHTTP %{http_code}\n'
   ```

   The routing placeholder in this block is filled by the two lines above, fetched live from the anonymous catalog response - the verbatim url field inside that domain's routing object; CATALOG in the block is the only catalog-entry literal on this face (assigned once, not restated in prose). This face hardcodes no domain or path; the credential variable comes from the local key established in the layer above (never into chat, never echoed in a terminal), and this block adds no new credential-reading step. The pass verdict stays exactly as written there; this block does not set up a second one.
   One precision note about the live reply: this endpoint may answer in SSE form (an event line followed by a data line), and the result.tools to look for lives inside that data payload - the verdict is unchanged, the body is just wrapped one layer deeper.
   One-command form (no need to edit the line inside the block): `cd cue-lead-pieces && python3 -B scripts/cue_connectivity_check.py --domain <your domain id> --post`. This shipped script sends nothing by default - without --post it only fetches the url inside that domain routing and shows it to you. To see which ids exist, run the same script with `--list` first (it lists domains and urls, no POST). This script sets up no second criterion, 4 means connectivity is not proven yet (rerun with --post), 5 means it connected but the live values did not satisfy it, 1 means nothing could be fetched, nothing could be sent, or the HTTP layer itself reported an error (4xx and 5xx included), 6 means the destination failed the two credential-egress gates - nothing was sent and not one credential byte was attached, 7 means the catalog entry itself was not https. On the default catalog entry this script only checks runtime-endpoint connectivity - it publishes nothing to any channel and creates no acceptance record. **A swapped source is not exempt from the check**: whether that url came from the default catalog, from --catalog-url or from the --catalog-file snapshot, the request carrying the key must first pass the same two gates - the scheme must be https, and the host must match an authorized suffix (the default one is derived from the catalog entry in this script header, not a list invented here; pass --allow-host to authorize another). If it does not pass, the script refuses and prints the reason together with that host, and it neither reads the key nor builds the request. The cost is stated in the same breath: the old "whatever the swapped source hands over gets dialled" behaviour is closed off, and what you get in exchange is credentials that never leave toward an unauthorised destination - if your legitimate endpoint sits outside the suffix, exit 6 is the script asking you to confirm it with --allow-host, not a claim that endpoint should not exist.

It also runs without Cue: `cue.py local` reads the same public filings with local parsing and the checking rules are identical — the measured numbers above were produced this way; but pages come from local extraction, tables may break into loose lines, and you do not see what Cue-channel evidence looks like.

## First try

After installing, tell your agent:

> Use cue-lead-pieces: what are the 5 most important credit-deterioration signals for Leslie's (LESL) right now? Give verbatim source text and page for each, and verify the quotes before answering.

The agent lists the filings, tells you how many it would parse with Omni and waits for consent, then parses, builds lead pieces, writes the answer and verifies it.

Or run it in the skill directory (Python 3.9+):

```sh
export CUE_SEC_UA="Your Name your@email"
python3 scripts/cue.py fetch /tmp/lesl --us LESL --months 12   # list only, no download, zero credit
python3 scripts/cue.py fetch /tmp/600606 --cn 600606 --months 12
# primary (billed): without --yes it only prints the plan; after consent, --yes parses each file grounded, ingests it and prints credits_charged
python3 scripts/cue.py omni /tmp/600606
python3 scripts/cue.py omni /tmp/600606 --yes
# US EDGAR (Omni cannot fetch EDGAR URLs today) or no Omni: local fallback
python3 scripts/cue.py local /tmp/lesl
python3 scripts/cue.py brief /tmp/600606
```

## Install

```sh
npx skills add huhoo/cue-awesome --skill cue-lead-pieces
```

This route requires Node.js/npm; copying this directory into your host's supported skills location also works (Claude Code: `~/.claude/skills/cue-lead-pieces`). This skill is not in the repository's v2026.09.27 release ZIPs.

## Requirements

- Python 3.9+ (standard library only).
- Primary parser: the official `cue-omni-reader`, installed and configured. The agent can call it over MCP itself; `cue.py omni`, and `ingest` when it reads a large result back, start the Omni Bridge (the command in `CUE_OMNI_BRIDGE`, default `npx -y @cueai/omni-reader-mcp@1.8.6`, needs Node.js). The Bridge reads the key itself; this script never reads or passes `CUE_API_KEY`.
- The local fallback needs PyMuPDF (`pip install pymupdf`) **or** the `pdftotext` command (poppler) for A-share PDFs; US EDGAR HTML does not.
- Filing lists come from the public cninfo and SEC EDGAR indexes, free. `fetch` only lists, `local` downloads files; `leads` / `brief` call a model endpoint only if the optional model variables below are set; everything else reads local files only.
- SEC EDGAR asks clients to identify themselves: set `CUE_SEC_UA="Your Name your@email"` (without it a placeholder contact is sent and SEC may refuse or throttle).
- Optional: set `CUE_LLM_BASE_URL`, `CUE_LLM_API_KEY`, `CUE_LLM_MODEL` (any OpenAI-compatible endpoint) and `leads` uses that model to align changes across sources; otherwise a deterministic grouping is used. Keep keys in your own secret facility, not in chat or Issues.

## Commands

| Command | What it does |
|---|---|
| `cue.py fetch DIR --cn 600606` / `--us LESL` | list the last 12 months of public filings with download URLs (no download, zero credit) |
| `cue.py fetch DIR --list list.json --company X --market CN` | register filings found elsewhere (e.g. Cue data-MCP) |
| `cue.py omni DIR [sources…] [--yes]` | grounded parse through the Omni Bridge, then ingest (billed; without `--yes` it only prints the plan); skips SEC EDGAR sources by default |
| `cue.py ingest DIR --omni-dir DIR/omni` | read Omni results saved by the agent (`<sid>.json` = the JSON returned when parse completes; a part judged `artifact` is read back hop by hop along its cursor, measured with no further charge - billing taken as returned; `<sid>.md` = plain text, stored as text blocks) |
| `cue.py local DIR [sources…]` | local fallback: download and extract text per page; `fetch … --local` does both in one step |
| `cue.py brief DIR` | one call: source catalog (with parser) + lead pieces + paste-ready verbatim evidence |
| `cue.py find DIR <terms…>` | sentences containing the terms, paste-ready |
| `cue.py page DIR <source> <pages> …` | read pages, e.g. `AR2025 54,196-198`, several sources at once |
| `cue.py verify DIR --json answer.json [--fix]` | check every quote; `--fix` corrects pages, swaps edited quotes for the original sentence, drops quotes not in the source |
| `cue.py verify DIR --quote "…" --source S --page N` | check one quote |

The recommended agent flow is in `SKILL.md`.

**What the output looks like**: `scripts/fixtures/good_lead_pack_sample.md` is the verbatim stdout of the `cue.py brief` command, run against this package's own synthetic fixture (`scripts/fixtures/omni_real_shape.json` - synthetic entity, fake ids), not one line edited. Its reproduction chain lands the lead cache first with `leads --no-llm` and then reads it, so no request goes out even when `CUE_LLM_BASE_URL`, `CUE_LLM_API_KEY` and `CUE_LLM_MODEL` are all set; the sample header spells out that condition and what happens without it.

## Delivery and verification

The measurement record is `references/verification.md` in this package; versions are in `CHANGELOG.md`. In short:

- Same agent (Claude Code), same question ("As a credit officer, what are the 5 most important credit-deterioration signals for this company right now? Each must have verbatim source evidence and page."), same public filings, 24 listed companies (12 A-share, 12 US, including 4 healthy controls), one run per company per arm. **All with the local parsing path.**
- Bare agent: 61% of 421 quotes found word for word on the cited page; 39% did not match (95% interval by company bootstrap 33%–46%).
- With this skill's flow: 95% of 443 quotes verbatim (95% interval 91%–98%). These figures were measured with the version before 0.3.0.
- 0.3.0 re-tested on the 14 previously slowest companies: 100% of 279 final quotes verbatim; the agent's draft before `verify --fix` was 98% (273/278); one 60-minute timeout versus four for the old version run at the same time.
- Numbers that appear nowhere in the source: 0 in both arms.
- 0.4.0 Omni path, measured (2026-10-07, two cninfo PDFs of Greenland Holdings 600606, grounded): a 3-page announcement and the 391-page 2025 annual report. Omni page count equals the PDF page count, and every page's text lands on the same PDF page number (3/3, 391/391); 99.9% of the numbers from local parsing appear on the same Omni page. Server-reported charges: 0.201 and 26.197 credits. In a mini run (brief, 8 quotes, verify, verify --fix) every quote kept was found on the same source PDF page (±1). The US 8-K could not be parsed through Omni (EDGAR URL `SOURCE_ACCESS_DENIED`, not billed). The 24-company rates above are still from local parsing; the Omni path has not been re-measured at that scale.

What this shows is whether quotes can be found word for word in the source. It does not show that the signals are right, and other models or hosts may give different numbers.

Self-check (offline):

```sh
python3 scripts/test_skill_regression.py
python3 scripts/cue.py --help
```

Two runs are byte-comparable: this self-check emits no elapsed-time line and no temporary paths - every file opened by the regression sample and by cue.py is closed immediately - the entry checks handles two ways: file objects still referenced and open after the run (these never get destructed and never emit ResourceWarning) plus warnings surfaced at destruction time; either non-zero flips the exit code, because no-warning alone does not mean no live handle, and the summary line reads only "Ran 12 tests" plus "OK/FAILED". Test count and verdicts are unchanged; only the conclusion is compared. The entry discriminates handle leaks itself too (the C1 family): after the suite it forces one collection pass, and any unclosed handle is named by count with a non-zero exit - the check lives inside the entry, not in an outer `-W` (which only turns the warning into "Exception ignored" and still exits 0), and not in a plain-run grep count (that branch is tautological: it reports 0 whether or not a handle leaks).

## FAQ and anti-patterns (you want to → this skill does not, because → go here instead)

- Decide whether the company will default → not this skill; it only guarantees quotes come from the source, not that signals are right → you or your credit model decide; this skill supplies checkable evidence.
- Check claims from research notes, news or third-party databases → not this skill; it reads the company's own filings only → find the underlying announcement or 10-K text first.
- Cover Hong Kong, bond prospectuses or private companies → not yet; `fetch` only lists cninfo and SEC EDGAR → you can parse other public files with Omni and register them with `ingest --sid … --kind … --date … --title …`, but that route is untested.
- Turn several filings into an updatable knowledge package that tracks cross-period changes and basis conflicts → not this skill; it verifies quotes and writes lead pieces → [cue-omni-ontology](../cue-omni-ontology/README.en.md) in this repository (a repository-relative path that does not ship inside the published artifact): updatable knowledge packages, change briefs and a numeric pack, with the same verbatim evidence.
- Treat `--fix` output as final → not recommended; the swapped-in sentence is the nearest original text chosen by the program, not reviewed by a person for whether it still supports the claim → for key conclusions, look at the page (`page` command).

## When something goes wrong (symptom → cause → recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write "not found" and log it on the pending or coverage list; a blank never stands in for it.
- Omni returns `OMNI_NOT_ENTITLED` / 403, credits run out, or you decline the spend → account not entitled or spend not approved → follow the official cue-omni-reader guidance; to avoid spending, run `cue.py local DIR` for the local fallback, and the answer says so.
- Omni returns `UNSUPPORTED_DETAIL` / `DETAIL_CAPABILITIES_UNAVAILABLE` → no grounded result with pages for this file → save the default text result as `<sid>.md` and `ingest` it; pages are then labeled as text-block numbers; for real pages use `cue.py local` for that file.
- `ingest` prints `warning: incomplete page [...]` or `truncated` → Omni did not finish some pages → quotes on those pages cannot be verified; ask the user before re-parsing (it may be billed again), or use `cue.py local` for that file.
- Omni returns `SOURCE_ACCESS_DENIED` for an SEC EDGAR URL (measured, not billed) → Omni cannot fetch EDGAR today → run `cue.py local DIR` for US filings; `omni` already skips EDGAR sources by default.
- `ingest` reports `read_result(...) failed: INVALID_RESULT_CURSOR` → the cursor is bound to its part and offset (measured: changing either is refused with `retryable:false`, `billed:false`) → follow the cursor this part was issued in the completion receipt, never a hand-made one; if the result is reported expired (past `expires_at`) → ask the user before re-parsing (billed again), or use `cue.py local` for that file.
- `ingest` reports `content does not match its sha256 digest` → the content read back is incomplete → nothing was ingested; re-run `ingest` (zero credit), else use `cue.py local`.
- `ingest` prints `page_basis=block` / `text-only result` → you saved Markdown (`save_result` export or the tool's text), which has no page sidecar (measured: under both delivery shapes `save_result` hands over the content file only, never the sidecar) → save the JSON returned when parse completes (while the sidecar is inline its page numbers live in `structuredContent`, so store that text in full on the spot; only a part judged `artifact` is read back by cursor), or just use `cue.py omni`.
- `cannot start the Omni Bridge` → Node.js missing or `CUE_OMNI_BRIDGE` wrong → install Node.js, or set `CUE_OMNI_BRIDGE` to your omni-reader launch command.
- `fetch` reports a network error or SEC returns 403 → no network, or no identification → check the network, set `CUE_SEC_UA`, retry.
- A-share `local` cannot find `pdftotext` → neither PyMuPDF nor poppler installed → `pip install pymupdf` or install poppler.
- `fetch` prints one line, `cue.py: error: unknown A-share code '999999': not in the cninfo stock list ...` (for US: `unknown US ticker '...'` or `unknown CIK '...'`), exit code 2 → the ticker/code was not found (wrong code or unsupported market) → use the 6-digit code for A-shares, the ticker or CIK for US.
- `brief` output too long and saved to a file by the host → some companies have a lot of material → let the agent read that file, or lower `--top`.
- `verify --fix` warns a signal has no checkable source evidence left → none of that signal's quotes are in the source → add one source sentence with `find`, or drop the signal.

## How to ask (three positive examples, one negative)

**Ask with a point in time; the output states its source date**: give the reporting period, reference date or look-back window in the request; the deliverable labels its **source date** on the first line, and when that differs from the date you asked about, the text never says "today" or "latest" - it reads "as of <date>".
- Positive: "Use cue-lead-pieces to find credit-deterioration signals in 600606's filings over the last year, with page numbers; parse the annual reports with Omni, announcements locally is fine."
- Positive: "Check sentence by sentence whether the quotes in this answer are really in the source." (with answer.json and the data directory)
- Positive: "Check the latest 10-Q of QVCG for going-concern and covenant language, with page numbers."
- Negative: "Predict whether this stock goes up next month." (out of scope)

## Boundaries and license

Uses only the company's public filings; not investment or credit advice. Lead pieces and verification output contain limited source excerpts; check the source's terms before sharing. Code and docs are MIT; the license text sits in this package's directory in the source repository, and the channel artifact does not carry it (the distribution exclusion list drops it along with the demo images). The Chinese README is authoritative; agent instructions follow `SKILL.md` (Chinese primary), and `SKILL.en.md` is its synchronized translation.
