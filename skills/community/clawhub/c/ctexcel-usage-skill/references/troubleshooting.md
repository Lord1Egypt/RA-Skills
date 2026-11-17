# Troubleshooting

## The CLI is missing

`command not found: ctexcel-usage` means the binary is not installed. Point the
user to the public release or have them build it from source. Do not install it
without permission.

## Network errors (exit 4)

The CLI uses Go's standard transport and honours `HTTPS_PROXY` / `HTTP_PROXY`.
It does **not** read the macOS system proxy.

```bash
HTTPS_PROXY=http://127.0.0.1:6518 ctexcel-usage usage --output json
```

If the proxy address is unknown, ask the user; do not guess or hardcode one.

Other checks:

- `curl -I https://www.ctexcel.com` through the same proxy.
- Confirm the proxy is actually running; a stale system proxy setting can leave
  a port closed.
- Retry once; repeated failures should be reported, not retried in a loop.

## SMS code never arrives

- Wait at least 180 seconds between requests; the service rate-limits re-sends.
- The CLI enforces a stricter **10-minute cooldown** and exits with code `5`
  during it. Report the remaining seconds instead of retrying.
- Confirm the phone number is the one registered with CTExcel.
- A pending login older than 10 minutes is rejected; request a new code after
  the cooldown.
- A wrong code returns a non-zero API code; ask the user to re-enter it. Do not
  automatically retry with another guess.

## Session expired (exit 3)

Expected when the server invalidates the cookie. Ask for a new SMS code and run
the two login steps. Do not reuse an old code.

## "unexpected response" or "decode bundle usage"

The web API changed shape. Check:

1. `ctexcel-usage usage --output json` to see the error.
2. Fetch the endpoint manually (with the user's permission) and compare fields.
3. Update `internal/ctexcel-usage` and its tests before relying on the output
   again. Until then, report that the carrier API changed; do not fabricate
   numbers.

## Bundles look empty

`bundleUsageList` can be empty while the account is still valid. Report "no
active bundle" rather than zero usage. A missing resource key means the plan
does not include it, not that the allowance is exhausted.

## Values differ from the web page by a few hundredths

The page may use the carrier's own percentage rounding (`bonusDataPercent`)
while the CLI recomputes `remaining / total`. Totals and remaining GB come from
the same megabyte values and should match.

## State file permissions

`ctexcel-usage` creates `state.json` with mode `0600`. If the file is copied or
restored with looser permissions:

```bash
chmod 600 ~/Library/Application\ Support/ctexcel-usage/state.json
```

Do not print the file contents in a chat or log.