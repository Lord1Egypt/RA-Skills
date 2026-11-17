## Description:

Use bird with Chrome cookies to read, search, and carefully post on X/Twitter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evandataforge](https://clawhub.ai/user/evandataforge)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through reading, searching, and inspecting X/Twitter content with bird and Chrome authentication. It also provides guarded browser-based posting and reply guidance when a user explicitly requests account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an authenticated X/Twitter browser session, which can expose account access through Chrome cookies.

Mitigation: Use a dedicated browser profile, verify the bird package source and version before use, and install only when this account access is acceptable.

Risk: Posting or replying from the user's account can publish unintended content or trigger platform account-protection systems.

Mitigation: Require explicit confirmation before each post or reply, avoid bird write commands, and use the browser workflow only for user-approved account actions.

Risk: Host browser control broadens the impact of an agent session beyond read-only command execution.

Mitigation: Avoid making host browser control a global default and allow it only for the specific browser profile and posting workflow that require it.

## Reference(s):

- [Bird CLI homepage](https://bird.fast)
- [Bird Chrome skill page](https://clawhub.ai/evandataforge/skills/bird-chrome)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request explicit user confirmation before posting or replying; read-oriented bird commands can be shaped for plain text or JSON output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
