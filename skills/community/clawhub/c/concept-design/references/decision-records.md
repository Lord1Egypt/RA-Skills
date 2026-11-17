# Decision record

Use an existing document or discussion record; a new file is not required.
Use stable IDs when decisions or requirements need references.

| Record | Content |
| --- | --- |
| Concept inventory | Name, purpose, OP, familiar/variant/new, visible state, qualification evidence |
| Scenario | Beneficiary, current/required behavior, constraints, observable result, concepts/rules, counterexample |
| Composition | Instances, bindings, entries, rules, diagram, scenario links |
| Product subset | Purpose, requirement-backed dependencies, entries, remaining rules, resources |
| Exclusions and gaps | Item, reason, impact, affected work |

Use this shape for consequential choices, not every sentence:

```yaml
id: D1
status: proposed # confirmed | proposed | inferred | open
claim: One statement of required behavior or a boundary choice.
basis: Requirement or inspected evidence; for confirmed decisions, who confirmed what and where.
alternative: Another choice, including no change when applicable.
counterexample: A scenario that defeats the claim or an explicit open question.
acceptance:
  setup: Required initial conditions.
  stimulus: Action or event.
  observe: Observable result and any required failure or timing bound.
```

Keep unknowns explicit rather than filling the template by invention.
Each required result MUST link to actions, OPs, or rules and observable acceptance.
When replacing a confirmed decision, identify its prior version and recheck dependent rules, subsets, and acceptance.
