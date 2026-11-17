## Description:

Automate web browser interactions using natural language via CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to navigate websites, interact with page elements, extract structured data, take screenshots, and automate browser workflows through CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a browser on authenticated sites and submit forms.

Mitigation: Use test accounts or an isolated browser profile, and review actions before submitting forms or logging in.

Risk: The skill may use an external AI service for browser actions and extraction without a per-use prompt.

Mitigation: Avoid sensitive or internal sites unless external processing is approved.

Risk: Browser sessions, screenshots, and downloads can persist after use.

Mitigation: Clean up .chrome-profile, browser_screenshots, and downloads directories after use, and verify downloaded files before opening or using them.

## Reference(s):

- [Browser Automation Examples](EXAMPLES.md)
- [Browser Automation CLI Reference](REFERENCE.md)
- [ClawHub Skill Page](https://clawhub.ai/abeltennyson/skills/abe-browser-automation)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce screenshots and downloaded files in local agent directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
