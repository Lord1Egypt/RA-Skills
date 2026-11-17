# HTTP From Scripts — curl, Status Codes, Retries, JSON

A deploy script, a webhook, a health check and a token refresh are all the same shape: call an endpoint, decide from the status code, parse the body. Bash makes each of those three steps easy to get wrong by default — curl exits 0 on a 500, and a body pasted into a JSON string breaks on the first quote.

## The Baseline Invocation

```bash
curl --fail-with-body --silent --show-error --location \
     --max-time 30 --connect-timeout 5 \
     -H "Accept: application/json" "$url"
# --fail-with-body needs curl >=7.76; older hosts: see the fallback below
```

- `--silent --show-error` (`-sS`) removes the progress meter but keeps the error message — a bare `-s` hides the reason the call failed
- `--fail` (`-f`) makes HTTP >=400 a nonzero exit but DISCARDS the body, which usually contains the API's explanation; `--fail-with-body` (`curl >=7.76`) keeps both. Below that floor — RHEL 8 ships 7.61, Ubuntu 20.04 ships 7.68, and many CI images are older still — the flag aborts with `option --fail-with-body: is unknown`; fall back to `-f` plus `-o body.txt -w '%{http_code}'` and read the body from the file (that pattern is the next section anyway), or gate on `curl --version`
- `--location` follows redirects; without it an endpoint that moved returns a 301 with an empty body and your parser blames the JSON
- Always bound the call: `--max-time` for the whole transfer, `--connect-timeout` for the handshake. An unbounded curl in a cron job is a job that never finishes (`cron.md`)
- Add `--compressed` for large JSON responses; `--no-progress-meter` (`curl >=7.67`) does what `-sS` does — hides the progress bar only — without `-s`'s side effect of also swallowing error messages

## Status Code And Body, Separately

```bash
# One attempt. Return 0 = done, 1 = retryable (caller loops with backoff), die = fatal.
attempt() {
  local url=$1 body=$2 code retry
  code=$(curl -sS -o "$body" -w '%{http_code}' -D "$body.hdr" \
           --max-time 30 "$url") || return 1   # transport failure: DNS/TLS/timeout, retryable
  case $code in
    2??)     return 0 ;;                                          # success
    3??)     die "unfollowed redirect $code — add --location" ;;  # no -L: body is empty
    401|403) die "auth rejected ($code)" ;;
    429)     retry=$(awk -F': ' 'tolower($1)=="retry-after"{print $2+0}' "$body.hdr")
             sleep "${retry:-5}"; return 1 ;;                     # slept, still NOT a success
    4??)     die "client error $code: $(head -c 300 "$body")" ;;  # our bug, do not retry
    *)       return 1 ;;                                          # 5xx and anything else: retry
  esac
}

body=$(mktemp); trap 'rm -f "$body" "$body.hdr"' EXIT
for n in 1 2 3; do
  attempt "$url" "$body" && break
  (( n < 3 )) || die "gave up after 3 attempts on $url"
done
```

- Distinguish TRANSPORT failure (curl's own exit code: DNS, TLS, timeout) from HTTP failure (the status code). They need different handling and different messages
- `-w '%{http_code}'` also carries `%{time_total}`, `%{size_download}` and `%{url_effective}` — the cheapest request log you will ever write
- 429 and 503 often carry `Retry-After`; honoring it beats a fixed backoff and keeps you off the vendor's block list. Sleeping is not succeeding: the 429 branch must still return nonzero so the caller retries — a `sleep` that falls out of the `case` turns rate limiting into a silent success (`die` is SKILL.md's abort helper)
- Retry 5xx and timeouts, never 4xx (`errors.md`): a malformed request fails identically every time

## Sending JSON Without Breaking On Quotes

```bash
payload=$(jq -n --arg id "$id" --arg msg "$message" '{id: $id, text: $msg, ts: now|floor}')
curl -sS --fail-with-body -X POST "$url" \
     -H 'Content-Type: application/json' --data-binary "$payload"
```

- Build JSON with `jq -n --arg` (or `--argjson` for numbers and booleans). String-interpolating a shell variable into a JSON literal breaks on the first quote, newline, or backslash the value contains — and is an injection hole when the value came from outside (`security.md`)
- `--data-binary @-` reads the body from stdin, which keeps a large payload off the command line: `printf '%s' "$payload" | curl … --data-binary @-`
- `--data` strips newlines; `--data-binary` does not. For anything but simple form fields, use the binary form
- Form fields need encoding: `--data-urlencode "q=$query"` handles spaces and ampersands that would otherwise split the parameter

## Reading Responses

- `jq -r` for scalar extraction, `@tsv` for several fields at once, `-e` to make "field missing" a nonzero exit (`text-processing.md`)
- Never mix headers into the body you parse: `-i` prepends them and every parser chokes. Capture them separately with `-D headers.txt`
- Pagination is a loop over a cursor, not a fixed page count:
  ```bash
  next=$start
  while [[ -n $next && $next != null ]]; do
    resp=$(curl -sS --fail-with-body "$next")
    jq -r '.items[].id' <<< "$resp"
    next=$(jq -r '.next // empty' <<< "$resp")
  done
  ```
- Bound every such loop with a maximum iteration count; a server that always returns the same cursor turns a sync job into an infinite one

## Credentials

- A token in the URL or in `-H "Authorization: …"` is visible in `ps` to every local user and in shell history. Keep it off argv with a config file read from stdin:
  ```bash
  curl -sS --config - "$url" <<EOF
  header = "Authorization: Bearer $token"
  EOF
  ```
- `--netrc-file ~/.netrc` (mode 0600) is the other argv-free option for basic auth
- `-u user:pass` has the same argv exposure; `-u user` prompts, which hangs unattended (`interactive.md`)
- Never `-k`/`--insecure` to "fix" a certificate error: point curl at the right CA bundle (`--cacert`, or `CURL_CA_BUNDLE`) and fix the trust problem
- Proxy settings arrive through `HTTPS_PROXY`/`NO_PROXY`; a script that works on a laptop and hangs on a locked-down host is usually missing them, not broken

## Waiting For A Service

```bash
i=0
until curl -sS --fail --max-time 3 "$health" >/dev/null 2>&1; do
  (( ++i > 30 )) && die "service not healthy after $(( i * 10 ))s"
  sleep 10
done
```

- Bound the wait and report the elapsed time — an unbounded readiness loop is the most common CI hang after prompts (`ci.md`)
- For a raw TCP check with no curl and no netcat, bash speaks TCP itself: `timeout 2 bash -c 'exec 3<>/dev/tcp/db/5432' && echo open` (this is a bash feature, absent in dash and in some minimal builds)
- Health-check a URL that actually exercises the dependency; a static `/ping` returns 200 from a process that cannot reach its database

## Downloads

- Verify before use: download to a temp path, check a separately published checksum, then move into place (`security.md`)
- `--retry 3 --retry-connrefused --retry-delay 2` covers transient network faults; curl retries only transient failures, so it never masks a 404
- `-C -` resumes a partial download; `-o` with `--create-dirs` writes into a path that does not exist yet
- `wget -q -O -` is the fallback when curl is absent; its exit codes and flags differ, so pick one at the top of the script and stick to it
