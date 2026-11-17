<rules>
{{RULES}}
</rules>
<role>
Fix round {{ROUND}}. You are a fresh session: everything you need is in this brief. Fix exactly the findings below with the given rulings and nothing else. Do not commit.
</role>
{{CONVENTIONS}}
<workspace>
- Baseline commit: {{SHA}}. Exact working directory: {{WORKDIR}}. Branch {{BRANCH}}. Never touch other directories.
- Before every shell command: {{ENV_EXPORTS}}
</workspace>
<findings>
Each finding is quoted from the review, then the orchestrator's exact ruling and the test that proves it:
{{FINDINGS}}
{{STRUCTURAL_RULING}}
</findings>
<still-applies>
Previous rulings that still apply: {{PRIOR_RULINGS}}
Invariants that must keep holding (each still tested): {{INVARIANTS}}
</still-applies>
<map>Files you may change (nothing else): {{FILES}}</map>
<gates>
Exact commands, per-package only (tests, typecheck, lint of the packages you change), one at a time, once at the end:
{{GATE_COMMANDS}}
</gates>
<report>
Reply with exactly this block and nothing before it, at most {{REPORT_LINES}} lines:
STATUS: done | partial | blocked
FILES: <every path you changed, comma-separated>
F<n>: fixed — <test that proves it> | not fixed — <reason>        (one line per finding)
GATE <command>: exit=<n> passed=<n> failed=<n>        (one line per gate)
BLOCKED: none | <question> — blocks <what>
Do not commit.
</report>
