## Description:

BFunbot Skill lets agents create BSC tokens, check fee earnings and balances, reload BFun.bot Credits, and use BFunBot's Agent API and LLM Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bfunbot](https://clawhub.ai/user/bfunbot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and BFunBot users use this skill to create and monitor BSC tokens, review fee earnings and wallet or credit balances, reload credits from a trading wallet, and route LLM calls through BFunBot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger financially impactful token launches and wallet-funded credit reloads.

Mitigation: Use a dedicated least-privilege BFunBot API key and require explicit confirmation for token launches, reload amounts, funding source, chain, and irreversible disable actions.

Risk: Agent Reload can move funds from a trading wallet into BFun.bot Credits.

Mitigation: Enable Agent Reload only when wallet-funded reloads are acceptable and keep daily reload limits low enough for the account's risk tolerance.

Risk: The LLM gateway routes prompts, secrets, or business data through a third-party service.

Mitigation: Do not send secrets or sensitive personal or business data through the BFunBot LLM Gateway unless third-party processing is approved.

## Reference(s):

- [BFunBot Agent API Quick Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/bfunbot/skills/bfunbot-skill)
- [BFunBot](https://bfun.bot)
- [BFunBot Agent API](https://bfun.bot/agent)
- [BFunBot API Keys](https://bfun.bot/settings/api-keys)
- [BFun LLM Gateway](https://bfun.bot/llm)
- [BFunBot Credits](https://bfun.bot/credits)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated API calls and state-changing actions that require user confirmation.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
