## Description:

Improvement Generator produces ranked improvement candidates for a target skill from target analysis, feedback signals, failure traces, and evaluator failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to propose documentation, guardrail, prompt, workflow, and test improvements for agent skills. It also helps retry improvement attempts by injecting prior failure traces and deprioritizing repeatedly failed strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate generation may call a local Claude CLI and send target SKILL.md plus evaluator failure details to it.

Mitigation: Use the skill only in environments where that data sharing is acceptable, and review inputs before enabling evaluator-driven fixes.

Risk: Model-generated SKILL.md changes can affect future agent behavior while being labeled low-risk and executor-supported.

Mitigation: Require human review and security scanning before applying generated SKILL.md changes.

Risk: Improvement proposals could introduce incorrect or misleading guidance into a skill.

Mitigation: Review proposed changes against the target skill's intended behavior before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/auto-improvement-generator)
- [Publisher Profile](https://clawhub.ai/user/lanyasheng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON candidate artifact with supporting Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes candidate identifiers, categories, risk levels, rationale, source references, executor support, execution plans, failure trace usage, and a truth anchor.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
