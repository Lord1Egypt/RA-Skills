## Description:

Triggers native system notifications across Windows, macOS, and Linux, including WSL, to alert the user when tasks are complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1tsnakers](https://clawhub.ai/user/1tsnakers)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send native desktop notifications after long-running work, urgent blockers, or high-impact actions complete across Windows, macOS, Linux, and WSL environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted notification text can be interpreted as AppleScript or PowerShell code on macOS, Windows, and WSL notification paths.

Mitigation: Use only trusted, fixed notification messages and titles until those platform branches pass values as data rather than concatenating them into script source.

Risk: The release has a suspicious security verdict from the authoritative scan evidence.

Mitigation: Review the skill before installing or deploying it, and treat notification inputs as untrusted unless they are fixed by the calling workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1tsnakers/skills/cross-platform-notifier)
- [Publisher profile](https://clawhub.ai/user/1tsnakers)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and usage guidance for triggering local desktop notifications; notification message and title should come from trusted, fixed text.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
