## Description:

Put a Gemini CLI subscription on the asale market: import it, set a price floor and a concurrency cap, and see which of its models are actually selling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users with Gemini CLI subscriptions use this skill to connect the local asale daemon, import a Gemini account, set selling limits, and monitor which Gemini models are offered on the asale market.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation runs remote scripts from the asale delivery channel.

Mitigation: Install only if the delivery channel is trusted, prefer a verified versioned installer, and review the installer before use.

Risk: The skill can operate a local daemon that imports Gemini credentials and puts subscription capacity on a market.

Mitigation: Review settings in the asale UI and confirm account import, enablement, price floor, concurrency, and daily limits before selling.

Risk: Selling settings can affect money or subscription capacity if changed from stale account state.

Mitigation: List accounts before changing selling status and do not lower the price floor without explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-sell-gemini)
- [asale homepage](https://asale.ai)
- [asale source repository](https://github.com/asale-ai/asale)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON RPC payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a local asale daemon token; actions target the loopback daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
