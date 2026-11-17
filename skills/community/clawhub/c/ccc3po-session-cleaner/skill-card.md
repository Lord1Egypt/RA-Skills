## Description:

Safely clean OpenClaw old session files and rebuild sessions.json for Ubuntu ARM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccc-3po](https://clawhub.ai/user/ccc-3po)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to clean older OpenClaw session files on Ubuntu ARM systems and rebuild the sessions.json index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permanent deletion of OpenClaw session history can occur without preview, confirmation, backup, or reliable protection of the main session.

Mitigation: Review commands before use, validate the session directory, preview files selected for deletion, require confirmation, exclude active or main sessions, and back up session files before deletion.

Risk: The cleanup commands use an absolute OpenClaw session path, which may be unsafe if run on an unexpected host or directory layout.

Mitigation: Confirm the target session directory before running cleanup and avoid executing the commands outside the intended Ubuntu ARM OpenClaw environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccc-3po/skills/ccc3po-session-cleaner)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown with shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands report session counts and sessions.json size, delete .jsonl files older than 3 days, and rebuild sessions.json.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
