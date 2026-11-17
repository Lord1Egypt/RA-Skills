## Description:

Automatically guides an agent to consult official documentation before answering uncertain tool, API, configuration, permission, or error questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ekin-chn](https://clawhub.ai/user/ekin-chn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make documentation-grounded decisions when configuring tools and APIs, diagnosing permission or authentication issues, or resolving uncertain command usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause additional external documentation fetches before answering.

Mitigation: Use it when documentation lookup is appropriate and narrow trigger language if always-on behavior is too broad.

Risk: Answers can still be wrong if documentation versions are mismatched or official docs are unavailable.

Mitigation: Have the agent state the documentation URL, date or version checked, and uncertainty when official docs do not resolve the question.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ekin-chn/skills/doc-first)
- [OpenClaw documentation](https://docs.openclaw.ai/llms.txt)
- [OpenAI API documentation](https://platform.openai.com/docs)
- [Anthropic documentation](https://docs.anthropic.com/)
- [GitHub REST API documentation](https://docs.github.com/rest)
- [Discord Developer documentation](https://discord.com/developers/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with cited documentation sources and optional code, command, or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include URLs, dates, or version numbers for checked official documentation.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
