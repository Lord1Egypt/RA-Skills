# Error Recovery Patterns

## Common Errors & Solutions

### File Not Found
```
Cause: Path typo, file not yet created, wrong directory
Fix: 
  1. ls/find to locate actual path
  2. Check if dependency step was completed
  3. Create file if it should exist
```

### Permission Denied
```
Cause: Read-only mount, wrong permissions
Fix:
  1. Copy file to /home/claude/ before editing
  2. chmod +x for scripts
  3. Never edit /mnt/user-data/uploads/ directly
```

### Command Failed (non-zero exit)
```
Cause: Missing dependency, syntax error, bad input
Fix:
  1. Read stderr output carefully
  2. pip install / npm install missing packages
  3. Validate input format before processing
  4. Try alternative tool/approach
```

### JSON Parse Error
```
Cause: Invalid JSON in input or output
Fix:
  1. python3 -m json.tool file.json (validate)
  2. Check for trailing commas, missing quotes
  3. Use jq for robust parsing: jq '.' file.json
```

### Network Error
```
Cause: Domain not in allowlist, timeout, rate limit
Fix:
  1. Check allowed domains in network config
  2. Retry with exponential backoff
  3. Try alternative data source
  4. Cache results to avoid repeated fetches
```

### Out of Space / Too Large
```
Cause: Large file processing, too many intermediates
Fix:
  1. Process in chunks/streams
  2. Clean working/ directory
  3. Use compression for large intermediates
```

## Recovery Strategy Matrix

| Error Type | Retry? | Alternative? | Escalate? |
|-----------|--------|-------------|-----------|
| Transient (network, timeout) | Yes, 3x | After retries | After alternatives |
| Input error (bad format) | No | Fix input first | If unfixable |
| Tool unavailable | No | Use different tool | If no alternative |
| Logic error (wrong output) | No | Revise approach | If 2 approaches fail |
| Resource limit | No | Reduce scope | Immediately |

## Retry Pattern

```python
MAX_RETRIES = 3
for attempt in range(MAX_RETRIES):
    try:
        result = execute_step()
        break
    except TransientError:
        wait = 2 ** attempt  # exponential backoff
        log_error(f"Attempt {attempt+1} failed, retrying in {wait}s")
        time.sleep(wait)
else:
    log_error("All retries exhausted")
    try_alternative_approach()
```
