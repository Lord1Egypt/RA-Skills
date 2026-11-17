## Description:

Generates test fixtures, mock data, example configurations, and pytest scaffolding for AgentScope agents and pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create AgentScope test data, pipeline configurations, and pytest scaffolding for development and CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real OpenAI API key may be written into generated fixture files when OPENAI_API_KEY is set.

Mitigation: Do not run with OPENAI_API_KEY set unless the generator is fixed to always emit a placeholder or redact secrets; inspect fixtures before committing or sharing them.

## Reference(s):

- [AgentScope project homepage](https://github.com/agentscope-ai/agentscope)

## Skill Output:

**Output Type(s):** [Configuration, Code, Test data]

**Output Format:** [JSON fixture files and Python pytest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports sequential, parallel, team, and dialogue fixture patterns.]

## Skill Version(s):

1.0.0 (source: ClawHub release; skill frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
