## Description:

Browser automation workflows through the agentbrowse CLI for launch, attach, observe, act, extract, navigation, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xor777](https://clawhub.ai/user/xor777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use AgentBrowse to control a real browser, inspect visible page state, interact with returned targets, navigate known URLs, extract structured page data, capture screenshots, and recover browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots and structured extraction can expose sensitive page contents.

Mitigation: Avoid screenshot or extract on sensitive pages unless needed, and switch to the appropriate protected-flow tool at login, identity, or payment boundaries.

Risk: AI-assisted observe and extract require API access that could be exposed through shared terminals, logs, or local configuration.

Mitigation: Keep API keys out of shared terminals and logs, and use reviewed local configuration practices before running AI-assisted features.

Risk: Installing the required CLI grants a third-party browser automation package access to automated browsing contexts.

Mitigation: Install only when the CLI publisher is trusted, prefer a reviewed pinned CLI version, and verify the installed agentbrowse command before use.

Risk: Browser refs can become stale after redirects, reloads, or dynamic page updates.

Mitigation: Re-run observe after meaningful page changes and discard stale refs before taking the next action.

## Reference(s):

- [AgentBrowse browser library and docs](https://github.com/MercuryoAI/agentbrowse)
- [OpenClaw marketplace README](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/openclaw/marketplace/README.md)
- [Operating guide](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/references/workflow.md)
- [Command guide](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/references/commands.md)
- [Failure recovery](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/references/statuses.md)
- [Boundaries and escalation](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/references/guardrails.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline shell commands and JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser session setup, page-action commands, structured extraction schemas, screenshot guidance, and recovery steps.]

## Skill Version(s):

0.1.22 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
