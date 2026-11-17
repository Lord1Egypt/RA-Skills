# Refactoring Catalog — structural and large-scale moves

Local, single-function cleanups (guard clauses, inline temp, rename local, remove dead branch, idiom polish) are covered by `simplify-code`; this catalog covers moves that cross function, file, module, or package boundaries, and the patterns for doing them while the code keeps shipping.

## Contents
1. Patterns for change at scale · 2. Structural moves (mechanics + risk) · 3. Smell → move · 4. Sequencing rules · 5. Tool-driven transforms by language · 6. Hidden-coupling checklist

## 1. Patterns for change at scale

**Parallel change (expand → migrate → contract).** For any interface change with more than a few callers:
1. *Expand:* add the new form next to the old one (new function, new parameter with default, new field). Old callers still compile.
2. *Migrate:* move callers over in batches; each batch is a green step. Keep the old form delegating to the new one so there is only one real implementation.
3. *Contract:* remove the old form once no caller remains (verify with search plus build of every consumer you can reach). For public APIs, contraction waits for a deprecation period and a major version.

**Forwarding shim.** When moving a symbol, leave a forwarder at the old location: re-export (JS/TS `export { X } from`, Python `from .new import X` in the old module or package `__init__`), type alias (Go `type Old = new.Type`, Kotlin `typealias`, TS `export type`), or a deprecated wrapper. Callers migrate at their own pace; the final step deletes the shim.

**Branch by abstraction.** To replace a subsystem (ORM, HTTP client, storage layer) without a long-lived branch:
1. Introduce an abstraction over the current implementation and route all callers through it.
2. Build the new implementation behind the same abstraction.
3. Switch callers (all at once via flag, or one by one), compare behavior.
4. Delete the old implementation, and the abstraction too if it no longer earns its keep.

**Strangler fig.** For a module or service being rewritten: put a routing layer in front, send one route/command/feature at a time to the new code, and shrink the old code until it can be deleted. See `rewrite-checklist.md`.

**Mikado method.** For a goal that keeps breaking things when you try it directly: try the change, note what breaks, revert, and record the prerequisites as a graph; implement leaf prerequisites first (each a green step), then retry the goal. Good for untangling when the dependency order is unknown.

**Preparatory refactoring.** When a feature is hard to add, first refactor so the feature becomes a small change, verify, then add the feature as a separate step. Make that separation visible in the report.

## 2. Structural moves (mechanics + risk)

Risk: **L** = mechanical, tool-verified; **M** = needs targeted tests over the touched paths; **H** = needs full safety net and user sign-off.

| Move | Mechanics (short) | Risk |
|---|---|---|
| Rename symbol across files | LSP/IDE rename; then grep strings, templates, config, reflection, serialized field names | L (M if serialized/reflected) |
| Move function/class to another module | Move, leave forwarding shim, update imports in batches, delete shim | M |
| Extract module/package from a large file | Group by responsibility (what changes together), move one group at a time behind re-exports, keep import paths stable | M |
| Split a package with cyclic deps | Introduce consumer-owned interface to break the cycle first, then split | H |
| Merge shallow modules | Inline thin pass-through modules into their single real user; keep public paths via re-export | M |
| Change function signature (many callers) | Parallel change; add new signature, delegate old → new, migrate callers, remove old | M–H |
| Introduce parameter object across callers | Parallel change; adapter from old positional form | M |
| Replace conditional type-switch with polymorphism/dispatch table | Add variants one at a time; keep default/unknown-case behavior identical | M |
| Replace inheritance with composition/delegation | Introduce delegate field, forward methods, migrate callers off base-class APIs, remove inheritance | H |
| Extract interface / introduce seam | Declare narrow interface at consumer, inject implementation | L–M |
| Move logic between layers (e.g. controller → service) | Move with tests at the outer boundary (HTTP/CLI) so the move is invisible to them | M |
| Replace global/singleton with injected dependency | Add parameter with default to the global, migrate callers to pass it, remove default | M |
| Convert callback/sync API to async across a codebase | Parallel change: async core + sync/callback adapter; migrate callers; mind ordering and error propagation | H |
| Split service/process (extract microservice) | That is a rewrite with a network seam; use `rewrite-checklist.md` | H |

## 3. Smell → move

| Smell (structural) | Likely move |
|---|---|
| God module/class: unrelated responsibilities changing for different reasons | Extract module by responsibility; keep a façade for existing callers |
| Shotgun surgery: one change touches many files | Move related logic together (gather what changes together) |
| Divergent change: one module changes for many reasons | Split along the reasons |
| Cyclic imports | Consumer-side interface; move shared types to a leaf module |
| Feature envy across modules | Move the function to the module that owns the data |
| Shallow modules: interface as complex as implementation | Merge/inline into a deeper module |
| Leaky abstraction: callers reach into internals | Narrow the interface; add the missing operation; migrate callers |
| Duplicated subsystems (two HTTP clients, two config loaders) | Branch by abstraction to converge on one |
| Long parameter lists repeated across a layer | Parameter object via parallel change |
| Hard-wired dependencies blocking tests | Introduce seam (injection) |

## 4. Sequencing rules

- Contracts/types first, then implementations, then callers, then tests that assert old internals, then shim removal.
- One kind of change per step: move, or rename, or change signature. Moving and editing the same code in one step makes the diff unreadable and the move unverifiable.
- Moves before optimizations; optimizations need benchmarks and are behavior-sensitive.
- File-disjoint steps can run in parallel (separate branches/worktrees); overlapping steps run in sequence.
- Keep each reviewable step small (a few hundred changed lines is a good upper bound for a human review).
- When a move would touch generated code, regenerate rather than hand-edit.

## 5. Tool-driven transforms by language

Prefer transforms that understand syntax and types; for repetitive edits across many sites, write a codemod and keep it with the change (it is reviewable and re-runnable).

| Language | Safe rename/move | Codemods / structural search-replace |
|---|---|---|
| TS/JS | tsserver/IDE rename & move file (updates imports) | ts-morph, jscodeshift, ast-grep |
| Python | rope, Pyright/Pylance rename, PyCharm | LibCST codemods, ast-grep |
| Go | gopls rename/extract/inline | `gofmt -r`, `eg`, gopatch, `go fix` analyzers |
| Rust | rust-analyzer rename/move/extract | rust-analyzer structural search-replace (SSR), ast-grep |
| Java/Kotlin | IntelliJ refactorings | OpenRewrite recipes, Error Prone refaster |
| C/C++ | clangd rename | clang-tidy fix-its, Coccinelle (C), Comby |
| C# | Roslyn/IDE refactorings | Roslyn analyzers + code fixes |
| PHP | PhpStorm refactorings | Rector |
| Any | — | Comby, ast-grep, sed only for truly textual changes (then build to verify) |

After any tool-driven rename or move, search for the old name as a string: reflection, DI configuration, templates, SQL, JSON/YAML field names, docs, and feature-flag keys are invisible to the compiler.

## 6. Hidden-coupling checklist

Before declaring a move safe, check for:
- Dynamic imports / `require(variable)` / `importlib` / plugin registries keyed by module path.
- Reflection, annotations, DI containers, ORMs, serializers keyed by class/field name.
- Pickle/Java serialization/protobuf field numbers bound to class paths or names.
- Public paths in package manifests (`exports`, `__all__`, entry points, `main`).
- Mocks/patches in tests that target the old path (`mock.patch("pkg.old.thing")`).
- Logs, metrics names, and error messages parsed by other systems.
- Build files and codegen configs listing source paths.
