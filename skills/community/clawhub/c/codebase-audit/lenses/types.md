# Types and modeling

Fires: always

Leading word: **unrepresentable**. Every illegal state the types allow is a bug waiting for the input that reaches it.

Artifact: a boundary table (boundary → where it is parsed → the type it becomes).

- **parse-at-edge**: Where does raw input (JSON, form fields, OCR text, env vars, URL params, model output, DB rows) cross a boundary and stay a string, number, date or dictionary deep inside? A finding is any boundary that yields a raw type, or a check repeated past the edge. Fix family: one constructor at the boundary that returns a domain type or an error.
- **primitive-obsession**: Which functions take two arguments of the same primitive that can be swapped with no compile error? userId/householdId, grams/ml, cents/dollars, start/end. Fix family: Swift wrapper struct, Kotlin `value class`, TS branded type, Python `NewType`, Go named type, Rust newtype, Dart extension type.
- **stringly-typed**: Which domain values travel as strings compared with `== "active"`, or as magic numbers? Each is an enum the compiler cannot check.
- **boolean-blindness**: List every type with two or more `Bool` fields and every call like `f(true, false)`. Enumerate the combinations; the impossible ones mean the pair is an enum.
- **optional-soup**: Find types where two or more optionals must be nil or set together (`data`/`error`, `isLoading`/`result`, `startedAt`/`endedAt`). One enum case carrying its payload replaces them.
- **catch-all**: Every `switch`/`when`/`match` over your own enum with `default:`, `else ->`, `_ =>`, `case _:` or a trailing `else`. Add a case in your head: what does it silently do? Fix family: exhaustive match (TS `assertNever`, Python `assert_never`); keep a catch-all only for enums you do not own.
- **units-and-time**: Where can a quantity meet a different unit, seconds meet milliseconds, UTC meet local, or an instant stand in for a calendar day, with no type stopping it?
- **assumption-ledger**: For each function on a critical path, list its input assumptions. Each held up by a comment, an assert or a docstring rather than a type is a finding when a caller can break it.
- **schema-twin** (when the project stores data in a database): Each invariant the code relies on (non-empty, positive, unique per owner, references a real row, one of N values) needs a matching constraint where the data is stored. List the mismatches; the data lens covers the storage side in depth.

Done: the boundary table covers every boundary in scope, and every match over a domain enum has been inspected.
