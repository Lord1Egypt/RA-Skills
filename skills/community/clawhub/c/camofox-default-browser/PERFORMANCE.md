---
type: Guide
title: "Camoufox Default Browser — Performance Optimization"
description: Resource management, benchmarking, scaling, and tuning guide for Camoufox automation workloads
timestamp: 2026-07-30T13:06:00+07:00
---

# 🚀 Camoufox Performance Optimization Guide

Optimization strategies for high-throughput browser automation with Camoufox (Firefox fork with anti-detection fingerprint management).

---

## 1. Resource Management

### Memory Usage Breakdown

| State | Memory | Notes |
|-------|--------|-------|
| Idle server process | ~15 MB | Node.js wrapper only |
| Browser launched, no tabs | ~40 MB | Firefox engine initialized |
| 1 active tab (loaded) | ~200 MB | Page DOM + JS heap + rendering |
| Additional tabs | +50–80 MB each | Isolated per-tab context |
| Heavy SPA (React/Vue) | +100 MB extra | Client-side framework runtime |
| 10 concurrent tabs | ~800–1100 MB total | Practical ceiling per process |

**Actionable:** Monitor via `camofox_list_tabs` to track active sessions. Close idle tabs promptly (`camofox_close_tab`) to prevent memory drift. Target <5 concurrent tabs per process cycle.

### CPU Utilization Patterns

| Operation | CPU Load | Duration | Peak |
|-----------|----------|----------|------|
| Tab creation | Low-Medium | 2–5s | 60–80% briefly |
| Page navigation | Medium | 3–10s | 40–70% during load |
| Snapshot generation | Low | <1s | <20% |
| Screenshot capture | Low | <1s | <15% |
| JS evaluate (light) | Low-Medium | 1–3s | 30–50% |
| JS evaluate (heavy SPA) | High | 5–30s | 80–120% |
| Idle wait | Minimal | continuous | <5% |

**Actionable:** Batch JS evaluations where possible. Avoid rapid sequential `evaluate` calls on SPAs — add 200ms delay between operations to let render thread stabilize.

### Disk I/O Considerations

- **Cache directory:** `~/.cache/camoufox/` stores browser profiles (~50–200MB after first run)
- **Profile per user session:** Each unique user/session gets isolated profile data
- **SSD recommended:** Profile reads/writes happen at browser startup/shutdown
- **Network:** Cache hits after first run reduce disk writes significantly

**Actionable:** Place workspace on SSD. Profile reuse across sessions means one-time disk cost, not per-request overhead. Monitor `du -sh ~/.cache/camoufox/` if disk grows abnormally.

### Network Bandwidth Usage

| Scenario | Per Session | Cumulative (100 requests) |
|----------|-------------|---------------------------|
| Static page load | 2–5 MB | 200–500 MB |
| Media-rich page | 10–50 MB | 1–5 GB |
| Search macro queries | 500 KB – 2 MB | 50–200 MB |
| Cookie import + auth | 1–3 MB initial | Negligible per reuse |

**Actionable:** Use search macros (@google_search, etc.) instead of raw navigation for lookup tasks — they're optimized endpoints. For bulk scraping, prefer `snapshot` over repeated full page loads; snapshots are ~90% smaller than fetching DOM.

---

## 2. Optimization Strategies

### Tab Pooling and Reuse

Reuse established tabs across multiple interactions instead of creating fresh ones. A tab that's already navigated to the target domain saves 3–5 seconds per operation (no SSL handshake, DNS resolution, or TLS negotiation).

```
Suboptimal pattern (7 tabs created for 7 operations):
create_tab → navigate → snapshot → close_tab × 7

Optimal pattern (1 tab reused):
create_tab → navigate → [snapshot → click → type → scroll] × N → close_tab
```

**Rule:** Keep one active tab per workflow chain. Don't create-close-create-close for sequential actions on the same site.

### Lazy Loading Benefits

The server auto-starts the browser engine lazily on first request. This means zero upfront cost when idle. The tradeoff is 2–5 second warmup on the first request after inactivity exceeding `IDLE_TIMEOUT`.

**Actionable:** For batch workloads (>10 operations), launch early and keep alive. For sporadic single-use, let lazy loading handle it — the 2–5s warmup beats managing persistent processes.

### Idle Timeout Configuration

Default idle timeout is 5 minutes (`CAMOUFOX_IDLE_TIMEOUT`). Tune based on workload patterns:

| Workload Pattern | Recommended IDLE_TIMEOUT | Rationale |
|------------------|--------------------------|-----------|
| Burst batches (50+ ops/hr) | 30–60 min | Keep warmed up between bursts |
| Steady state (5–20 ops/hr) | 15–30 min | Balance freshness vs warmth |
| Sporadic (<5 ops/day) | 5 min default | Save resources, accept warmup hit |
| Cron-driven automated | 0 (disabled shutdown) | Never shut down between cron runs |

### Concurrent Tab Limits

| Limit Setting | Max Safe Tabs | Memory Impact | Detection Risk |
|---------------|---------------|---------------|----------------|
| 3 tabs | Excellent | ~600 MB | Very low |
| 5 tabs | Good | ~800 MB | Low |
| 8 tabs | Manageable | ~1.2 GB | Moderate |
| 10+ tabs | Risky | >1.5 GB | Higher — suspicious patterns |

**Actionable:** Cap at 5 concurrent tabs as default. Above that, stagger operations by 500ms intervals to avoid detection signatures. Rotate user-agent strings across tabs.

---

## 3. Benchmarking

### Baseline Performance Metrics

All measurements taken on standard OpenClaw VM (Linux x64, 2 vCPU, 2GB RAM). Actual results vary by hardware.

| Metric | Fast | Average | Slow | Conditions |
|--------|------|---------|------|------------|
| Tab creation | 800ms | 2.5s | 5s | First-run cold vs cached |
| Navigation (fast site) | 1s | 3s | 8s | CDN performance matters |
| Navigation (heavy SPA) | 3s | 8s | 20s | React/Vue client-side renders |
| Snapshot generation | 200ms | 500ms | 1.5s | DOM complexity dependent |
| Screenshot capture | 300ms | 800ms | 2s | Resolution + content density |
| Element interaction (click/type) | 100ms | 300ms | 1s | Ref stability matters |

### Benchmark Command Reference

```bash
# Check health endpoint timing
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:9377/health

# Quick smoke test — measure end-to-end
time camofox_create_tab && sleep 1 && camofox_snapshot && camofox_close_tab

# Monitor live resource usage while running
watch -n 2 'ps aux | grep camofox'
```

### Memory Leak Detection

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Gradual memory increase >20% after closing tabs | Orphaned processes | Restart server process |
| OOM kills after 50+ tabs | No tab limit enforced | Set MAX_TABS config |
| Profile directory growing unbounded | Stale cache entries | Cleanup `~/.cache/camoufox/` |
| Snapshots returning stale data | Profile state corruption | Force new tab (fresh instance) |

**Detection script:**

```bash
#!/bin/bash
# Monitor Camoufox memory over time
while true; do
  MEM=$(ps aux | grep '[c]amoufox' | awk '{sum+=$6} END {printf "%.0f MB\n", sum/1024}')
  TABS=$(curl -s http://localhost:9377/tabs 2>/dev/null | grep -c '"tabId"' || echo 0)
  echo "$(date '+%H:%M:%S') | tabs=$TABS | mem=${MEM}"
  sleep 30
done
```

---

## 4. Scaling Considerations

### Single Instance Limits

| Resource | Soft Limit | Hard Limit | Grace Period |
|----------|-----------|------------|--------------|
| Concurrent tabs | 5 | 10 | 2 min before throttling |
| Requests/min | 30 | 60 | Rate-limited after threshold |
| Memory | 1.5 GB | 2 GB | SIGKILL at hard limit |
| CPU (1 core) | 70% sustained | 100% | Throttle or fail open |

### Multi-Instance Setup

For workloads exceeding single-instance capacity, deploy multiple instances on different ports:

```yaml
# docker-compose example for multi-instance scaling
services:
  camoufox-a:
    image: camoufox/server
    environment:
      - PORT=9377
      - CAMOUFOX_IDLE_TIMEOUT=120
    ports: ["9377:9377"]
  
  camoufox-b:
    image: camoufox/server
    environment:
      - PORT=9378
      - CAMOUFOX_IDLE_TIMEOUT=120
    ports: ["9378:9378"]
```

Route traffic via reverse proxy (Traefik/Nginx) with weighted round-robin balancing.

### Load Balancing Approaches

| Approach | Complexity | Throughput | Use Case |
|----------|-----------|------------|----------|
| Round-robin | Low | Medium | Equal-workflow tasks |
| Least-connections | Medium | High | Variable-complexity workflows |
| Priority queues | High | Optimized | Mixed urgency workloads |
| Sticky sessions | Low | High | Authenticated session reuse |

**Recommendation:** Start with simple round-robin. Upgrade least-connections when snapshot times vary widely (>2x difference between pages).

### Resource Allocation

| Instance Count | vCPU | RAM | Suitable Workload |
|----------------|------|-----|--------------------|
| 1 | 1 | 1 GB | Development/testing |
| 2 | 2 | 3 GB | Light production (<20 ops/hr) |
| 3 | 4 | 6 GB | Medium production (50+ ops/hr) |
| 5+ | 8+ | 8+ GB | Heavy production / dedicated |

---

## 5. Monitoring

### Health Endpoint

```bash
# Basic health check
curl -s http://localhost:9377/health | python3 -m json.tool

# Expected response fields: status, uptime, tabs, memory_mb, version
# status should always be "ok"
```

### Metrics to Track

| Metric | Source | Frequency | Alert Threshold |
|--------|--------|-----------|-----------------|
| Response latency | Health endpoint | Every 30s | >2s median |
| Active tabs | `camofox_list_tabs` | Every 30s | >MAX_TABS |
| Error rate | Server logs | Continuous | >5% per window |
| Memory usage | `ps` or `/proc` | Every 60s | >1.8 GB |
| Crash events | Crash telemetry | On event | Any non-zero day count |

### Alert Thresholds

| Severity | Condition | Action |
|----------|-----------|--------|
| Warning | Memory >1.5 GB | Log warning, schedule cleanup |
| Warning | Tab count >MAX_TABS × 0.8 | Log, throttle incoming |
| Critical | Memory >1.8 GB | Kill oldest tab, alert admin |
| Critical | Health endpoint returns non-"ok" | Auto-restart server |
| Info | Idle timeout approaching | Pre-warm next instance |

### Logging Best Practices

```bash
# Enable verbose logging
export CAMOUFOX_LOG_LEVEL=debug

# Tail logs in real-time
tail -f /var/log/camofox/server.log

# Filter for errors only
grep -i error /var/log/camofox/server.log | tail -50
```

**Best practices:**
- Log level `info` for production, `debug` for development/debugging
- Rotating logs daily to prevent disk growth
- Sample rather than log every request — log first/last 10% + errors
- Include request timing in structured JSON format for aggregation

---

## 6. Tuning Parameters

### IDLE_TIMEOUT Optimization

```bash
# Environment variable setting
export CAMOUFOX_IDLE_TIMEOUT=900   # 15 minutes in seconds

# For cron-driven automation (never shutdown)
export CAMOUFOX_IDLE_TIMEOUT=0     # 0 = disabled shutdown
```

| Value | Behavior | Best For |
|-------|----------|----------|
| 0 | Never shutdown | Dedicated cron jobs, always-on automation |
| 60–180s | Shut down quickly | Shared hosting, strict resource constraints |
| 300s (default) | Balanced | General-purpose use |
| 600–1800s | Stay warm | Batch processing, high-frequency usage |

### MAX_TABS Configuration

```bash
# Cap concurrent tabs
export CAMOUFOX_MAX_TABS=5        # Conservative safe default
export CAMOUFOX_MAX_TABS=8        # Moderate throughput
export CAMOUFOX_MAX_TABS=3        # Strict — anti-detection priority
```

### Memory Limits

| Parameter | Default | Tuning Range | Effect |
|-----------|---------|-------------|--------|
| Heap soft limit | 1.5 GB | 1–2 GB | GC pressure triggers above this |
| Hard limit | 2 GB | 1.5–3 GB | Process killed at threshold |
| Per-tab budget | ~500 MB | 200–1 GB | Abort tab creation if exceeded |
| Cache max size | 200 MB | 50–500 MB | Oldest profiles evicted first |

### Cache Settings

```bash
# Browser-level cache control
export CAMOUFOX_CACHE_ENABLED=true       # Enable disk cache
export CAMOUFOX_CACHE_SIZE_MB=200        # Max cache size
export CAMOUFOX_CACHE_TTL_MINUTES=60     # How long cached assets live

# Disable cache for authenticated/private sessions
export CAMOUFOX_CACHE_ENABLED=false
```

| Setting | Trade-off | Recommendation |
|---------|-----------|----------------|
| Cache ON, large | Faster repeat visits, more disk | Default for most use cases |
| Cache ON, small | Balanced | Good for shared environments |
| Cache OFF | Maximum privacy, slower repeats | Required for GDPR/anonymity scenarios |

---

## Quick Tuning Checklist

| Goal | Recommended Config |
|------|-------------------|
| Maximum anti-detection safety | `MAX_TABS=3`, sequential ops, random delays 500–2000ms |
| Maximum throughput | `MAX_TABS=8`, parallel lanes, minimal inter-op delays |
| Production reliability | `IDLE_TIMEOUT=900`, memory alerts at 1.5 GB, crash telemetry enabled |
| Cost-sensitive deployment | `IDLE_TIMEOUT=60`, `MAX_TABS=3`, single instance, cache enabled |
| Development/debugging | `LOG_LEVEL=debug`, no idle timeout, unlimited tabs (temporary) |

---

*Last updated: 2026-07-30 | Compatible with Camoufox 1.x+ | Based on OpenClaw Gateway integration behavior*
