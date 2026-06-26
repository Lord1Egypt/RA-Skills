---
name: debug-detective
description: >
  Activate this skill whenever a user needs help debugging, diagnosing, or profiling issues
  in their application. Covers systematic debugging methodology, git bisect, Chrome DevTools
  deep dive, Node.js and Python debugger usage, system-level debugging with strace and
  tcpdump, database query debugging with EXPLAIN ANALYZE, network debugging with curl and
  DNS tools, memory leak detection, CPU and performance profiling with flame graphs, structured
  logging and distributed tracing with OpenTelemetry, and production debugging strategies.
  Provides step-by-step workflows and a comprehensive pitfalls reference.
license: MIT
compatibility: "Openclaw"
metadata:
  version: "1.0.0"
  author: "OpenClaw"
  category: "debugging"
---

# Debug Detective — Systematic Debugging Methodology

Find and fix bugs efficiently across the full stack using structured investigation techniques.

## 1. Debugging Mindset

### 1.1 The scientific method for debugging

```
1. OBSERVE     — What exactly is happening? (symptoms, error messages, logs)
2. HYPOTHESIZE — What could cause this? (list 3+ possibilities)
3. PREDICT     — If hypothesis X is correct, then Y should be true
4. TEST        — Design the smallest experiment to test the prediction
5. ANALYZE     — Did the test confirm or refute the hypothesis?
6. REPEAT      — If refuted, move to next hypothesis; if confirmed, fix and verify
```

### 1.2 Key debugging principles

- **The bug is never where you think it is.** Widen your search radius before going deep.
- **Reproduce first, fix second.** A bug you can't reproduce is a bug you can't verify as fixed.
- **Change one thing at a time.** Multiple simultaneous changes make it impossible to identify the fix.
- **Trust nothing.** Verify assumptions — check that the code you're reading is the code that's running.
- **Read the error message.** Fully. Including the stack trace. Including the "caused by" chain.

### 1.3 Cognitive biases that hinder debugging

| Bias | How it hurts | Counter-strategy |
|------|-------------|------------------|
| **Confirmation bias** | You look for evidence supporting your theory, ignore contradicting evidence | Actively try to disprove your hypothesis |
| **Anchoring** | First theory dominates even when evidence points elsewhere | Write down 3+ hypotheses before investigating any |
| **Recency bias** | "I just changed X, so X must be the problem" | Check git log — the bug might predate your change |
| **Availability bias** | "Last time it was a race condition, so it must be again" | Consider all categories: data, logic, timing, config, environment |
| **Sunk cost** | "I've spent 2 hours on this theory, it must be right" | Set a timebox: 30 min per hypothesis, then move on |

### 1.4 Rubber duck debugging

Explain the problem out loud (to a duck, a colleague, or a text file):

1. State what the code is supposed to do
2. Walk through the code line by line, explaining each step
3. The act of articulating often reveals the gap between expectation and reality

### 1.5 Feynman technique

1. Write the bug description as if explaining to a non-programmer
2. Identify gaps in your explanation — those are gaps in your understanding
3. Go back to the code to fill those gaps
4. Simplify your explanation further

## 2. Systematic Debugging Workflow

### 2.1 The six-step process

```
┌─────────────┐
│ 1. REPRODUCE │ ← Can you trigger the bug reliably?
└──────┬──────┘
       ▼
┌─────────────┐
│ 2. ISOLATE   │ ← Narrow down: which component, input, or path?
└──────┬──────┘
       ▼
┌─────────────┐
│ 3. IDENTIFY  │ ← Root cause found
└──────┬──────┘
       ▼
┌─────────────┐
│ 4. FIX       │ ← Minimal, targeted change
└──────┬──────┘
       ▼
┌─────────────┐
│ 5. VERIFY    │ ← Bug no longer reproduces; no regressions
└──────┬──────┘
       ▼
┌─────────────┐
│ 6. PREVENT   │ ← Add test, monitoring, or documentation
└─────────────┘
```

### 2.2 Reproducing the bug

**Minimal reproduction checklist:**

1. Start from a clean state (fresh install, empty database, incognito browser)
2. List exact steps to trigger the bug
3. Note the environment: OS, runtime version, browser, config
4. Strip away unrelated code until the bug is isolated
5. If intermittent: identify the timing/concurrency pattern

```bash
# Create a minimal reproduction project
mkdir bug-repro && cd bug-repro
npm init -y
# Add only the minimum dependencies needed to demonstrate the bug
npm install problematic-library@1.2.3
# Write the smallest possible script that triggers the issue
```

### 2.3 Binary search debugging

When you don't know where the bug is, bisect:

**Code bisection:**
```
// Add a return/exit at the midpoint of the suspect code
// If the bug disappears → bug is after the midpoint
// If the bug persists → bug is before the midpoint
// Repeat on the narrowed half
```

**Data bisection:**
```bash
# If a large input causes the bug, split it in half
head -n 500 input.csv > first_half.csv
tail -n 500 input.csv > second_half.csv
# Test each half — which one triggers the bug?
```

**Config bisection:**
```bash
# Comment out half the config, test
# Narrow down which config option causes the issue
```

### 2.4 Reading stack traces

```
Error: Cannot read properties of undefined (reading 'email')
    at getUserEmail (src/services/user.ts:42:18)        ← WHERE it crashed
    at processOrder (src/services/order.ts:87:24)        ← WHO called it
    at OrderController.create (src/controllers/order.ts:23:5)  ← Entry point
    at Layer.handle (node_modules/express/lib/router/layer.js:95:5)
```

**Read bottom-up:** The bottom shows where the call originated. The top shows where it failed. The line `src/services/user.ts:42` is where to look, but the **cause** might be in `order.ts:87` (passing undefined).

## 3. Git Bisect

### 3.1 Manual bisect

```bash
# Start bisecting
git bisect start

# Mark current (broken) commit as bad
git bisect bad

# Mark a known-good commit (e.g., last release tag)
git bisect good v2.0.0

# Git checks out the midpoint — test it
# If this commit is broken:
git bisect bad
# If this commit works:
git bisect good

# Repeat until git identifies the first bad commit
# Git outputs: "abc1234 is the first bad commit"

# Done — reset
git bisect reset
```

### 3.2 Automated bisect

```bash
# Automated: provide a test script that exits 0 (good) or 1 (bad)
git bisect start HEAD v2.0.0
git bisect run npm test

# Or with a custom script
git bisect run bash -c '
  npm run build 2>/dev/null && \
  node -e "
    const { buggyFunction } = require(\"./dist\");
    const result = buggyFunction(\"test-input\");
    process.exit(result === expected ? 0 : 1);
  "
'

# Reset when done
git bisect reset
```

### 3.3 Bisect with skip

```bash
# If a commit can't be tested (e.g., build broken for unrelated reason)
git bisect skip

# Skip a range of untestable commits
git bisect skip v2.0.1..v2.0.5
```

## 4. Frontend Debugging

### 4.1 Chrome DevTools — Console power features

```js
// $0 — reference to currently selected element in Elements panel
$0.textContent

// $$() — querySelectorAll shortcut
$$('button.primary').length

// copy() — copy any value to clipboard
copy(JSON.stringify(data, null, 2))

// monitor() — log all calls to a function
monitor(fetch)
// unmonitor(fetch) to stop

// monitorEvents() — log all events on an element
monitorEvents($0, 'click')
// unmonitorEvents($0) to stop

// queryObjects() — find all instances of a constructor
queryObjects(Promise)  // Find all live Promises

// table() — display array/object as table
console.table(users, ['name', 'email', 'role'])

// time/timeEnd — measure execution time
console.time('render')
renderComponent()
console.timeEnd('render')  // render: 42.3ms

// group — organize related logs
console.group('API Request')
console.log('URL:', url)
console.log('Method:', method)
console.log('Body:', body)
console.groupEnd()

// assert — log only when condition fails
console.assert(user.id, 'User ID is missing', user)
```

### 4.2 Sources panel — Advanced breakpoints

| Breakpoint type | How to set | Use case |
|----------------|-----------|----------|
| Line breakpoint | Click line number | Stop at specific line |
| Conditional | Right-click line → "Add conditional" | Stop only when condition is true |
| Logpoint | Right-click → "Add logpoint" | Log without modifying code |
| DOM breakpoint | Elements panel → right-click → "Break on" | Stop when DOM changes |
| XHR breakpoint | Sources → XHR Breakpoints → add URL pattern | Stop on matching fetch/XHR |
| Event listener | Sources → Event Listener Breakpoints | Stop on click, keypress, etc. |
| Exception | Sources → pause icon → "Pause on exceptions" | Stop on any thrown error |

### 4.3 Performance panel — Finding slow code

```
1. Click Record (or Ctrl+E)
2. Perform the slow action in the app
3. Click Stop
4. Analyze the flame chart:
   - Wide bars = slow functions
   - Look for "Long Task" markers (>50ms)
   - Check "Bottom-Up" tab for aggregate time per function
   - Check "Call Tree" for the hot path
```

### 4.4 Memory panel — Finding leaks

```
1. Take Heap Snapshot (baseline)
2. Perform the action suspected of leaking
3. Take another Heap Snapshot
4. Select Snapshot 2, change view to "Comparison"
5. Sort by "# Delta" — positive deltas are new allocations
6. Look for:
   - Detached DOM trees (elements removed from page but still referenced)
   - Growing arrays or maps
   - Event listeners not cleaned up
```

### 4.5 CSS debugging techniques

```css
/* Outline all elements to see layout issues */
* { outline: 1px solid red !important; }

/* More detailed — color by nesting depth */
* { outline: 1px solid rgba(255, 0, 0, 0.3) !important; }
* * { outline: 1px solid rgba(0, 255, 0, 0.3) !important; }
* * * { outline: 1px solid rgba(0, 0, 255, 0.3) !important; }

/* Debug z-index stacking */
* { position: relative; }
*::after {
  content: attr(class);
  position: absolute;
  top: 0; left: 0;
  font-size: 10px;
  background: yellow;
  z-index: 99999;
}
```

### 4.6 React DevTools profiler

```
1. Open React DevTools → Profiler tab
2. Click Record
3. Interact with the app
4. Click Stop
5. Analyze:
   - Flame chart shows component render times
   - Ranked chart shows slowest components
   - "Why did this render?" shows trigger reasons
   - Look for unnecessary re-renders (grey = didn't render)
```

## 5. Node.js / JavaScript Debugging

### 5.1 Inspect flag

```bash
# Start with debugger
node --inspect src/server.js

# Break on first line
node --inspect-brk src/server.js

# Then open chrome://inspect in Chrome and click "inspect"
```

### 5.2 VS Code launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Server",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/src/server.ts",
      "runtimeExecutable": "tsx",
      "console": "integratedTerminal",
      "env": { "NODE_ENV": "development" }
    },
    {
      "name": "Debug Tests",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/vitest",
      "args": ["run", "--reporter=verbose", "${file}"],
      "console": "integratedTerminal"
    },
    {
      "name": "Attach to Process",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "restart": true
    }
  ]
}
```

### 5.3 Memory leak hunting in Node.js

```bash
# Take heap snapshots programmatically
node --expose-gc -e "
  const v8 = require('v8');
  const fs = require('fs');

  global.gc();  // Force GC before snapshot
  const snapshot = v8.writeHeapSnapshot();
  console.log('Snapshot written to:', snapshot);
"

# Monitor memory usage over time
node -e "
  setInterval(() => {
    const used = process.memoryUsage();
    console.log(
      'RSS:', (used.rss / 1024 / 1024).toFixed(1), 'MB',
      'Heap:', (used.heapUsed / 1024 / 1024).toFixed(1), 'MB'
    );
  }, 5000);
"
```

### 5.4 Debugging async code

```ts
// Enable async stack traces (default in Node 16+)
// Errors will show the full async call chain

// Common async debugging pattern: add context to errors
async function processOrder(orderId: string) {
  try {
    const order = await fetchOrder(orderId);
    const payment = await chargePayment(order);
    return await fulfillOrder(order, payment);
  } catch (error) {
    // Wrap with context — don't lose the original stack
    throw new Error(`Failed to process order ${orderId}`, { cause: error });
  }
}
```

### 5.5 Why is Node.js not exiting?

```bash
# Find what's keeping Node alive
npm install why-is-node-running
```

```ts
import why from "why-is-node-running";

// After your work is done, if the process doesn't exit:
setTimeout(() => {
  why(); // Prints active handles keeping the process alive
}, 5000);
```

## 6. Python Debugging

### 6.1 Built-in debugger

```python
# Insert breakpoint anywhere in code
def process_data(items):
    result = []
    for item in items:
        breakpoint()  # Drops into pdb (or ipdb if installed)
        transformed = transform(item)
        result.append(transformed)
    return result

# pdb commands:
# n        — next line (step over)
# s        — step into function
# c        — continue to next breakpoint
# p expr   — print expression
# pp expr  — pretty print
# l        — show current code location
# w        — show call stack
# u/d      — move up/down the call stack
# b 42     — set breakpoint at line 42
# cl       — clear all breakpoints
# q        — quit debugger
```

### 6.2 ipdb (enhanced debugger)

```bash
pip install ipdb
```

```python
# Use ipdb instead of pdb for better UX (tab completion, syntax highlighting)
import ipdb; ipdb.set_trace()

# Or set as default debugger
# In ~/.bashrc or environment:
# export PYTHONBREAKPOINT=ipdb.set_trace
```

### 6.3 py-spy — Production profiling

```bash
pip install py-spy

# Profile a running process (no restart needed!)
py-spy top --pid 12345

# Generate flame graph
py-spy record -o flamegraph.svg --pid 12345

# Profile a script
py-spy record -o flamegraph.svg -- python my_script.py

# Dump current stack traces
py-spy dump --pid 12345
```

### 6.4 Memory profiling

```bash
pip install memory-profiler
```

```python
from memory_profiler import profile

@profile
def memory_intensive():
    data = [i ** 2 for i in range(1_000_000)]  # Watch memory spike here
    filtered = [x for x in data if x % 2 == 0]
    return len(filtered)

# Output shows per-line memory usage:
# Line #  Mem usage    Increment  Line Contents
# 4       45.2 MiB     0.0 MiB   @profile
# 5       45.2 MiB     0.0 MiB   def memory_intensive():
# 6       83.5 MiB    38.3 MiB       data = [i ** 2 for ...]
# 7       99.1 MiB    15.6 MiB       filtered = [x for ...]
```

### 6.5 tracemalloc — Built-in memory tracking

```python
import tracemalloc

tracemalloc.start()

# ... run your code ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")

print("Top 10 memory allocations:")
for stat in top_stats[:10]:
    print(stat)
```

## 7. System-Level Debugging

### 7.1 strace — Trace system calls

```bash
# Trace a running process
strace -p 12345

# Trace a command from start
strace -f node server.js  # -f follows child processes

# Only trace specific calls
strace -e trace=open,read,write node server.js

# Trace network calls only
strace -e trace=network node server.js

# Count call statistics
strace -c node server.js

# Output to file with timestamps
strace -tt -o trace.log node server.js
```

**Common findings:**
```
open("/etc/resolv.conf", O_RDONLY) = -1 ENOENT  ← DNS config missing
connect(3, {AF_INET, 10.0.0.5:5432}, 16) = -1 ETIMEDOUT  ← DB unreachable
write(1, "Error: ENOSPC\n", 14)  ← Disk full
```

### 7.2 Process inspection

```bash
# What files does a process have open?
lsof -p 12345

# What ports is a process listening on?
ss -tlnp | grep node

# Process resource usage
top -p 12345
# Or more detailed:
cat /proc/12345/status | grep -E "VmRSS|VmSize|Threads"

# File descriptors (detect fd leaks)
ls /proc/12345/fd | wc -l
```

### 7.3 tcpdump — Network packet capture

```bash
# Capture traffic on port 5432 (PostgreSQL)
sudo tcpdump -i any port 5432 -w capture.pcap

# Capture HTTP traffic to specific host
sudo tcpdump -i any host api.example.com and port 443

# Read captured packets
tcpdump -r capture.pcap

# Show packet contents as ASCII
sudo tcpdump -A -i any port 8080

# Count packets per source IP
sudo tcpdump -i any -c 1000 -nn 2>/dev/null | awk '{print $3}' | sort | uniq -c | sort -rn
```

## 8. Database Debugging

### 8.1 EXPLAIN ANALYZE

```sql
-- Always use ANALYZE to get actual execution times
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, count(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 20;
```

**Reading the output:**
```
Sort  (cost=1234..1235 rows=20 width=40) (actual time=45.2..45.3 rows=20 loops=1)
  Sort Key: (count(o.id)) DESC
  Sort Method: top-N heapsort  Memory: 27kB
  ->  HashAggregate  (cost=1200..1220 rows=500 width=40) (actual time=44.1..44.5 rows=500 loops=1)
        Group Key: u.id
        ->  Hash Right Join  (cost=100..800 rows=5000 width=40) (actual time=2.1..30.5 rows=5000 loops=1)
              ->  Seq Scan on orders o  (cost=0..500 rows=10000 width=16) (actual time=0.01..10.2 rows=10000 loops=1)
              ←── PROBLEM: Sequential scan on orders (missing index?)
```

**Key things to look for:**
- `Seq Scan` on large tables → missing index
- `actual rows` much larger than `rows` estimate → stale statistics (`ANALYZE table`)
- `loops=1000` → N+1 query pattern
- `Sort Method: external merge Disk` → not enough work_mem

### 8.2 Finding slow queries

```sql
-- PostgreSQL: enable slow query log
-- In postgresql.conf:
-- log_min_duration_statement = 100  (log queries > 100ms)

-- Find slow queries with pg_stat_statements
SELECT
  calls,
  round(total_exec_time::numeric, 2) as total_ms,
  round(mean_exec_time::numeric, 2) as mean_ms,
  round(max_exec_time::numeric, 2) as max_ms,
  left(query, 80) as query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

### 8.3 Lock debugging

```sql
-- Find blocked queries
SELECT
  blocked.pid AS blocked_pid,
  blocked.query AS blocked_query,
  blocking.pid AS blocking_pid,
  blocking.query AS blocking_query,
  now() - blocked.query_start AS blocked_duration
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid
JOIN pg_locks kl ON kl.locktype = bl.locktype
  AND kl.database IS NOT DISTINCT FROM bl.database
  AND kl.relation IS NOT DISTINCT FROM bl.relation
  AND kl.pid != bl.pid
JOIN pg_stat_activity blocking ON blocking.pid = kl.pid
WHERE NOT bl.granted;
```

### 8.4 N+1 query detection

```python
# Django: use django-debug-toolbar or nplusone
# pip install nplusone
INSTALLED_APPS = ['nplusone.ext.django', ...]
MIDDLEWARE = ['nplusone.ext.django.NPlusOneMiddleware', ...]
NPLUSONE_RAISE = True  # Raise exception on N+1

# SQLAlchemy: enable echo to see all queries
engine = create_engine("postgresql://...", echo=True)
# Count queries in tests
```

## 9. Network Debugging

### 9.1 curl deep dive

```bash
# Verbose output — see full request/response headers
curl -v https://api.example.com/health

# Show timing breakdown
curl -w "\
  DNS:        %{time_namelookup}s\n\
  Connect:    %{time_connect}s\n\
  TLS:        %{time_appconnect}s\n\
  TTFB:       %{time_starttransfer}s\n\
  Total:      %{time_total}s\n\
  HTTP Code:  %{http_code}\n\
  Size:       %{size_download} bytes\n" \
  -o /dev/null -s https://api.example.com/health

# Test specific HTTP method with headers
curl -X POST https://api.example.com/data \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"key": "value"}' \
  -w "\nHTTP %{http_code} in %{time_total}s\n"

# Follow redirects
curl -L -v https://example.com

# Ignore TLS errors (debugging only!)
curl -k https://self-signed.example.com

# Resolve to specific IP (bypass DNS)
curl --resolve api.example.com:443:10.0.0.5 https://api.example.com
```

### 9.2 DNS debugging

```bash
# Query DNS records
dig example.com A          # IPv4 address
dig example.com AAAA       # IPv6 address
dig example.com CNAME      # Canonical name
dig example.com MX         # Mail servers
dig example.com TXT        # TXT records (SPF, DKIM, verification)

# Use specific DNS server
dig @8.8.8.8 example.com

# Trace full resolution path
dig +trace example.com

# Check reverse DNS
dig -x 93.184.216.34

# Quick check
nslookup example.com
host example.com
```

### 9.3 SSL/TLS debugging

```bash
# Check certificate chain
openssl s_client -connect example.com:443 -servername example.com < /dev/null

# Check certificate expiry
openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Check supported TLS versions
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3

# Verify certificate chain
openssl verify -CAfile chain.pem server.pem
```

### 9.4 CORS debugging checklist

```
1. Check the browser console for the exact CORS error message
2. Verify the response includes:
   - Access-Control-Allow-Origin: <your origin or *>
   - Access-Control-Allow-Methods: <the method you're using>
   - Access-Control-Allow-Headers: <any custom headers>
3. For preflight requests (OPTIONS):
   - Is the server handling OPTIONS requests?
   - Is it returning 200/204 for OPTIONS?
   - Is Access-Control-Max-Age set for caching?
4. Common causes:
   - Origin mismatch (http vs https, port difference, www vs non-www)
   - Missing Access-Control-Allow-Credentials: true (for cookies)
   - Wildcard (*) origin not allowed with credentials
```

## 10. Memory Debugging

### 10.1 Common memory leak patterns

| Language | Common cause | Detection |
|----------|-------------|-----------|
| JavaScript | Event listeners not removed | Heap snapshot comparison |
| JavaScript | Closures capturing large objects | Heap snapshot retainer tree |
| JavaScript | Detached DOM nodes | DevTools Memory → "Detached" filter |
| JavaScript | Growing Map/Set/Array (cache without eviction) | Monitor `process.memoryUsage()` |
| Python | Circular references with `__del__` | `gc.get_referrers()`, `objgraph` |
| Python | Global/module-level caches | `tracemalloc` |
| Go | Goroutine leaks | `runtime.NumGoroutine()`, pprof |
| Go | Unclosed channels | `runtime.Stack()` |

### 10.2 JavaScript memory leak debugging workflow

```
1. Open DevTools → Memory tab
2. Take Heap Snapshot #1 (baseline)
3. Perform the suspected leaking action 5-10 times
4. Force GC (click trash can icon)
5. Take Heap Snapshot #2
6. Select Snapshot #2 → "Objects allocated between Snapshot 1 and Snapshot 2"
7. Sort by "Retained Size" descending
8. Inspect the retainer tree to find what's holding references
```

### 10.3 Container OOM debugging

```bash
# Check if process was OOM killed
dmesg | grep -i "oom\|killed"

# Check container memory limits
docker stats container_name

# Check Kubernetes pod events
kubectl describe pod my-pod | grep -A5 "Events"

# Set memory limits with monitoring
docker run --memory=512m --memory-swap=512m my-app

# Profile in container
docker exec -it container_name node --expose-gc --max-old-space-size=256 app.js
```

## 11. Performance Profiling

### 11.1 Flame graphs

```bash
# Node.js — generate flame graph
node --prof app.js
# Process the log
node --prof-process isolate-*.log > processed.txt

# Better: use 0x for automatic flame graph
npx 0x app.js
# Open the generated HTML flame graph

# Python — py-spy flame graph
py-spy record -o flamegraph.svg -- python app.py
# Open flamegraph.svg in browser

# Linux — perf + flame graph
perf record -g -p $(pgrep my-app)
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg
```

**Reading flame graphs:**
- X-axis = proportion of time (NOT chronological)
- Y-axis = call stack depth (bottom = entry point, top = leaf functions)
- Wide bars = functions consuming the most CPU time
- Look for "plateaus" — wide, flat tops indicate hot functions

### 11.2 Core Web Vitals debugging

| Metric | Target | How to debug |
|--------|--------|-------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | DevTools → Performance → "LCP" marker; check image loading, font loading, render-blocking resources |
| **INP** (Interaction to Next Paint) | < 200ms | DevTools → Performance → click "Interactions"; look for long tasks blocking the main thread |
| **CLS** (Cumulative Layout Shift) | < 0.1 | DevTools → Performance → "Layout Shifts"; add explicit width/height to images and ads |

```bash
# Measure from command line
npx lighthouse https://example.com --output=html --output-path=report.html

# Core Web Vitals in JavaScript
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

### 11.3 Load testing for debugging

```bash
# k6 — modern load testing
k6 run --vus 50 --duration 30s script.js

# wrk — simple HTTP benchmarking
wrk -t4 -c100 -d30s http://localhost:3000/api/users

# Apache Bench
ab -n 1000 -c 50 http://localhost:3000/api/health
```

## 12. Logging Strategies

### 12.1 Structured logging

```ts
// BAD: unstructured
console.log("User " + userId + " failed to login: " + error.message);

// GOOD: structured (JSON)
import pino from "pino";

const logger = pino({ level: "info" });

logger.error({
  event: "login_failed",
  userId,
  error: error.message,
  ip: request.ip,
  userAgent: request.headers["user-agent"],
}, "Login failed for user");
```

### 12.2 Log levels

| Level | When to use | Example |
|-------|-------------|---------|
| `fatal` | Application cannot continue | Database connection lost permanently |
| `error` | Operation failed, needs attention | Payment processing failed |
| `warn` | Unexpected but handled | Rate limit approaching threshold |
| `info` | Significant business events | User registered, order placed |
| `debug` | Detailed technical info | SQL query executed, cache hit/miss |
| `trace` | Very fine-grained | Function entry/exit, variable values |

### 12.3 Correlation IDs

```ts
// Generate a unique ID per request for tracing
import { randomUUID } from "crypto";

app.use((req, res, next) => {
  req.requestId = req.headers["x-request-id"]?.toString() ?? randomUUID();
  res.setHeader("x-request-id", req.requestId);

  // Attach to all logs for this request
  req.log = logger.child({ requestId: req.requestId });
  next();
});

// Now all logs from this request are correlated
app.get("/api/orders", (req, res) => {
  req.log.info({ userId: req.user.id }, "Fetching orders");
  // ...
  req.log.info({ count: orders.length }, "Orders fetched");
});
```

### 12.4 OpenTelemetry basics

```ts
// Distributed tracing across services
import { trace, context, SpanStatusCode } from "@opentelemetry/api";

const tracer = trace.getTracer("order-service");

async function processOrder(orderId: string) {
  return tracer.startActiveSpan("processOrder", async (span) => {
    try {
      span.setAttribute("order.id", orderId);

      const order = await tracer.startActiveSpan("fetchOrder", async (childSpan) => {
        const result = await db.orders.findById(orderId);
        childSpan.end();
        return result;
      });

      await tracer.startActiveSpan("chargePayment", async (childSpan) => {
        childSpan.setAttribute("payment.amount", order.total);
        await paymentService.charge(order);
        childSpan.end();
      });

      span.setStatus({ code: SpanStatusCode.OK });
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

## 13. Debugging in Production

### 13.1 Debug without redeploying

```ts
// Feature flag for debug mode
const debugMode = await featureFlags.isEnabled("debug-orders", {
  userId: currentUser.id,
});

if (debugMode) {
  logger.level = "debug";
  logger.debug({ order, paymentResult }, "Order processing debug info");
}
```

### 13.2 Safe debug endpoints

```ts
// Secure debug endpoint (requires admin role + API key)
app.get("/debug/connections", requireAdmin, requireApiKey, async (req, res) => {
  const pool = db.pool;
  res.json({
    total: pool.totalCount,
    idle: pool.idleCount,
    waiting: pool.waitingCount,
    activeQueries: await getActiveQueries(),
  });
});
```

### 13.3 Sentry error tracking

```ts
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1, // 10% of transactions
  beforeSend(event) {
    // Scrub PII
    if (event.request?.headers) {
      delete event.request.headers["authorization"];
      delete event.request.headers["cookie"];
    }
    return event;
  },
});

// Add context to errors
Sentry.setUser({ id: user.id, email: user.email });
Sentry.setTag("feature", "checkout");
Sentry.addBreadcrumb({
  category: "payment",
  message: `Charging ${amount} to card ending ${last4}`,
  level: "info",
});
```

## 14. Common Pitfalls

| Pitfall | Symptom | Investigation Approach |
|---------|---------|----------------------|
| Debugging the wrong environment | Fix works locally, not in staging | Compare env vars, node versions, OS; use `printenv` diff |
| Stale code running | Changes seem to have no effect | Hard refresh (Ctrl+Shift+R); restart dev server; check build output timestamps |
| Caching hiding the bug | Bug appears intermittently | Disable all caches (browser, CDN, Redis, ORM query cache); test in incognito |
| Race condition | Bug only happens under load or "randomly" | Add logging with timestamps; use `--inspect-brk` to slow execution; test with concurrent requests |
| Timezone bug | Dates off by hours; works in some regions | Log `new Date().toISOString()` at each step; check DB timezone settings; use UTC everywhere |
| Encoding issue | Garbled text, emoji broken, special chars wrong | Check Content-Type headers; verify UTF-8 at every boundary (DB, API, file I/O) |
| Silent error swallowed | Code does nothing; no error visible | Search for empty catch blocks; add `.catch(console.error)` to all promises |
| Missing await | Function returns Promise instead of value | TypeScript strict mode; search for `async` functions without `await` on calls |
| Circular dependency | Module is undefined at import time | Check import order; use dynamic imports; restructure to break the cycle |
| DNS resolution failure | "ENOTFOUND" errors in containers | Check `/etc/resolv.conf`; verify DNS from inside the container with `nslookup` |
| Connection pool exhaustion | Timeouts after running fine for hours | Monitor active connections; check for uncommitted transactions; add pool max/idle settings |
| Off-by-one error | Wrong count, missing first/last item | Log array lengths and indices; test boundary values: 0, 1, N-1, N |
| Environment variable missing | `undefined` used as string, silent failures | Log all env vars on startup (redacted); use zod to validate env at boot |
| File descriptor leak | "EMFILE: too many open files" | `lsof -p PID | wc -l`; check for unclosed streams, database connections, or file handles |
| Wrong dependency version | Code works in one project but not another | Check `npm ls package-name`; delete `node_modules` and reinstall; check for hoisting issues |
| Debugging minified code | Stack traces show line 1, column 43827 | Enable source maps; upload them to Sentry; use `--no-minify` for debugging |
