## Description:

Generates a Python test harness with a fake model for checking an AgentScope agent's response before live model testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can generate a pytest scaffold for an AgentScope agent and check its response with a fake model before using a live model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an OpenAI-compatible API key despite describing an offline workflow; the included generator does not use the key.

Mitigation: Review the credential requirement before installing; avoid exposing a key unless its use is necessary and acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/trend0522/skills/agentscope-agent-test-harness)
- [AgentScope project (listed homepage)](https://github.com/agentscope-ai/agentscope)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Python pytest file and Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated test uses a fake response; pytest reports its result.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
