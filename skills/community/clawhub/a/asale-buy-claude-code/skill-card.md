## Description:

Switches Claude Code between buying from the asale market and using its own subscription, and reports which running sessions are still using the previous configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to inspect and switch Claude Code between direct subscription usage and routing through a local asale proxy or market. It also helps them identify running Claude Code sessions that still use configuration read at process startup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and updater execute remote scripts from asale's delivery path.

Mitigation: Review the installer source before installation and install only when the publisher and delivery path are trusted.

Risk: Enabling the switch changes Claude Code authentication and routes future Claude Code requests through asale.

Mitigation: Confirm user intent before enabling, inspect the reported configuration paths, and tell users the change applies when Claude Code is next started.

Risk: The workflow relies on a local daemon token and loopback RPC endpoint.

Mitigation: Keep the daemon token private, call only the loopback endpoint with the token header, and do not start the daemon or retry sign-in failures without user action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-buy-claude-code)
- [asale homepage](https://asale.ai)
- [asale source repository](https://github.com/asale-ai/asale)
- [asale Unix installer](https://asale.ai/dl/install.sh)
- [asale Windows installer](https://asale.ai/dl/install.ps1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON RPC payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local daemon calls and Claude Code configuration changes; the skill itself does not produce standalone files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
