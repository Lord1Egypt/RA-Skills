---
name: entropyFA Financial Planning
description: Verified financial planning data and blazing-fast, deterministic calculators for Monte Carlo projection, goal solving, Roth conversions, RMDs, income tax, estate tax, and pension analysis.
metadata: {"openclaw":{"homepage":"https://github.com/Entropy-Financial-Technologies/entropyfa-cli/tree/main/integrations/openclaw/entropyfa","requires":{"bins":["entropyfa"]}}}
---

# entropyFA Financial Planning

Use this skill when the user needs source-backed financial planning reference data or deterministic calculations from the local `entropyfa` CLI.

## Workflow

1. If the user needs to discover available reference data, run `entropyfa data coverage`.
2. If the user needs an official value, trust status, or source URL, run `entropyfa data lookup ...`.
3. If the user needs a compute command and the required inputs are unclear, run `entropyfa compute <command> --schema` first.
4. When the inputs are known, run `entropyfa compute <command> --json '<JSON>'`.
5. Use `entropyfa compute projection --visual --json ...` only when the user explicitly wants terminal visuals. Keep projection JSON-only otherwise.

## Behavior

- Prefer `data lookup` over recollection when a shipped dataset exists.
- Surface `verification_status`, `pipeline_reviewed`, and `sources` when provenance matters.
- Do not invent annual tax or planning thresholds when a lookup key exists.
- Keep machine-readable JSON on `stdout` and treat visuals as human-facing `stderr` output.

For fuller workflow guidance, read [references/workflows.md](references/workflows.md).
For exact commands and prompt-style examples, read [references/examples.md](references/examples.md).
