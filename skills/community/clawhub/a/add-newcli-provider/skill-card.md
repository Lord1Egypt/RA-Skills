## Description:

Configures OpenClaw to use NewCLI/FoxCode as a model proxy for Claude, GPT, and Gemini, including provider definitions, aliases, fallback routing, and validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jooey](https://clawhub.ai/user/jooey)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw administrators use this skill to add NewCLI/FoxCode model-provider routes for Claude, GPT, and Gemini, then validate model availability, aliases, and fallback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw traffic and an API key may be routed through a third-party model proxy.

Mitigation: Install only after independently verifying NewCLI/FoxCode, use a dedicated scoped key where possible, and avoid sensitive test prompts.

Risk: Provider, alias, and fallback changes can persistently alter model routing.

Mitigation: Back up the OpenClaw configuration before applying changes and review fallback routes before restarting the gateway.

Risk: Promotional or unapproved routes may be included in the setup material.

Mitigation: Remove referral-driven links and any unapproved endpoints before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jooey/skills/add-newcli-provider)
- [NewCLI/FoxCode service](https://code.newcli.com)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [Markdown with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides persistent OpenClaw provider, alias, and fallback configuration changes.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
