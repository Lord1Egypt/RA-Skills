## Description:

API-key-free online research via the built-in browser tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to perform browser-based online research when API-key-backed web search is unavailable, while checking source quality and falling back when browser access is blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser availability guard reads recent local OpenClaw session logs as part of its diagnostic check.

Mitigation: Review before installing and use only when local diagnostic access to recent OpenClaw session logs is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/browser-research-lite)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text]

**Output Format:** [Markdown guidance with inline shell commands and concise text answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return JSON status from the browser availability guard.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
