## Description:

Download purchased tracks from Beatport using the openclaw headless browser tool (CDP).

This skill is ready for commercial/non-commercial use.

## Publisher:

[esanle](https://clawhub.ai/user/esanle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through downloading purchased Beatport tracks with an authenticated OpenClaw-controlled browser session, including login, download setup, queue handling, and local file cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to an authenticated Beatport browser session and may expose account cookies or credentials if reused in a shared browser profile.

Mitigation: Use a dedicated temporary Chrome profile for Beatport, avoid profiles with other logged-in sites, and do not paste cookies into shell history or logs.

Risk: The skill enables local browser downloads and includes cleanup commands that remove files matching download patterns.

Mitigation: Use a dedicated download directory and review cleanup commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/esanle/skills/beatport-dl-with-browser-tool)
- [Beatport](https://www.beatport.com/)
- [Beatport account login](https://account.beatport.com/)
- [Beatport library downloads](https://www.beatport.com/library/downloads)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation guidance and local download handling steps for authenticated Beatport sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
