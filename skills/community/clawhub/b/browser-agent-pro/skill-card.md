## Description:

Automate browser tasks locally with headless Chrome or via Browserbase cloud for stealth, CAPTCHA-solving, and protected sites access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maikimolto](https://clawhub.ai/user/maikimolto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to guide browser automation tasks such as navigating websites, filling forms, clicking controls, taking screenshots, extracting page data, and setting up local or Browserbase-backed browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install and run a global browser automation CLI that can control browser sessions.

Mitigation: Prefer a pinned or local agent-browser install and review commands before execution.

Risk: Browser automation can access cookies, saved logins, local storage, clipboard content, and persisted session state.

Mitigation: Use isolated sessions by default, avoid real Chrome profiles unless necessary, close sessions after use, and clean up saved state files.

Risk: Browserbase mode requires an API key and may expose cloud browser access if the key is mishandled.

Mitigation: Store Browserbase credentials in a dedicated private file, keep file permissions restrictive, and avoid logging or sharing the key.

## Reference(s):

- [agent-browser command reference](artifact/references/commands.md)
- [Browserbase sign-up](https://www.browserbase.com/sign-up)
- [ClawHub skill page](https://clawhub.ai/maikimolto/skills/browser-agent-pro)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation command sequences, troubleshooting steps, and credential-handling guidance.]

## Skill Version(s):

2.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
