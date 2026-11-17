# The fact contract (adjudication-layer consumption guide)

> This is a **consumption guide**, not a design document. It answers: after receiving a fact, what can the adjudication layer infer from it, and what can it not.
>
> The full contract is in the repository's `docs/fact-contract.md`.

---

## What a fact looks like

```jsonc
{
  "id": "fact-007",
  "kind": "history",                 // fact kind
  "statement": "This change deleted 4 lines of code from commit ab877f9d70...",
  "status": "established",           // established | refuted | unknown
  "evidence": { "file": "src/a.js", "line": 104, "commit": "ab877f9d70" },
  "method": "command",
  "command": "git blame --porcelain -L 104,104 <rev> -- src/a.js",
  "confidence": "exact",             // exact | approximate
  "detail": { }                      // kind-specific structured payload
}
```

---

## The three consumption rules

### Rule 1: `unknown` is not "clean"

The three states are a hard convention:

| status | What the adjudication layer can do |
|---|---|
| `established` | May draw conclusions from it |
| `refuted` | May draw conclusions from it (in reverse) |
| **`unknown`** | **Nothing can be inferred**. It is neither support nor opposition — it is "don't know" |

Treating `unknown` as "no problem" is the only usage error in this contract that is fatal.

### Rule 2: `approximate` may not participate in gates

Facts with `confidence: approximate` are **explicitly excluded from gate adjudication**.

This is not conservatism — it comes from practice: some tools synthesize an approximate result when "scope cannot be determined",
and explicitly mark it as **not participating in blocking even in enforcement mode**. This framework follows the same convention.

Gates only consume `exact`.

### Rule 3: when data is missing, read the coverage table first

The report's `coverage.notEvaluated` lists **what was not measured, and why**.

**Before citing any "clean" conclusion, read this section first.**
When `notEvaluated` is non-empty, do not read it as "tested, no problem".

---

## What facts do **not** contain (this is design, not an omission)

| Not present | Why |
|---|---|
| Scores (score / 0–100) | Scores cannot be recomputed; they would become "using a score as a gate" |
| Severity levels | Severity is a **judgment**, not a fact |
| Fix suggestions | Same as above |
| "may" / "probably" | Weasel words mask gaps |

**Measurement stays measurement; judgment stays judgment.** If a fact carries `severity: high`,
it means the layer that produced it already made the decision for the adjudication layer — and that decision cannot be recomputed.

---

## How to read each fact kind

### `history` — the origin of deleted code

| Field | How to read it |
|---|---|
| `detail.classification` | `security` / `fix` / `none`. **The classifier's two error costs are asymmetric**: missing a security commit is more dangerous than over-reporting, so it is biased wide |
| `detail.byFile` | **How many lines per file**. `blamedLines` is the total and may span multiple files — do not assume the file in the evidence contains everything |
| `detail.commitSubject` | The commit message verbatim. **Do not look only at the classification; read the message itself** |
| `command` | A directly executable reproduction command, with the real line ranges |

**Note**: `history` only says "which commit this line comes from and whether that commit looks like a security fix";
it does **not** say "deleting it is a vulnerability". The latter is the adjudication layer's business.

### `reintroduction` — removed and added back

A non-`null` `detail.securityOrigin` means: the line's occurrence count was once changed by a commit whose message contains security keywords.
Combined with "the line does not exist in the base revision", you can infer **it was removed before and has now been added back**.

**This does not equal "this is a regression"** — it equals "someone needs to look here". The adjudication layer decides from this whether to raise priority.

### `test_coverage` — invocation counts

⚠️ **This kind can only falsify, never confirm.**

| Fact | What it lets you infer |
|---|---|
| Invocation count = 0 (`status: established`) | ✅ **Really never invoked**. All behavior depending on it was never exercised |
| Invocation count > 0 (`status: unknown`) | ❌ **Cannot** infer "executed". Entering a function does not equal any specific call site having run |

Reason: the underlying coverage data reports **call sites that never executed as covered** (straight-line code after a thrown exception is the classic case),
so the "covered" direction is unreliable in itself. **The producer has no "executed" output at all** — this is deliberate.

Corollary: **do not** use "non-zero count" to close a "not tested here" concern. To prove something actually executed,
only a demonstration that truly reaches that call site can do it.

### `artifact` — artifact evidence

The report file, plus the exit code and case count of the demonstration run. **Gates 1 and 4 rely on it.**

How to read it: the exit code and case count must be **actually captured output**, not expected values.
A "pass" with 0 cases is not a pass.

---

## Producer exit codes

The accompanying CLI's exit codes are an external contract, usable directly in CI:

| Code | Meaning | How the adjudication layer should react |
|---|---|---|
| `0` | Measured, no security-related findings | Continue normally |
| `10` | Measured, and at least one `security`-classified fact exists | **Raise priority**; do not treat it as a conclusion directly |
| `1` | Usage error | Fix the command |
| **`2`** | **Could not measure at all** | **Must not be read as clean**. Either switch measurement methods or mark the relevant criteria as not evaluable |

The difference between `2` and `0` is the essence of why this contract exists: **failing to measure and measuring clean are two different things.**
