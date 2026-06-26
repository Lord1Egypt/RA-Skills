---
name: dotnet-dump-perf-analyzer
version: 1.0.1
description: >
  End-to-end .NET application performance diagnostics using the dotnet diagnostic toolchain
  — dotnet-dump, dotnet-counters, dotnet-trace, WinDbg, and PAL thresholds.
  Covers CPU hotspots, GC pressure, managed memory leaks, thread pool exhaustion,
  and system-level resource contention. Generates interactive HTML reports.
  Works for ASP.NET Core, ASP.NET on IIS, WPF, and Console apps on Windows, Linux, and macOS.
tags:
  - dotnet
  - performance
  - diagnostics
  - dotnet-dump
  - dotnet-counters
  - dotnet-trace
  - dotnet-gcdump
  - memory-leak
  - gc
  - aspnetcore
  - iis
  - w3wp
  - windbg
  - perfmon
  - perfview
  - PAL
  - dotmemory
  - html-report
  - cpu-profiling
---

# dotnet-dump-perf-analyzer

> **Core focus**: .NET application performance diagnosis — CPU profiling, GC analysis,
> managed memory leak hunting, and thread pool diagnostics.
> Windows perfmon / relog / HTML reporting are optional supplements covered at the end.

---

## Use Cases

- ASP.NET Core / ASP.NET on IIS / WPF / Console apps with sustained high CPU, frequent GC, or slow response
- .NET apps with memory leaks or continuously growing working set
- Want to find which method or request path is causing the bottleneck
- Need to compare metrics against industry benchmarks (PAL thresholds) and produce a visual report
- Team lacks dotMemory / ANTS Performance Profiler license — need a free open-source alternative

---

## Toolchain Overview

| Stage | Tool | Purpose |
|-------|------|---------|
| **Rapid triage** | `dotnet-counters` | Live CPU, GC, thread pool metrics — no restart needed |
| **Deep sampling** | `dotnet-trace` | CPU sampling trace collection (Windows, Linux, macOS) |
| **Dump capture** | `dotnet-dump` | Full-process core dump of a running app (all platforms) |
| **Heap snapshot** | `dotnet-gcdump` | GC heap-only dump, smaller than full dump |
| **System metrics** | `perfmon` + `relog.exe` | OS-level CPU/mem/disk/net counters including Process V2 |
| **Dump analysis** | `dotnet-dump analyze` / **WinDbg** | Inspect objects, heap, threads in a dump |
| **GC analysis** | `dotnet-counters` + PAL | GC frequency and pause time vs. thresholds |
| **Report generation** | Python + Chart.js | Dark-themed interactive HTML dashboard |

> **Note**: dotnet-dump, dotnet-counters, dotnet-trace, and dotnet-gcdump are all bundled
> with the [.NET diagnostic tools](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/).
> Install the .NET SDK and you have them all. WinDbg requires a separate install (see the
> Tool Downloads table below).

---

## Core Workflow

### Step 1 — Live Diagnostics: Real-Time Counters (No Code Changes)

**Goal**: Observe CPU, GC, and thread pool anomalies without restarting the app or adding logging.

```bash
# Install (if not already present)
dotnet tool install -g dotnet-counters

# List all available .NET processes
dotnet-counters ps

# Monitor a target process (PID or process name)
dotnet-counters monitor -p <PID> --counters "System.Runtime,Microsoft.AspNetCore.Http.Connections"
```

Key counters to watch (press Ctrl+C to stop):

| Counter | Normal range | Alert signal |
|---------|-------------|--------------|
| `cpu-usage` | < 80% | Consistently > 90% |
| `gen-0-collected / sec` | < 1000 | Consistently > 5000 |
| `gen-1-collected / sec` | < 100 | Consistently > 500 |
| `gen-2-collected / sec` | < 10 | Consistently > 50 |
| `threadpool-queue-length` | < 10 | Consistently > 50 |
| `threadpool-thread-count` | — | Approaching ThreadPool MinThreads limit |

---

### Step 2 — Deep Sampling: dotnet-trace (Pinpoint Hot Methods)

**Goal**: Identify which methods consume the most CPU time.

```bash
# Install (if not already present)
dotnet tool install -g dotnet-trace

# Sample the target process for 60 seconds
dotnet-trace collect -p <PID> --duration 00:01:00 -o app_trace.nettrace

# (Works on Linux/macOS too — no .NET Runtime support dependency)
```

Open the resulting `.nettrace` file with:
- **Visual Studio 2022** (built-in Performance Viewer)
- **[PerfView](https://github.com/Microsoft/perfview/releases)** — free, supports CPU sampling, GC Heap, .NET Runtime events
- **dotnet-trace** CLI (outputs Top-N methods directly)

```bash
# CLI report
dotnet-trace report app_trace.nettrace --type cpu
```

---

### Step 3 — Dump Capture: dotnet-dump (Offline Deep Dive)

**Goal**: Capture a process dump at the moment of failure for post-mortem analysis.

```bash
# Install (if not already present)
dotnet tool install -g dotnet-dump

# List .NET processes
dotnet-dump ps

# Capture full dump
dotnet-dump collect -p <PID> -o app_dump.dmp
```

**When to capture a dump**:
- CPU spike peak moment (capture immediately when `dotnet-counters` shows a spike)
- Memory leak trend is clear (working set is growing continuously)
- Requests are starting to timeout / thread pool is exhausting

---

### Step 4 — Dump Analysis: dotnet-dump analyze (Managed Heap / Threads)

```bash
dotnet-dump analyze app_dump.dmp

# Common REPL commands:
dumpheap -stat              # Heap summary by type (find largest instances)
dumpheap -type <TypeName>  # All instances of a specific type
gcroot <object_address>     # GC Root chain (root cause of leaks)
threads                     # List all threads and their stacks
setclrpath <path>           # Set .NET Runtime path (required for full dumps)
```

> **Linux dump caveat**: When analyzing a Linux `.dmp` on Windows, configure the SOS
> extension's Runtime path first:
> ```
> setclrpath /usr/share/dotnet/shared/Microsoft.NETCore.App/<version>/
> ```

---

### Step 5 — System-Level Metrics: perfmon + relog (Optional)

> This is a **Windows-only** supplement for OS-level system resource visibility.
> If `dotnet-counters` already pinpointed the in-process issue, you can skip this step.

#### 5.1 Collection Setup (perfmon GUI)

1. Win+R → `perfmon` → Performance Monitor
2. Right-click Data Collector Sets → User Defined → New
3. Add these counters:

```
\Processor Information(_Total)\% Processor Time
\Processor(_Total)\% Processor Time
\System\Processor Queue Length
\Memory\Available MBytes
\Memory\Committed Bytes
\PhysicalDisk(_Total)\Avg. Disk Queue Length
\PhysicalDisk(_Total)\Avg. Disk sec/Read
\PhysicalDisk(_Total)\Avg. Disk sec/Write
\TCPv4\Segments Retransmitted/sec
\Process V2(*)\% Processor Time
\Process V2(*)\Working Set
\Process V2(*)\ID Process
\ASP.NET Applications(*)\Requests/Sec
\ASP.NET Apps v4.0.30319(*)\Requests Current
```

> Use **`Process V2`** instead of the legacy `Process` counter — `Process V2` supports
> the `name:PID` format to distinguish multiple instances of the same process name
> (e.g., multiple w3wp.exe worker processes).

Recommended interval: **15 seconds** (production monitoring) or **5 seconds** (problem reproduction).
4. Start collection, then export the `.blg` file when done.

#### 5.2 BLG → CSV Conversion (using relog.exe)

> **Pitfall**: Do NOT use PowerShell's `Export-Counter -Format CSV` (it still outputs BLG).
> Also avoid calling `relog` directly in PowerShell with quoted arguments — nested
> quotes break path parsing. Use `System.Diagnostics.ProcessStartInfo` instead.

```powershell
# export_blg.ps1
$blgPath = "<path-to-BLG-file>"    # e.g., C:\Logs\DataCollector01.blg
$csvPath = "<output-CSV-path>"      # e.g., C:\Logs\output.csv

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "relog.exe"
$psi.Arguments = "`"$blgPath`" -f CSV -o `"$csvPath`" -y"
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError  = $true
$psi.CreateNoWindow = $true

$proc = [System.Diagnostics.Process]::Start($psi)
$stdout = $proc.StandardOutput.ReadToEnd()
$stderr = $proc.StandardError.ReadToEnd()
$proc.WaitForExit()

if ($proc.ExitCode -eq 0 -and (Test-Path $csvPath)) {
    Write-Host "Success! Size: $([math]::Round((Get-Item $csvPath).Length/1MB,2)) MB"
}
```

> `relog.exe` is a Windows built-in at `C:\Windows\System32\relog.exe` — no separate install needed.

---

### Step 6 — Python Analysis + HTML Report

Save the script below as `analyze_perf.py`, update `csv_path` and `output_html`, then run it.

```python
# analyze_perf.py — perfmon BLG → Process CPU + System Baselines + PAL + HTML Report
# -*- coding: utf-8 -*-
import csv, os, re, sys, statistics
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except: pass

csv_path    = r"<path-to-CSV>"       # e.g., C:\Logs\output.csv
output_html = r"<output-HTML-path>"  # e.g., C:\Logs\perf_report.html

# ── Read CSV ─────────────────────────────────────────────────────────────────
with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
    all_rows = list(csv.reader(f))
headers   = all_rows[0]
data_rows = all_rows[1:]
print(f"Rows: {len(data_rows)}, Fields: {len(headers)}")

# ── Locate Process V2 % Processor Time counters ───────────────────────────────
# Format: \\HOSTNAME\Process V2(name:PID)\% Processor Time
proc_cpu_cols = {}
for i, h in enumerate(headers):
    if 'Process V2' in h and '% Processor Time' in h and '(_Total)' not in h:
        parts = h.split('\\')
        if len(parts) >= 4:
            m = re.search(r'Process V2\(([^:]+):(\d+)\)', parts[3])
            if m:
                proc_cpu_cols[i] = (m.group(1).lower(), m.group(2))
print(f"Found {len(proc_cpu_cols)} process CPU counters")

# ── Aggregate CPU by process name ────────────────────────────────────────────
proc_cpu_times = defaultdict(list)
for row in data_rows:
    snap = defaultdict(float)
    for ci, (pname, _) in proc_cpu_cols.items():
        if ci < len(row):
            v = row[ci].strip().strip('"')
            if v and v not in ('', 'N/A'):
                try: snap[pname] += float(v)
                except: pass
    for pname, val in snap.items():
        proc_cpu_times[pname].append(val)

# ── Statistics ────────────────────────────────────────────────────────────────
proc_stats = []
for pname, times in proc_cpu_times.items():
    if len(times) >= 3:
        srt = sorted(times)
        proc_stats.append({
            'name': pname, 'avg': statistics.mean(times),
            'max': max(times), 'p90': srt[int(len(srt)*0.9)], 'n': len(times)
        })
proc_stats.sort(key=lambda x: x['avg'], reverse=True)

print("\nTop 15 Processes by CPU:")
print(f"{'Rank':<4} {'Process':<28} {'Avg%':>7} {'Max%':>7} {'P90%':>7}")
for i, s in enumerate(proc_stats[:15], 1):
    print(f"{i:<4} {s['name']:<28} {s['avg']:>7.2f} {s['max']:>7.2f} {s['p90']:>7.2f}")

# ── System baseline counters ─────────────────────────────────────────────────
BASELINE = {
    'CPU%':         lambda h: 'Processor Information(_Total)' in h and '% Processor Time' in h,
    'Proc Queue':   lambda h: 'Processor Queue Length' in h,
    'Mem Avail MB': lambda h: 'Memory' in h and 'Available MBytes' in h,
    'Disk Queue':   lambda h: 'PhysicalDisk(_Total)' in h and 'Avg. Disk Queue' in h,
    'TCP Retrans':  lambda h: 'TCP' in h and 'Retransmitted' in h,
    'Disk Read ms': lambda h: 'PhysicalDisk(_Total)' in h and 'Disk sec/Read' in h,
    'Disk Write ms':lambda h: 'PhysicalDisk(_Total)' in h and 'Disk sec/Write' in h,
}
bl_cols = {}
for i, h in enumerate(headers):
    hc = h.strip()
    for name, fn in BASELINE.items():
        if fn(hc) and name not in bl_cols:
            bl_cols[name] = i

bl_stats = {}
for name, ci in bl_cols.items():
    vals = []
    for row in data_rows:
        v = row[ci].strip().strip('"') if ci < len(row) else ''
        if v and v not in ('', 'N/A'):
            try: vals.append(float(v))
            except: pass
    if vals:
        srt = sorted(vals)
        bl_stats[name] = {
            'avg': statistics.mean(vals), 'max': max(vals),
            'p90': srt[int(len(srt)*0.9)], 'n': len(vals)
        }

# ── PAL threshold check ───────────────────────────────────────────────────────
PAL = [
    ('CPU%',          85,  95),
    ('Proc Queue',     2,   4),
    ('TCP Retrans',    1,   5),
    ('Disk Queue',     2,   4),
    ('Disk Read ms',  10,  20),
    ('Disk Write ms', 10,  20),
]
print("\nPAL Threshold Check:")
for name, warn, crit in PAL:
    if name in bl_stats:
        s = bl_stats[name]
        st = 'CRITICAL' if s['max'] >= crit else ('WARNING' if s['max'] >= warn else 'OK')
        print(f"  [{st:8}] {name:<15} avg={s['avg']:>8.2f} max={s['max']:>8.2f} P90={s['p90']:>8.2f}")

# ── Time-series + high-CPU periods + HTML generation ──────────────────────────
# (See the full HTML generation code in the Chinese SKILL.md for the complete script)
print("\nDone. See the full HTML generation block for chart output.")
```

> Python 3.8+ includes the `statistics` stdlib — no pip install needed.
> Chart.js is loaded via CDN, no local dependency either.

---

### Step 7 — WinDbg: Advanced Dump Analysis

When `dotnet-dump analyze` is not enough (e.g., native heap, GC Card Table, Loader Heap analysis),
use WinDbg (supports both kernel and user mode).

```bash
# Load SOS for managed heap analysis
.loadby sos clr                    # .NET 4 uses .loadby sos mscorwks
!dumpheap -stat                    # Heap summary
!gcroot <object_addr>             # GC Root tracing
!threads                           # All threads
!clrstack                          # Managed call stack
!dumpasync -roots                  # AsyncStateMachine leak detection
```

> **SOS / SOSEX extensions**:
> .NET Framework: `C:\Windows\Microsoft.NET\Framework64\<version>\sos.dll` (built-in)
> .NET Core / .NET 5+: ships with dotnet-dump; load with `.load <path>/sos.dll`

---

## Tool Download Reference

| Tool | Download | Notes |
|------|----------|-------|
| **.NET SDK** | https://dotnet.microsoft.com/download/dotnet | Install once, get all dotnet diagnostic tools |
| **dotnet-dump** | `dotnet tool install -g dotnet-dump` | Bundled with SDK |
| **dotnet-counters** | `dotnet tool install -g dotnet-counters` | Bundled with SDK |
| **dotnet-trace** | `dotnet tool install -g dotnet-trace` | Bundled with SDK |
| **dotnet-gcdump** | `dotnet tool install -g dotnet-gcdump` | Bundled with SDK |
| **PerfView** | https://github.com/Microsoft/perfview/releases | CPU sampling, GC Heap, .NET Runtime events |
| **WinDbg (Store)** | https://apps.microsoft.com/detail/windbg | Modern WinDbg from Microsoft Store |
| **WinDbg Preview** | https://apps.microsoft.com/detail/windbg | UWP WinDbg with better UX |
| **dotMemory** | https://www.jetbrains.com/profiler/ | JetBrains — free CLI edition available |
| **Windows Performance Toolkit** | https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/ | Includes WPR and WPA for WPR trace analysis |

> All dotnet diagnostic tools are installed via `dotnet tool install -g <tool-name>`.
> For offline environments, pre-download on a machine with internet access first.

---

## .NET Performance Troubleshooting Quick Reference

| Symptom | First check | Tool |
|---------|-------------|------|
| CPU continuously high | Top methods, full sampling | `dotnet-trace` + PerfView CPU view |
| CPU intermittent spikes | GC pauses, high-frequency GC | `dotnet-counters` watching GC counters |
| Memory continuously growing | Managed heap leak | `dotnet-dump` + `dumpheap -stat` |
| Memory leak persists after GC | Large object heap, GC Root | `dotnet-dump analyze` + `gcroot` |
| Request queue backlog | IIS AppPool Queue Length, thread pool | `perfmon` Processor Queue + dotnet-counters |
| GC pause time too long | GC event pause time | `dotnet-counters` GC pause time / PerfView GC events |
| Thread pool exhaustion | Queue Length + Thread Count | `dotnet-counters` threadpool-* |
| Slow HTTP requests | Hot request paths, DB calls | `dotnet-trace` + custom trace sources |
| Slow startup | NGEN, Assembly Load, JIT | PerfView Startup diagnostics |

---

## PAL 2.8.1 .NET / IIS Reference Thresholds

| Counter | Warning | Critical | Notes |
|---------|---------|----------|-------|
| `Processor(_Total)\% Processor Time` | 85% | 95% | |
| `System\Processor Queue Length` | 2 | 4 | |
| `\ASP.NET Apps v4.0.30319(*)\Requests Executing` | 40 | 80 | IIS-hosted .NET 4.x |
| `\ASP.NET Apps v4.0.30319(*)\Requests Wait` | 10 | 25 | |
| `TCP\Segments Retransmitted/sec` | 1 | 5 | |
| `PhysicalDisk\Avg. Disk Queue Length` | 2 | 4 | |
| `PhysicalDisk\Avg. Disk sec/Read (ms)` | 10 ms | 20 ms | |
| `PhysicalDisk\Avg. Disk sec/Write (ms)` | 10 ms | 20 ms | |
| `Memory\% Committed Bytes In Use` | 80% | 90% | |

> PAL (Performance Analysis of Logs) is Microsoft's official IIS/DotNet performance baseline tool.
> Download: https://github.com/clinthuffman/PAL

---

## Common Pitfalls & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| `dotnet-counters ps` can't find the process | Process is 32-bit or running on a different Runtime | Check .NET Runtime version, use `dotnet-counters ps -v` for details |
| dotnet-trace fails on Linux | Missing `lttng` or insufficient permissions | Use `sudo dotnet-trace collect ...` or install `lttng` |
| `.loadby sos clr` fails in WinDbg | 32/64-bit mismatch or Runtime version issue | Use `.load <full-path>\sos.dll`, confirm correct bitness |
| Dump file is huge (tens of GB) | Captured full dump from a large-memory app | Use `dotnet-dump collect -m 1` to limit to heap-only dump |
| CSV columns are misaligned | `relog.exe` vs `Export-Counter` — the latter omits quotes around values | Always use relog.exe for CSV export |
| Can't find Process V2 counters | Collected using the legacy `Process` counter instead | Re-collect with `Process V2` checked in perfmon |
| SOS commands fail in `dotnet-dump analyze` | Full dump requires Runtime path to be set | Run `setclrpath <dotnet-shared-lib-path>` before SOS commands |
| Windows console shows garbled text for emoji | cp936 encoding doesn't support emoji | Add `sys.stdout.reconfigure(encoding='utf-8')` at the top of the script |
| High GC frequency but heap size is stable | Many short-lived objects — may be normal or an allocation pattern issue | Use `dotnet-trace` sampling to identify allocation hotspots |
