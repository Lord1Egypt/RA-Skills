## Description:

Guides OpenClaw administrators through configuring MiniMax model providers, model definitions, aliases, fallback behavior, and validation for API-key or OAuth access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jooey](https://clawhub.ai/user/jooey)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw administrators use this skill to add MiniMax as a model source, choose between API-key and OAuth access, and validate the resulting provider configuration before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable main-branch download instructions can install code that differs from the validated release.

Mitigation: Install from the trusted ClawHub release when possible, or pin and verify the downloaded archive before use.

Risk: The skill guides live edits to ~/.openclaw/openclaw.json, which can break OpenClaw if incorrect fields or values are added.

Mitigation: Back up the OpenClaw configuration first, run JSON validation and openclaw doctor, and restart only after validation passes.

Risk: API keys, OAuth setup, and recurring quota-check commands may trigger billed or account-affecting API calls.

Mitigation: Confirm credentials and billing posture before testing, and treat any cron-based quota check as a deliberate live request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jooey/skills/add-minimax-provider)
- [MiniMax platform](https://platform.minimaxi.com)
- [MiniMax OpenAI-compatible chat completions endpoint](https://api.minimaxi.com/v1/chat/completions)
- [MiniMax Anthropic-compatible API base](https://api.minimaxi.com/anthropic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live API test commands, OpenClaw configuration edits, fallback recommendations, and troubleshooting steps.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
