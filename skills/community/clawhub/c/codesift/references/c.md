# C review

Use --lang c for a C package. Read patterns.md for reachability and gates.

## Contracts and active paths

Trace entry points and public headers to mutation/I/O. Check lengths, ownership,
allocation failure, error propagation and lifetime assumptions. A suspicious
library call is a candidate; establish the actual input and bounds.

Investigate duplicate parsing, allocation, copies, locks and sync on active
paths with a profiler supported by the host OS. Do not assume every allocation
or strong sync is wasteful.

## Unused code

Inspect compiler diagnostics for unused static functions/variables and unreachable
code using the project's real compile commands. Include all supported targets and
macro configurations. Follow callbacks, function-pointer tables, linker sections,
startup hooks, generated registrations and FFI consumers.

An exported symbol without a local caller may be an external API. An unlinked
file can be obsolete, a platform variant or a packaging mistake; verify which.
Compiler/linker elimination is evidence for a build, not every supported build.

## Gates

Check error-code-to-caller propagation, bounds checks and build-time feature
conditions. Exercise valid and invalid cases. A macro permanently false in one
build is not automatically obsolete in others. Repeated validation may be needed
after mutation or at a separate trust boundary.

## Validation

Use existing tests. For memory/lifetime candidates, a separate ASan/UBSan build
can provide evidence. Configure instrumentation at configure/compile/link time;
setting CFLAGS only when invoking cmake --build does not reconfigure the build.

Use a disposable build directory and clean it on all outcomes. A sanitizer is
not mandatory evidence for unrelated logical or architectural findings.
The bundled runner uses existing CTest directories and requires CMake/CTest
3.21+ for JUnit output; it does not build a target automatically.

Dependency helpers inventory supported manifests. CMake/Make are executable
build logic; public registry guesses cannot prove their resolved libraries exist.

Source: [Clang instrumentation options](https://clang.llvm.org/docs/UsersManual.html#controlling-code-generation),
checked 2026-11-03.
