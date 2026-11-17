## Description:

AgentVibes内容技能 helps users generate marketing copy, written content, title optimizations, and structured content outputs through an AgentVibes-oriented workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and teams use this skill to generate marketing copy, writing content, optimized titles, and reusable content outputs in Chinese-friendly Agent workflows. It is not positioned for pure technical documentation writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local file and command-execution authority without a clear need.

Mitigation: Install and run it with restricted file and command access, and supervise any command or file operation it proposes.

Risk: API keys may be exposed if used in sensitive workspaces or stored directly in files.

Mitigation: Store API keys in environment variables and avoid using the skill in workspaces containing sensitive files unless tool scope is restricted.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JSON response examples and shell environment commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include structured success, data, and error fields; API-key configuration is described through an environment variable.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
