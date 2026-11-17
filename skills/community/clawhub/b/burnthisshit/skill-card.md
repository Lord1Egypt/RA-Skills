## Description:

Forensically obliterate an OpenClaw session and all its traces -- transcript, trajectory, bak files, deleted archives, and sessions.json entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genortg](https://clawhub.ai/user/genortg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to remove OpenClaw session files and matching session-index entries when they deliberately need irreversible local session erasure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intentionally destructive and can irreversibly erase local OpenClaw session records.

Mitigation: Install and invoke it only when irreversible session erasure is intended, and keep separate audit or backup records if recovery or accountability matters.

Risk: Security evidence reports skipped normal confirmation and path-handling flaws that could delete or corrupt more than intended.

Mitigation: Require an explicit confirmation flow, avoid natural-language auto-triggering, and validate the target agent path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/genortg/skills/burnthisshit)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Destructive actions are irreversible and should require explicit confirmation before execution.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
