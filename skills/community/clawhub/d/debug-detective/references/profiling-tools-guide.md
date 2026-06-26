# Profiling Tools Guide

Comparison of profiling tools across languages and runtimes for CPU, memory, and I/O analysis.

---

## Python Profiling

### py-spy (Sampling Profiler)

**Install:** `pip install py-spy`

| Feature | Details |
|---------|---------|
| Type | Sampling profiler (low overhead) |
| Attach to running | Yes — `py-spy top --pid PID` |
| Flame graph | `py-spy record -o flame.svg -- python app.py` |
| Native extensions | Shows C/C++ frames with `--native` |
| Subprocesses | `--subprocesses` flag |
| Overhead | ~2-5% |

```bash
# Live top-like view of running process
py-spy top --pid 12345

# Record flame graph for 30 seconds
py-spy record -o profile.svg --duration 30 --pid 12345

# Profile a command from start
py-spy record -o flame.svg -- python manage.py runserver

# Show only lines taking >5% of time
py-spy top --pid 12345 --rate 100
```

### cProfile / profile (Built-in)

```bash
# Run with cProfile
python -m cProfile -s cumulative app.py

# Save to file and analyse with pstats
python -m cProfile -o output.prof app.py
python -c "
import pstats
p = pstats.Stats('output.prof')
p.sort_stats('cumulative').print_stats(20)
"

# Visualise with snakeviz
pip install snakeviz
snakeviz output.prof   # opens browser
```

| Option | Description |
|--------|-------------|
| `-s cumulative` | Sort by cumulative time |
| `-s tottime` | Sort by total time in function |
| `-s calls` | Sort by call count |
| `-o file.prof` | Save binary profile output |

### Scalene (CPU + Memory + GPU)

**Install:** `pip install scalene`

```bash
# Profile with CPU, memory, and GPU breakdown
scalene app.py

# Focus on specific file
scalene --cpu --memory --reduced-profile app.py

# Profile as JSON
scalene --json --outfile profile.json app.py
```

| Feature | Details |
|---------|---------|
| CPU time | Separates Python vs native (C) time |
| Memory | Tracks allocations per line |
| GPU | CUDA memory tracking |
| Copy volume | Identifies excessive copying |
| Overhead | ~20-30% |

### memray (Memory Profiler)

**Install:** `pip install memray`

```bash
# Record memory allocations
memray run app.py

# Generate flame graph
memray flamegraph output.bin -o memory.html

# Live view while running
memray run --live app.py

# Show top allocations
memray summary output.bin

# Generate table of allocations by location
memray table output.bin
```

---

## Node.js Profiling

### node --prof (V8 Built-in)

```bash
# Record V8 profile (creates isolate-*.log)
node --prof app.js

# Process the log into readable output
node --prof-process isolate-0x*.log > processed.txt

# Key sections in output:
#   [Summary]        — time breakdown by category
#   [JavaScript]     — JS function hotspots
#   [C++]            — native code hotspots
#   [Bottom up]      — callee → caller chains
```

### node --inspect (Chrome DevTools)

```bash
# Start with inspector
node --inspect app.js

# Break on first line
node --inspect-brk app.js

# Then open: chrome://inspect in Chrome
# Click "inspect" on the listed target
```

**DevTools profiling workflow:**
1. Open chrome://inspect → click "inspect"
2. Go to **Performance** tab → click Record
3. Do the action you want to profile
4. Stop recording → analyse flame chart

### 0x (Flame Graph Generator)

**Install:** `npm install -g 0x`

```bash
# Generate flame graph (opens browser automatically)
0x app.js

# With custom port
0x -p 3000 app.js

# Output as SVG instead of interactive HTML
0x --output-dir ./profiles app.js

# Profile for specific duration
0x --collect-delay 5000 app.js
```

| Feature | Details |
|---------|---------|
| Type | Sampling via V8 profiler |
| Output | Interactive HTML flame graph |
| Overhead | Low when sampling |
| Best for | Finding CPU hotspots in Node.js |

### clinic.js (Diagnostic Suite)

**Install:** `npm install -g clinic`

```bash
# Doctor — auto-detects common issues
clinic doctor -- node app.js

# Flame — CPU flame graph
clinic flame -- node app.js

# Bubbleprof — async I/O analysis
clinic bubbleprof -- node app.js

# Heap profiler — memory analysis
clinic heapprofiler -- node app.js
```

| Tool | Detects |
|------|---------|
| `doctor` | Event loop delays, I/O issues, GC pressure, active handles |
| `flame` | CPU hotspots (built on 0x) |
| `bubbleprof` | Async flow bottlenecks, I/O patterns |
| `heapprofiler` | Memory leaks, allocation hotspots |

---

## System-Level Profiling (Linux)

### perf (Linux Performance Counter)

```bash
# Record CPU profile of a process
sudo perf record -g -p PID

# Record a specific command
sudo perf record -g -- node app.js

# Show report (interactive TUI)
sudo perf report

# Show top functions
sudo perf top -p PID

# Generate flame graph (with Brendan Gregg's tools)
sudo perf record -F 99 -g -p PID -- sleep 30
sudo perf script > out.perf
./stackcollapse-perf.pl out.perf > out.folded
./flamegraph.pl out.folded > flame.svg

# Stat summary (counters: cache misses, branch mispredictions, etc.)
sudo perf stat -d -- ./myprogram
```

| Feature | Details |
|---------|---------|
| Type | Hardware performance counters + software events |
| Overhead | Very low (~1-3%) |
| Scope | System-wide or per-process |
| Output | Interactive TUI, scriptable text |
| Root required | Yes (or `perf_event_paranoid` sysctl) |

### Flame Graphs (Brendan Gregg Method)

```bash
# Clone the flame graph tools
git clone https://github.com/brendangregg/FlameGraph.git

# Workflow: perf → collapse → flamegraph
sudo perf record -F 99 -a -g -- sleep 30
sudo perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > flame.svg

# For Node.js (using perf with --perf-basic-prof)
node --perf-basic-prof app.js &
sudo perf record -F 99 -p $! -g -- sleep 30
sudo perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > node-flame.svg
```

**Reading a flame graph:**

| Element | Meaning |
|---------|---------|
| X axis | Alphabetical stack sort (NOT time) |
| Y axis | Stack depth (bottom = entry point) |
| Width | % of total samples (wider = more CPU time) |
| Colour | Random warm palette (no special meaning) |
| Plateau | Wide flat top = function spending lots of CPU |
| Narrow tower | Deep call stack but fast |

### strace / ltrace

```bash
# Trace system calls
strace -p PID
strace -e trace=network -p PID      # network calls only
strace -e trace=file -p PID         # file operations only
strace -c -p PID                    # summary: call counts and times
strace -T -p PID                    # show time spent in each syscall
strace -f -p PID                    # follow child processes/threads

# Trace library calls
ltrace -p PID
ltrace -c -p PID                    # summary
```

---

## Database Query Profiling

### PostgreSQL

```sql
-- Enable timing
\timing on

-- Basic EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN with actual execution
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'test@example.com';

-- Log slow queries (in postgresql.conf)
-- log_min_duration_statement = 100   -- log queries > 100ms

-- pg_stat_statements extension (top queries by time)
SELECT query, calls, total_exec_time, mean_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

### MySQL

```sql
-- Enable profiling for session
SET profiling = 1;

-- Run your query
SELECT * FROM users WHERE email = 'test@example.com';

-- Show profile
SHOW PROFILES;
SHOW PROFILE FOR QUERY 1;

-- EXPLAIN
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Slow query log (in my.cnf)
-- slow_query_log = 1
-- long_query_time = 0.1
```

---

## Tool Selection Matrix

| Scenario | Python | Node.js | System |
|----------|--------|---------|--------|
| **CPU hotspot** | py-spy | 0x / clinic flame | perf |
| **Memory leak** | memray / Scalene | clinic heapprofiler / --inspect | Valgrind |
| **Async bottleneck** | — | clinic bubbleprof | strace |
| **Line-by-line** | Scalene / cProfile | --prof-process | perf annotate |
| **Production safe** | py-spy (low overhead) | 0x (sampling) | perf record |
| **Quick overview** | cProfile | clinic doctor | perf stat |
| **Flame graph** | py-spy record | 0x / clinic flame | perf + FlameGraph |
| **GPU profiling** | Scalene | — | nvidia-smi / nsys |

## Quick Decision Tree

```
Is the app slow?
├── CPU-bound? ──→ Use flame graph (py-spy / 0x / perf)
├── Memory issue? ──→ Use heap profiler (memray / clinic heapprofiler)
├── I/O-bound? ──→ Use async profiler (clinic bubbleprof / strace)
├── Database slow? ──→ EXPLAIN ANALYZE + pg_stat_statements
└── Network slow? ──→ DevTools Network tab + curl timing
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Profiling in development only | Production has different behaviour — use low-overhead tools (py-spy, perf) in prod |
| Ignoring warm-up | First requests include JIT compilation — run warm-up before profiling |
| Micro-benchmarking | Isolated benchmarks miss system interactions — profile realistic workloads |
| Not using flame graphs | Flat profiles hide call-chain context — always generate flame graphs for CPU issues |
| Profiling with debugger attached | Debuggers add overhead — profile without breakpoints or debug mode |
| Root cause vs symptom | High CPU in GC means memory issue, not CPU issue — look deeper |
| Forgetting to check I/O | CPU profilers miss I/O waits — combine with strace or async profilers |
