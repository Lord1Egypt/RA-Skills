## Description:

Enables AI agents to self-audit decision steps, identify reasoning bottlenecks, and generate improvement patches via chain-of-thought critique.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to review JSON execution traces, surface reasoning bottlenecks, and produce reflection reports that inform improvements to autonomous agent loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reflection reports and logs may contain sensitive information from agent trace files.

Mitigation: Use only controlled trace inputs and output locations, and treat generated reports as sensitive artifacts.

Risk: The current local script may need a bug fix before it works as advertised.

Mitigation: Review and test the script in a local sandbox before integrating it into agent loops or release workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/agent-reflection-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON report descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local reflection reports from JSON trace files; generated reports can contain sensitive trace-derived content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
