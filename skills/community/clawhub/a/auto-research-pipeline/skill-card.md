## Description:

Auto Research Pipeline automates an AutoResearch experiment loop, analysis, multi-agent project orchestration, and skill packaging from a single agent invocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fireflywwj](https://clawhub.ai/user/fireflywwj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run AutoResearch setup, execution, and analysis, then coordinate specialized agents to apply the selected project changes and package the result as a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate experiments and multi-agent project work automatically, which may produce broad code or configuration changes.

Mitigation: Use it only in a workspace where broad automated edits are acceptable, and configure AutoResearch setup with explicit editable files, metrics, and allowed commands before execution.

Risk: The security scan summary flags insufficient user control and boundaries for autonomous research and orchestration.

Mitigation: Review the generated plan, experiment outputs, and final workspace diff before accepting or publishing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fireflywwj/skills/auto-research-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, shell commands, configuration, guidance]

**Output Format:** [Markdown, code changes, configuration, and command-oriented agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate automated experiments and multi-agent workspace changes through the surrounding agent environment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
