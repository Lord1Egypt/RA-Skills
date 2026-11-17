## Description:

ClawCap is a spending-cap proxy for OpenClaw that routes model-provider traffic through one proxy URL to enforce daily and monthly limits, detect runaway activity, and support remote agent stops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kintupercy](https://clawhub.ai/user/kintupercy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use ClawCap to route OpenClaw model-provider requests through a spending-cap proxy, enforce daily and monthly limits, monitor usage, and stop runaway agent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw provider traffic and provider credentials are routed through a third-party proxy service.

Mitigation: Install only after deciding that ClawCap is trusted to process prompts, responses, metadata, and provider API credentials.

Risk: The setup process persists a live ClawCap proxy token and rewrites local OpenClaw provider base URLs.

Mitigation: Protect ~/.openclaw/openclaw.json, review which providers were patched, and use the uninstall script or backup file to restore direct provider URLs when stopping use.

Risk: Provider API keys may remain valid after testing with the proxy.

Mitigation: Consider rotating provider keys after testing, especially before using production accounts.

## Reference(s):

- [ClawCap skill page](https://clawhub.ai/kintupercy/skills/clawcap)
- [ClawCap website](https://clawcap.co)
- [ClawCap setup page](https://clawcap.co/setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a CLAWCAP_TOKEN value; setup changes OpenClaw provider base URLs and writes a backup before saving configuration.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
