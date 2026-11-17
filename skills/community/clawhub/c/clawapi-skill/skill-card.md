## Description:

Build your AI Company -- 8 models across 4 providers act as your CEO, CTO, CMO, CFO, and Workers, with crypto-native pay-as-you-go access through ClawAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawapiorg](https://clawhub.ai/user/clawapiorg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure OpenClaw-compatible agents to call ClawAPI's OpenAI-compatible model endpoint, select among listed models, check account balance, and handle common provider errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes unattended crypto deposits using a wallet private key.

Mitigation: Do not give agents wallet private keys or permission to auto-deposit funds; use manual deposits through the website.

Risk: The skill directs users to place API keys in plaintext configuration files.

Mitigation: Keep CLAWAPI_KEY in one protected secret location and avoid committing or unnecessarily duplicating the key.

Risk: The skill points agents to remotely fetched provider documentation.

Mitigation: Treat remote documentation as data to review rather than instructions to execute.

Risk: The skill routes agent work through a third-party paid model provider.

Mitigation: Install only if that provider relationship is acceptable, and monitor usage, balance, and billing behavior.

## Reference(s):

- [ClawAPI homepage](https://clawapi.org)
- [ClawAPI skill docs](https://clawapi.org/api/skill)
- [ClawAPI structured skill docs](https://clawapi.org/api/skill?format=json)
- [ClawHub skill listing](https://clawhub.ai/clawapiorg/skills/clawapi-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/clawapiorg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, environment variable, shell, curl, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLAWAPI_KEY for ClawAPI access and includes paid API usage plus crypto funding guidance.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
