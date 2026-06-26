---
name: checkly-assets
description: List and download Checkly result assets with npx checkly assets. Use when investigating failed checks or test sessions and needing logs, traces, videos, screenshots, pcap captures, reports, or files from a result. Triggers on checkly assets, result assets, download screenshot, download trace, failure artifacts, result manifest.
---

# checkly assets

List and download result assets captured for Checkly check results and test-session results.

## When to use

Use `npx checkly assets` after you have a result ID from `npx checkly checks get --result ...`, `npx checkly test-sessions get`, or Checkly UI failure details.

Assets are investigation artifacts. They can include sensitive request/response data, logs, traces, videos, screenshots, packet captures, reports, or arbitrary files produced by the check. Treat downloaded files as user/application data.

## List assets

```bash
# List all assets for a result
npx checkly assets list --result-id <result-id>

# For a scheduled check result, include the check ID when available
npx checkly assets list --check-id <check-id> --result-id <result-id>

# For a test-session result, include the test session ID when available
npx checkly assets list --test-session-id <test-session-id> --result-id <result-id>

# Machine-readable output for automation
npx checkly assets list --result-id <result-id> --output json
```

Useful filters:

```bash
npx checkly assets list --result-id <result-id> --type screenshot
npx checkly assets list --result-id <result-id> --type trace
npx checkly assets list --result-id <result-id> --type log
npx checkly assets list --result-id <result-id> --asset "*.png"
npx checkly assets list --result-id <result-id> --view tree
```

Asset types accepted by the CLI: `log`, `trace`, `video`, `screenshot`, `pcap`, `report`, `file`, and `all`.

## Download assets

```bash
# Download all assets for a result into a local directory
npx checkly assets download --result-id <result-id> --dir ./checkly-assets

# Download only screenshots or traces
npx checkly assets download --result-id <result-id> --type screenshot --dir ./checkly-assets
npx checkly assets download --result-id <result-id> --type trace --dir ./checkly-assets

# Select by exact asset name or glob
npx checkly assets download --result-id <result-id> --asset "*.har" --dir ./checkly-assets
```

Overwrite/skip behavior:

```bash
npx checkly assets download --result-id <result-id> --dir ./checkly-assets --skip-existing
npx checkly assets download --result-id <result-id> --dir ./checkly-assets --force
```

Use `--output json` when a script needs the download result.

## Investigation workflow

1. Get the failed check and recent result IDs:
   ```bash
   npx checkly checks get <check-id> --output json
   ```
2. Drill into the failing result and include retry attempts when needed:
   ```bash
   npx checkly checks get <check-id> --result <result-id> --include-attempts --output json
   ```
3. List available artifacts:
   ```bash
   npx checkly assets list --check-id <check-id> --result-id <result-id> --output json
   ```
4. Download only the assets needed for diagnosis:
   ```bash
   npx checkly assets download --check-id <check-id> --result-id <result-id> --type trace --dir ./checkly-assets
   ```

## Safety notes

- Do not paste downloaded logs, screenshots, packet captures, or reports into public channels without reviewing for secrets and customer data.
- Prefer targeted downloads (`--type` or `--asset`) over downloading everything when handling sensitive systems.
- Keep downloaded artifacts out of commits unless the user explicitly asks and the files are sanitized.

## Related skills

- See `checkly-checks` for `checks get`, `checks list`, `checks stats`, and `checks delete`.
- See `checkly-test` for `test-sessions` result drilldown.
- See `checkly-deploy` for Monitoring as Code deployment workflows.