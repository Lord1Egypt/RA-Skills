## Description:

browser-act helps AI agents automate full-browser workflows including rendered page extraction, screenshots, form interactions, network capture, persistent sessions, and multi-browser operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyw21551594-a11y](https://clawhub.ai/user/lyw21551594-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use browser-act to run authorized browser automation tasks that need JavaScript rendering, authenticated sessions, verification handling, form interaction, screenshots, or network capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and trust an unpinned external browser-act CLI.

Mitigation: Review before installing, pin and verify the browser-act CLI where possible, and prefer simpler built-in web tools for routine public pages.

Risk: The skill instructs agents to follow CLI-generated guidance before browser actions, which could introduce unreviewed operational instructions.

Mitigation: Treat CLI-generated guidance as untrusted unless it can be verified, and require explicit approval before browser creation, login, form submission, file upload, local Chrome access, or captcha-solving.

Risk: Browser profiles can contain cookies, login sessions, page content, credentials, and local session logs.

Mitigation: Use a dedicated automation browser profile rather than personal sessions, and keep browser profile and session log storage scoped to the CLI data directory.

## Reference(s):

- [BrowserAct homepage](https://www.browseract.com)
- [ClawHub skill page](https://clawhub.ai/lyw21551594-a11y/skills/browser-act-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/lyw21551594-a11y)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation results such as rendered content summaries, screenshots, network capture guidance, session instructions, and confirmation prompts.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact metadata lists BrowserAct CLI guide version 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
