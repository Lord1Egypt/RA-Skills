# Audit Dimensions

Each codebase audit spans these five dimensions. For each dimension, spawn a dedicated subagent that fetches source files and verifies issues against actual code.

## 1. Security (安全审计)

**Focus**: Vulnerabilities that allow unauthorized access, data exfiltration, or resource abuse.

**Key questions to probe**:
- Are there SSRF attack vectors? Check URL fetching/redirect logic, DNS resolution, IP filtering
- Are there command injection risks? Search for `subprocess`, `shell=True`, unchecked file path concatenation
- Are there auth token leaks? Check logging, error messages, HTTP response handling
- Are there path traversal risks? Check file operations with user-controlled paths
- Are third-party dependencies validated? Check version pinning, integrity checks

**Verification method**: Trace the full attack path from user input to exploit. For each defense claim in the code, verify it actually works at the call site.

## 2. Concurrency & State Machine Safety (并发与状态机安全)

**Focus**: Race conditions, data corruption, inconsistent state in multi-thread/multi-process environments.

**Key questions to probe**:
- Are file locks (flock/fcntl) used for shared state? Is the lock scope correct (covers read-modify-write)?
- Are state transitions atomic? Check `load → modify → save` and `load → transition → save` patterns
- Are there TOCTOU (Time-of-check-time-of-use) gaps? Gap between check and action
- Are there duplicate definitions of the same named exception/class?
- Is there any lock-free concurrent write to the same file?
- For append-only logs: is `append_jsonl` properly flocked?
- For json writes: is tmp-rename used for atomicity?

**Verification method**: Construct a timeline with two concurrent operations, trace each thread's read and write points.

## 3. UX & Implementation Logic (用户体验与实现逻辑)

**Focus**: Whether the code actually implements what the docs/release-notes claim, and whether user-facing behavior is correct.

**Key questions to probe**:
- Do feature flags/modes actually enforce their claimed semantics? (e.g., "review-only" truly limits to reviews)
- Are there dead code paths that silently swallow errors?
- Are error messages actionable? Do they tell the user how to fix the problem?
- Can users recover from mistakes? Is there undo/backtrack/revisit?
- Are there implicit access control gaps? (e.g., no @-mention check in group chats)
- Do test mocks hide real bugs? Check if mocked interfaces match actual call signatures
- Are there misleading code comments that describe behavior not implemented?

**Verification method**: Trace each code branch and confirm the actual behavior against the documented claim. For each error path, read the error message and assess if a user could act on it.

## 4. Test Quality & Coverage Blind Spots (测试质量)

**Focus**: Whether tests actually catch the bugs they claim to prevent.

**Key questions to probe**:
- Do integration tests use real dependencies or mocks? If mocked, do mocks validate call signatures?
- Are there end-to-end tests in CI? If not, what's the smoke test strategy?
- What bug classes are invisible to the current test suite?
- Do test fixtures match production call signatures?

**Verification method**: Read a representative sample of test files. Check if a wrong call signature or wrong return type would cause any test to fail.

## 5. Simplicity & Over-Engineering (简洁性与过度工程) — NEW v1.1.0

**Focus**: Whether the code's complexity is justified by the problem it solves. AI-generated code is prone to "massive overkill" — hundreds of lines with new services, patterns, and abstractions for what should be a small incremental change.

**Background**: Community experience (Hacker News 2025 State of AI Code Quality discussion, Reddit r/ExperiencedDevs) consistently reports that AI coding agents over-engineer solutions. A "batching" request that should be 2 methods becomes a new service class + background worker + suite of tests. This dimension explicitly hunts for these patterns.

**Key questions to probe**:
- **AI-bloat check**: For each changed file, compute the ratio of "conceptual complexity needed" to "lines of code added". Does this PR add a new class/module/abstraction where a function would suffice?
- **Abstraction audit**: Does the code introduce interfaces, factories, strategies, or dependency injection where direct calls would work? For each, ask: "What concrete problem does this abstraction solve today, not hypothetically?"
- **Dead or speculative code**: Are there code paths, config keys, or extension points with zero current consumers? Flag "future-proofing" that isn't tied to a known roadmap item.
- **Config sprawl**: Count new env vars, CLI flags, and config keys. Is each justified by a real user-facing need?
- **Dependency footprint**: Count new third-party imports. Does every new dependency carry its weight?
- **Rube Goldberg detection**: Could the same result be achieved with a simpler approach using existing infrastructure?

**Verification method**: For each module changed, write a one-sentence description of "what this module actually does." If that sentence is surprisingly short compared to the code volume, flag it.

**Simplicity Score**: At the end of the Simplicity audit, assign a 1-5 score:
- 5 = Elegantly minimal — every line earns its place
- 4 = Clean — minor nitpicks but nothing egregious
- 3 = Acceptable — some bloat but functional
- 2 = Over-engineered — substantial unnecessary complexity
- 1 = Massively bloated — requires refactoring before merge
