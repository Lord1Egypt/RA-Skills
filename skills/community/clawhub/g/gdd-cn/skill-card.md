## Description:

Guides agents through Chinese-language single-system game design document drafting, covering positioning, rules, formulas, configuration tables, edge cases, dependencies, tunable values, acceptance criteria, and review checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharinchan233](https://clawhub.ai/user/sharinchan233)

### License/Terms of Use:

MIT-0

## Use Case:

Game designers and development teams use this skill to draft and maintain Chinese-language single-system GDDs through a confirmation-driven workflow. It reads project planning context, records rules and formulas, defines configuration table structure, checks dependencies and conflicts, and produces QA-ready acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read existing project planning files and create or edit GDD and session-tracking files.

Mitigation: Use it in a project workspace where those planning files are intended inputs, and review each proposed section or file edit before confirming writes.

## Reference(s):

- [Configuration Table Specification](references/config-table-spec.md)
- [Naming Glossary and Style Constraints](references/naming-glossary.md)
- [Review Checklists](references/review-checklists.md)
- [Section Playbook](references/section-playbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Chinese-language Markdown documents with configuration table schemas and review prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or edits project planning files only after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
