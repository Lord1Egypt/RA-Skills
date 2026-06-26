---
name: formal-methods
description: Formal verification with Lean 4, Coq, and Z3 SMT solver
metadata:
  openclaw:
    emoji: 🔬
    tags: [formal-verification, lean4, coq, z3, proofs]
    source: https://github.com/Prismer-AI/Prismer
    homepage: https://github.com/Prismer-AI/Prismer
    requires:
      bins: [lean, coqc, z3]
      os: [darwin, linux]
      runtime: node
---

# formal-methods

Formal verification tools for the academic workspace. Type-check Lean 4 proofs, verify Coq theories, and solve SMT satisfiability problems with Z3.

## Prerequisites

This skill requires the following binaries installed locally (declared in `metadata.openclaw.requires.bins`):

| Binary | Install |
|--------|---------|
| `lean` | [Lean 4](https://leanprover.github.io/lean4/doc/setup.html) via `elan` |
| `coqc` | [Coq](https://coq.inria.fr/download) via `opam install coq` |
| `z3` | [Z3](https://github.com/Z3Prover/z3) via package manager or GitHub releases |

Use `prover_status` to check which provers are available before use. The skill gracefully handles missing binaries — only installed provers will work.

**Source:** [github.com/Prismer-AI/Prismer](https://github.com/Prismer-AI/Prismer) (Apache-2.0)

## Description

This skill invokes locally installed formal verification provers via subprocess. No Docker, containers, or external services required.

**Execution model:** Each invocation writes source code to a temporary directory (`os.tmpdir()/formal-methods-<hash>/`), runs the prover binary with `cwd` set to that directory, captures stdout/stderr, and applies a 60-second timeout. The exact commands are:

- Lean: `lean <filepath>` — may read Lean 4 stdlib and elan-managed toolchains from `~/.elan/`
- Coq: `coqc <filepath>` — may read Coq stdlib and opam-managed packages from the opam switch
- Z3: `z3 <filepath>` — self-contained, only reads the input file. Accepts declarative SMT-LIB2 format only.

**Filesystem access:** The skill itself only writes to the temp directory. However, Lean and Coq read their installed standard libraries and search paths (managed by elan/opam) as part of normal operation. The skill does not explicitly constrain `--include` paths or environment variables.

**Network access:** The skill does not make network requests. However, if Lean source contains `import` of unresolved packages, `lake` tooling could theoretically attempt a fetch — this is a Lean runtime behavior, not initiated by the skill. To prevent this, avoid `lakefile.lean` or `lake-manifest.json` in the temp directory (which the skill does not create).

## Usage Examples

- "Check if this Lean 4 proof type-checks"
- "Verify my Coq induction proof"
- "Is this SMT formula satisfiable?"
- "What provers are available?"

## Process

1. **Check availability** — Use `prover_status` to see which provers are installed
2. **Write proof** — Draft your Lean/Coq code or SMT formula
3. **Verify** — Use `lean_check`, `coq_check`, or `z3_solve` to verify
4. **Iterate** — Fix errors based on output and re-check

## Tools

### lean_check

Type-check Lean 4 code.

**Parameters:**
- `code` (string, required): Lean 4 source code
- `filename` (string, optional): Source filename (default: `check.lean`)

**Returns:** `{ success, output, errors, returncode }`

**Example:**
```json
{ "code": "theorem add_comm (a b : Nat) : a + b = b + a := Nat.add_comm a b" }
```

### coq_check

Check a Coq proof for correctness.

**Parameters:**
- `code` (string, required): Coq source code
- `filename` (string, optional): Source filename (default: `check.v`)

**Returns:** `{ success, compiled, output, errors, returncode }`

**Example:**
```json
{ "code": "Theorem plus_comm : forall n m : nat, n + m = m + n.\nProof. intros. lia. Qed." }
```

### coq_compile

Compile a Coq file to a `.vo` object file.

**Parameters:**
- `code` (string, required): Coq source code
- `filename` (string, optional): Source filename (default: `compile.v`)

**Returns:** `{ success, compiled, output, errors, returncode }`

### z3_solve

Solve a satisfiability problem using Z3 with SMT-LIB2 format.

**Parameters:**
- `formula` (string, required): SMT-LIB2 formula

**Returns:** `{ success, result, model }`

**Example:**
```json
{ "formula": "(declare-const x Int)\n(assert (> x 5))\n(check-sat)\n(get-model)" }
```

### prover_status

Check which formal provers are available and their versions.

**Parameters:** None

**Returns:** `{ provers: { lean4: { available, version }, coq: { available, version }, z3: { available, version } } }`

## Notes

- Requires provers declared in `metadata.openclaw.requires.bins`: `lean`, `coqc`, `z3`
- Z3 only accepts declarative SMT-LIB2 format — no arbitrary code execution
- Each invocation has a 60-second timeout (`execSync` with `timeout: 60000`)
- Temp files are written to `os.tmpdir()/formal-methods-<hash>/`
- Lean/Coq will read their installed standard libraries (elan/opam managed) as part of normal type-checking
- The skill itself makes no network requests; Lean imports should avoid lake-managed dependencies to prevent unintended fetches
