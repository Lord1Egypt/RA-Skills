---
name: ax-development
description: "Agent Experience (AX) development framework. Apply when building libraries, CLIs, APIs, or any software that will be consumed by AI agents — not just humans. Covers: deterministic design, machine-readable contracts, fail-fast validation, composable primitives, documentation co-location. Use when: (1) starting a new project/lib that agents will use, (2) reviewing code for agent-friendliness, (3) designing CLI output contracts, (4) structuring error handling for machine consumption, (5) writing tests for deterministic behavior."
---

# AX Development — Agent Experience Framework

Software is increasingly consumed by AI agents, not just humans. AX (Agent Experience) is the discipline of designing code, APIs, and interfaces that agents can operate reliably and autonomously.

## The 8 Principles

### 1. Fast Fail Early

Reject invalid inputs before expensive operations. Validate at the boundary, not deep in the call stack.

```typescript
// ✅ Validate sync rules before building composite
const errors = validateSyncRules(rules, knownSources);
if (errors.length > 0) throw new AXError("INVALID_SYNC_RULES", errors);

// ❌ Discover invalid rule during HTML rendering
```

### 2. Deterministic Outputs

Same inputs → same outputs. No wall-clock dependencies, no random IDs in deterministic paths, no hidden state mutations.

```typescript
// ✅ Pure function, predictable
function buildDescriptor(resources, orchestration) { ... }

// ❌ Result depends on Date.now() or Math.random() silently
```

When non-determinism is necessary (UUIDs, timestamps), isolate it and make it injectable.

### 3. Machine-Readable Errors

Structured errors with codes, not just string messages. Agents parse error codes, not prose.

```typescript
// ✅ Structured, parseable
{ code: "ORPHAN_SYNC_TARGET", target: "viz:render", available: ["postgres:query"] }

// ❌ Just a string
throw new Error("Target not found in resources");
```

### 4. Explicit Over Implicit

No magic defaults that silently change behavior. Every configuration has a visible default. No hidden heuristics.

```typescript
// ✅ Default is explicit and documented
function render(descriptor, { theme = "auto" } = {}) { ... }

// ❌ Silently detects theme from environment variable
```

### 5. Composable Primitives

Each function does one thing. Pipeline steps are independent and recombinable. Agents can use each step separately.

```
Collector → Composer → Renderer  // Full pipeline
Collector → custom logic → Renderer  // Agent skips composer
```

### 6. Narrow Contracts

Minimal required inputs, maximal type safety. Accept only what you need. Return only what's useful. Avoid God objects.

```typescript
// ✅ Takes exactly what it needs
function resolveSyncRules(rules: UiSyncRule[], sources: string[]): ResolvedSyncRule[]

// ❌ Takes the entire config object when it only needs two fields
function resolveSyncRules(config: FullAppConfig): ResolvedSyncRule[]
```

### 7. Co-located Documentation

Docs live next to the code they describe. Each module has its own contract. Agents find docs by exploring the file tree, not by searching a wiki.

```
src/sync/
├── mod.ts           # Public exports
├── resolver.ts      # Implementation
├── resolver_test.ts # Tests ARE documentation
└── contract.md      # I/O contract, invariants (optional, for complex modules)
```

### 8. Test-First Invariants

Every behavior has a test. Tests are the executable specification that agents read to understand contracts. Prioritize boundary tests over happy-path.

```typescript
// Test the edges, not just the middle
Deno.test("empty resources → empty descriptor", ...);
Deno.test("orphan sync target → validation error", ...);
Deno.test("broadcast rule → resolves to all-except-sender", ...);
```

## Applying AX — Decision Checklist

Before shipping any module, verify:

- [ ] Can an agent call this function with zero ambient knowledge?
- [ ] Are all errors machine-parseable (code + structured data)?
- [ ] Does the output change if I run it twice with same inputs?
- [ ] Is there any implicit behavior not visible in the function signature?
- [ ] Can I use this module without importing unrelated modules?
- [ ] Do the tests cover invalid/edge inputs, not just happy paths?
- [ ] Is there documentation within 1 directory level of the code?
- [ ] Would an agent need to read source code to understand the contract, or are types + tests sufficient?

## CLI Contracts (for CLI tools)

When building CLIs that agents will invoke:

- Default to **machine-readable output** (JSON/JSONL), human-readable opt-in via `--human`
- Include **stable keys** in output (not just pretty-printed text)
- Use **exit codes** consistently (0 = success, 1 = user error, 2 = system error)
- **Version output format** — breaking changes to JSON structure need a flag or migration path
- Prefer **explicit flags** over positional arguments for agent discoverability

See `references/cli-contracts.md` for detailed patterns.

## Error Taxonomy

Standard error code prefixes for AX-compliant projects:

| Prefix | Domain | Example |
|--------|--------|---------|
| `INVALID_*` | Input validation | `INVALID_SYNC_RULES` |
| `MISSING_*` | Required data absent | `MISSING_RESOURCE_URI` |
| `ORPHAN_*` | Reference to non-existent entity | `ORPHAN_SYNC_TARGET` |
| `CONFLICT_*` | Contradictory configuration | `CONFLICT_LAYOUT_CHILDREN` |
| `UNSUPPORTED_*` | Valid but not implemented | `UNSUPPORTED_LAYOUT` |

Adopt this taxonomy or define your own — the point is consistency within a project.
