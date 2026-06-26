#!/usr/bin/env bash
# ConcurrencyGuard -- Concurrency Safety Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Race conditions that can cause data corruption or security issues
#   high     -- Concurrency hazards likely to cause intermittent bugs
#   medium   -- Potential concurrency issues, may be false positives
#   low      -- Informational, style issues, missing annotations
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \w, etc.)

set -euo pipefail

# ============================================================================
# 1. SHARED STATE (SS-001 through SS-015)
# ============================================================================

declare -a CONCURRENCYGUARD_SS_PATTERNS=()

CONCURRENCYGUARD_SS_PATTERNS+=(
  # --- SS-001: Global mutable variable in Go accessed without sync ---
  'var[[:space:]]+[[:alnum:]_]+[[:space:]]+(map|(\[\])|chan[[:space:]])|critical|SS-001|Global mutable variable (map/slice/chan) declared at package level in Go|Protect with sync.Mutex or sync.RWMutex, or use sync.Map for concurrent map access'

  # --- SS-002: Unprotected static mutable field in Java ---
  'static[[:space:]]+(private|public|protected|volatile)?[[:space:]]*[[:alpha:]]+[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*new[[:space:]]|critical|SS-002|Mutable static field initialized with new object in Java (not final)|Make field final or protect all access with synchronized blocks'

  # --- SS-003: Module-level mutable state in Python ---
  '^[[:alpha:]_]+[[:space:]]*=[[:space:]]*(\{|\[|dict\(|list\(|set\(|collections\.|defaultdict)|high|SS-003|Module-level mutable data structure in Python (shared across threads)|Use threading.local() or pass as parameter; protect with threading.Lock()'

  # --- SS-004: Shared variable without volatile in Java ---
  'private[[:space:]]+static[[:space:]]+[[:alpha:]]+[[:space:]]+[[:alnum:]_]+[[:space:]]*;|high|SS-004|Non-volatile static field in Java (may not be visible across threads)|Add volatile keyword or use AtomicReference/AtomicInteger for thread visibility'

  # --- SS-005: Global object mutation in Node worker threads ---
  'workerData|parentPort|SharedArrayBuffer|Atomics|high|SS-005|Node.js worker thread shared memory usage detected|Use Atomics for SharedArrayBuffer access; avoid sharing mutable state between workers'

  # --- SS-006: Mutable class variable in Python ---
  'class[[:space:]]+[[:alnum:]_]+.*:[[:space:]]*$|high|SS-006|Python class with potential shared mutable class variables|Use instance variables (self.x) instead of class variables for mutable state'

  # --- SS-007: Static collection modified without sync in Java ---
  'static[[:space:]]+(final[[:space:]]+)?[[:alpha:]]*[[:space:]]*(List|Map|Set|Queue|Deque|Collection)[[:space:]]*<|high|SS-007|Static collection field in Java (potential concurrent modification)|Use ConcurrentHashMap, CopyOnWriteArrayList, or Collections.synchronized* wrappers'

  # --- SS-008: Unprotected global counter ---
  '(count|total|counter|num_|idx|index)[[:space:]]*(\+\+|\+=|-=|--)|medium|SS-008|Global counter modified with non-atomic increment/decrement|Use atomic operations (AtomicInteger, sync/atomic, Interlocked) or protect with mutex'

  # --- SS-009: Shared dict without concurrent variant in Python ---
  'threading\.(Thread|Lock|RLock)|high|SS-009|Threading module usage detected -- verify all shared state is protected|Audit all module-level and class-level mutable variables for proper synchronization'

  # --- SS-010: Go global modified in goroutine ---
  'go[[:space:]]+func[[:space:]]*\(|critical|SS-010|Goroutine launched with potential closure over shared variable|Capture variables by value in goroutine closure, or protect shared state with sync.Mutex'

  # --- SS-011: Rust unsafe mutable static ---
  'static[[:space:]]+mut[[:space:]]|critical|SS-011|Unsafe mutable static in Rust (data race risk)|Use std::sync::Mutex, std::sync::RwLock, or std::sync::atomic types instead'

  # --- SS-012: Module-level list append in Python ---
  '^[[:alpha:]_]+\.(append|extend|insert|pop|remove|update|clear)\(|medium|SS-012|Module-level collection mutation in Python|Protect with threading.Lock() if accessed from multiple threads'

  # --- SS-013: Shared buffer modification ---
  '(shared|global|static)[[:space:]]*[[:alpha:]]*[[:space:]]*(buf|buffer|data|cache)[[:space:]]*[=\[]|high|SS-013|Shared buffer or data array without explicit synchronization|Use synchronized access, concurrent data structures, or immutable buffers'

  # --- SS-014: Global config modified at runtime ---
  '(config|settings|options|params)\.(set|update|modify|put|remove|delete|clear)\(|medium|SS-014|Global configuration object modified at runtime|Make configuration immutable after initialization; use copy-on-write for updates'

  # --- SS-015: C# static field without lock ---
  'private[[:space:]]+static[[:space:]]+[[:alpha:]]+[[:space:]]+_[[:alnum:]]+[[:space:]]*=|high|SS-015|C# private static field (potential shared mutable state)|Protect with lock statement, use Interlocked class, or make readonly'
)

# ============================================================================
# 2. LOCKING & MUTEX (LK-001 through LK-015)
# ============================================================================

declare -a CONCURRENCYGUARD_LK_PATTERNS=()

CONCURRENCYGUARD_LK_PATTERNS+=(
  # --- LK-001: Missing synchronized on shared method in Java ---
  'public[[:space:]]+static[[:space:]]+void[[:space:]]+[[:alnum:]_]+[[:space:]]*\([^)]*\)[[:space:]]*\{|critical|LK-001|Public static method without synchronized keyword in Java|Add synchronized keyword or use explicit ReentrantLock for thread-safe access'

  # --- LK-002: Missing lock in C# ---
  'static[[:space:]]+[[:alpha:]]+[[:space:]]+[[:alnum:]_]+[[:space:]]*\([^)]*\)[[:space:]]*\{|high|LK-002|Static method in C# without lock protection for shared state|Use lock(lockObj) statement or Interlocked class for atomic operations'

  # --- LK-003: Missing mutex.Lock in Go ---
  '\.(Lock|RLock)\(\)|high|LK-003|Mutex Lock() call detected -- verify matching Unlock() exists|Ensure every Lock() has a corresponding defer Unlock() immediately after'

  # --- LK-004: Lock without defer Unlock in Go ---
  '\.Lock\(\)[[:space:]]*$|critical|LK-004|Mutex Lock() without defer Unlock() on same line or next line in Go|Always use defer mu.Unlock() immediately after mu.Lock() to prevent missed unlocks'

  # --- LK-005: Nested lock acquisition ---
  'synchronized[[:space:]]*\([[:alnum:]_]+\)[[:space:]]*\{[^}]*synchronized[[:space:]]*\(|high|LK-005|Nested synchronized blocks in Java (deadlock risk)|Use a single lock or establish consistent lock ordering; consider java.util.concurrent'

  # --- LK-006: Missing RWMutex for read-heavy data in Go ---
  'sync\.Mutex|high|LK-006|Using sync.Mutex -- consider sync.RWMutex if reads greatly outnumber writes|Use sync.RWMutex with RLock()/RUnlock() for read operations to improve throughput'

  # --- LK-007: Spin lock in user code ---
  'while[[:space:]]*\([[:space:]]*(true|1|![[:space:]]*done|![[:space:]]*ready|![[:space:]]*flag)|medium|LK-007|Busy-wait spin loop detected (CPU waste, potential livelock)|Use proper synchronization: condition variables, semaphores, or channels'

  # --- LK-008: Lock not deferred in Go ---
  '([[:alnum:]_]+)\.Lock\(\)[[:space:]]*\n[^d]|high|LK-008|Go mutex Lock() not followed by defer Unlock()|Always defer Unlock() immediately after Lock() to ensure unlock on panic'

  # --- LK-009: Missing threading.Lock in Python ---
  'import[[:space:]]+threading|high|LK-009|Python threading module imported -- verify Lock usage for shared state|Use threading.Lock() or threading.RLock() to protect all shared mutable state'

  # --- LK-010: Conditional unlock ---
  'if[[:space:]]*\(.*\)[[:space:]]*\{[^}]*(\.Unlock|\.unlock|Release|Monitor\.Exit)|critical|LK-010|Lock unlock inside conditional block (may not execute on all paths)|Move unlock outside conditional; use try-finally or defer for guaranteed unlock'

  # --- LK-011: Using Lock where RLock appropriate ---
  'threading\.Lock\(\)|medium|LK-011|Python threading.Lock used -- consider RLock if re-entrant locking needed|Use threading.RLock() if the same thread may need to acquire the lock multiple times'

  # --- LK-012: Mutex not held during condvar wait ---
  '(Condition|cond)\.(wait|Wait)\(|high|LK-012|Condition variable wait detected -- verify mutex is held during wait|Always hold the associated mutex/lock when calling wait() on a condition variable'

  # --- LK-013: Missing lock in C# property ---
  'public[[:space:]]+(static[[:space:]]+)?[[:alpha:]]+[[:space:]]+[[:alnum:]_]+[[:space:]]*\{[[:space:]]*get[[:space:]]*;[[:space:]]*set[[:space:]]*;|high|LK-013|Auto-property in C# without lock protection (if shared across threads)|Use lock statement in custom getter/setter, or use Interlocked for primitive types'

  # --- LK-014: Manual lock implementation ---
  '(while|for)[[:space:]]*\(.*\.(compareAndSet|compareAndSwap|CompareExchange)\(|medium|LK-014|Manual CAS-based lock implementation detected|Prefer language-provided lock primitives (synchronized, lock, sync.Mutex) over hand-rolled locks'

  # --- LK-015: Sync.Mutex copied by value in Go ---
  'func[[:space:]]+[[:alnum:]_]+\([[:space:]]*[[:alnum:]_]+[[:space:]]+[[:alnum:]_]*Mutex|high|LK-015|Go sync.Mutex or struct containing Mutex passed by value (copy risk)|Always pass Mutex by pointer; embed with pointer receiver methods'
)

# ============================================================================
# 3. TOCTOU & ATOMICITY (TC-001 through TC-015)
# ============================================================================

declare -a CONCURRENCYGUARD_TC_PATTERNS=()

CONCURRENCYGUARD_TC_PATTERNS+=(
  # --- TC-001: Check-then-act without sync ---
  'if[[:space:]]*\(.*\.(contains|has|get|exists|ContainsKey|TryGetValue|containsKey)\(|critical|TC-001|Check-then-act pattern on shared collection (TOCTOU risk)|Use atomic putIfAbsent/computeIfAbsent, or protect the check-and-act with a lock'

  # --- TC-002: File exists then open (TOCTOU) ---
  '(os\.path\.exists|File\.Exists|Files\.exists|os\.Stat|fs\.existsSync|Path\.exists)\(|critical|TC-002|File existence check followed by file operation (TOCTOU vulnerability)|Use atomic file operations: open with O_CREAT|O_EXCL, or use lockfile/flock'

  # --- TC-003: Read-modify-write without CAS ---
  '([[:alnum:]_]+)[[:space:]]*=[[:space:]]*\1[[:space:]]*[\+\-\*\/]|critical|TC-003|Read-modify-write on variable (x = x + n) without atomic operation|Use atomic increment (AtomicInteger, sync/atomic, Interlocked.Add) or protect with lock'

  # --- TC-004: Double-checked locking without volatile ---
  'if[[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*==[[:space:]]*null|high|TC-004|Null-check pattern (possible double-checked locking without volatile)|Ensure field is volatile (Java) or use Lazy<T> (C#) or sync.Once (Go) for safe lazy init'

  # --- TC-005: Non-atomic counter increment ---
  '\+\+[[:space:]]*;|\+\+[[:space:]]*$|[[:alnum:]_]+\+\+|critical|TC-005|Increment operator (++) which is not atomic on shared variable|Use AtomicInteger.incrementAndGet(), atomic.AddInt64(), or Interlocked.Increment()'

  # --- TC-006: Compare-and-swap needed ---
  'if[[:space:]]*\(.*==[[:space:]]*[[:alnum:]_]+\)[[:space:]]*\{[^}]*=[[:space:]]|high|TC-006|Compare-then-assign pattern without atomic CAS operation|Use compareAndSet/CompareExchange or protect with synchronized/lock'

  # --- TC-007: Get-then-put on Map ---
  '\.(get|Get)\([^)]+\)[[:space:]]*;[^;]*\.(put|Put|set|Set)\(|critical|TC-007|Get-then-put on Map/Dictionary without atomic operation|Use putIfAbsent, computeIfAbsent, ConcurrentDictionary.AddOrUpdate, or lock'

  # --- TC-008: Test-and-set without atomic ---
  'if[[:space:]]*\([[:space:]]*![[:alnum:]_]+(Done|Ready|Started|Initialized|Running)\)|high|TC-008|Boolean flag test-and-set without atomic operation|Use AtomicBoolean, atomic.Bool, or protect flag check-and-set with lock'

  # --- TC-009: Non-atomic boolean flag ---
  '(volatile|static)?[[:space:]]*(boolean|bool)[[:space:]]+[[:alnum:]_]*(flag|done|ready|running|started|stopped|cancelled)|critical|TC-009|Boolean flag used for thread communication (non-atomic risk)|Use AtomicBoolean (Java), atomic.Bool (Go), volatile (C#), or threading.Event (Python)'

  # --- TC-010: Lazy init without sync ---
  'if[[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*==[[:space:]]*(null|nil|None|undefined)\)[[:space:]]*\{|critical|TC-010|Lazy initialization with null check (thread-unsafe without synchronization)|Use sync.Once (Go), Lazy<T> (C#), double-checked locking with volatile, or @synchronized'

  # --- TC-011: Balance check then debit ---
  'if[[:space:]]*\(.*\.(balance|amount|quantity|stock|inventory|count)[[:space:]]*(>|>=|<|<=)|critical|TC-011|Balance/quantity check before modification (lost update risk)|Use database transaction with SELECT FOR UPDATE or optimistic locking with version field'

  # --- TC-012: Collection size then index ---
  '\.(size|length|count|Count)\(\)[[:space:]]*(>|>=|!=)[[:space:]]*0|high|TC-012|Collection size check before index access (TOCTOU on concurrent collection)|Use atomic operations on concurrent collections; lock around size-check-and-access'

  # --- TC-013: Non-atomic file write ---
  '(open|fopen|File\.Open|os\.OpenFile)\([^)]*["'"'"'](w|write)|medium|TC-013|File opened in write mode (non-atomic write risk for concurrent access)|Use atomic write pattern: write to temp file, then rename; or use file locks'

  # --- TC-014: DB read-check-write without FOR UPDATE ---
  'SELECT[[:space:]]+.*FROM[[:space:]]+.*WHERE|high|TC-014|Database SELECT without FOR UPDATE (lost update risk in concurrent transactions)|Use SELECT ... FOR UPDATE or optimistic locking with version column'

  # --- TC-015: Non-atomic multi-field update ---
  '\.(set[A-Z]|Set[A-Z])[[:alnum:]_]*\([^)]+\)[[:space:]]*;[^;]*\.(set[A-Z]|Set[A-Z])|critical|TC-015|Multiple setter calls without atomic publication (torn read risk)|Publish state atomically: use immutable objects, builder pattern, or protect with lock'
)

# ============================================================================
# 4. ASYNC/AWAIT PITFALLS (AW-001 through AW-015)
# ============================================================================

declare -a CONCURRENCYGUARD_AW_PATTERNS=()

CONCURRENCYGUARD_AW_PATTERNS+=(
  # --- AW-001: Await inside loop ---
  '(for|while|forEach)[[:space:]]*\(.*\)[[:space:]]*\{[^}]*await[[:space:]]|high|AW-001|Await inside loop executes sequentially instead of in parallel|Use Promise.all() or Promise.allSettled() with Array.map() for parallel execution'

  # --- AW-002: Missing await on async call ---
  '[[:alnum:]_]+\.(then|catch)\(|critical|AW-002|Promise used with .then()/.catch() -- may indicate missing await|Use await keyword instead of .then() chains for clearer error handling and flow control'

  # --- AW-003: Async void method in C# ---
  'async[[:space:]]+void[[:space:]]+[[:alnum:]_]+|high|AW-003|Async void method in C# (unobserved exceptions, cannot be awaited)|Use async Task instead of async void; only use async void for event handlers'

  # --- AW-004: Fire-and-forget promise ---
  '[[:alnum:]_]+\([^)]*\)[[:space:]]*;[[:space:]]*(//|/\*|$)|critical|AW-004|Potential fire-and-forget async call (no await, no .catch)|Add await keyword or attach .catch() handler to prevent unhandled rejections'

  # --- AW-005: State update after await ---
  'await[[:space:]]+[^;]+;[[:space:]]*[[:alnum:]_]+[[:space:]]*[+\-*/]?=[[:space:]]|high|AW-005|Shared state modification after await point (race condition risk)|Re-read state after await, use atomic operations, or protect with async mutex'

  # --- AW-006: Missing Promise.all ---
  'const[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*await[[:space:]]+[[:alnum:]_]+\([^)]*\)[[:space:]]*;[[:space:]]*const[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*await|high|AW-006|Sequential await calls that could run in parallel|Use Promise.all([fn1(), fn2()]) or Promise.allSettled() for independent operations'

  # --- AW-007: Async function without try/catch ---
  'async[[:space:]]+function[[:space:]]+[[:alnum:]_]+|medium|AW-007|Async function detected -- verify proper error handling exists|Add try/catch block or ensure caller handles rejected promise'

  # --- AW-008: Shared state across await boundary ---
  'this\.[[:alnum:]_]+[[:space:]]*=[[:space:]].*await|high|AW-008|Instance property mutation across await boundary (stale state risk)|Re-read this.prop after await; use local variable to capture state before await'

  # --- AW-009: Multiple awaits on same promise ---
  '(await[[:space:]]+[[:alnum:]_]+)[[:space:]]*;[^;]*(await[[:space:]]+[[:alnum:]_]+)|critical|AW-009|Same variable potentially awaited multiple times (double resolution)|Await a promise only once; store result in a variable for reuse'

  # --- AW-010: Callback mixed with async ---
  'callback\(|cb\(|next\(|done\(|medium|AW-010|Callback-based pattern mixed with async/await code|Convert callbacks to promises (util.promisify) or use fully async patterns'

  # --- AW-011: Missing error propagation ---
  '\.catch\([[:space:]]*\(\)[[:space:]]*=>[[:space:]]*\{[[:space:]]*\}|medium|AW-011|Empty catch handler swallowing async errors|Log the error or re-throw; empty catch blocks hide failures silently'

  # --- AW-012: Async generator without cleanup ---
  'async[[:space:]]+\*[[:space:]]*[[:alnum:]_]+|high|AW-012|Async generator function detected -- verify proper cleanup on early exit|Use try-finally in generator to clean up resources when consumer stops iteration'

  # --- AW-013: Unhandled promise rejection ---
  'new[[:space:]]+Promise[[:space:]]*\([[:space:]]*\([[:space:]]*(resolve|reject)|critical|AW-013|Promise constructor detected -- verify rejection is always handled|Always provide reject handler or use .catch(); unhandled rejections crash Node.js'

  # --- AW-014: Sequential async that could be parallel ---
  'await[[:space:]]+fetch\(|await[[:space:]]+axios|await[[:space:]]+http|medium|AW-014|Sequential HTTP await calls that may be parallelizable|Group independent HTTP calls with Promise.all() for better performance'

  # --- AW-015: Lock held across await ---
  '(lock|Lock|acquire)[[:space:]]*\([^)]*\)[[:space:]]*;[^;]*await[[:space:]]|high|AW-015|Lock or mutex held across an await point (may cause async deadlock)|Release lock before await, use async-aware mutex, or restructure to minimize lock scope'
)

# ============================================================================
# 5. THREAD SAFETY (TS-001 through TS-015)
# ============================================================================

declare -a CONCURRENCYGUARD_TS_PATTERNS=()

CONCURRENCYGUARD_TS_PATTERNS+=(
  # --- TS-001: Thread-unsafe singleton ---
  'private[[:space:]]+static[[:space:]]+[[:alnum:]_]+[[:space:]]+instance[[:space:]]*;|critical|TS-001|Thread-unsafe singleton pattern (unprotected static instance field)|Use enum singleton (Java), Lazy<T> (C#), sync.Once (Go), or volatile + double-checked locking'

  # --- TS-002: HashMap without sync in Java ---
  'new[[:space:]]+HashMap[[:space:]]*<|critical|TS-002|HashMap created without synchronization (not thread-safe)|Use ConcurrentHashMap or Collections.synchronizedMap() for concurrent access'

  # --- TS-003: Non-thread-safe SimpleDateFormat ---
  'new[[:space:]]+SimpleDateFormat[[:space:]]*\(|high|TS-003|SimpleDateFormat is not thread-safe in Java|Use DateTimeFormatter (Java 8+) which is thread-safe, or use ThreadLocal<SimpleDateFormat>'

  # --- TS-004: Mutable default in Python ---
  'def[[:space:]]+[[:alnum:]_]+\([^)]*=[[:space:]]*(\[|\{|dict\(|list\(|set\()|high|TS-004|Mutable default argument in Python function (shared across calls)|Use None as default and create new mutable inside function: if arg is None: arg = []'

  # --- TS-005: Lazy init without double-check ---
  'if[[:space:]]*\([[:space:]]*instance[[:space:]]*==[[:space:]]*null[[:space:]]*\)[[:space:]]*\{[^}]*instance[[:space:]]*=[[:space:]]*new|critical|TS-005|Lazy initialization without double-checked locking (race condition)|Use double-checked locking with volatile, Lazy<T>, or synchronized lazy init'

  # --- TS-006: StringBuilder shared across threads ---
  'static[[:space:]]+(final[[:space:]]+)?StringBuilder[[:space:]]|high|TS-006|Static StringBuilder in Java/C# (not thread-safe)|Use local StringBuilder per thread, or StringBuffer (synchronized) if sharing required'

  # --- TS-007: Shared regex object ---
  'static[[:space:]]+(final[[:space:]]+)?Pattern[[:space:]]|high|TS-007|Static Pattern/Regex object shared across threads (Matcher is not thread-safe)|Pattern is thread-safe but Matcher is not; create new Matcher per thread'

  # --- TS-008: Thread-unsafe cache ---
  '(Cache|cache)[[:space:]]*=[[:space:]]*new[[:space:]]+(HashMap|Dictionary|dict|Map)\b|critical|TS-008|Cache implemented with non-concurrent data structure|Use ConcurrentHashMap, ConcurrentDictionary, or a thread-safe cache library'

  # --- TS-009: Shared Random instance ---
  'static[[:space:]]+(final[[:space:]]+)?Random[[:space:]]|high|TS-009|Shared static Random instance (contention, poor randomness under concurrency)|Use ThreadLocalRandom (Java), or create per-thread Random instances'

  # --- TS-010: Mutable return from synchronized ---
  'synchronized[[:space:]]*.*return[[:space:]]+[[:alnum:]_]+[[:space:]]*;|medium|TS-010|Returning mutable reference from synchronized method (escaping lock)|Return defensive copy or immutable view of the data'

  # --- TS-011: Thread-unsafe event handler ---
  '(addEventListener|on\([[:space:]]*["'"'"']|\.on[A-Z][[:alnum:]_]*[[:space:]]*=)|high|TS-011|Event handler registration without synchronization|Use thread-safe event bus or synchronize handler list modifications'

  # --- TS-012: Publishing this in constructor ---
  'this\.[[:alnum:]_]+[[:space:]]*=[[:space:]]*this[[:space:]]*;|critical|TS-012|Publishing this reference during construction (object may be incomplete)|Never leak this reference during construction; use factory method pattern'

  # --- TS-013: Iteration over shared collection ---
  'for[[:space:]]*\([[:alnum:][:space:]_]+:[[:space:]]*[[:alnum:]_]+\)|high|TS-013|Enhanced for-loop over potentially shared collection (ConcurrentModificationException)|Use iterator from ConcurrentHashMap, copy collection before iteration, or sync'

  # --- TS-014: Thread-unsafe collection usage ---
  'new[[:space:]]+(ArrayList|LinkedList|HashSet|TreeSet|TreeMap|LinkedHashMap|PriorityQueue)[[:space:]]*[<(]|medium|TS-014|Non-thread-safe collection created (verify not shared across threads)|Use concurrent equivalents: CopyOnWriteArrayList, ConcurrentSkipListSet, etc.'

  # --- TS-015: Missing @ThreadSafe annotation ---
  '@(Singleton|Service|Component|Repository|Controller)[[:space:]]*$|high|TS-015|Spring/Jakarta bean without @ThreadSafe annotation (shared by default)|Add @ThreadSafe annotation and ensure all fields are immutable or properly synchronized'
)

# ============================================================================
# 6. DEADLOCK & STARVATION (DL-001 through DL-015)
# ============================================================================

declare -a CONCURRENCYGUARD_DL_PATTERNS=()

CONCURRENCYGUARD_DL_PATTERNS+=(
  # --- DL-001: Inconsistent lock ordering ---
  'synchronized[[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*\).*synchronized[[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)|critical|DL-001|Multiple synchronized blocks with potentially inconsistent lock ordering|Always acquire locks in a consistent global order; use Lock.tryLock() with timeout'

  # --- DL-002: Lock held while calling external ---
  'synchronized[[:space:]]*\([^)]*\)[[:space:]]*\{[^}]*\.[[:alnum:]_]+\([^)]*\)|high|DL-002|Calling external/virtual method while holding lock (deadlock risk)|Release lock before calling external methods; use open call pattern'

  # --- DL-003: Go channel without timeout ---
  '<-[[:space:]]*[[:alnum:]_]+[[:space:]]*$|critical|DL-003|Blocking channel receive without timeout in Go (potential goroutine leak)|Use select with time.After or context.Done for timeout on channel operations'

  # --- DL-004: Unbuffered channel in goroutine ---
  'make\(chan[[:space:]]+[[:alnum:]_]+\)[[:space:]]*$|high|DL-004|Unbuffered channel created (sender blocks until receiver ready)|Use buffered channel make(chan T, n) or ensure goroutine pairs are properly managed'

  # --- DL-005: Missing select default ---
  'select[[:space:]]*\{[^}]*case[^}]*\}|high|DL-005|Select statement without default case (may block indefinitely)|Add default case for non-blocking operation, or use time.After for timeout'

  # --- DL-006: Lock across await point ---
  '(lock|Lock|synchronized|mutex)\([^)]*\)[[:space:]]*\{[^}]*await[[:space:]]|critical|DL-006|Lock/mutex held across await point (async deadlock risk)|Release lock before await, or use async-compatible lock (SemaphoreSlim in C#)'

  # --- DL-007: Recursive lock acquisition ---
  'synchronized[[:space:]]*\([[:space:]]*this[[:space:]]*\).*synchronized[[:space:]]*\([[:space:]]*this[[:space:]]*\)|high|DL-007|Recursive synchronized on same monitor (reentrant but fragile)|Use explicit ReentrantLock or restructure to avoid nested locking on same object'

  # --- DL-008: Multiple locks without ordering ---
  '(lock|Lock)\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)[[:space:]]*;[^;]*(lock|Lock)\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)|critical|DL-008|Acquiring multiple locks without consistent ordering (deadlock risk)|Define and enforce a global lock ordering; use java.util.concurrent.locks.Lock.tryLock()'

  # --- DL-009: Blocking call inside synchronized ---
  'synchronized[[:space:]]*\([^)]*\)[[:space:]]*\{[^}]*(Thread\.sleep|wait\(\)|\.get\(\)|\.join\(\)|\.await\(\))|high|DL-009|Blocking call inside synchronized block (starvation and deadlock risk)|Move blocking operations outside the synchronized block; use condition variables'

  # --- DL-010: Thread.sleep inside lock ---
  '(Thread\.sleep|time\.sleep|Task\.Delay|time\.Sleep)\(|medium|DL-010|Thread sleep call detected -- verify not inside a lock or synchronized block|Never sleep while holding a lock; use condition variables or timed waits instead'

  # --- DL-011: Missing timeout on lock acquisition ---
  '\.lock\(\)[[:space:]]*;|\.Lock\(\)|high|DL-011|Lock acquisition without timeout (may deadlock indefinitely)|Use tryLock(timeout) in Java, Monitor.TryEnter in C#, or select with timeout in Go'

  # --- DL-012: Goroutine without context ---
  'go[[:space:]]+[[:alnum:]_]+\(|critical|DL-012|Goroutine spawned without context.Context (potential goroutine leak)|Pass context.Context and select on ctx.Done() for cancellation support'

  # --- DL-013: WaitGroup.Add inside goroutine ---
  'go[[:space:]]+func.*wg\.Add\(|high|DL-013|WaitGroup.Add() called inside goroutine (race with wg.Wait())|Call wg.Add() BEFORE launching the goroutine, not inside it'

  # --- DL-014: Reader-writer with writer starvation ---
  'RWMutex|ReentrantReadWriteLock|ReadWriteLock|medium|DL-014|Reader-writer lock detected -- verify writers are not starved|Monitor for writer starvation; consider fair read-write lock or write-preferring lock'

  # --- DL-015: Semaphore without timeout ---
  '(Semaphore|semaphore)\.(acquire|Acquire|Wait|wait)\(|high|DL-015|Semaphore acquisition without timeout|Use tryAcquire(timeout) or WaitOne(timeout) to prevent indefinite blocking'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
concurrencyguard_pattern_count() {
  local count=0
  count=$((count + ${#CONCURRENCYGUARD_SS_PATTERNS[@]}))
  count=$((count + ${#CONCURRENCYGUARD_LK_PATTERNS[@]}))
  count=$((count + ${#CONCURRENCYGUARD_TC_PATTERNS[@]}))
  count=$((count + ${#CONCURRENCYGUARD_AW_PATTERNS[@]}))
  count=$((count + ${#CONCURRENCYGUARD_TS_PATTERNS[@]}))
  count=$((count + ${#CONCURRENCYGUARD_DL_PATTERNS[@]}))
  echo "$count"
}

# List patterns by category
concurrencyguard_list_patterns() {
  local filter_type="${1:-all}"
  local -n _cg_patterns_ref

  case "$filter_type" in
    SS) _cg_patterns_ref=CONCURRENCYGUARD_SS_PATTERNS ;;
    LK) _cg_patterns_ref=CONCURRENCYGUARD_LK_PATTERNS ;;
    TC) _cg_patterns_ref=CONCURRENCYGUARD_TC_PATTERNS ;;
    AW) _cg_patterns_ref=CONCURRENCYGUARD_AW_PATTERNS ;;
    TS) _cg_patterns_ref=CONCURRENCYGUARD_TS_PATTERNS ;;
    DL) _cg_patterns_ref=CONCURRENCYGUARD_DL_PATTERNS ;;
    all)
      concurrencyguard_list_patterns "SS"
      concurrencyguard_list_patterns "LK"
      concurrencyguard_list_patterns "TC"
      concurrencyguard_list_patterns "AW"
      concurrencyguard_list_patterns "TS"
      concurrencyguard_list_patterns "DL"
      return
      ;;
    *)
      echo "Unknown category: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_cg_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "%-12s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a category
get_concurrencyguard_patterns_for_category() {
  local category="$1"
  case "$category" in
    ss) echo "CONCURRENCYGUARD_SS_PATTERNS" ;;
    lk) echo "CONCURRENCYGUARD_LK_PATTERNS" ;;
    tc) echo "CONCURRENCYGUARD_TC_PATTERNS" ;;
    aw) echo "CONCURRENCYGUARD_AW_PATTERNS" ;;
    ts) echo "CONCURRENCYGUARD_TS_PATTERNS" ;;
    dl) echo "CONCURRENCYGUARD_DL_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# All category names for iteration
get_all_concurrencyguard_categories() {
  echo "ss lk tc aw ts dl"
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
