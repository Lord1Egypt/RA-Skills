# Class playbook — living notebook (guidance, not rules)

Task **shape** → collaboration recipe. Seed rows come from real work; when the same shape shows up again, add one line: shape → who ran it → which verification actually caught a problem → review verdict. Keep rows short. Unknowns stay marked "pending". Mark a line stale when the tooling or models it names change. Learned, not legislated.

| Shape | Hand down to | Verification that worked | Review needed? | Notes |
|---|---|---|---|---|
| N-repo read-only status sweep (fixed CLI commands) | cheap model | spot-check 2 rows caught a summary count slip (the table itself was right) | spot-check sufficed; no full review | 2026-09-23 first run: claims verified 2/2 |
| Rename a published package + republish to 3 marketplaces | main line drives; command chain can be handed down | grep/diff/remote read-back + marketplace scan verdict | human GO per external gate | many mechanical steps, few judgment points |
| Draft a bounded doc delta to an exact spec | cheap model (high reasoning) | word-count gate + grep gate + main line reads the diff | spot-check; full review only for high risk | this playbook was drafted exactly this way |
| Pre-release security pre-scan | not an LLM — a script | the script's own output | none | deterministic by construction |
