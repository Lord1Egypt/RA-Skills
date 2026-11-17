## Description:

Automate web browser interactions using natural language via CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peytoncasper](https://clawhub.ai/user/peytoncasper)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to automate browser navigation, page actions, structured data extraction, element discovery, screenshots, form workflows, and browser cleanup from CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs dependencies and globally links an unaudited CLI.

Mitigation: Review the package files before running npm install or npm link, and install only inside a sandbox or trusted project.

Risk: Remote Browserbase mode can process browsing data outside the local machine.

Mitigation: Prefer local-only mode unless remote browsing is intentional and the data being browsed is appropriate for Browserbase processing.

Risk: Persistent browser profiles can retain saved passwords, cookies, and sessions.

Mitigation: Use isolated browser profiles and avoid persistent profiles for sensitive accounts or confidential browsing workflows.

Risk: The CLI can submit forms, log in, and download files through automated browser actions.

Mitigation: Confirm before submitting forms, logging in, or downloading files, and verify downloaded file integrity before opening or using them.

## Reference(s):

- [Browser Automation CLI ClawHub Page](https://clawhub.ai/peytoncasper/skills/browser-pc)
- [EXAMPLES.md](artifact/EXAMPLES.md)
- [REFERENCE.md](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with inline bash examples; browser commands return JSON status or data and may create screenshot or download files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are PNG files, downloads are saved to a local downloads directory, and browser sessions may use a persistent Chrome profile.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
