# async-concurrency-reviewer

## Description
Review async and concurrency code across any language. Finds real bugs — deadlocks, race conditions, missing cancellation, blocking calls in async contexts, and misused primitives. Returns a structured report with severity ratings and corrected code.

## Use when
- "review my async code"
- "is this thread-safe"
- "could this deadlock"
- "check my concurrency"
- "await/promise/goroutine review"
- "is this race condition-safe"
- Any code with: async/await, promises, goroutines, threads, locks, channels, semaphores, actors

## Supported languages
Python, JavaScript/TypeScript, C#, Go, Rust, Java, Kotlin — and any other language with async or concurrency primitives.

## Input
Paste code. Optionally specify: language, runtime (Node, .NET, JVM, etc.), context (web server, CLI, background worker).

## Output format

```
## Async/Concurrency Review

### Critical (fix before shipping)
- [Finding] — [why it causes bugs in production]
  ✗ Before: [problematic code]
  ✓ After:  [corrected code]

### Warnings (should fix)
- [Finding] — [explanation]

### Suggestions (nice to have)
- [Finding] — [explanation]

### What's correct
- [Specific patterns done right — always include at least one]

### Summary
[2–3 sentences: biggest risk, top fix, one pattern to adopt going forward]
```

## Review checklist by language

### Python
- `asyncio.run()` called inside an already-running event loop
- Blocking calls (`time.sleep`, `requests.get`) inside `async def` — use `asyncio.sleep`, `httpx`
- `asyncio.create_task()` result not stored — task gets garbage collected
- Missing `await` on coroutines (silent no-op bug)
- `threading.Lock()` inside async code — use `asyncio.Lock()`
- Shared mutable state across tasks without locks

### JavaScript / TypeScript
- `await` inside `forEach` — use `Promise.all` with `map`
- Unhandled promise rejections
- `async` function called without `await` (fire and forget — often unintentional)
- Sequential `await` where parallel `Promise.all` would work
- Mixing callbacks and promises in the same flow
- `setTimeout` used as a poor-man's debounce in async context

### C# / .NET
- `.Result` or `.Wait()` — deadlocks in sync-over-async
- `async void` — exceptions swallowed, no awaitable
- Missing `CancellationToken` on public async methods
- `ConfigureAwait(false)` missing in library code
- `Task.Run` wrapping sync CPU-bound work — correct; wrapping async — wrong
- `lock` keyword in async code — use `SemaphoreSlim`
- `await` inside `lock` — compiler error but watch for equivalent patterns

### Go
- Goroutine leak — goroutine started, no way to stop it
- Channel send/receive without select+default or timeout — blocks forever
- `WaitGroup.Add()` called inside goroutine — race condition
- Shared map written from multiple goroutines without mutex
- Forgetting to close channels — range loop never terminates
- Context not passed through call chain — cancellation doesn't propagate

### Rust
- `block_on` inside an async runtime — panic
- `.unwrap()` on `JoinHandle` — hides panics
- Holding a `Mutex` lock across an `.await` — deadlock
- `spawn` without storing the handle — fire and forget, errors lost
- `Arc<Mutex<T>>` contention hotspot — consider `RwLock` or message passing

### Java / Kotlin
- `CompletableFuture.get()` blocking on the event thread
- Kotlin `runBlocking` inside a coroutine scope
- `GlobalScope.launch` — unstructured concurrency, leaks
- Missing `Dispatchers.IO` for blocking I/O in coroutines
- `synchronized` on wrong object — lock doesn't protect the shared state

## Severity definitions
- **Critical:** Will deadlock, lose data, swallow exceptions, or cause race conditions in production
- **Warning:** Performance issue, resource leak, or hard-to-debug behaviour
- **Suggestion:** Style, clarity, or future-proofing improvement

## Self-improvement instructions
After each review, note the most common finding. After 20 reviews, surface the top 3 patterns in your response as "Most common issues in [language]" to help users learn, not just fix.
