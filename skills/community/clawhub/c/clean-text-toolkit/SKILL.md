---
name: clean-text-toolkit
description: Local text cleanup and inspection toolkit. Extract structured items (URLs, emails, phones, IPs, dates, hashtags, money), redact PII (email/phone/credit-card-with-Luhn/SSN/JWT/AWS keys/UUIDs), normalize (BOM/CRLF/smart-quotes/whitespace/tabs/case/Unicode NFC), line utilities (count/dedupe/sort/shuffle/head/tail), word-frequency stats with stopwords, three-mode text diffs (unified/side/HTML), no-Jinja2 template renderer with filters and defaults, URL-safe slug generator, and Markdown converter (strip-to-text / minimal HTML / extract headings/links/images/code/lists). Pure Python 3 standard library, no third-party dependencies, no remote calls.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit"}}
---

# clean-text-toolkit

v0.4.0

A small, honest local toolkit for the work agents end up doing constantly: read some text someone sent you, find the structured bits, clean it up, redact the secrets, and forward it downstream. Built on Python 3 standard library only. No `pandas`, no `nltk`, no pip installs, no remote calls.

This skill is the companion to [`clean-csv-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit): that one handles structured tabular data, this one handles unstructured text.

## What this skill does

- `scripts/extract.py` — pull structured items out of any text file. Kinds: `url`, `email`, `phone`, `ipv4`, `ipv6`, `hashtag`, `mention`, `hex-color`, `money`, `iso-date`. Output to stdout (one-per-line or JSON), or to a `.txt` / `.json` / `.jsonl` file. Optional `--unique`, `--sort`, `--with-line` (prefix with the source line number).
- `scripts/normalize.py` — clean up messy text. Chainable transforms applied in command-line order: `--trim`, `--collapse-spaces`, `--strip-blank`, `--to-unix`, `--to-crlf`, `--dehyphenate` (rejoin OCR/PDF hyphenated line-breaks), `--unsmart` (smart quotes / em-dashes → ASCII), `--strip-bom`, `--strip-zwsp` (zero-width spaces and joiners), `--tabs-to-spaces N`, `--spaces-to-tabs N`, `--lower` / `--upper` / `--title`, `--normalize-unicode NFC|NFD|NFKC|NFKD`.
- `scripts/redact.py` — anonymize text by replacing PII-like patterns with placeholder tokens. Kinds: `email`, `phone`, `ipv4`, `ipv6`, `url`, `credit-card` (with Luhn validation to suppress false positives), `ssn-us`, `uuid`, `hex-token` (32+ hex chars, typical for tokens / hashes), `aws-access-key` (AKIA…), `jwt` (three base64url segments with the `eyJ` header). `--keep-counts` makes the same value always get the same placeholder; `--preserve-length` pads/truncates the placeholder to the original length.
- `scripts/lines.py` — line-oriented utilities. `--op count | dedupe | sort | shuffle | head | tail`. Streams `count`, `head`, `tail`. `dedupe` and `sort` are O(N) memory in the number of lines, but each line is small so 1 M lines is fine on a laptop. `--case-insensitive`, `--keep first|last`, `--numeric`, `--reverse`, `--seed` for deterministic shuffles.
- `scripts/wordcount.py` — word / character / line / sentence statistics. Optional `--top N` for most-frequent words, `--stopwords PATH`, `--min-length N`, `--ignore-case`, `--regex PATTERN` (default `[A-Za-z']+`).
- `scripts/diff_text.py` — three-mode text diff using stdlib `difflib`. `--mode unified` (default), `--mode side` (custom two-column layout), `--mode html` (writes a full HTML file with red/green coloring). `--ignore-case`, `--ignore-whitespace`, `--context N`.
- `scripts/template.py` (NEW in v0.2.0) — substitute placeholders in a text file with values from a JSON object or inline `--set key=value` overrides. Mustache (`{{name}}`), dollar (`${name}`), or percent (`%(name)s`) syntax. Filters: upper, lower, title, strip, capitalize, reverse, len, escape-html, escape-json, urlencode. Default values: `{{name ?Unknown}}`. Strict mode (`--strict`) exits 1 if any placeholder is unresolved. **No Jinja2, no `eval`.**
- `scripts/slug.py` (NEW in v0.2.0) — turn strings into URL-safe slugs. Single string mode (`--text "Hello World"`) or batch mode (line-in-file -> line-out-file). Options: `--separator`, `--max-length`, `--no-lower`, `--ascii` (Unicode -> ASCII transliteration via NFKD), `--keep-dots` (useful for filenames), `--dedupe`.
- `scripts/markdown.py` (NEW in v0.2.0) — strip Markdown to plain text, render a minimal HTML approximation, or extract structured items (headings, links, images, code blocks, list items) as JSON / JSONL / TSV. For text mode, `--link-style anchor|url|both` controls how `[text](url)` is rendered.
- `scripts/replace.py` (NEW in v0.3.0) — find-and-replace with regex / literal / word-boundary modes, capture-group back-references (`\1`, `\2`), multiple `--find/--replace` pairs in a single pass, or a JSON `--rules` file with per-rule settings. `--dry-run` previews matches with line:col and context; `--max N` caps replacements per rule. Returns exit 1 when zero replacements happen so it slots into CI.
- `scripts/htmlstrip.py` (NEW in v0.4.0) — strip HTML tags from scraped pages. Three modes: `text` (collapse to plain readable text, drop `<script>`/`<style>` content, preserve line breaks at block tags), `html` (sanitize — remove `script,style,iframe,object,embed,form,input` tags + all `on*` event-handler attributes + inline `style=`, keep the rest intact), `extract` (pull links/images/headings/tables as JSON/JSONL/TSV). Built on Python stdlib `html.parser`. The single most-asked-for agent capability: turn scraped HTML into something useful in one command.
- `scripts/check_deps.sh` — verify `python3` is available.

## What this skill does not do

- It does not call any LLM, web service, or remote API.
- It does not load entire files into memory unless an operation truly needs the whole file (full-content normalization, sort-and-write, diff). Streaming-friendly operations (`extract`, `lines --op count|head|tail`, `wordcount` for chars/lines counters) read one line at a time.
- It does not write outside the input/output paths the caller provides.

## Quick start

### 1. Pull every email out of a log file

```bash
python3 scripts/extract.py app.log --kind email --unique --sort
python3 scripts/extract.py app.log --kind email --output emails.txt --unique
```

### 2. Find every URL and tag it with the source line

```bash
python3 scripts/extract.py article.md --kind url --with-line
```

### 3. Clean up a messy OCR dump

```bash
python3 scripts/normalize.py scanned.txt clean.txt \
    --strip-bom --to-unix --dehyphenate --collapse-spaces \
    --unsmart --strip-blank --normalize-unicode NFC
```

The transforms run in the order you list them on the command line.

### 4. Redact PII before sharing a transcript

```bash
python3 scripts/redact.py transcript.txt safe.txt
# default kinds = all
# default placeholder = [REDACTED_{kind}_{i}]
```

```bash
# Only redact emails and phones, give the same email the same placeholder
python3 scripts/redact.py transcript.txt safe.txt \
    --kinds email,phone --keep-counts
```

```bash
# Custom template
python3 scripts/redact.py log.txt safe.txt \
    --token-template "<<{kind}#{i}>>"
```

```bash
# Pad placeholder to match original length (for fixed-width layouts)
python3 scripts/redact.py log.txt safe.txt --preserve-length
```

Credit-card matches are validated against the Luhn checksum so 16 random digits in a row don't trigger a false positive.

### 5. Line utilities

```bash
# Quick file stats
python3 scripts/lines.py haystack.txt --op count

# Drop duplicates, case-insensitive
python3 scripts/lines.py users.txt --op dedupe --case-insensitive --output unique.txt

# Numeric sort (so "100" > "23" > "7")
python3 scripts/lines.py scores.txt --op sort --numeric --reverse

# Deterministic shuffle
python3 scripts/lines.py prompts.txt --op shuffle --seed 42

# Look at the head and tail of a multi-gig log
python3 scripts/lines.py huge.log --op head -n 20
python3 scripts/lines.py huge.log --op tail -n 20
```

### 6. Word counts

```bash
# Basic stats
python3 scripts/wordcount.py essay.txt

# Top words with stopwords filter
python3 scripts/wordcount.py essay.txt --top 20 --ignore-case --stopwords stop.txt

# Machine-readable output
python3 scripts/wordcount.py essay.txt --top 10 --json > stats.json
```

### 7. Text diff

```bash
# Standard unified diff
python3 scripts/diff_text.py before.txt after.txt

# Side-by-side
python3 scripts/diff_text.py before.txt after.txt --mode side

# HTML report (colorized) for sharing
python3 scripts/diff_text.py before.txt after.txt --mode html --output diff.html

# Whitespace-insensitive compare
python3 scripts/diff_text.py before.txt after.txt --ignore-whitespace
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success / one or more matches / files identical |
| 1 | zero matches / zero redactions / files differ / empty input |
| 2 | bad arguments / unsafe path / missing input / unknown kind / bad regex / unsupported output extension |

This 0 / 1 / 2 split is consistent across all six scripts so they slot into shell pipelines cleanly:

```bash
# Normalize, then redact, then count words in one shot
python3 scripts/normalize.py raw.txt clean.txt --to-unix --dehyphenate \
  && python3 scripts/redact.py clean.txt safe.txt \
  && python3 scripts/wordcount.py safe.txt --top 10
```

## Safety properties

- Pure Python 3 standard library. No third-party dependencies, no `pip install`.
- No `subprocess` calls. No shell invocation.
- All file paths are validated against a strict allowlist regex that rejects shell metacharacters (`;`, `|`, `&`, `>`, `<`, `$`, `` ` ``, etc.). The same `safe_path()` helper that powers `clean-csv-toolkit`.
- Scripts only read the input paths the caller provides and write to the output paths the caller provides.
- All inputs and outputs default to UTF-8; reads fall back through `utf-8-sig`, `cp1252`, `latin-1` if needed. Writes are always UTF-8.
- Deterministic where it matters: `shuffle --seed N` is reproducible; `extract` and `wordcount` always emit results in the same order for a given input.

## Performance

- `lines.py --op dedupe` processes 100,000 short lines (500 distinct) in ~0.06 s.
- `lines.py --op sort` processes 100,000 lines in ~0.10 s.
- `extract.py` scans the file in a single streaming pass — memory does not grow with file size.

## Known limitations

- The PII patterns are pragmatic heuristics, not strict RFC validators. The `email` regex accepts `user@host.tld` shapes but does not validate that `host.tld` resolves. `phone` accepts three telltale formats (`+<digits>`, `(XXX) XXX-XXXX`, `XXX-XXX-XXXX` / `XXX XXX XXXX`) so it doesn't grab IPs, dates, or credit-card numbers — but it will miss exotic local formats.
- `credit-card` uses the Luhn checksum, but `hex-token` (and similar high-recall patterns) intentionally over-match; review the count before sharing redacted output publicly.
- `diff_text.py --mode html` produces the standard `difflib.HtmlDiff` markup, which embeds inline styles. The file is portable but the styling is not customizable.

## v0.4.0 changes

- Added `scripts/htmlstrip.py`: HTML → plain text / sanitized HTML / structured extract. Built on stdlib `html.parser`. Three modes (text / html / extract), keeps links optionally, drops `<script>/<style>/<noscript>` content entirely in text mode, removes `on*` event-handler attributes in sanitize mode. Extract mode pulls links, images, headings, and full table data as JSON.
- Specifically designed for agents that scrape web pages: one command turns a raw HTML dump into plain text or a structured links/images/tables JSON.
- Same safe-path policy and 0/1/2 exit-code contract as the rest of the toolkit.

## v0.3.0 changes

- Added `scripts/replace.py`: sed-like find-and-replace with optional regex, capture-group back-references, multiple find/replace pairs in one pass, JSON `--rules` file, `--dry-run` preview with line:col context, `--max N` cap per rule, `--word` boundaries for literal mode.
- Fixed `extract.py`: `--kind url` was grabbing trailing sentence-punctuation (`.`, `)`, `,`, etc.) as part of the URL. Now strips a single trailing punctuation char so `Visit https://example.com.` correctly extracts `https://example.com` instead of `https://example.com.`.
- Fixed `slug.py`: `--text` mode with input that slugifies to an empty string (e.g. `"!!! @@@"`) now exits 1, matching the existing batch-mode behaviour. Previously it returned 0 silently.

## v0.2.0 changes

- Added `scripts/template.py`: no-Jinja2 template renderer. Three placeholder syntaxes (mustache `{{x}}`, dollar `${x}`, percent `%(x)s`), pipe filters, fallback defaults, and an optional `--strict` mode for CI. **Hand-rolled regex tokenizer, no `eval`, no `subprocess`.**
- Added `scripts/slug.py`: URL-safe slug generator. Single-string mode (prints to stdout) or batch mode (one slug per input line). Unicode-aware with optional ASCII transliteration via NFKD; `--keep-dots` for filename use; `--dedupe` for batch outputs.
- Added `scripts/markdown.py`: three-mode Markdown processor. `text` strips all markup; `html` renders a minimal HTML approximation (headings, paragraphs, lists, blockquotes, fenced code, links, images, bold/italic/code); `extract` pulls structured items (headings, links, images, code blocks, list items) as JSON / JSONL / TSV.
- All three new scripts share the same safe-path policy and 0 / 1 / 2 exit-code contract as the rest of the toolkit.

## v0.1.0 changes

- First public release of clean-text-toolkit.
- Six scripts: `extract.py`, `normalize.py`, `redact.py`, `lines.py`, `wordcount.py`, `diff_text.py`.
- Shared `_common.py` with `safe_path`, `read_text`, `iter_lines`, and `write_text` helpers (mirrors the design of `clean-csv-toolkit/scripts/_common.py`).
- Bug fixed during development: initial `phone` regex was too greedy and matched IPs / ISO dates / credit-card-with-spaces; tightened to three explicit shapes (international, parenthesized, 3-3-4 dashed) that don't collide with those other patterns. Tested against a mixed-content fixture with 5 valid phones and 3 confusable non-phones.
- Zero third-party dependencies; works on any system that ships Python 3.

## Pairs well with

- [`clean-csv-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit) — same author, same design philosophy (pure stdlib, exit-code contract, safe-path policy), for structured tabular data.
- [`openclaw-prompt-shield`](https://clawhub.ai/gopendrasharma89-tech/openclaw-prompt-shield) — pair `extract.py --kind email,url` with prompt-shield's redaction pipeline to scrub user-supplied text before passing it to an LLM.

## License

MIT
