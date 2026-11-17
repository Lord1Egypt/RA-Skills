## Description:

Generates comprehensive campaign documents, task decompositions, and context documents from minimal input for ClawTeam continuous iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hickhe](https://clawhub.ai/user/hickhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn minimal project inputs and Code Archaeology analysis into campaign documents, task decompositions, context documents, validation standards, and ClawTeam-ready execution plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe file-writing scope can write generated artifacts to user-provided output paths.

Mitigation: Run the skill in a constrained workspace and review output paths before execution.

Risk: Untrusted analysis text can be carried into AI-executable plans.

Mitigation: Use trusted input files only and manually review generated execution plans before giving them to tool-enabled agents.

Risk: Unvalidated projectName values can influence generated directory and file paths.

Mitigation: Validate projectName values before running workflow generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hickhe/skills/ai-plan-generator)
- [Usage examples](artifact/EXAMPLE.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown and JSON files, with ClawTeam task data and generated command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates campaign documents, task decompositions, context documents, completeness reports, and AI execution plans in user-provided output paths.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
