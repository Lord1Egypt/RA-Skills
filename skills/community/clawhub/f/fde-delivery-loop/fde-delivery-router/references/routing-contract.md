# Routing and handoff contract

## Routing response

```markdown
## Current assessment
- Current stage:
- Recommended skill:
- Evidence and confidence:

## Missing entry evidence
-

## Expected handoff
-

## Next gate
- Entry conditions:
- Next skill:
```

## Entry conditions

| Skill | Minimum entry evidence | If missing |
|---|---|---|
| `fde-problem-discovery` | A customer, scenario, or initial signal | Collect interviews, tickets, observations, or business data |
| `fde-engagement-charter` | Evidence-backed problem-discovery package | Complete users, problem, impact, baseline, and evidence |
| `fde-prd-writer` | Approved problem-discovery package and POC charter | Clarify success criteria, scope, responsibilities, and commitments |
| `fde-deployment-architect` | Acceptance-ready POC PRD | Complete system boundaries, NFRs, and acceptance requirements |
| `fde-agent-skill-designer` | Approved PRD, architecture, and risk controls | Complete missing behavior or deployment constraints |
| `fde-poc-runner` | Runnable solution, test path, and frozen acceptance criteria | Resolve architecture or skill-design blockers |
| `fde-adoption-and-value` | Observable POC or pilot usage evidence | Collect real behavior, burden, and outcome data |
| `fde-playbook-productizer` | Reviewed delivery learning and evidence of repetition | Complete adoption/value review or collect more delivery evidence |

## Minimum handoff

Every handoff includes confirmed facts and sources, assumptions and validation methods, in/out of scope, risks and owners, the current decision, and inputs directly usable by the next skill.

For stateful delivery, also hand over `fde-project.json`, the four gate statuses, new decisions or unresolved blockers, and one prioritized `next_action`. The state file indexes artifacts; it never replaces their business review.
