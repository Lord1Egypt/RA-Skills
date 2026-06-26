# Exec Error Taxonomy (Practical)

Use this as a fast decision map.

## 1) `Unknown JSON field` (CLI schema mismatch)

**Examples**
- `gh search repos ... --json nameWithOwner ...`

**Fix**
- Replace unsupported fields (e.g., `nameWithOwner` → `fullName`)
- Use `scripts/gh_search_repos_safe.sh`

## 2) `command not found` / `ENOENT` / `spawn ... ENOENT`

**Cause**
- Missing binary or unavailable launcher in environment.

**Fix**
- Install required binary, verify with `command -v <bin>`
- In headless environments, avoid browser launch requirements and use token-based auth where possible

## 3) Auth/session missing

**Examples**
- `Error: Not logged in. Run: ...`

**Fix**
- Re-authenticate
- Verify identity (`whoami` style command)

## 4) Permission denied / EACCES

**Fix**
- Check file permissions, ownership, and execution bit
- Avoid blind sudo; correct permission scope first

## 5) Timeout / killed (`SIGKILL`, `signal 9`, code 124)

**Fix**
- Increase timeout for known-long operations
- Reduce workload/chunk work
- Check resource pressure (memory/CPU) and background kills

## 6) Transient platform state (indexing/moderation/scan)

**Examples**
- post-publish temporary `Skill not found`
- pending security scan visibility

**Fix**
- Backoff and retry with bounded attempts
- Confirm success signal from initial publish step

## 7) Network/transient transport

**Examples**
- `ECONNRESET`, `ENOTFOUND`, temporary 5xx

**Fix**
- Retry with backoff
- Validate DNS/connectivity
- Re-run after short cool-down

## 8) Invalid args/usage

**Fix**
- Re-check command help and supported flags/fields
- Prefer wrapper scripts for fragile commands
