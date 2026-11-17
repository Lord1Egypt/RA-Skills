## Description:

Uses the agent-browser CLI for browser automation tasks such as check-ins, form filling, screenshots, and web content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huang-shao](https://clawhub.ai/user/huang-shao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused users use this skill to drive a browser through the agent-browser CLI for navigation, element selection, form interaction, screenshots, scheduled check-ins, and page-content extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can perform live account actions such as logins, submissions, purchases, and check-ins.

Mitigation: Use it only where automated actions are allowed and require confirmation before login, submit, purchase, or check-in steps run.

Risk: Screenshots and page dumps can capture sensitive page or account data, especially in scheduled workflows.

Mitigation: Avoid saving sensitive screenshots or page dumps, and review scheduled scripts before enabling recurring execution.

Risk: The documented global npm install can change over time and may not be pinned to a reviewed version.

Mitigation: Prefer a pinned local install over a mutable global npm installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huang-shao/skills/agent-browser-cli-bak)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples cover browser navigation, page interaction, content extraction, screenshots, and cron-based automation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
