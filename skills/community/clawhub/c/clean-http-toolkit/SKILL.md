---
name: clean-http-toolkit
description: Local HTTP client + tiny server toolkit for AI agents. GET / POST / PUT / PATCH / DELETE with retries on 5xx/429, gzip decoding, redirect following, --bearer / --basic auth, JSON pretty-print, custom headers, --query params, --status-only mode. Stream large file downloads with progress, resume, SHA-256 / MD5 checksum verification. Run a local static-file or JSON-echo server for tests. Pure Python 3 standard library, no requests, no httpx, no remote calls.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/clean-http-toolkit"}}
---

# clean-http-toolkit

v0.1.0

Fifth member of the `clean-*` family. AI agents constantly need to fetch a URL, POST to an API, download a dataset, or run a mock server for tests — and currently the only option is shell-out to `curl` (no retry logic) or pip-install `requests`. This toolkit gives them all four in pure stdlib.

## Scripts

- `scripts/get.py` — HTTP GET with retries (5xx/429), gzip decoding, redirect-following, `--bearer TOKEN`, `--basic USER:PASS`, `--header 'Name: V'`, `--query K=V`, `--json` pretty-print, `--print-headers`, `--status-only`, `--fail` (exit 1 on non-2xx).
- `scripts/post.py` — POST / PUT / PATCH / DELETE via `--method`. Body sources: `--json '<JSON>'`, `--json-file PATH`, `--form K=V` (repeatable), `--raw-file PATH` (with `--content-type`). Same auth + retry options as `get.py`.
- `scripts/download.py` — streaming file download with progress bar on stderr, retries on transient errors, `--resume` for incomplete files, `--sha256 HEX` / `--md5 HEX` verification, configurable `--chunk-size`. Memory stays bounded regardless of file size.
- `scripts/serve.py` — tiny local HTTP server for tests. Two modes: `static` (serve a directory, like `python3 -m http.server` but with `--max-requests N` cutoff so CI tests can run and exit cleanly) and `echo` (reply to every request with a JSON envelope describing the request itself — perfect for webhook smoke tests). Binds to `127.0.0.1` by default for safety.
- `scripts/check_deps.sh` — verify `python3`.

## Quick start

```bash
# Simple GET
python3 scripts/get.py https://api.example.com/users

# GET with auth, query params, JSON pretty-print
python3 scripts/get.py https://api.example.com/users \
    --bearer "$TOKEN" \
    --query 'limit=20' --query 'page=1' \
    --json

# Just the status code (great for health checks)
python3 scripts/get.py https://example.com --status-only

# POST JSON
python3 scripts/post.py https://api.example.com/users \
    --json '{"name":"Alice","email":"alice@example.com"}' \
    --bearer "$TOKEN"

# POST a form
python3 scripts/post.py https://example.com/login \
    --form 'user=alice' --form 'pass=secret'

# PUT a JSON file
python3 scripts/post.py https://api.example.com/items/42 \
    --method PUT --json-file payload.json

# Download with progress + SHA-256 verification
python3 scripts/download.py \
    https://releases.example.com/model.tar.gz \
    ~/Downloads/model.tar.gz \
    --sha256 abc123def456...

# Resume an incomplete download
python3 scripts/download.py URL out.bin --resume

# Local static server for tests
python3 scripts/serve.py --directory ./public --port 8080

# Echo server for webhook smoke tests (auto-exits after 5 requests)
python3 scripts/serve.py --mode echo --port 9000 --max-requests 5
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success / 2xx response (or any response if `--fail` not set) |
| 1 | `--fail` and response was non-2xx; or `--sha256` / `--md5` mismatch on download |
| 2 | bad arguments / unsafe path / bad URL / network error / non-2xx download |

## Safety properties

- Pure Python 3 standard library (`urllib`, `http.server`). No `requests`, no `httpx`, no pip install.
- All file paths validated against the same safe-path policy as the other `clean-*` toolkits.
- All URLs validated: must be `http://` or `https://` with a host.
- `serve.py` binds to `127.0.0.1` by default; you must pass `--bind 0.0.0.0` explicitly to expose it.
- `--insecure` is opt-in only — TLS verification is on by default.
- Retries are bounded (`--retries N`, default 3) with exponential backoff capped at the backoff base × 2^attempt.

## Why pure stdlib

Agents are usually run in restricted environments (sandboxes, CI runners, ephemeral containers) where `pip install` either fails, is forbidden, or burns minutes of setup time. Every script here uses only Python stdlib so it can run anywhere Python 3 is present.

## Pairs well with

- [`clean-text-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit) — pipe `get.py URL` into `htmlstrip.py` to scrape a page to plain text in one command.
- [`clean-json-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-json-toolkit) — pipe API responses into `query.py` / `validate.py` / `merge.py`.
- [`clean-log-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-log-toolkit) — `serve.py` static mode is useful for replaying captured log files over HTTP for parser tests.
- [`clean-csv-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit) — download a CSV with `download.py`, then `inspect.py` / `validate.py` it.

## v0.1.0 changes

- First public release. Four scripts: `get.py`, `post.py`, `download.py`, `serve.py`.
- Shared `_common.py` with `safe_path`, `safe_url`, `parse_headers`, `fetch` (with retry + gzip + redirect handling).
- All five `clean-*` toolkits now share the same safe-path policy, the same 0 / 1 / 2 exit-code contract, and the same zero-dependency principle.

## License

MIT
