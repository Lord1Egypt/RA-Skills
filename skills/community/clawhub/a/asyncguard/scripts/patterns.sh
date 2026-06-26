#!/usr/bin/env bash
# AsyncGuard -- Async/Await Anti-Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Async issues that can cause data loss, resource leaks, or crashes
#   high     -- Async hazards likely to cause intermittent bugs or degraded performance
#   medium   -- Potential async issues, may be false positives
#   low      -- Informational, style issues, best practice suggestions
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \w, etc.)
# - No pipe alternation inside the regex field

set -euo pipefail

# ============================================================================
# 1. PROMISE/FUTURE MISUSE (PM-001 through PM-015)
# ============================================================================

declare -a ASYNCGUARD_PM_PATTERNS=()

ASYNCGUARD_PM_PATTERNS+=(
  # --- PM-001: Unhandled promise (no .catch and no await) ---
  '[[:alnum:]_]+\([^)]*\)[[:space:]]*;[[:space:]]*(//|$)|critical|PM-001|Potential unhandled promise -- no await and no .catch() attached|Add await keyword or attach .catch() handler to prevent unhandled rejections'

  # --- PM-002: new Promise with async executor ---
  'new[[:space:]]+Promise[[:space:]]*\([[:space:]]*async|critical|PM-002|Promise constructor with async executor function (exceptions will be lost)|Remove async from executor; use reject() for errors instead of throw'

  # --- PM-003: Promise.all on dependent operations ---
  'Promise\.all[[:space:]]*\([[:space:]]*\[|high|PM-003|Promise.all used -- verify operations are independent (no shared state dependencies)|Ensure promises in Promise.all do not depend on each other or share mutable state'

  # --- PM-004: Missing return in .then() handler ---
  '\.then\([[:space:]]*\([^)]*\)[[:space:]]*=>[[:space:]]*\{|high|PM-004|Arrow function with braces in .then() -- verify it returns a value|Add explicit return statement in .then() block body to avoid resolving with undefined'

  # --- PM-005: Deferred antipattern ---
  'let[[:space:]]+resolve[[:space:]]*,[[:space:]]*reject|critical|PM-005|Deferred antipattern -- extracting resolve/reject from Promise constructor|Use async/await or return new Promise directly; deferred pattern is error-prone'

  # --- PM-006: Promise constructor antipattern ---
  'new[[:space:]]+Promise[[:space:]]*\([[:space:]]*\([[:space:]]*resolve[[:space:]]*\)[[:space:]]*=>[[:space:]]*resolve\(|medium|PM-006|Promise constructor wrapping a value that could use Promise.resolve()|Use Promise.resolve(value) instead of new Promise(resolve => resolve(value))'

  # --- PM-007: Nested .then chains (callback hell) ---
  '\.then\([^)]*\)[[:space:]]*\.[[:space:]]*then\([^)]*\)[[:space:]]*\.[[:space:]]*then\(|high|PM-007|Deeply nested .then() chain (promise callback hell)|Refactor to async/await for readability and proper error propagation'

  # --- PM-008: Void promise (fire-and-forget without logging) ---
  'void[[:space:]]+[[:alnum:]_]+\([^)]*\)|medium|PM-008|Void operator on async call suppresses rejection handling|Replace void with proper await or attach .catch() for error visibility'

  # --- PM-009: Promise.race without timeout cleanup ---
  'Promise\.race[[:space:]]*\([[:space:]]*\[|high|PM-009|Promise.race without cleanup of losing promises (resource leak risk)|Cancel or clean up non-winning promises after race settles using AbortController'

  # --- PM-010: Resolve and reject both callable in same path ---
  'resolve\([^)]*\)[[:space:]]*;[^;]*reject\(|critical|PM-010|Both resolve() and reject() may be called in same code path|Ensure only one of resolve/reject is called; use if/else or early return'

  # --- PM-011: .then().then() without error handler ---
  '\.then\([^)]*\)\.then\([^)]*\)[[:space:]]*;|high|PM-011|Chained .then() calls with no .catch() at end of chain|Add .catch() at end of promise chain or convert to async/await with try/catch'

  # --- PM-012: Promise.any without fallback ---
  'Promise\.any[[:space:]]*\(|medium|PM-012|Promise.any without fallback for AggregateError when all promises reject|Handle AggregateError case when all promises in Promise.any reject'

  # --- PM-013: Mixing callbacks and promises ---
  'function[[:space:]]*\([^)]*callback[^)]*\)[[:space:]]*\{[^}]*return[[:space:]]+new[[:space:]]+Promise|high|PM-013|Mixing callback parameter with Promise return (dual async interface)|Choose one pattern: either callback or promise. Use util.promisify for conversion'

  # --- PM-014: Raw new Promise wrapping existing promise ---
  'new[[:space:]]+Promise[[:space:]]*\([^)]*\{[^}]*await[[:space:]]|critical|PM-014|new Promise wrapping an await call (redundant promise construction)|Remove the Promise wrapper; async functions already return promises'

  # --- PM-015: Promise resolved with another promise ---
  'resolve[[:space:]]*\([[:space:]]*new[[:space:]]+Promise|medium|PM-015|Resolving a promise with another promise (unnecessary nesting)|Return the inner promise directly instead of wrapping in resolve()'
)

# ============================================================================
# 2. ASYNC RESOURCE LEAKS (AR-001 through AR-015)
# ============================================================================

declare -a ASYNCGUARD_AR_PATTERNS=()

ASYNCGUARD_AR_PATTERNS+=(
  # --- AR-001: Async iterator not closed ---
  'for[[:space:]]+await[[:space:]]*\(|high|AR-001|for-await loop detected -- verify async iterator is properly closed on break|Use try/finally to ensure async iterator .return() is called on early exit'

  # --- AR-002: Unclosed async database connection ---
  '(createConnection|getConnection|createClient|createPool)\([^)]*\)|critical|AR-002|Database connection created -- verify it is closed after use|Use try/finally or connection pool with automatic release after query'

  # --- AR-003: Missing AbortController cleanup ---
  'new[[:space:]]+AbortController[[:space:]]*\(\)|high|AR-003|AbortController created -- verify abort() is called on cleanup|Call controller.abort() in cleanup/dispose to cancel pending operations'

  # --- AR-004: Async stream not piped or drained ---
  'createReadStream[[:space:]]*\(|high|AR-004|ReadStream created -- verify it is piped, consumed, or destroyed|Pipe to destination, consume with for-await, or call .destroy() to prevent leak'

  # --- AR-005: Dangling EventSource without close ---
  'new[[:space:]]+EventSource[[:space:]]*\(|high|AR-005|EventSource (SSE) connection opened without guaranteed close|Call eventSource.close() in cleanup function or component unmount'

  # --- AR-006: Missing async dispose / Symbol.asyncDispose ---
  'Symbol\.asyncDispose|medium|AR-006|Symbol.asyncDispose detected -- verify await using declaration is used|Use await using syntax (TC39) or try/finally for async resource cleanup'

  # --- AR-007: WebSocket opened without close handler ---
  'new[[:space:]]+WebSocket[[:space:]]*\(|high|AR-007|WebSocket connection opened -- verify close handler and cleanup exist|Add ws.onclose handler and call ws.close() in cleanup/teardown'

  # --- AR-008: Async file handle not closed ---
  'fs\.promises\.open[[:space:]]*\(|critical|AR-008|File handle opened with fs.promises.open -- must be explicitly closed|Use try/finally with fileHandle.close() or use fs.promises.readFile instead'

  # --- AR-009: Database pool not released after query ---
  'pool\.query[[:space:]]*\(|high|AR-009|Database pool query -- verify connection is released back to pool|Use pool.query() which auto-releases, or manually call client.release() in finally'

  # --- AR-010: ReadableStream not cancelled ---
  'new[[:space:]]+ReadableStream[[:space:]]*\(|medium|AR-010|ReadableStream created -- verify cancel() is called if consumer stops early|Call reader.cancel() or stream.cancel() when consumption stops before completion'

  # --- AR-011: setInterval in async without clearInterval ---
  'setInterval[[:space:]]*\(|high|AR-011|setInterval in async context -- verify clearInterval on cleanup|Store interval ID and call clearInterval() in cleanup/dispose/unmount handler'

  # --- AR-012: Async generator not returned ---
  'async[[:space:]]+function[[:space:]]*\*|high|AR-012|Async generator function -- verify consumer calls .return() on early exit|Use try/finally inside generator for cleanup; consumer should call .return() on break'

  # --- AR-013: Open cursor without close ---
  '\.cursor[[:space:]]*\(|high|AR-013|Database cursor opened -- verify it is closed after iteration|Call cursor.close() in finally block or use for-await with automatic close'

  # --- AR-014: SSE connection without cleanup ---
  'text/event-stream|medium|AR-014|Server-Sent Events content type detected -- verify connection cleanup|Implement close handler for SSE connections and clean up on client disconnect'

  # --- AR-015: Pending timers after async operation ---
  'setTimeout[[:space:]]*\([[:space:]]*async|high|AR-015|setTimeout with async callback -- timer reference may be needed for cleanup|Store timeout ID for clearTimeout() in cancellation or teardown logic'
)

# ============================================================================
# 3. EVENT LOOP BLOCKING (EL-001 through EL-015)
# ============================================================================

declare -a ASYNCGUARD_EL_PATTERNS=()

ASYNCGUARD_EL_PATTERNS+=(
  # --- EL-001: JSON.parse on large payload blocking loop ---
  'JSON\.parse[[:space:]]*\([[:space:]]*[[:alnum:]_]+\)|medium|EL-001|JSON.parse may block event loop on large payloads|Use streaming JSON parser or worker thread for large payloads (>1MB)'

  # --- EL-002: Synchronous crypto operations ---
  '(pbkdf2Sync|randomBytesSync|scryptSync|createCipheriv)[[:space:]]*\(|critical|EL-002|Synchronous crypto operation blocks the event loop|Use async variant: pbkdf2, randomBytes, scrypt with callback or promise'

  # --- EL-003: Sync file I/O in async context ---
  '(readFileSync|writeFileSync|appendFileSync|mkdirSync|readdirSync|statSync|existsSync)[[:space:]]*\(|critical|EL-003|Synchronous file I/O blocks the event loop|Use async fs.promises.readFile, writeFile, etc. or fs with callbacks'

  # --- EL-004: CPU-intensive loop in request handler ---
  '(app\.get|app\.post|router\.get|router\.post)[[:space:]]*\([^)]*\)[[:space:]]*.*for[[:space:]]*\(|high|EL-004|Loop inside request handler may block event loop for other requests|Offload CPU-intensive work to worker thread or background job queue'

  # --- EL-005: Regex backtracking in async context ---
  'new[[:space:]]+RegExp[[:space:]]*\([[:space:]]*[[:alnum:]_]+|medium|EL-005|Dynamic RegExp with user input may cause catastrophic backtracking|Validate regex complexity or use RE2 library for safe regex matching'

  # --- EL-006: Synchronous DNS lookup ---
  'dns\.lookup[[:space:]]*\(|high|EL-006|dns.lookup is backed by the thread pool and can block under load|Use dns.resolve (pure async) or dns.promises.resolve for non-blocking DNS'

  # --- EL-007: process.nextTick flood ---
  'process\.nextTick[[:space:]]*\(|medium|EL-007|process.nextTick can starve I/O callbacks if called recursively|Use setImmediate() instead to allow I/O callbacks between iterations'

  # --- EL-008: console.log in hot async path ---
  'console\.(log|info|debug|trace)[[:space:]]*\(|low|EL-008|Console output in production async path may block on stdout|Use async logger (winston, pino) in production; console is synchronous in Node.js'

  # --- EL-009: Synchronous child_process.execSync ---
  '(execSync|spawnSync|execFileSync)[[:space:]]*\(|critical|EL-009|Synchronous child process execution blocks the event loop|Use async exec, spawn, or execFile with callback or util.promisify'

  # --- EL-010: Large array sort in event handler ---
  '\.(sort|reverse)[[:space:]]*\([[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*,[[:space:]]*[[:alnum:]_]+|medium|EL-010|Array sort with comparator may block event loop on large datasets|Offload large sorts to worker thread or use streaming/pagination approach'

  # --- EL-011: Blocking while loop in async function ---
  'async[[:space:]]+function[^{]*\{[^}]*while[[:space:]]*\([[:space:]]*(true|1)|critical|EL-011|Blocking while(true) loop inside async function|Add await or setImmediate yield point inside loop to release event loop'

  # --- EL-012: Synchronous compression ---
  '(gzipSync|gunzipSync|deflateSync|inflateSync|brotliCompressSync|brotliDecompressSync)[[:space:]]*\(|high|EL-012|Synchronous compression blocks the event loop|Use async zlib.gzip, gunzip, deflate, inflate, or brotliCompress'

  # --- EL-013: URL parsing of untrusted input ---
  'new[[:space:]]+URL[[:space:]]*\([[:space:]]*[[:alnum:]_]+|low|EL-013|URL constructor with variable input may throw on malformed URLs|Wrap in try/catch; consider using URL.canParse() for validation first'

  # --- EL-014: Synchronous JSON serialization of large objects ---
  'JSON\.stringify[[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)|medium|EL-014|JSON.stringify may block event loop on large objects with circular refs|Use streaming serializer or worker thread for large object serialization'

  # --- EL-015: Blocking database query in event loop ---
  '(query|execute)[[:space:]]*\([[:space:]]*['"'"'"`]SELECT[[:space:]]|medium|EL-015|Direct SQL query execution -- verify it uses async driver with pool|Ensure database driver is non-blocking and uses connection pooling'
)

# ============================================================================
# 4. CANCELLATION & ABORTION (CA-001 through CA-015)
# ============================================================================

declare -a ASYNCGUARD_CA_PATTERNS=()

ASYNCGUARD_CA_PATTERNS+=(
  # --- CA-001: Missing AbortSignal propagation ---
  'fetch[[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)|high|CA-001|fetch() call without signal option (cannot be cancelled)|Pass { signal: controller.signal } as second argument to fetch()'

  # --- CA-002: No cancellation token forwarding ---
  'async[[:space:]]+function[[:space:]]+[[:alnum:]_]+[[:space:]]*\([[:space:]]*\)|high|CA-002|Async function with no parameters (no cancellation signal accepted)|Accept AbortSignal or CancellationToken parameter for cancellable operations'

  # --- CA-003: Orphaned async tasks after component unmount ---
  'useEffect[[:space:]]*\([[:space:]]*\(\)[[:space:]]*=>[[:space:]]*\{[^}]*async|critical|CA-003|Async operation in useEffect without cleanup function (memory leak risk)|Return cleanup function that aborts pending operations using AbortController'

  # --- CA-004: Missing context.Done check in Go ---
  'ctx[[:space:]]+context\.Context|medium|CA-004|context.Context parameter present -- verify ctx.Done() is checked in loops|Add select case <-ctx.Done() in long-running loops for cancellation support'

  # --- CA-005: No CancellationToken in C# async ---
  'async[[:space:]]+Task[[:space:]]*<|medium|CA-005|C# async Task method -- verify CancellationToken parameter is accepted|Add CancellationToken parameter and pass to downstream async calls'

  # --- CA-006: Timeout without abort cleanup ---
  'setTimeout[[:space:]]*\([^,]+,[[:space:]]*[0-9]+|high|CA-006|setTimeout used as timeout -- verify cleanup on cancellation path|Use AbortController with AbortSignal.timeout() or clear timeout on cancel'

  # --- CA-007: fetch without AbortController ---
  'await[[:space:]]+fetch[[:space:]]*\(|high|CA-007|Awaited fetch without AbortController (cannot timeout or cancel)|Create AbortController and pass signal to fetch; abort on timeout or unmount'

  # --- CA-008: Missing signal option in axios/fetch ---
  'axios\.(get|post|put|delete|patch|request)[[:space:]]*\(|high|CA-008|axios request without signal/cancelToken option|Pass { signal: controller.signal } or CancelToken for request cancellation'

  # --- CA-009: setTimeout without clearTimeout on cancel ---
  'const[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*setTimeout[[:space:]]*\(|medium|CA-009|setTimeout ID stored -- verify clearTimeout is called on cleanup|Call clearTimeout() in cleanup, unmount, or cancellation handler'

  # --- CA-010: No cleanup function in useEffect with async ---
  'useEffect[[:space:]]*\([[:space:]]*\(\)[[:space:]]*=>[[:space:]]*\{|high|CA-010|useEffect detected -- verify cleanup function is returned for async work|Return a cleanup function that cancels subscriptions and pending requests'

  # --- CA-011: AbortController created but signal not passed ---
  'new[[:space:]]+AbortController|medium|CA-011|AbortController created -- verify .signal is passed to async operations|Pass controller.signal to fetch, streams, and other cancellable APIs'

  # --- CA-012: Missing cancel on subscription/observable ---
  '\.(subscribe|on)[[:space:]]*\([[:space:]]*[[:alnum:]_({]|high|CA-012|Subscription or event listener created -- verify unsubscribe on cleanup|Store subscription reference and call unsubscribe() or off() on teardown'

  # --- CA-013: Race condition on cancellation path ---
  '\.abort[[:space:]]*\(\)[[:space:]]*;[^;]*await[[:space:]]|medium|CA-013|Abort called before await completes (potential race in cancellation)|Check signal.aborted before proceeding with operations after abort'

  # --- CA-014: No cleanup after Promise.race timeout ---
  'Promise\.race[[:space:]]*\([[:space:]]*\[[^]]*setTimeout|high|CA-014|Promise.race used for timeout without cleanup of pending promise|Cancel the losing promise after race settles; clear the timeout timer'

  # --- CA-015: Concurrent requests without abort on new request ---
  'let[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*null[[:space:]]*;[^;]*fetch|high|CA-015|Potential concurrent request pattern without aborting previous request|Abort previous request with AbortController before starting new one'
)

# ============================================================================
# 5. ASYNC ERROR PATTERNS (AE-001 through AE-015)
# ============================================================================

declare -a ASYNCGUARD_AE_PATTERNS=()

ASYNCGUARD_AE_PATTERNS+=(
  # --- AE-001: .catch returning undefined (swallowed rejection) ---
  '\.catch[[:space:]]*\([[:space:]]*\([[:space:]]*[[:alnum:]_]*[[:space:]]*\)[[:space:]]*=>[[:space:]]*\{[[:space:]]*\}[[:space:]]*\)|critical|AE-001|Empty .catch() handler swallows promise rejection silently|Log the error or re-throw; empty catch blocks hide failures and cause silent bugs'

  # --- AE-002: Async function returning rejected promise silently ---
  'async[[:space:]]+function[[:space:]]+[[:alnum:]_]+[^{]*\{[^}]*return[[:space:]]+Promise\.reject|high|AE-002|Async function explicitly returns Promise.reject instead of throwing|Use throw new Error() instead of return Promise.reject() in async functions'

  # --- AE-003: Unhandled rejection from detached promise ---
  '[[:alnum:]_]+\([^)]*\)\.then\([^)]*\)[[:space:]]*;|critical|AE-003|Promise chain with .then() but no .catch() -- unhandled rejection risk|Add .catch() at end of chain or use await with try/catch'

  # --- AE-004: Error in async event handler not caught ---
  '\.on[[:space:]]*\([[:space:]]*['"'"'"][[:alnum:]_]+['"'"'"][[:space:]]*,[[:space:]]*async|high|AE-004|Async event handler -- errors will become unhandled rejections|Wrap async event handler body in try/catch to handle errors properly'

  # --- AE-005: Missing try-catch in async IIFE ---
  '\([[:space:]]*async[[:space:]]*\([[:space:]]*\)[[:space:]]*=>[[:space:]]*\{|high|AE-005|Async IIFE without visible try/catch (unhandled rejection risk)|Add try/catch inside async IIFE or attach .catch() to the invocation'

  # --- AE-006: Error boundary not catching async errors ---
  'componentDidCatch[[:space:]]*\(|medium|AE-006|React componentDidCatch does not catch async errors in event handlers|Use error boundary plus global onunhandledrejection for async error coverage'

  # --- AE-007: .catch with empty function ---
  '\.catch[[:space:]]*\([[:space:]]*\(\)[[:space:]]*=>[[:space:]]*\{\}|critical|AE-007|Empty arrow function in .catch() silently swallows all errors|At minimum log the error: .catch(err => console.error(err))'

  # --- AE-008: Async callback without error parameter ---
  'async[[:space:]]*\([[:space:]]*\)[[:space:]]*=>[[:space:]]*\{|medium|AE-008|Async callback with no parameters -- may be missing error context|Verify the callback signature matches expected error-first or event pattern'

  # --- AE-009: Promise rejection without Error object ---
  'reject[[:space:]]*\([[:space:]]*['"'"'"`]|high|AE-009|Promise rejected with string instead of Error object (no stack trace)|Use reject(new Error(message)) to preserve stack trace for debugging'

  # --- AE-010: try/catch not wrapping await ---
  'try[[:space:]]*\{[[:space:]]*(const|let|var)[[:space:]]|medium|AE-010|try block detected -- verify all await expressions are inside try/catch|Ensure every await that can reject is wrapped in try/catch or has .catch()'

  # --- AE-011: Async forEach with no error handling ---
  '\.forEach[[:space:]]*\([[:space:]]*async|critical|AE-011|async callback in forEach -- errors are silently lost and execution is not sequential|Use for...of with await, or Promise.all with .map() for parallel execution'

  # --- AE-012: Missing rejection handler on Promise.all ---
  'Promise\.all[[:space:]]*\([^)]*\)[[:space:]]*;|high|AE-012|Promise.all without .catch() -- first rejection crashes entire batch|Use Promise.allSettled() or add .catch() to handle partial failures'

  # --- AE-013: Error swallowed in async middleware ---
  'catch[[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)[[:space:]]*\{[[:space:]]*(//|$)|high|AE-013|Catch block appears to swallow error without re-throwing or passing to next|Re-throw error or call next(error) in middleware to propagate failures'

  # --- AE-014: No error propagation in async chain ---
  '\.then[[:space:]]*\([[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)[[:space:]]*=>[[:space:]]*\{|medium|AE-014|.then() handler with block body -- verify errors are returned or thrown|Return rejected promise or throw in .then() to propagate errors down the chain'

  # --- AE-015: Finally block hiding original error ---
  'finally[[:space:]]*\{[^}]*return[[:space:]]|high|AE-015|Return statement inside finally block replaces the original error or result|Remove return from finally block; use finally only for cleanup, not values'
)

# ============================================================================
# 6. ASYNC COORDINATION (AC-001 through AC-015)
# ============================================================================

declare -a ASYNCGUARD_AC_PATTERNS=()

ASYNCGUARD_AC_PATTERNS+=(
  # --- AC-001: Missing semaphore for concurrent limit ---
  'Promise\.all[[:space:]]*\([[:space:]]*[[:alnum:]_]+\.map|high|AC-001|Array.map with Promise.all -- no concurrency limit on parallel operations|Use p-limit, p-map, or async.mapLimit to bound concurrent operations'

  # --- AC-002: No p-limit/p-queue for parallel control ---
  'await[[:space:]]+Promise\.all[[:space:]]*\([[:space:]]*\[|high|AC-002|Promise.all without concurrency control -- may overwhelm resources|Use p-limit or p-queue to restrict the number of concurrent promises'

  # --- AC-003: Unbounded Promise.all (many concurrent) ---
  '\.map[[:space:]]*\([[:space:]]*async[[:space:]]*\([^)]*\)[[:space:]]*=>[[:space:]]*\{|critical|AC-003|Unbounded async map over collection -- can spawn unlimited concurrent tasks|Limit concurrency with p-map(items, fn, {concurrency: N}) or batching'

  # --- AC-004: Async mutex needed but missing ---
  'await[[:space:]]+[[:alnum:]_]+[[:space:]]*;[^;]*await[[:space:]]+[[:alnum:]_]+\.[[:alnum:]_]+[[:space:]]*=[[:space:]]|medium|AC-004|Sequential awaits with shared state mutation -- may need async mutex|Use async-mutex or p-mutex for atomic read-modify-write in async context'

  # --- AC-005: Missing debounce/throttle on async calls ---
  'addEventListener[[:space:]]*\([[:space:]]*['"'"'"](input|keydown|keyup|scroll|resize)['"'"'"][[:space:]]*,[[:space:]]*async|high|AC-005|Async handler on high-frequency event without debounce or throttle|Wrap async handler with debounce() or throttle() to prevent flooding'

  # --- AC-006: Sequential API calls where concurrent possible ---
  'const[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*await[[:space:]]+[[:alnum:]_]+\([^)]*\)[[:space:]]*;[[:space:]]*const[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*await|medium|AC-006|Sequential await calls that may be independent and parallelizable|Use Promise.all([call1(), call2()]) for independent async operations'

  # --- AC-007: No batching for multiple async operations ---
  'for[[:space:]]*\([^)]*\)[[:space:]]*\{[^}]*await[[:space:]]+[[:alnum:]_]+\.[[:alnum:]_]+(save|create|insert|update|delete)\(|high|AC-007|Individual async database operations in loop -- consider batching|Use bulk/batch operations: insertMany, bulkWrite, or transaction batching'

  # --- AC-008: Missing rate limiter on async loop ---
  'while[[:space:]]*\([[:space:]]*(true|![[:alnum:]_])|medium|AC-008|Unbounded async loop without rate limiting or delay|Add await delay() or rate limiter between iterations to prevent API flooding'

  # --- AC-009: Unbounded async event emission ---
  '\.emit[[:space:]]*\([[:space:]]*['"'"'"][[:alnum:]_]+['"'"'"]|medium|AC-009|Event emission in async context -- verify listeners are bounded|Ensure event listeners are limited; use setMaxListeners and remove on cleanup'

  # --- AC-010: No backpressure handling on streams ---
  '\.pipe[[:space:]]*\([[:space:]]*[[:alnum:]_]+|medium|AC-010|Stream piped without explicit backpressure or error handling|Use pipeline() instead of pipe() for proper backpressure and error propagation'

  # --- AC-011: Parallel writes without coordination ---
  'Promise\.all[[:space:]]*\([[:space:]]*\[[^]]*\.write|high|AC-011|Parallel write operations without coordination (data corruption risk)|Sequence writes with for...of await, or use write queue for ordered operations'

  # --- AC-012: Missing async barrier/latch ---
  'let[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*0[[:space:]]*;[^;]*\+\+[[:space:]]*[[:alnum:]_]|medium|AC-012|Manual counter for async coordination (fragile pattern)|Use Promise.all, CountDownLatch, or async barrier for reliable coordination'

  # --- AC-013: No connection limit on pool ---
  'createPool[[:space:]]*\([[:space:]]*\{|medium|AC-013|Connection pool created -- verify max connections limit is configured|Set max/connectionLimit in pool config to prevent resource exhaustion'

  # --- AC-014: Simultaneous async initialization race ---
  'if[[:space:]]*\([[:space:]]*![[:alnum:]_]+\)[[:space:]]*\{[^}]*await[[:space:]]|high|AC-014|Lazy async initialization without mutex (concurrent callers may race)|Use once-pattern or async mutex to prevent double initialization'

  # --- AC-015: Missing async queue for ordered processing ---
  '\.push[[:space:]]*\([[:space:]]*async|medium|AC-015|Async tasks pushed to array without queue management|Use p-queue or async.queue for ordered, bounded async task processing'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
asyncguard_pattern_count() {
  local count=0
  count=$((count + ${#ASYNCGUARD_PM_PATTERNS[@]}))
  count=$((count + ${#ASYNCGUARD_AR_PATTERNS[@]}))
  count=$((count + ${#ASYNCGUARD_EL_PATTERNS[@]}))
  count=$((count + ${#ASYNCGUARD_CA_PATTERNS[@]}))
  count=$((count + ${#ASYNCGUARD_AE_PATTERNS[@]}))
  count=$((count + ${#ASYNCGUARD_AC_PATTERNS[@]}))
  echo "$count"
}

# Get count of patterns in a specific category
asyncguard_category_count() {
  local category="$1"
  local upper
  upper=$(echo "$category" | tr '[:lower:]' '[:upper:]')
  case "$upper" in
    PM) echo "${#ASYNCGUARD_PM_PATTERNS[@]}" ;;
    AR) echo "${#ASYNCGUARD_AR_PATTERNS[@]}" ;;
    EL) echo "${#ASYNCGUARD_EL_PATTERNS[@]}" ;;
    CA) echo "${#ASYNCGUARD_CA_PATTERNS[@]}" ;;
    AE) echo "${#ASYNCGUARD_AE_PATTERNS[@]}" ;;
    AC) echo "${#ASYNCGUARD_AC_PATTERNS[@]}" ;;
    *)  echo "0" ;;
  esac
}

# Get patterns array name for a category
get_asyncguard_patterns_for_category() {
  local category="$1"
  local upper
  upper=$(echo "$category" | tr '[:lower:]' '[:upper:]')
  case "$upper" in
    PM) echo "ASYNCGUARD_PM_PATTERNS" ;;
    AR) echo "ASYNCGUARD_AR_PATTERNS" ;;
    EL) echo "ASYNCGUARD_EL_PATTERNS" ;;
    CA) echo "ASYNCGUARD_CA_PATTERNS" ;;
    AE) echo "ASYNCGUARD_AE_PATTERNS" ;;
    AC) echo "ASYNCGUARD_AC_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# Get human-readable label for a category
get_asyncguard_category_label() {
  local category="$1"
  local upper
  upper=$(echo "$category" | tr '[:lower:]' '[:upper:]')
  case "$upper" in
    PM) echo "Promise/Future Misuse" ;;
    AR) echo "Async Resource Leaks" ;;
    EL) echo "Event Loop Blocking" ;;
    CA) echo "Cancellation & Abortion" ;;
    AE) echo "Async Error Patterns" ;;
    AC) echo "Async Coordination" ;;
    *)  echo "Unknown" ;;
  esac
}

# All category codes for iteration
get_all_asyncguard_categories() {
  echo "PM AR EL CA AE AC"
}

# Get categories available for a tier level
# Free=PM+AR (30), Pro=PM+AR+EL+CA (60), Team=all 6 (90)
get_asyncguard_categories_for_tier() {
  local tier_level="${1:-0}"
  case "$tier_level" in
    0) echo "PM AR" ;;
    1) echo "PM AR EL CA" ;;
    2) echo "PM AR EL CA AE AC" ;;
    3) echo "PM AR EL CA AE AC" ;;
    *) echo "PM AR" ;;
  esac
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# List patterns by category
asyncguard_list_patterns() {
  local filter_type="${1:-all}"

  case "$filter_type" in
    PM|AR|EL|CA|AE|AC)
      local patterns_name
      patterns_name=$(get_asyncguard_patterns_for_category "$filter_type")
      local -n _ag_patterns_ref="$patterns_name"
      local label
      label=$(get_asyncguard_category_label "$filter_type")

      echo -e "  ${BOLD:-}${filter_type} -- ${label}${NC:-}"
      for entry in "${_ag_patterns_ref[@]}"; do
        IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
        printf "    %-12s %-8s %s\n" "$check_id" "$severity" "$description"
      done
      echo ""
      ;;
    all)
      asyncguard_list_patterns "PM"
      asyncguard_list_patterns "AR"
      asyncguard_list_patterns "EL"
      asyncguard_list_patterns "CA"
      asyncguard_list_patterns "AE"
      asyncguard_list_patterns "AC"
      ;;
    *)
      echo "Unknown category: $filter_type"
      return 1
      ;;
  esac
}

# Validate category code
is_valid_asyncguard_category() {
  local category="$1"
  case "$category" in
    PM|AR|EL|CA|AE|AC) return 0 ;;
    *) return 1 ;;
  esac
}
