# Port Pairs — mapping tables for common language pairs

Read only the section for your pair. Each section maps constructs to the target's *idiom* (not nearest syntax), then lists traps and ecosystem equivalents. Library suggestions are common, well-maintained choices, not mandates — prefer what the target project already uses. Verify versions against the project's toolchain.

## Contents
1. Python → Go · 2. Go → Python · 3. JavaScript/TypeScript → Rust · 4. Rust → TypeScript · 5. Java → Kotlin · 6. Kotlin → Java · 7. C → Rust · 8. Rust → C (FFI surface) · 9. JavaScript → TypeScript (gradual typing) · 10. Python → Rust · 11. Rust → Python · 12. TypeScript → Go · 13. Go → TypeScript

---

## 1. Python → Go

### Types and data
| Python | Go | Notes |
|---|---|---|
| `int` (unbounded) | `int`/`int64`; `math/big.Int` when values can exceed 64 bits | Go wraps silently on overflow — decide per value |
| `float` | `float64` | |
| `str` (code points) | `string` (UTF-8 bytes) | `len` counts bytes; `s[i]` is a byte; iterate runes with `for _, r := range s` or convert to `[]rune` |
| `bytes` | `[]byte` | |
| `list` | slice `[]T` | Heterogeneous lists need a real type (struct/interface), not `[]any` |
| `dict` | `map[K]V` | Go map iteration order is random — sort keys or keep an ordered slice when order is observable |
| `set` | `map[T]struct{}` | |
| `tuple` / multiple returns | multiple return values or a small struct | |
| `None` / `Optional[T]` | zero value, `*T`, or `(T, bool)` "comma ok" | Pick deliberately: zero values hide "missing" vs "zero" |
| `@dataclass` | `struct` (+ constructor `NewX` if invariants) | `==` works only for comparable fields |
| `Enum` | typed constants with `iota` + `String()` method | Validate unknown values explicitly |
| class with inheritance | struct + embedding + small interfaces | Interfaces are implicit; define them at the consumer |
| duck typing / `Protocol` | interface | |
| `__str__` / `__repr__` | `String() string` (fmt.Stringer) | |
| decorators | higher-order functions / middleware wrappers | |
| generators / `yield` | `iter.Seq[T]` (Go 1.23+ range-over-func), or callback; channels only when concurrency is intended | A goroutine-backed generator leaks if the consumer stops early |
| comprehensions | `for` loops; `slices`/`maps` helpers | |
| `**kwargs` / defaults | options struct or functional options | |

### Errors and resources
- `raise` → return `error` as last value; `raise X from e` → `fmt.Errorf("context: %w", err)`.
- `except SomeError` → `errors.Is` (sentinel) / `errors.As` (typed). Keep one error type or sentinel per distinct exception class callers catch.
- `try/finally`, `with` → `defer` right after acquiring the resource; check `Close()` errors on writers.
- `panic` only for programmer errors, never for input the Python code raised a catchable exception for.
- Exception messages that callers or tests match must be reproduced in `Error()` text.

### Concurrency
- No GIL in Go: code that was accidentally safe under CPython can race. Guard shared state with `sync.Mutex` or confine it to one goroutine; run `go test -race`.
- `threading` / `concurrent.futures` → goroutines + `sync.WaitGroup` or `errgroup.Group`.
- `asyncio` → goroutines and channels; propagate `context.Context` for cancellation and deadlines as the first parameter.
- `asyncio.gather` order of results → collect into an indexed slice to keep input order.

### Numeric and string traps
- `//` floors toward −∞; Go `/` truncates toward 0: `-7 // 2 == -4` vs `-7 / 2 == -3`. `%`: Python `-7 % 2 == 1`, Go `-7 % 2 == -1`. Write a `floorDiv`/`floorMod` helper when negatives are possible.
- `round(2.5) == 2` (banker's) vs `math.Round(2.5) == 3`; use `math.RoundToEven` to match.
- `str(1.0) == "1.0"` vs `fmt.Sprint(1.0) == "1"`; `repr` of floats vs `strconv.FormatFloat(f, 'g', -1, 64)` — check formatting of whole numbers and large exponents.
- `sorted()` is stable; `sort.Slice` is not — use `slices.SortStableFunc` / `sort.SliceStable`.
- `json.dumps` default separators are `", "` and `": "`; Go `json.Marshal` is compact and sorts map keys (structs keep field order). Python keeps dict insertion order.
- `re` supports lookaround/backreferences; Go `regexp` (RE2) does not. Rewrite the pattern or the logic; a third-party backtracking engine is a last resort.
- `datetime` naive vs aware; Go `time.Time` always has a location. Format layouts use the reference time `2006-01-02 15:04:05`.

### Ecosystem
| Python | Go |
|---|---|
| `requests` / `httpx` | `net/http` (set timeouts explicitly; default client has none) |
| `json` / `pydantic` | `encoding/json` + struct tags; validation via `go-playground/validator` or explicit checks |
| `argparse` / `click` / `typer` | `flag` (stdlib) or `spf13/cobra` |
| `logging` | `log/slog` |
| `pathlib` / `os.path` | `path/filepath`, `os` |
| `subprocess` | `os/exec` |
| `collections.Counter` / `defaultdict` | `map[K]int` / map with explicit init |
| `heapq` | `container/heap` |
| `functools.lru_cache` | explicit cache (map + mutex) or `sync.OnceValue` for single values |
| `itertools` | loops, `slices`, `iter` package |
| `pytest` / `unittest` | `testing` with table-driven tests; `go-cmp` for diffs; golden files |
| `unittest.mock` | interfaces + hand-written fakes |
| `SQLAlchemy` | `database/sql` + `sqlc` or `sqlx` |
| `FastAPI` / `Flask` | `net/http` (Go 1.22+ pattern routing), `chi`, or `gin` |
| `numpy` / `pandas` | limited equivalents (`gonum`); consider keeping that part in Python behind a process boundary |

Project: `pyproject.toml` → `go.mod`; package per directory; exported = Capitalized; `gofmt`, `go vet`, `golangci-lint`.

---

## 2. Go → Python

| Go | Python | Notes |
|---|---|---|
| multiple returns `(T, error)` | return value; raise exception on error | Define an exception class per sentinel/typed error callers distinguish |
| `errors.Is/As`, `%w` wrapping | exception hierarchy; `raise New(...) from err` | |
| `defer` | `try/finally`, `with`, `contextlib.ExitStack` | Deferred calls run LIFO — preserve order |
| interfaces (implicit) | `typing.Protocol` (static) / duck typing | |
| struct embedding | composition (preferred) or inheritance | |
| zero values | explicit defaults in `__init__`/dataclass fields | Missing fields no longer silently zero — decide |
| fixed-width ints with wraparound | `int` is unbounded | Mask (`& 0xFFFFFFFF`) where wraparound was relied on (hashes, checksums) |
| `[]byte` vs `string` | `bytes` vs `str` | Go strings may hold invalid UTF-8; Python `str` cannot — keep as `bytes` when unsure |
| goroutines + channels | `asyncio` tasks + `asyncio.Queue` (I/O-bound); `concurrent.futures`/`multiprocessing` (CPU-bound, GIL) | `select` → `asyncio.wait(..., return_when=FIRST_COMPLETED)` |
| `context.Context` cancellation | `asyncio` cancellation / timeouts (`asyncio.timeout`) | |
| `map` iteration (random) | dict (insertion order) | If Go output order was sorted for determinism, keep the sort |
| `sort.Slice` (unstable) | `sorted` (stable) | Ties may now come out in a different (stable) order — check fixtures |
| `math.Round` (half away) | `round` is banker's → use `decimal` with `ROUND_HALF_UP` or a helper | |
| `/` on ints truncates | `//` floors | Use `int(a / b)` carefully (float precision) or a truncating helper for negatives |
| `encoding/json` | `json` (use `separators=(",", ":")`, `sort_keys=True` to match Go output) | |
| `testing` table tests | `pytest.mark.parametrize` | |

---

## 3. JavaScript/TypeScript → Rust

### Types and data
| JS/TS | Rust | Notes |
|---|---|---|
| `number` | choose: `i64`/`u32`/`usize`/`f64` | JS integers are exact only up to 2^53; bitwise ops in JS truncate to 32-bit signed (`x \| 0`, `>>>`) |
| `bigint` | `i128` / `num-bigint` | |
| `string` (UTF-16) | `String` / `&str` (UTF-8) | `.length` counts UTF-16 units; Rust `.len()` counts bytes; `.chars().count()` counts scalar values; byte-index slicing panics off char boundaries |
| `null` / `undefined` / optional props | `Option<T>` | Distinguish "missing" vs "null" in JSON with `Option<Option<T>>` or serde attributes when it matters |
| `a?.b ?? c` | `a.as_ref().and_then(\|x\| x.b).unwrap_or(c)` or `?` inside a fn returning `Option` | |
| interface / object type | `struct` (nominal) | TS is structural; Rust needs named types or traits |
| discriminated union | `enum` with data + exhaustive `match` | |
| `any` / `unknown` at boundaries | concrete types; `serde_json::Value` only at genuinely dynamic edges | |
| class + inheritance | struct + `impl` + traits; composition | |
| closures capturing mutable shared state | ownership redesign: pass `&mut`, return new values, `move` closures; `Rc<RefCell<T>>` / `Arc<Mutex<T>>` only when sharing is real | |
| object graphs with back-references | arena / `Vec` + indices / IDs | Avoid raw pointers and `Rc` cycles |
| `Map` / `Set` (insertion order) | `HashMap` / `HashSet` (unordered); `indexmap::IndexMap` to keep insertion order; `BTreeMap` for sorted | |
| array methods `map/filter/reduce` | iterator adapters `.iter().map().filter().fold()` | `reduce` without initial value throws on empty in JS; `Iterator::reduce` returns `Option` |
| `Array.prototype.sort` | `sort_by` (stable) / `sort_unstable_by` | JS default `sort()` compares as strings; comparator returns number vs `Ordering`; `f64` needs `total_cmp`/`partial_cmp` |
| `Date` | `chrono` / `time` / `jiff` | JS months are 0-based |
| enums (TS) | `enum` (+ `#[repr(..)]`/serde rename for wire values) | |

### Errors
- `throw` / `try-catch` → `Result<T, E>` with `?`. Libraries: an error `enum` (e.g. via `thiserror`) with one variant per failure mode callers handle; applications: `anyhow` with context.
- Rejected promises → `Err` from `async fn`.
- Never `unwrap()`/`expect()` on input-dependent values; panics are for broken invariants.
- If the JS code threw for invalid input, the Rust code returns an error for the same inputs (fixtures cover them).

### Async and concurrency
- JS promises start immediately; Rust futures do nothing until awaited/spawned. A "fire and forget" call must become an explicit `tokio::spawn` (or be awaited).
- Single-threaded event loop → multi-threaded runtime: shared state needs `Send + Sync` (`Arc<Mutex<_>>`, channels); holding a `std::sync::Mutex` guard across `.await` is a bug — restructure or use `tokio::sync::Mutex`.
- `Promise.all` → `futures::future::try_join_all` / `tokio::try_join!` / `JoinSet`; `Promise.allSettled` → `join_all` collecting `Result`s; `setTimeout` → `tokio::time::sleep`; `AbortController` → `CancellationToken` / dropping the future.

### Serialization traps
- `JSON.stringify(1.0) === "1"`; `serde_json` writes `1.0` for `f64`. Use integer types where the value is integral, or a custom serializer if exact text matters.
- `JSON.stringify` keeps object insertion order; `serde_json::Map` is sorted unless the `preserve_order` feature is enabled (struct fields keep declaration order).
- `undefined` fields are omitted by JSON.stringify; `None` serializes as `null` unless `#[serde(skip_serializing_if = "Option::is_none")]`.

### Ecosystem
| JS/TS | Rust |
|---|---|
| Express / Fastify / Koa | `axum`, `actix-web` |
| `fetch` / axios | `reqwest` |
| zod / yup | `serde` + `validator` or `garde`; parse at the boundary into typed structs |
| lodash | std iterators, `itertools` |
| commander / yargs | `clap` |
| dotenv | `dotenvy` |
| winston / pino | `tracing` + `tracing-subscriber` |
| jest / vitest | `cargo test`, `insta` (snapshots), `proptest`, `rstest` (parametrized) |
| `regex` (backtracking) | `regex` (no lookaround/backrefs); `fancy-regex` only if unavoidable |
| `uuid`, `crypto` | `uuid`, RustCrypto crates (`sha2`, `hmac`, …) / `ring` |
| Node `fs/promises` | `std::fs` / `tokio::fs` |
| Prisma / TypeORM | `sqlx`, `diesel`, `sea-orm` |

Integration options: whole replacement (CLI/service), or Rust core exposed to Node via `napi-rs` / to the browser via `wasm-bindgen` (end state B or C). Format with `rustfmt`, lint with `clippy`.

---

## 4. Rust → TypeScript

| Rust | TypeScript | Notes |
|---|---|---|
| `Result<T, E>` | discriminated union `{ ok: true, value } \| { ok: false, error }` or throw typed errors | Pick one convention per module; document it |
| `Option<T>` | `T \| undefined` (or `null` if the wire format uses null) | |
| `enum` with data + `match` | discriminated union + `switch` with exhaustive `never` check | |
| integer types (`u8`…`u64`, `i128`) | `number` (exact ≤ 2^53) or `bigint` | `u8` wraparound → `& 0xff`; `u32` → `>>> 0`; overflow checks become manual |
| ownership / borrowing | references are shared and mutable | Where Rust moved or cloned, the TS code may now alias — copy defensively or make data immutable (`readonly`, `Object.freeze`) |
| traits | interfaces (structural) | Blanket impls → helper functions |
| macros | functions, generics, or build-time codegen | |
| threads / rayon | `worker_threads` / Web Workers; often just async I/O | |
| `serde` | zod/valibot schemas at boundaries + types | Re-check float and key-order formatting (section 3) in reverse |
| `cargo test` | vitest/jest | |

---

## 5. Java → Kotlin

### Approach
- Migrate file by file in a mixed Java/Kotlin module; Java and Kotlin call each other directly. Start with tests or leaf classes (models, utilities), then services, then entry points.
- IntelliJ's Java-to-Kotlin converter (J2K) gives a draft; treat it as transliteration and idiomatize after the tests pass on the draft (two separate steps).
- Keep the JVM signatures Java callers use stable until they are migrated too.

### Mapping
| Java | Kotlin | Interop / traps |
|---|---|---|
| nullable references | `T?` vs `T` | Java types without nullability annotations become platform types (`T!`) — decide nullability explicitly; avoid `!!`; add `@Nullable/@NonNull` on remaining Java side |
| getters/setters | properties | JVM names stay `getX()/setX()`; booleans `isX()`; use `@JvmName` to keep any other existing name |
| `static` members | top-level functions, `companion object`, or `object` | Java callers need `@JvmStatic` / `@JvmField` to keep `Foo.bar()` call syntax |
| overloads for optional args | default parameters | Add `@JvmOverloads` so Java callers keep the overloads |
| checked exceptions | none | Add `@Throws(IOException::class)` so Java callers can still catch them at compile time |
| POJO with `equals/hashCode/toString` | `data class` | `equals` uses primary-constructor properties only; `toString` format changes (`User(id=1, …)`); not for JPA entities (need no-arg + open: `kotlin-jpa`, `all-open` plugins) |
| `final` opt-in | classes/methods final by default | Spring proxies and Mockito need `open` → `kotlin-spring`/`all-open` plugin, or `mockito-inline`/MockK |
| `switch` / if-chains on type | `when` (exhaustive for `sealed`/`enum` when used as expression) | |
| class hierarchies for variants | `sealed` classes/interfaces | |
| streams | collection operations (eager, intermediate lists) or `asSequence()` (lazy) | Laziness and short-circuit side effects differ — keep `Sequence` where the stream relied on laziness |
| `Collectors.toMap` | `associate` / `associateBy` | `toMap` **throws** on duplicate keys; `associate` keeps the **last** value silently — add an explicit duplicate check to preserve behavior |
| `Collectors.groupingBy` | `groupBy` | Result map type/order may differ (`LinkedHashMap` in Kotlin) |
| `Optional<T>` | `T?` | Keep `Optional` in signatures Java callers still use |
| Lombok `@Data/@Builder/@Value` | data class, named/default args, `val` | Remove Lombok from a class only when converting it; kapt + Lombok mixes are fragile |
| `==` on objects / `equals` | `==` is `equals`; `===` is identity | Java `==` on boxed `Integer` was identity (cache −128..127) — check intent before translating |
| `CompletableFuture`, executors | coroutines (`suspend`, `Dispatchers.IO`, structured concurrency) | `suspend` functions aren't callable from Java; expose `CompletableFuture` wrappers (`kotlinx.coroutines.future.future { }`, part of kotlinx-coroutines-core since 1.7) for Java callers |
| `synchronized`, `volatile` | `@Synchronized`, `@Volatile`, or `Mutex` in coroutines | |
| implicit widening (`int` → `long`) | explicit conversion (`toLong()`) | `Char` is not a number in Kotlin |
| string concatenation / `String.format` | templates `"$x"`; `String.format` still available | Format locale defaults unchanged |
| `List` (mutable) | `List` (read-only view) / `MutableList` | A Kotlin `List` from Java may still be mutated by Java code |

Tests: JUnit 5 works unchanged; MockK fits Kotlin finals; keep the Java tests running against Kotlin code during migration (best parity evidence).

---

## 6. Kotlin → Java

| Kotlin | Java (17/21) | Notes |
|---|---|---|
| `data class` | `record` (immutable; accessors are `x()` not `getX()`) or POJO when mutability/inheritance/JPA needed | Callers using `getX()` break with records |
| default/named args | overloads or builder | |
| extension functions | static utility methods | |
| null safety | `@Nullable/@NonNull` annotations + `Optional` for return values | Add explicit null checks where Kotlin's compiler guaranteed non-null |
| `sealed` + `when` | `sealed interface` + records + pattern-matching `switch` (Java 21) | |
| coroutines | `CompletableFuture`, virtual threads (Java 21), or executors | Structured cancellation must be re-implemented |
| `object` | singleton (enum singleton or static holder) | |
| `associate` (last wins) | `toMap(k, v, (a, b) -> b)` | Without the merge function Java throws on duplicates |
| top-level functions | `final class XKt { static … }` style utility class | Keep `@file:JvmName` names if Java callers exist |

---

## 7. C → Rust

### Approach
- Choose the end state first (playbook section 3). Common path: Rust module behind the existing C header (end state C or B), leaf modules first, C tests kept running against the Rust implementation.
- `c2rust` can produce a mechanical (unsafe) translation as a starting point for large code; treat it as scaffolding to refactor into safe Rust, not as the result.
- Build integration: `cc` crate to compile remaining C from Cargo; `bindgen` to call C from Rust; `cbindgen` to generate C headers for Rust exports; `corrosion` for CMake projects.

### Mapping
| C | Rust | Notes |
|---|---|---|
| `malloc`/`free`, manual lifetimes | `Box`, `Vec`, `String`, `Drop` | Ownership replaces conventions like "caller frees" — document who owned what in the C API |
| pointer + length | slice `&[T]` / `&mut [T]` | |
| `char *` strings | `&[u8]`/`Vec<u8>` (bytes); `&str` only if UTF-8 is guaranteed; `CStr`/`CString` at FFI | C strings are NUL-terminated bytes with no encoding guarantee |
| `NULL` | `Option<&T>`, `Option<Box<T>>`; `Option<NonNull<T>>` / nullable raw pointer at FFI | |
| return codes, `errno`, `-1` | `Result<T, E>` with an error enum | At the FFI boundary convert back to the original codes exactly |
| out-parameters | return value / tuple / struct | Keep out-params only in the FFI shim |
| `goto cleanup` | early return + `Drop`, `?` | |
| tagged struct + `union` | `enum` with data | `#[repr(C)] union` only at FFI |
| `#define` constants/macros | `const`, `const fn`, `#[inline]` fns, generics; `macro_rules!` sparingly | |
| bit-fields | explicit masks/shifts or `bitflags` | Layout of C bit-fields is implementation-defined — match the actual compiler's layout at FFI |
| function pointer + `void *user_data` | closures / trait objects; at FFI `extern "C" fn` + `*mut c_void` | |
| linked lists, graphs with raw pointers | `Vec` + indices, arenas, `slotmap`; `VecDeque` for queues | |
| global mutable state | context struct passed explicitly; `static` with `OnceLock`/`Mutex`/atomics | |
| pthreads, mutex protecting data by convention | `std::thread`, `Mutex<T>` owning the data, `Arc`, atomics with the same memory orderings | `volatile` is not synchronization in either language |
| struct layout relied on | `#[repr(C)]` for every type crossing FFI or mapped onto bytes | |

### Integer and memory semantics (the main parity risk)
- Signed overflow is undefined behavior in C; Rust panics in debug and wraps in release by default. Decide per operation: `wrapping_*` (match two's-complement intent, e.g. hashes), `checked_*` (return error), `saturating_*`.
- C integer promotions and implicit conversions → explicit `as` (truncates/sign-extends silently) or `TryFrom` (fails loudly). Audit every `as`.
- `char` signedness, `int`/`long` width, and `size_t` are platform-dependent: use `c_int`, `c_long`, `usize` at FFI, fixed-width types internally after checking the actual ranges.
- Out-of-bounds access that "worked" in C now panics. Characterize with sanitizers (ASan/UBSan) on the C side first; an existing OOB bug is a source bug to record, not a behavior to reproduce silently.
- Shift by ≥ width is UB in C and a panic (debug) in Rust; `wrapping_shl` masks the amount.

### FFI rules
- Exported functions: `#[unsafe(no_mangle)] pub extern "C" fn` (Rust 2024 syntax; `#[no_mangle]` on older editions), never unwind across FFI — catch panics (`std::panic::catch_unwind`) and convert to error codes.
- Validate every pointer from C (null, alignment, length) before creating references; document each `unsafe` block with a `// SAFETY:` comment stating the invariant relied on.
- Ownership across the boundary: memory allocated by Rust is freed by a Rust-exported function, and vice versa.
- Test the boundary: run the original C test suite against the Rust implementation, differential-fuzz C vs Rust (`cargo-fuzz` calling both), and run Miri on unsafe-heavy Rust code.

---

## 8. Rust → C (FFI surface)

Rare as a full port; usually means exposing Rust to C. Provide an opaque handle type (`typedef struct Foo Foo;`), constructor/destructor pairs, error codes instead of `Result`, out-parameters for multiple returns, and NUL-terminated strings with explicit free functions. Generate the header with `cbindgen` and keep a C test that exercises every exported function.

---

## 9. JavaScript → TypeScript (gradual typing)

Not a language change at runtime, but a port of the type surface:
- Enable `allowJs` (+ `checkJs` optionally), rename files leaf-first (`.js` → `.ts`), keep emitted JS behavior identical (same target/module settings, no new downlevel transforms).
- Start with `strict: false`, then enable strict flags one at a time (`noImplicitAny`, `strictNullChecks`, …) as separate steps; track the remaining `any` count in the report.
- Type the existing behavior, including quirks (a function that returns `string | undefined` today is typed that way, not "fixed" to `string`).
- Runtime validation (zod/valibot) at external boundaries is a behavior change if it starts rejecting input — propose, don't slip it in.
- Run the existing JS tests against the TS build output; compare bundles/emitted output when the project ships compiled JS.

---

## 10. Python → Rust

Two common end states: a standalone Rust binary/crate (A), or a Rust core imported from Python via PyO3 + maturin (B, the Python API stays the product). Decide first — under B the Python-facing signatures, exception classes, and return types are the parity unit.

### Types and data
| Python | Rust | Notes |
|---|---|---|
| `int` (unbounded) | `i64`/`u64`/`usize`; `i128` or `num-bigint` when values can exceed 64 bits | Decide overflow policy per value (`checked_*` to raise like Python would never overflow silently) |
| `float` | `f64` | `f64` is not `Ord`/`Eq`: sorting needs `total_cmp`, map keys need a wrapper (`ordered-float`) |
| `str` (code points) | `String`/`&str` (UTF-8) | `len()` → `.chars().count()` for code points; `s[i]` → `.chars().nth(i)` (O(n)); byte slicing panics off char boundaries |
| `bytes` | `Vec<u8>` / `&[u8]` | |
| `list` | `Vec<T>` | Mixed-type lists need an `enum` |
| `dict` | `HashMap` (unordered) / `indexmap::IndexMap` (insertion order like Python) / `BTreeMap` (sorted) | Pick `IndexMap` when output order is observable |
| `set` | `HashSet` / `IndexSet` / `BTreeSet` | |
| `None` / `Optional[T]` | `Option<T>` | |
| `@dataclass` | `struct` with `#[derive(Debug, Clone, PartialEq)]` as needed | |
| `Enum` | `enum` (+ `#[repr]`/serde rename for wire values) | |
| class hierarchy / duck typing | traits + structs; `enum` when the set of variants is closed | |
| generators / `yield` | `impl Iterator` (custom `struct` + `Iterator` impl, or `std::iter::from_fn`) | Laziness preserved; early exit is natural |
| comprehensions | iterator chains `.iter().filter().map().collect()` | |
| `**kwargs`, default args | builder or options struct with `Default` | |
| `collections.Counter` | `HashMap<K, usize>` + explicit sort for `most_common` | `most_common` breaks ties by first insertion — reproduce with `IndexMap` or a stable sort over first-seen order |

### Errors and resources
- Exceptions → `Result<T, E>` with `?`; one error enum variant per exception class callers distinguish (`thiserror` for libraries, `anyhow` for binaries).
- `raise X from e` → error variant wrapping the source (`#[source]`).
- Under PyO3 (end state B): map each error variant to the *same* Python exception class and message as before (`PyErr::new::<PyValueError, _>(msg)` or custom exceptions via `create_exception!`). Never let a Rust panic reach Python as a crash; it surfaces as `PanicException`, which callers don't catch.
- `with` / `try/finally` → RAII (`Drop`); explicit `flush()` where Python relied on context-manager exit to flush.

### Numbers and formatting traps
- `//` and `%` floor (`-7 // 2 == -4`, `-7 % 2 == 1`); Rust `/` and `%` truncate → use `div_euclid`/`rem_euclid` (same as Python for positive divisors; differ for negative divisors — write a `floor_div` helper if divisors can be negative).
- `round()` is banker's rounding; `f64::round` rounds half away from zero → use `f64::round_ties_even` (stable since Rust 1.77).
- `str(1.0) == "1.0"`; Rust `format!("{}", 1.0)` gives `"1"`, `{:?}` gives `"1.0"`. Large/small floats: Python switches to exponent at 1e16; Rust `{}` never uses exponent notation for `f64`. Write a formatting helper and pin it with fixtures.
- `json.dumps` defaults: `", "`/`": "` separators, `ensure_ascii=True` (`\uXXXX` escapes), insertion order; `serde_json` writes compact output, raw UTF-8, `1.0` for floats, and sorted keys for `Map` unless `preserve_order`. Use a custom `Formatter` or post-process when byte-identical output is required.
- `re` (backtracking) vs `regex` crate (no lookaround/backreferences; Unicode classes by default); `str.isalpha()` ≈ `char::is_alphabetic()` (check combining marks and digits in other scripts).
- `sorted()` stable → `sort`/`sort_by` (stable), not `sort_unstable`.

### Concurrency
- GIL removal: CPython code safe "by accident" becomes a data race candidate — the compiler will force `Send`/`Sync`; don't paper over with `Arc<Mutex<_>>` everywhere, restructure ownership.
- `threading`/`multiprocessing` CPU work → `rayon`; `asyncio` → `tokio` (futures are lazy; `asyncio.gather` → `join_all`/`try_join_all`, results in input order).
- PyO3: release the GIL (`py.allow_threads`) around long Rust computations.

### Ecosystem
| Python | Rust |
|---|---|
| `argparse` / `click` | `clap` |
| `json` / `pydantic` | `serde` + `serde_json`; validation via `validator`/`garde` or `TryFrom` |
| `requests` / `httpx` | `reqwest` |
| `logging` | `tracing` / `log` + `env_logger` |
| `pathlib` | `std::path::{Path, PathBuf}` |
| `datetime` | `chrono` / `time` / `jiff` |
| `csv` | `csv` crate |
| `numpy` | `ndarray` (+ `numpy` crate for PyO3 interop) |
| `pytest` | `cargo test`, `rstest` (parametrize), `insta` (snapshots), `proptest` (≈ hypothesis) |
| extension packaging | `pyo3` + `maturin` (wheels per platform — end state B must ship every platform the old package did) |

Keep the Python test suite running against the PyO3 module during migration; it is the best parity evidence for end state B.

---

## 11. Rust → Python

| Rust | Python | Notes |
|---|---|---|
| `Result<T, E>` | return value / raise an exception class per error variant | Keep variant names as exception class names |
| `Option<T>` | `T \| None` (`Optional[T]`) | |
| `enum` with data + `match` | `dataclass` variants + `match` (3.10+) or `isinstance` | Exhaustiveness is no longer checked — add a default branch that raises |
| fixed-width ints, `wrapping_*` | `int` (unbounded) | Mask explicitly (`& 0xFFFFFFFF`) where wrapping was intended |
| `div_euclid`/`rem_euclid` | `//`, `%` (equal for positive divisors) | Rust `/` on negatives truncates → `int(a / b)` loses precision for big ints; write `trunc_div` |
| `f64::round` (half away) | `round` is banker's → `decimal.Decimal.quantize(..., ROUND_HALF_UP)` or helper | |
| `{}` float formatting | `str()` prints `1.0` where Rust printed `1` | Pin with fixtures |
| ownership / moves | shared mutable references | Copy where Rust cloned; freeze or use tuples/frozen dataclasses for data Rust treated as immutable |
| traits | `typing.Protocol` / ABCs | |
| iterators (lazy) | generators / `itertools` | |
| `rayon` / threads | `concurrent.futures`, `multiprocessing` (GIL) | |
| `serde_json` | `json` (`separators=(",", ":")`, `ensure_ascii=False`, `sort_keys=True` to match sorted-map output) | |

---

## 12. TypeScript → Go

### Types and data
| TypeScript | Go | Notes |
|---|---|---|
| `number` | `int`/`int64`/`float64` chosen per value | TS has one numeric type; integer division needs explicit truncation in TS (`Math.trunc`) but is native in Go |
| `bigint` | `math/big.Int` | |
| `string` (UTF-16) | `string` (UTF-8 bytes) | `.length` counts UTF-16 units; Go `len` counts bytes; `utf8.RuneCountInString` counts code points |
| `interface` / type alias of object | `struct` (+ small Go interfaces for behavior) | TS structural typing ≈ Go implicit interfaces for methods, but data shapes need named structs |
| union `A \| B` / discriminated union | interface with a marker method + type switch, or struct with a `Kind` field | Go has no exhaustive switch — add a `default` that errors/panics on unknown kinds |
| string literal unions / `enum` | typed string/int constants | Validate unknown values at boundaries |
| optional props `x?: T`, `null` | pointer `*T`, zero value, or `(T, bool)` | JSON: `omitempty` drops zero values too (0, "", false) — not the same as omitting `undefined` |
| generics | Go generics (type parameters) | Generic methods exist only from Go 1.27 (check the `go` directive in go.mod; before that use generic functions); interface methods can't be generic; constraints are interface-based |
| `class` with inheritance | struct + embedding + interfaces | |
| `readonly` / `as const` | unexported fields + getters, or copy on return | Go has no deep immutability |
| `Array` methods | `for` loops, `slices` package | `sort()` default string compare; Go `slices.Sort` numeric; `slices.SortFunc` not stable → `SortStableFunc` |
| `Map`/`Set` (insertion order) | `map` (random order) | Keep an order slice when output order is observable |
| `Record<string, T>` | `map[string]T` | `encoding/json` sorts map keys on output; JS keeps insertion order |
| `Date` | `time.Time` | JS months 0-based; JS `Date` is ms since epoch, Go `UnixNano`/`UnixMilli` |

### Errors and async
- `throw`/`try-catch` → `error` return values; `instanceof` checks → `errors.As`; custom error classes → error types; keep messages callers match.
- Uncaught async rejections → goroutines must report errors explicitly (`errgroup`); a panic in a goroutine kills the process.
- `async/await` on one event loop → goroutines run in parallel: shared state needs `sync.Mutex` or channel confinement; run `go test -race`.
- `Promise.all` → `errgroup.Group` (cancels on first error via context) collecting into an indexed slice to keep order; `Promise.allSettled` → `sync.WaitGroup` + per-item results.
- `AbortController`/timeouts → `context.Context` with deadline, passed as first parameter.
- JS promises start immediately; a Go call is synchronous unless you start a goroutine — "fire and forget" calls need an explicit `go` and someone owning its error.

### Serialization traps
- `JSON.stringify` keeps insertion order and omits `undefined`; Go `json.Marshal` uses struct field order, sorts map keys, writes `null` for nil slices (vs `[]`) unless initialized, and escapes `<`, `>`, `&` as `\u003c` etc. by default (use an `Encoder` with `SetEscapeHTML(false)` to match JS).
- Numbers: `JSON.stringify(1e21)` → `"1e+21"`; Go `float64` marshals `1e21` as `1e+21` too, but integer-valued floats print without `.0` in both — compare large/small exponent thresholds with fixtures.
- Unknown JSON fields: JS keeps them on the object; Go silently drops them unless decoded into `map[string]any` or `json.RawMessage` (or rejected with `DisallowUnknownFields`).

### Ecosystem
| TypeScript/Node | Go |
|---|---|
| Express / Fastify / NestJS | `net/http` (Go 1.22+ routing), `chi`, `echo`, `gin` |
| zod / class-validator | struct tags + `go-playground/validator` or explicit validation |
| axios / fetch | `net/http` client (set timeouts) |
| Prisma / TypeORM | `database/sql` + `sqlc`/`sqlx`, or `gorm` |
| winston / pino | `log/slog` |
| commander / yargs | `flag` / `spf13/cobra` |
| jest / vitest | `testing` (table tests), `testify` if the project uses it, golden files |
| dotenv | `os.Getenv` + `joho/godotenv` if needed |
| ws / socket.io | `nhooyr.io/websocket` / `gorilla/websocket` (no direct socket.io equivalent — protocol-level work) |
| npm workspaces | Go modules / `go.work` |

---

## 13. Go → TypeScript

| Go | TypeScript | Notes |
|---|---|---|
| `(T, error)` | throw typed errors, or a `Result` union — pick one per module | |
| `errors.Is/As` | `instanceof` on error classes, `cause` chains (`new Error(msg, { cause })`) | |
| zero values | explicit defaults | Missing JSON fields become `undefined`, not `0`/`""` |
| `int64` / `uint64` | `number` (exact ≤ 2^53) or `bigint` | IDs and counters above 2^53 must be `bigint` or strings |
| integer `/` truncation | `Math.trunc(a / b)` | `%` sign rules match (both truncated) |
| goroutines + channels | `async` functions, `Promise.all`, async iterators; worker threads for CPU-bound work | No preemptive parallelism on the main thread |
| `select` / `context` cancellation | `Promise.race`, `AbortController`/`AbortSignal` | |
| `defer` | `try/finally` (or `using` with explicit resource management where supported) | Deferred calls run LIFO |
| map iteration (random) | `Map` (insertion order) | If Go code sorted keys for determinism, keep the sort |
| `encoding/json` | `JSON.stringify` | Map keys were sorted in Go output; nil slice → `null` vs `[]` |
| interfaces (implicit) | interfaces (structural) | Natural fit |
| `testing` table tests | `test.each` (vitest/jest) | |
