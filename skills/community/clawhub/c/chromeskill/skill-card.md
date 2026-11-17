## Description:

Browser automation via Chrome AI Action (CAA) bridge. Control Chrome programmatically by navigating, clicking, typing, taking screenshots, extracting content, and using other browser actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jami-lin](https://clawhub.ai/user/jami-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate Chrome browser workflows such as page navigation, form interaction, screenshots, content extraction, network inspection, cookie and storage management, and PDF export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The startup flow can install and run mutable third-party npm code globally.

Mitigation: Install only after reviewing and pinning the bridge package, and approve package installation before first use.

Risk: The skill gives an agent broad control over Chrome sessions and browser data.

Mitigation: Use a separate Chrome profile with no sensitive logins, and require explicit approval before logins, cookie or storage access, JavaScript injection, uploads, downloads, network mocking, or transactions.

Risk: The bridge controls a local browser automation endpoint and may interact with live websites.

Mitigation: Keep the bridge local, close Chrome normally after use, and review proposed browser actions before they affect accounts, data, or transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jami-lin/skills/chromeskill)
- [Bridge API Reference](artifact/references/bridge-api.md)
- [Setup Guide](artifact/references/setup-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API requests]

**Output Format:** [Markdown guidance with JSON browser-action requests and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local bridge on 127.0.0.1 and produce browser automation requests for navigation, interaction, screenshots, extraction, storage, cookies, network controls, file operations, and PDF export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
