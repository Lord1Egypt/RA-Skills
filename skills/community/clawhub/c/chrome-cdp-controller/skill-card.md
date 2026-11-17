## Description:

Control a local Chrome browser with Chrome DevTools Protocol (CDP) through Puppeteer for navigation, form interaction, screenshots, JavaScript evaluation, and network response interception.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiaolin](https://clawhub.ai/user/hanxiaolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused agents use this skill to operate a user-started local Chrome instance through CDP for web navigation, UI interaction, scraping, testing workflows, screenshots, JavaScript evaluation, and network-response inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over a live Chrome browser session, which can expose logged-in accounts or sensitive pages.

Mitigation: Use a separate Chrome profile with no sensitive logins and close the DevTools-enabled browser when the task is finished.

Risk: A remote debugging port can expose browser control if it is reachable beyond the local machine.

Mitigation: Keep the DevTools port bound to localhost and do not expose it on a network interface.

Risk: Network interception can capture private or sensitive site traffic.

Mitigation: Avoid interception on private sites and review captured responses before storing or sharing them.

Risk: Browser automation dependencies may become outdated after release.

Mitigation: Update dependencies before use and review dependency changes before running the controller.

## Reference(s):

- [Chrome Remote Debugging Setup](references/chrome-setup.md)
- [CDP Controller Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/hanxiaolin/skills/chrome-cdp-controller)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON command sequences, JavaScript snippets, shell commands, and optional generated screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command execution can return structured JSON results from browser actions and captured network responses.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
