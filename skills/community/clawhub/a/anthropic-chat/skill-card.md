## Description:

Interact directly with Claude via Anthropic Messages API using your own API key to send and receive natural language tasks and responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liutao0401-afk](https://clawhub.ai/user/liutao0401-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to send natural-language tasks to Claude through Anthropic's Messages API with their own Anthropic API key, optionally selecting a Claude model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content is sent to Anthropic's API and may expose secrets, regulated data, or proprietary material if users include it in prompts.

Mitigation: Use the skill only when Anthropic API transfer is approved, and avoid sending sensitive content unless that transfer is authorized.

Risk: Server security guidance says the current script is expected to fail until the TASK input handling bug is fixed.

Mitigation: Fix and test task input handling with non-sensitive prompts before relying on the skill in normal workflows.

## Reference(s):

- [Anthropic Messages API endpoint](https://api.anthropic.com/v1/messages)
- [ClawHub skill page](https://clawhub.ai/liutao0401-afk/skills/anthropic-chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Natural-language responses and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ANTHROPIC_API_KEY and optional ANTHROPIC_MODEL environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
