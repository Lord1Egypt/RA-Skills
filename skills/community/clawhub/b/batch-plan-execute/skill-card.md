## Description:

Use when the user wants AI to turn a requirement text, requirement document, and existing reviewed plan files into dependency-ordered implementation plans and, only after an explicit execution command, implement those plans with subagents in parallel where safe and in sequence where required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[micooz](https://clawhub.ai/user/micooz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to create, revise, retire, and execute dependency-aware implementation plans from requirements, reviewed plan files, or a plans directory. It is intended for repository planning workflows where execution is gated by an explicit user command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans or code changes may be inappropriate if execution is started before careful review.

Mitigation: Review generated plans before issuing a clear execution command.

Risk: Parallel execution can create conflicting changes when ownership of shared interfaces, schemas, migrations, or utilities is ambiguous.

Mitigation: Use dependency layers, assign one owner for each shared change, and hold downstream work until upstream validation succeeds.

Risk: A hidden planning state file may be created under plans/.

Mitigation: Inspect plans/.batch-plan-state.json when reviewing planning lineage, and do not treat it as permission to execute.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/micooz/skills/batch-plan-execute)
- [Plan Mode Contract](docs/plan.md)
- [Execute Mode Contract](docs/execute.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans, implementation summaries, scoped code changes, validation commands, and planning state updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update plan files under plans/ and a hidden plans/.batch-plan-state.json lineage file.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
