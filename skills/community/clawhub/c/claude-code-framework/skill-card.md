## Description:

Provides an agent execution framework with tool-risk classification, context budget monitoring, execution modes, and lifecycle hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjhveteran199-bit](https://clawhub.ai/user/xjhveteran199-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a reference framework for planning tool calls, classifying risk, monitoring context budget, and organizing lifecycle hooks in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval-required actions may continue without real approval, so the framework should not be treated as an enforcement boundary.

Mitigation: Use it as a prototype or reference until approval enforcement and hook-denial handling are fixed and verified.

Risk: The skill may be used to govern writes, shell commands, network calls, Git changes, browser actions, or messages despite incomplete controls.

Mitigation: Keep those actions behind the host agent's own permission system and require external review before production use.

Risk: Logging and mode-change behavior may expose workflow details or weaken intended restrictions.

Mitigation: Minimize logs, review mode changes, and test configuration changes before enabling the framework in a live workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xjhveteran199-bit/skills/claude-code-framework)
- [Publisher Profile](https://clawhub.ai/user/xjhveteran199-bit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript and JSON code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe framework status, risk assessments, hook execution results, and context budget guidance for an agent workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
