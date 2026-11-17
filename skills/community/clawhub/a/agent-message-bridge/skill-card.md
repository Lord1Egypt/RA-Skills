## Description:

Agent Message Bridge lets Python agents exchange JSON messages through a local file-backed inbox bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[digital-baseline](https://clawhub.ai/user/digital-baseline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let multiple Python agents send, check, and poll local messages for coordination without manual relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted agent names can lead the bridge to read, write, or delete JSON files outside the intended message area.

Mitigation: Deploy only in a tightly controlled local environment, validate agent identifiers, constrain file paths to the bridge data directory, and disable deletion by default.

Risk: Received messages may be treated as trusted operational instructions by downstream agents.

Mitigation: Do not send secrets or sensitive operational data, and require downstream review, authentication, or signatures before acting on messages in real workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/digital-baseline/skills/agent-message-bridge)
- [Publisher profile](https://clawhub.ai/user/digital-baseline)
- [Digital Baseline community](https://digital-baseline.cn/)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Python code, shell command examples, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are represented as JSON files in a local inbox directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
