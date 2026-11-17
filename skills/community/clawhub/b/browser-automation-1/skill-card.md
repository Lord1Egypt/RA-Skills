## Description:

Automate web browser interactions via CLI for browsing websites, navigating pages, extracting data, taking screenshots, filling forms, clicking buttons, and interacting with web applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuradil](https://clawhub.ai/user/nuradil)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to control a local browser from an agent workflow for web navigation, form interaction, screenshots, downloads, and structured data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad web, local-network, persistent-session, download, and screenshot capabilities can expose sensitive data or reach unintended targets.

Mitigation: Use a dedicated temporary browser profile, avoid internal or localhost targets unless explicitly intended, and delete profile, screenshot, and download artifacts after sensitive tasks.

Risk: Authenticated browsing can persist saved passwords, cookies, and session state between runs.

Mitigation: Avoid real credentials unless necessary and isolate browser sessions for sensitive work.

Risk: Downloaded files and model-backed page extraction may expose or mishandle sensitive content.

Mitigation: Treat downloads and extracted page data as untrusted, review outputs before reuse, and verify downloaded files before opening or processing them.

## Reference(s):

- [Browser Automation CLI Reference](artifact/REFERENCE.md)
- [Browser Automation Examples](artifact/EXAMPLES.md)
- [ClawHub skill page](https://clawhub.ai/nuradil/skills/browser-automation-1)
- [ClawHub publisher profile](https://clawhub.ai/user/nuradil)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create browser screenshots, downloads, and persistent browser profile data during execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
