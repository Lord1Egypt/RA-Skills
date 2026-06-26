# concurrencyguard

<p align="center">
  <img src="https://img.shields.io/badge/patterns-90+-blue" alt="90+ patterns">
  <img src="https://img.shields.io/badge/categories-6-purple" alt="6 categories">
  <img src="https://img.shields.io/badge/languages-6-orange" alt="6 languages">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Find the race conditions hiding in your code. Fix them before production does.</h3>

<p align="center">
  <a href="https://concurrencyguard.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#detection-categories">Categories</a> &middot;
  <a href="https://concurrencyguard.pages.dev/#pricing">Pricing</a>
</p>

---

## Your codebase has concurrency bugs. Hidden ones.

Race conditions are the hardest bugs to find. They happen intermittently. They pass all your tests. They only surface under load in production -- corrupting data, causing deadlocks, producing wrong results silently.

Unprotected shared state. Missing mutexes. Check-then-act without synchronization. Await inside loops instead of Promise.all. Thread-unsafe singletons. Inconsistent lock ordering. Fire-and-forget promises. Non-atomic read-modify-write operations.

These patterns are predictable. They follow recognizable code shapes. ConcurrencyGuard finds them.

**90+ concurrency safety patterns across 6 languages.** JS/TS, Python, Java, Go, Rust, C#. Pre-commit hooks. Local scanning. Markdown reports. Zero data leaves your machine.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install concurrencyguard

# 2. Scan your repo
concurrencyguard scan

# 3. Install pre-commit hooks (free)
concurrencyguard hook install
```

That's it. Every commit is now scanned for concurrency issues before it lands.

## What It Does

### Scan files for concurrency hazards
One command to scan any file, directory, or your entire repo. 90+ regex patterns detect concurrency issues across shared state, locking, atomicity, async/await, thread safety, and deadlock risk.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged file. If concurrency issues are detected, the commit is blocked with a clear remediation message.

### Generate concurrency safety reports
Produce markdown reports with severity breakdowns, hazard categories, and remediation priority. Ideal for code reviews and architecture audits.

### Continuous watch mode (Pro)
Monitor your codebase in real time during development. Every file save triggers a re-scan and immediate feedback on new concurrency issues.

### CI/CD integration (Pro)
Strict exit codes and machine-readable output for GitHub Actions, GitLab CI, Jenkins, and any CI system.

### Team-level reporting (Team)
Aggregate concurrency metrics across your team with hotspot analysis, per-module breakdowns, and trend indicators for sprint retrospectives.

### Baseline known issues (Team)
Record existing concurrency issues in legacy codebases so future scans only report new hazards. Allowlist files let teams manage known exceptions.

## How It Compares

| Feature | ConcurrencyGuard | ThreadSanitizer | go vet | RacerD | CHESS |
|---------|:----------------:|:---------------:|:------:|:------:|:-----:|
| Static analysis (no runtime) | Yes | No | Partial | Yes | No |
| Multi-language (6 langs) | Yes | C/C++ | Go only | Java | C# |
| Pre-commit hooks | Yes | No | No | No | No |
| Score & grades | Yes | No | No | No | No |
| Baseline/allowlist | Yes | No | No | No | No |
| Zero config scan | Yes | Build integration | Go toolchain | Build integration | Build integration |
| No binary deps | Yes | LLVM | Go toolchain | Build system | .NET |
| Markdown reports | Yes | No | No | No | No |
| CI/CD integration | Yes | Manual | Manual | Manual | Manual |
| Local-only (no cloud) | Yes | Yes | Yes | Yes | Yes |
| Zero telemetry | Yes | Yes | Yes | Yes | Yes |
| ClawHub integration | Yes | No | No | No | No |
| Price (individual) | Free/$19/mo | Free | Free | Free | Free |

## Detection Categories

ConcurrencyGuard detects 90+ concurrency safety patterns across 6 categories:

### Shared State (SS) -- 15 patterns

| Check ID | Severity | Description |
|----------|----------|-------------|
| SS-001 | Critical | Global mutable variable accessed without synchronization |
| SS-002 | Critical | Unprotected static mutable field in Java/C# |
| SS-003 | High | Module-level mutable state in Python (shared across threads) |
| SS-004 | High | Shared variable without volatile/atomic annotation |
| SS-005 | Critical | Global object mutation in Node.js worker threads |
| SS-006 | High | Mutable class variable shared between threads |
| SS-007 | High | Static collection modified without synchronization |
| SS-008 | Medium | Unprotected global counter or accumulator |
| SS-009 | High | Shared mutable Map/Dict without concurrent variant |
| SS-010 | Critical | Go global variable modified in goroutine |
| SS-011 | High | Rust unsafe mutable static reference |
| SS-012 | Medium | Module-level list/array mutation in Python |
| SS-013 | High | Shared buffer/array without synchronization |
| SS-014 | Medium | Global configuration object modified at runtime |
| SS-015 | High | Thread-local storage not used for per-thread state |

### Locking & Mutex (LK) -- 15 patterns

| Check ID | Severity | Description |
|----------|----------|-------------|
| LK-001 | Critical | Missing synchronized keyword on shared method in Java |
| LK-002 | Critical | Missing lock statement in C# for shared resource |
| LK-003 | Critical | Missing mutex.Lock()/Unlock() in Go for shared state |
| LK-004 | Critical | Lock acquired without corresponding Unlock/Release |
| LK-005 | High | Nested lock acquisition (deadlock risk) |
| LK-006 | High | Missing RWMutex for read-heavy shared data in Go |
| LK-007 | Medium | Spin lock implementation in user code |
| LK-008 | High | Lock not deferred in Go (risk of missing unlock on panic) |
| LK-009 | High | Missing threading.Lock() in Python for shared state |
| LK-010 | Critical | Lock/Unlock on different code paths (conditional unlock) |
| LK-011 | Medium | Using basic Lock where RLock is appropriate |
| LK-012 | High | Mutex not held during condition variable wait |
| LK-013 | High | Missing lock in C# property getter/setter |
| LK-014 | Medium | Manual lock implementation instead of language primitives |
| LK-015 | High | Sync.Mutex value copied in Go (pass by value) |

### TOCTOU & Atomicity (TC) -- 15 patterns

| Check ID | Severity | Description |
|----------|----------|-------------|
| TC-001 | Critical | Check-then-act without synchronization (generic) |
| TC-002 | Critical | File exists check followed by file open (TOCTOU) |
| TC-003 | Critical | Read-modify-write without compare-and-swap (CAS) |
| TC-004 | High | Double-checked locking without volatile/atomic |
| TC-005 | Critical | Non-atomic counter increment (i++ on shared variable) |
| TC-006 | High | Compare-and-swap needed for conditional update |
| TC-007 | Critical | Get-then-put on Map without atomic operation |
| TC-008 | High | Test-and-set without atomic instruction |
| TC-009 | Critical | Non-atomic boolean flag for thread communication |
| TC-010 | High | Check-if-null-then-create without synchronization |
| TC-011 | Critical | Balance check then debit without transaction isolation |
| TC-012 | High | Collection size check followed by index access |
| TC-013 | Medium | Non-atomic file write (no rename-based atomic write) |
| TC-014 | High | Database read-check-write without SELECT FOR UPDATE |
| TC-015 | Critical | Non-atomic publish of multi-field state |

### Async/Await Pitfalls (AW) -- 15 patterns

| Check ID | Severity | Description |
|----------|----------|-------------|
| AW-001 | High | Await inside loop (sequential instead of parallel) |
| AW-002 | Critical | Missing await on async function call |
| AW-003 | High | Async void method (unobserved exceptions in C#) |
| AW-004 | Critical | Fire-and-forget promise (no .catch or await) |
| AW-005 | High | Race condition in state update after await point |
| AW-006 | High | Missing Promise.all/Promise.allSettled for parallel ops |
| AW-007 | Medium | Async function without try/catch error handling |
| AW-008 | High | Shared mutable state across await boundaries |
| AW-009 | Critical | Multiple awaits on same promise (double resolution) |
| AW-010 | High | Callback-based API mixed with async/await |
| AW-011 | Medium | Missing error propagation in promise chain |
| AW-012 | High | Async generator without proper cleanup |
| AW-013 | Critical | Unhandled promise rejection (no rejection handler) |
| AW-014 | Medium | Sequential async calls that could be parallel |
| AW-015 | High | Holding resource lock across await point |

### Thread Safety (TS) -- 15 patterns

| Check ID | Severity | Description |
|----------|----------|-------------|
| TS-001 | Critical | Thread-unsafe singleton initialization |
| TS-002 | Critical | HashMap/ArrayList without synchronization in Java |
| TS-003 | High | Non-thread-safe datetime formatting (SimpleDateFormat) |
| TS-004 | High | Mutable default arguments shared across threads in Python |
| TS-005 | Critical | Lazy initialization without double-check locking |
| TS-006 | High | StringBuilder shared across threads in Java/C# |
| TS-007 | High | Regular expression object shared across threads |
| TS-008 | Critical | Non-thread-safe cache implementation |
| TS-009 | High | Shared Random instance without synchronization |
| TS-010 | Medium | Mutable return value from synchronized method |
| TS-011 | High | Thread-unsafe event handler registration |
| TS-012 | Critical | Publishing this reference in constructor |
| TS-013 | High | Non-synchronized iteration over shared collection |
| TS-014 | Medium | Using thread-unsafe collection in concurrent context |
| TS-015 | High | Missing @ThreadSafe/@GuardedBy annotation |

### Deadlock & Starvation (DL) -- 15 patterns

| Check ID | Severity | Description |
|----------|----------|-------------|
| DL-001 | Critical | Inconsistent lock ordering across methods |
| DL-002 | High | Holding lock while calling external/virtual method |
| DL-003 | Critical | Channel operation without timeout in Go |
| DL-004 | High | Unbuffered channel send in goroutine (potential block) |
| DL-005 | High | Missing select with default for non-blocking channel op |
| DL-006 | Critical | Lock held across await point (async deadlock) |
| DL-007 | High | Recursive lock acquisition (reentrant deadlock) |
| DL-008 | Critical | Acquiring multiple locks without consistent ordering |
| DL-009 | High | Blocking call inside synchronized block |
| DL-010 | Medium | Thread.sleep inside lock (starvation risk) |
| DL-011 | High | Missing timeout on lock acquisition |
| DL-012 | Critical | Goroutine leak (spawned without cancellation context) |
| DL-013 | High | WaitGroup.Add called inside goroutine |
| DL-014 | Medium | Reader-writer lock with writer starvation risk |
| DL-015 | High | Semaphore acquire without timeout |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot scan | 5 files | Unlimited | Unlimited |
| 90+ detection patterns | Yes | Yes | Yes |
| 6 language support | Yes | Yes | Yes |
| Pre-commit hooks | Yes | Yes | Yes |
| Concurrency reports | Yes | Yes | Yes |
| Watch mode | | Yes | Yes |
| CI/CD integration | | Yes | Yes |
| Team-level reports | | | Yes |
| Baseline/allowlist | | | Yes |
| Custom policy rules | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "concurrencyguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "allowlistFile": ".concurrencyguard-allowlist",
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Ecosystem

ConcurrencyGuard is part of the ClawHub code quality suite:

- **[SecretScan](https://secretscan.pages.dev)** -- Hardcoded secrets & credential leak detection
- **[AccessLint](https://accesslint.pages.dev)** -- Accessibility compliance scanning
- **[StyleGuard](https://styleguard.pages.dev)** -- Code style & consistency enforcement
- **[EnvGuard](https://envguard.pages.dev)** -- Environment variable safety
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[APIShield](https://apishield.pages.dev)** -- API security scanning
- **[DeadCode](https://deadcode.pages.dev)** -- Dead code and unused export detection
- **[TypeDrift](https://typedrift.pages.dev)** -- Type safety drift detection
- **[PerfGuard](https://perfguard.pages.dev)** -- Performance regression detection
- **[GitPulse](https://gitpulse.pages.dev)** -- Git workflow analytics
- **[DocSync](https://docsync.pages.dev)** -- Documentation drift detection
- **[SQLGuard](https://sqlguard.pages.dev)** -- SQL injection & query safety detection
- **[MemGuard](https://memguard.pages.dev)** -- Memory safety & leak detection
- **[MigrateSafe](https://migratesafe.pages.dev)** -- Database migration safety checking
- **[LicenseGuard](https://licenseguard.pages.dev)** -- License compliance scanning
- **[ConcurrencyGuard](https://concurrencyguard.pages.dev)** -- Race condition & concurrency safety analysis

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies beyond bash

## License

MIT
