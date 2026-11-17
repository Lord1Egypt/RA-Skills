## Description:

AI-powered Creem store monitor for real-time Telegram alerts, churn analysis, and retention actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[malakhov-dmitrii](https://clawhub.ai/user/malakhov-dmitrii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SaaS operators use this skill to monitor Creem webhook events, receive Telegram alerts, analyze churn signals, and trigger or approve retention actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic retention actions can change live billing or subscription state.

Mitigation: Use test-mode Creem credentials first and disable automatic execution unless an approval policy is in place.

Risk: Weak authorization or validation controls can let untrusted inputs influence operational actions.

Mitigation: Restrict Creem API key permissions, limit Telegram operators, and validate webhook body sizes and LLM outputs before production use.

Risk: Production deployment can expose revenue workflows to incorrect or overconfident churn decisions.

Mitigation: Review action recommendations, monitor outcomes, and require manual approval for material account changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/malakhov-dmitrii/skills/creem-store-agent)
- [Publisher profile](https://clawhub.ai/user/malakhov-dmitrii)
- [Creem](https://creem.io)
- [Creem documentation](https://docs.creem.io)
- [OpenClaw](https://openclaw.dev)
- [Anthropic Console](https://console.anthropic.com)
- [Demo video](https://youtube.com/shorts/M9A876D5JEE)
- [Tutorial article](https://dev.to/hennessy811/building-an-ai-agent-that-saves-your-saas-revenue-nkf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code, configuration details, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Creem, Telegram, and Anthropic credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
