## Description:

杠精 Gangjing is a Chinese-language contrarian review and red-team skill for product, architecture, and code decisions that starts with verbal critique and escalates to code attack validation only when requested or when strong claims are made about workspace code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blurooo](https://clawhub.ai/user/blurooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to challenge product, architecture, API, data model, and code decisions before release. It surfaces vague requirements, hidden assumptions, alternatives, scalability and rollback risks, then provides remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and run attack harnesses against workspace code without strong enforced isolation or explicit execution consent.

Mitigation: Before allowing code testing, use an isolated disposable workspace or container, remove secrets from the environment, disable network access where possible, and require clear manual confirmation before any harness is written or run.

Risk: The skill uses an aggressive Chinese-language red-team review posture that may be unsuitable for routine assistance or users expecting neutral tone.

Mitigation: Install and invoke it only when an aggressive reviewer is desired, and use its documented intensity controls to downgrade or stop the review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blurooo/skills/gangjing)
- [Clawdis homepage](https://github.com/agent-dance/harness-engineering/tree/main/skills/gangjing)
- [Attack Dimensions](references/attack-dimensions.md)
- [Attack Pattern Library](references/attack-patterns.md)
- [Intensity Calibration](references/intensity-calibration.md)
- [Tool Integration](references/tool-integration.md)
- [Attack Engine Kit](templates/attack-engine-kit.md)
- [Decision Autopsy Template](templates/decision-autopsy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language Markdown with optional JSON attack configurations and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce temporary harness instructions or reports only when code testing is explicitly authorized by the user.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
