## Description:

AI-agent skill for Taiwan stock, futures, and options operations via fubon-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mofesto](https://clawhub.ai/user/mofesto)

### License/Terms of Use:


## Use Case:

Developers and trading workflow operators use this skill to run Fubon Neo authentication, account queries, market data retrieval, order management, realtime subscriptions, conditional orders, and fubon-cli natural-language command flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles brokerage credentials and API keys.

Mitigation: Use an isolated non-admin environment, pin and verify the exact fubon-cli version, and avoid placing brokerage passwords or API keys directly in chat or command-line arguments.

Risk: The skill can assist with live trading actions while safety controls are under-scoped.

Mitigation: Require explicit confirmation of account, symbol, quantity, price, and action before submitting any live order, then verify order state after submission.

## Reference(s):

- [Fubon Cli ClawHub skill page](https://clawhub.ai/mofesto/skills/fubon-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON or JSONL command output contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-streaming commands return JSON with success and error fields; streaming commands return JSONL.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
