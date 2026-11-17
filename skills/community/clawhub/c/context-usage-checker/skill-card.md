## Description:

Context Usage Checker estimates the current conversation's token use and replies with used tokens, remaining tokens, usage percentage, a progress bar, and threshold-based guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to check whether a current conversation is approaching the model context limit before continuing, compacting, or starting a new session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the current conversation history to estimate token usage, although it reports only aggregate counts.

Mitigation: Use it in environments where aggregate context metrics are acceptable and avoid triggering it when conversation history contains information that should not be inspected by utility skills.

Risk: Token counts are estimates and may differ from platform-reported usage.

Mitigation: Treat the result as planning guidance and rely on platform statistics for exact limits when available.

Risk: The trigger phrases are broad and the skill is primarily documented in Chinese.

Mitigation: Review trigger configuration and user-facing language before deployment in multilingual or tightly controlled agent environments.

## Reference(s):

- [Context Usage Checker on ClawHub](https://clawhub.ai/rfdiosuao/skills/context-usage-checker)
- [Publisher profile](https://clawhub.ai/user/rfdiosuao)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status message with token counts, percentage, progress bar, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token counts are estimated from current session history and model-specific context window defaults.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
