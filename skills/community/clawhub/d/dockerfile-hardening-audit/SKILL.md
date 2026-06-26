---
name: dockerfile-hardening-audit
description: Statically audit Dockerfiles for common container hardening risks (root user, unpinned/latest base images, missing healthchecks, and risky build patterns).
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# Dockerfile Hardening Audit

Use this skill to statically audit Dockerfiles before insecure container defaults land in production.

## What this skill does
- Scans Dockerfiles and scores hardening risk per file
- Flags missing non-root `USER` declarations
- Flags base images using floating tags (`:latest`, `:main`, `:master`, `:edge`) or no tag/digest
- Flags missing `HEALTHCHECK`
- Flags `ADD` instructions (when `COPY` is safer/clearer)
- Flags `curl|bash`/`wget|sh` style remote script execution
- Supports include/exclude regex filters and fail-gate mode

## Inputs
Optional:
- `DOCKERFILE_GLOB` (default: `**/Dockerfile*`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_SCORE` (default: `3`)
- `CRITICAL_SCORE` (default: `6`)
- `REQUIRE_NON_ROOT_USER` (`0`/`1`, default: `1`)
- `REQUIRE_HEALTHCHECK` (`0`/`1`, default: `1`)
- `FLAG_FLOATING_TAGS` (`0`/`1`, default: `1`)
- `FLAG_UNPINNED_IMAGES` (`0`/`1`, default: `1`)
- `FLAG_ADD_INSTRUCTIONS` (`0`/`1`, default: `1`)
- `FLAG_REMOTE_SCRIPT_PIPE` (`0`/`1`, default: `1`)
- `FILE_MATCH` (regex include filter on Dockerfile path, optional)
- `FILE_EXCLUDE` (regex exclude filter on Dockerfile path, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Run

Text report:

```bash
DOCKERFILE_GLOB='**/Dockerfile*' \
bash skills/dockerfile-hardening-audit/scripts/dockerfile-hardening-audit.sh
```

JSON output + fail gate:

```bash
DOCKERFILE_GLOB='**/Dockerfile*' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/dockerfile-hardening-audit/scripts/dockerfile-hardening-audit.sh
```

Run against bundled fixtures:

```bash
DOCKERFILE_GLOB='skills/dockerfile-hardening-audit/fixtures/*Dockerfile*' \
bash skills/dockerfile-hardening-audit/scripts/dockerfile-hardening-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more Dockerfiles are critical
- Text mode prints summary + ranked Dockerfile risks
- JSON mode prints summary + ranked Dockerfiles + critical Dockerfiles
