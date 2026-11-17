# Code Review Auditor

`code-review-auditor` is a Codex skill for deep code review across bugs, security, architecture, SOLID, code smells, justified design-pattern opportunities, anti-patterns, performance, observability, testability, hotspots, and planned refactoring.

The skill is designed to be conservative: analysis does not alter source code, and fixes/refactors are planned before implementation.

## What It Produces

Every run creates a review package inside the reviewed project:

```text
review/YYYY-MM-DD_HH-mm-ss/
|-- summary.md
|-- findings.md
|-- security.md
|-- architecture.md
|-- bugs.md
|-- code-smells.md
|-- patterns.md
|-- performance.md
|-- testing.md
|-- observability.md
|-- hotspots.md
|-- refactoring-plan.md
|-- metadata.json
`-- metrics/
    |-- score.md
    `-- score.json
```

Some category files may say "No findings" when nothing meaningful was found.

## Modes

- `complete`: broad review across all categories.
- `diff` / `changed`: review changed files and relevant call sites.
- `security`: security-focused review.
- `architecture`: architecture, SOLID, layers, boundaries.
- `smells`: maintainability and local quality issues.
- `patterns`: justified design-pattern opportunities.
- `performance`: latency, throughput, memory, query and IO issues.
- `tests`: testability and test coverage risks.
- `hotspots`: risk ranking by churn, complexity, coupling, and criticality.
- `explain`: explain findings and tradeoffs.
- `fix`: plan then implement fixes after approval.
- `refactor`: plan then implement behavior-preserving refactors after approval.
- `challenge`: critique an implementation or proposal.

## Example Prompts

```text
Use $code-review-auditor in complete mode on this repository.
```

```text
Use $code-review-auditor in diff mode. Focus on security and architecture.
```

```text
Use $code-review-auditor to challenge this refactoring plan and identify overengineering risks.
```

```text
Use $code-review-auditor to create a refactoring plan for the hotspots, but do not change code yet.
```

## Installation

Copy this folder to your Codex skills directory:

```text
$CODEX_HOME/skills/code-review-auditor
```

If `CODEX_HOME` is not set, use:

```text
~/.codex/skills/code-review-auditor
```

Then invoke it explicitly as `$code-review-auditor` or let Codex select it automatically for code review tasks.

## Safety Model

- Analysis modes are read-only for source code.
- `fix` and `refactor` create a `refactoring-plan.md` first.
- Implementation requires explicit approval unless already requested by the user.
- The skill prioritizes concrete risks over aesthetic preferences.
- Design patterns are recommended only when they reduce real complexity.
