# C++ review

Use --lang cpp. C/C++ mixed native sources use cpp; package-level mixed language
manifests require explicit scope. Read patterns.md for reachability and gates.

## Coding conventions

Check the repository's selected C++ standard, naming, exception policy, ownership
conventions and test framework. Self-contained headers should include their direct
dependencies. Prefer scoped ownership and clear return contracts, and use the
project's established type and function style.

Do not impose a float-only rule, a universal ban on deduced return types, fixed
filename casing, a ban on main.cpp, or GoogleTest-only tests on unrelated projects.
Apply those constraints when an explicit project policy requires them. A policy
that claims the Google C++ Style Guide while requiring exceptions needs an
explicit local override: Google's guide does not use C++ exceptions.

## Contracts and cost

Trace overload/template dispatch and actual callers before declaring a fast path
unused. Check object lifetime, iterator invalidation, exception boundaries,
ownership and concurrency. Measure copies, allocations and shared_ptr refcount
work on the relevant workload; pass-by-value can be intentional and efficient.

Check whether flushing, caching, pooling and invalidation meet requirements.
An extra wrapper may preserve ABI, platform adaptation or ownership.

## Unused code

Use compiler diagnostics and project-aware analysis with actual compile_commands.
Review public APIs, explicit template instantiations, virtual dispatch, callbacks,
static initialization, reflection/serialization registration and linker sections.
Analyze the supported platform/feature matrix. An unreferenced template may be
a public facility; an unreachable mutually dependent cluster may still be dead.

Trace CMake target membership as well as source-level calls. Missing build
membership can make an otherwise valid implementation ineffective.

## Gates

Inspect constexpr/preprocessor flags, runtime feature dispatch, optional-package
fallbacks and success/error propagation. Determine whether a fallback is supported,
tested and observable. Do not mistake an intentional stub for an active backend.
Test a failed configure/dependency lookup and verify the intended result reaches CI.

## Validation

Run relevant existing tests. Use ASan+UBSan and TSan in **separate builds**:
-fsanitize=address,undefined and -fsanitize=thread must not be combined.
Set compile and link options during configuration in isolated build directories.

Sanitizer availability does not cap severity of statically established unrelated
defects. Google Benchmark/Catch2 measurements should compare equivalent work,
not whole suite duration against a single-operation baseline.

C/C++ dependency results are partial manifest evidence, never automatic proof of
installed library, feature or ABI compatibility.

Source: [Clang sanitizer compatibility](https://clang.llvm.org/docs/UsersManual.html#controlling-code-generation),
checked 2026-11-03.
Convention reference: [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html#Exceptions).
