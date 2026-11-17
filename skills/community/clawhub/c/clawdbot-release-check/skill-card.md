## Description:

Check for new clawdbot releases and notify once per new version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pors](https://clawhub.ai/user/pors)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check whether their installed Clawdbot version is behind the latest published release and to receive a one-time notification when an update is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled update checks may process untrusted release data before notifying the user.

Mitigation: Review or patch the skill before enabling the scheduled job; prefer manual checks until release notes are handled as quoted untrusted data.

Risk: Release tag parsing may be unsafe for non-numeric or unexpected version strings.

Mitigation: Validate release tags as numeric versions before Bash arithmetic or skip comparison for unsupported tag formats.

Risk: Fixed temporary file paths can be overwritten or raced on shared systems.

Mitigation: Replace fixed files under /tmp with mktemp-created paths or files in the skill state directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pors/skills/clawdbot-release-check)
- [Clawdbot repository](https://github.com/clawdbot/clawdbot)
- [Clawdbot releases API](https://api.github.com/repos/clawdbot/clawdbot/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown notifications with inline shell commands and plain-text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local state, cache release data, and install or remove a scheduled notification job.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
