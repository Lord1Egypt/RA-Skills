## Description:

Cn LLM helps agents use AIsa for model routing, provider setup, and Chinese LLM access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure AIsa access, inspect supported Chinese LLM routing options, and send or compare chat requests against routed models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, system prompts, and message histories passed to the CLI are sent to AIsa and may be routed to downstream model providers.

Mitigation: Avoid sending secrets, private conversation history, or regulated data unless that data sharing is approved for the intended use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/cn-llm)
- [Publisher profile](https://clawhub.ai/user/baofeng-tech)
- [AIsa API endpoint](https://api.aisa.one/v1)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses are text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY for chat and compare requests; the models command can run without an API key.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
