## Description:

Query Anthropic Admin API for token usage reports (daily, weekly, monthly) with model breakdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leaofelipe](https://clawhub.ai/user/leaofelipe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query Anthropic Organization Admin API usage, summarize token consumption across daily, weekly, or monthly windows, and optionally break usage down by model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a high-privilege Anthropic Admin API key.

Mitigation: Configure the key through the OpenClaw API-key field or a controlled local secret configuration, and do not paste the key into chat.

Risk: Bundled tests may accidentally use real credentials if a real ANTHROPIC_ADMIN_API_KEY is exported.

Mitigation: Unset real credentials before running tests, or run tests only after the curl stub issue described by the security evidence is fixed.

## Reference(s):

- [Anthropic Usage ClawHub Page](https://clawhub.ai/leaofelipe/skills/anthropic-usage)
- [OpenClaw](https://openclaw.dev)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [Anthropic Usage Report API Endpoint](https://api.anthropic.com/v1/organizations/usage_report/messages)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs token usage summaries, optional per-model tables, and agent-side cost estimates based on live Anthropic pricing.]

## Skill Version(s):

1.0.7 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
