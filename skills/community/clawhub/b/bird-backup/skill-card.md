## Description:

X/Twitter CLI for reading, searching, posting, and engagement via cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwarranto](https://clawhub.ai/user/qwarranto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent install and operate the bird CLI for reading X/Twitter content, searching timelines, managing bookmarks and likes, and performing account actions when authenticated with cookies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external bird CLI package that is not pinned in the artifact.

Mitigation: Review the package source and resolved version before installation, and install only from trusted package registries or taps.

Risk: The CLI can access live X/Twitter cookies or browser profiles and may read private account data.

Mitigation: Use a dedicated browser profile when possible and avoid placing live cookies directly in shell history, commands, or project configuration.

Risk: Authenticated commands can perform account actions such as posting, following, or unfollowing.

Mitigation: Review commands before execution and prefer read-only workflows unless account actions are explicitly intended.

## Reference(s):

- [Bird homepage](https://bird.fast)
- [ClawHub skill page](https://clawhub.ai/qwarranto/skills/bird-backup)
- [ClawHub publisher profile](https://clawhub.ai/user/qwarranto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to run the external bird CLI and may request JSON, full JSON, or plain CLI output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
