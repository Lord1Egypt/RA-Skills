---
name: agent-tests
description: Define, run, and track tests for agent behavior. Test cases, assertions, regression tracking, and performance benchmarking. Zero external dependencies.
---

# Agent Tests 🧪

**Stop guessing if your agent still works. Start testing it.**

## The Problem

Agent behavior changes with every model update, config change, and skill addition. Without tests, you have no way to know if something broke until a user catches it.

Agent Tests gives you a lightweight testing framework for agent behavior.

## Quick Start

### Add a test case

```bash
node skills/agent-tests/agent-tests.js --test --add greet "Say hello" "Hello" "contains:Hello"
```

### List all tests

```bash
node skills/agent-tests/agent-tests.js --test --list
```

### Run a specific test

```bash
node skills/agent-tests/agent-tests.js --test --run greet
```

### Run all tests

```bash
node skills/agent-tests/agent-tests.js --test --run
```

### Run performance benchmark

```bash
node skills/agent-tests/agent-tests.js --benchmark greet 10
```

Runs the test 10 times, reports average/min/max duration and pass rate.

### Check regression report

```bash
node skills/agent-tests/agent-tests.js --regression
```

Shows pass rates, recent failures, and performance trends for all tests.

### Remove a test

```bash
node skills/agent-tests/agent-tests.js --test --remove greet
```

### Status overview

```bash
node skills/agent-tests/agent-tests.js --status
```

## Assertion Types

| Assertion | Example | What it checks |
|-----------|---------|----------------|
| Default | `"expected text"` | Expected text is in output |
| `contains:` | `contains:Hello` | Output contains "Hello" |
| `not_contains:` | `not_contains:error` | Output does NOT contain "error" |
| `regex:` | `regex:\d{3}` | Output matches regex pattern |
| `length:` | `length:42` | Output is exactly 42 chars |

## Features

### Test Management

- Add/remove tests with name, prompt, and expected output
- Track run count and pass rate per test
- Persistent storage in `memory/agent-tests/tests.json`

### Assertion Engine

- Simple assertion syntax (no test framework needed)
- Supports contains, not_contains, regex, and length checks
- Extensible for custom assertions

### Regression Tracking

- Groups results by test name
- Shows pass rate, total runs, and average duration
- Lists recent failures with specific assertion failures
- Flags tests below 80% pass rate with ⚠️

### Performance Benchmarking

- Runs tests multiple iterations
- Reports average, min, max duration
- Tracks pass rate across iterations
- Saves benchmark history (last 50 runs per test)

### Result History

- Stores last 1000 results per test
- Timestamps for every run
- Actual vs expected output captured

## Configuration

Data files stored in: `memory/agent-tests/`

- `tests.json` — Test definitions
- `results.json` — Test results history (last 1000)
- `benchmarks.json` — Benchmark history (last 50 per test)

Override data directory:
```bash
--dir /path/to/data
```

## Agent Protocol

When testing agent behavior:

1. **Add tests** — `--test --add` for critical behaviors
2. **Run before changes** — `--test --run` before model/config updates
3. **Benchmark periodically** — `--benchmark` to track performance drift
4. **Check regressions** — `--regression` during heartbeats
5. **Remove stale tests** — `--test --remove` for outdated test cases

## Limitations

- Test execution simulates output (actual agent output integration needed)
- Assertion engine is simple (regex, contains, length)
- No parallel test execution
- Results limited to 1000 entries

## Comparison

| Approach | Test Framework | Regression | Benchmark |
|----------|---------------|------------|-----------|
| Manual checking | ❌ | ❌ | ❌ |
| Full test framework | ✅ | ⚠️ | ❌ |
| **Agent Tests** | **✅** | **✅** | **✅** |

**Agent Tests gives you behavior testing + regression tracking + benchmarking with zero dependencies.**

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js, no npm packages
3. **Simple assertions** — Easy to write, hard to misinterpret
4. **Persistent** — Tests and results survive restarts
5. **Transparent** — Every run is logged and reportable
