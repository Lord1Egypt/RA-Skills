# Error Pattern Reference

Catalog of known error patterns, their root causes, and remediation steps.
The analyzer script (`scripts/analyze_logs.py`) uses built-in pattern matching, but this reference provides deeper context for manual review.

## Table of Contents
1. [Memory Issues](#memory-issues)
2. [Network / Connection](#network--connection)
3. [Disk / Filesystem](#disk--filesystem)
4. [Authentication / Authorization](#authentication--authorization)
5. [Database](#database)
6. [SSL / TLS](#ssl--tls)
7. [Process / System](#process--system)
8. [HTTP Status Codes](#http-status-codes)
9. [Application-Specific](#application-specific)

---

## Memory Issues

| Pattern | Severity | Root Cause | Fix |
|---------|----------|------------|-----|
| `out of memory` / `OOM` / `cannot allocate memory` | FATAL | Process exceeded memory limit | Increase memory limit, fix memory leaks, add swap |
| `heap out of memory` (Node.js) | FATAL | V8 heap exhausted | `--max-old-space-size=N`, check for retained objects |
| `MemoryError` (Python) | FATAL | Python process exhausted RAM | Process data in chunks, use generators |
| `GC overhead limit exceeded` (Java) | ERROR | Garbage collector can't free enough memory | Increase heap (`-Xmx`), fix object retention |

## Network / Connection

| Pattern | Severity | Root Cause | Fix |
|---------|----------|------------|-----|
| `ECONNREFUSED` / `connection refused` | ERROR | Target service down or not listening | Check target service, verify port/host |
| `ECONNRESET` / `connection reset` | WARN | Connection dropped by peer | Check upstream timeouts, load balancer health |
| `ETIMEDOUT` / `timeout` | ERROR | Network or service too slow | Increase timeout, check network latency |
| `EHOSTUNREACH` / `no route to host` | ERROR | Network path unavailable | Check network, routing, VPN |
| `ENOTFOUND` / `DNS resolution failed` | ERROR | Hostname doesn't resolve | Check DNS config, hostname spelling |
| `too many open files` / `EMFILE` | ERROR | File descriptor limit hit | `ulimit -n`, check fd leaks |

## Disk / Filesystem

| Pattern | Severity | Root Cause | Fix |
|---------|----------|------------|-----|
| `ENOSPC` / `no space left on device` | FATAL | Disk full | Clean up, expand volume, add log rotation |
| `EROFS` / `read-only file system` | ERROR | Filesystem mounted read-only | Remount, check disk health (`fsck`) |
| `EACCES` / `permission denied` | ERROR | Insufficient file permissions | `chmod`/`chown`, check process user |

## Authentication / Authorization

| Pattern | Severity | Root Cause | Fix |
|---------|----------|------------|-----|
| `401 Unauthorized` | WARN | Invalid/expired credentials | Refresh token, check API key |
| `403 Forbidden` | WARN | Insufficient permissions | Check IAM roles, API scopes |
| `invalid token` / `jwt expired` | WARN | Token expired or malformed | Implement token refresh logic |
| `authentication failed` | ERROR | Wrong credentials | Verify credentials, check auth service |

## Database

| Pattern | Severity | Root Cause | Fix |
|---------|----------|------------|-----|
| `deadlock detected` | ERROR | Concurrent transactions conflict | Review transaction isolation, add retry logic |
| `lock wait timeout exceeded` | ERROR | Long-running transaction blocking | Optimize slow queries, reduce transaction scope |
| `too many connections` | ERROR | Connection pool exhausted | Increase pool size, check for connection leaks |
| `relation does not exist` | ERROR | Missing table/view | Run migrations, check schema |

## SSL / TLS

| Pattern | Severity | Root Cause | Fix |
|---------|----------|------------|-----|
| `certificate has expired` | ERROR | SSL cert expired | Renew certificate |
| `self-signed certificate` | WARN | Untrusted cert in production | Use CA-signed cert or add to trust store |
| `handshake failure` | ERROR | Protocol/cipher mismatch | Update TLS version, check cipher suite |

## Process / System

| Pattern | Severity | Root Cause | Fix |
|---------|----------|------------|-----|
| `SIGSEGV` / `segmentation fault` | FATAL | Memory access violation | Update native modules, check bindings |
| `SIGKILL` / `killed` | FATAL | Process killed (usually by OOM killer) | Increase memory, check `dmesg` |
| `maximum call stack exceeded` | ERROR | Infinite recursion | Fix recursive logic |
| `core dumped` | FATAL | Process crashed | Analyze core dump with `gdb` |

## HTTP Status Codes

| Code | Severity | Meaning | Common Fix |
|------|----------|---------|------------|
| 400 | WARN | Bad request | Validate input before sending |
| 401 | WARN | Unauthorized | Check auth credentials |
| 403 | WARN | Forbidden | Check permissions/roles |
| 404 | INFO | Not found | Check URL, routing config |
| 408 | WARN | Request timeout | Increase client timeout |
| 429 | WARN | Rate limited | Implement backoff/retry |
| 500 | ERROR | Internal server error | Check server logs for root cause |
| 502 | ERROR | Bad gateway | Check upstream service health |
| 503 | ERROR | Service unavailable | Service overloaded or in maintenance |
| 504 | ERROR | Gateway timeout | Increase proxy timeout, check backend |

## Application-Specific

### Node.js
- `UnhandledPromiseRejectionWarning` → Add `.catch()` or `try/catch` in async code
- `MaxListenersExceededWarning` → Memory leak in event emitters, check `on()` calls

### Python
- `RecursionError` → Infinite recursion or deep nesting; increase `sys.setrecursionlimit()` or refactor
- `BrokenPipeError` → Client disconnected; handle gracefully in web servers

### Docker
- `OCI runtime create failed` → Image or runtime issue; rebuild image, check Docker daemon
- `container killed` → OOM or health check failure; check resource limits
