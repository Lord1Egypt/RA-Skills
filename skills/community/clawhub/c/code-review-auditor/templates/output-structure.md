# Output Structure

Every run must create:

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

## summary.md

Include:

- reviewed scope
- mode
- timestamp
- stack(s)
- top risks
- count by severity and category
- recommended next actions
- links to category files

## findings.md

Aggregate all findings or link to category files. Findings must follow `templates/finding.md`.

## Category Files

Use one file per major category. If no finding exists, write a short "No findings" note and mention the scope reviewed.

## hotspots.md

List top files/modules/components with reason, evidence, score, and recommended action.

## metrics/score.md

Human-readable scorecard using `rules/scoring.md`.

## metrics/score.json

Machine-readable version of the scorecard.

## metadata.json

Include:

```json
{
  "skill": "code-review-auditor",
  "mode": "complete",
  "created_at_local": "YYYY-MM-DDTHH:mm:ss",
  "review_directory": "review/YYYY-MM-DD_HH-mm-ss",
  "repository": {
    "root": "",
    "git_branch": "",
    "git_commit": "",
    "dirty": null
  },
  "scope": {
    "included": [],
    "excluded": [],
    "reason": ""
  },
  "stacks_detected": [],
  "commands_used": [],
  "limitations": []
}
```

## refactoring-plan.md

Create when proposing `fix`, `refactor`, design-pattern adoption, architecture changes, or any high-effort recommendation. If no refactor is proposed, write "No refactoring plan created for this run" with rationale.
