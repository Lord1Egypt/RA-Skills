## Description:

Provides real-time voice announcements for OpenClaw agent events, with CLI and Python helpers for short spoken status updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wililam](https://clawhub.ai/user/wililam)

### License/Terms of Use:

MIT

## Use Case:

Developers using OpenClaw can add concise local voice announcements for received messages, task progress, completion, errors, startup checks, and integration tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to make announcements mandatory across sessions and persist those rules in workspace behavior files.

Mitigation: Install only when always-on voice announcements are desired, and remove or decline global behavior rules and session hooks before use.

Risk: Announcement text may be sent to a remote text-to-speech backend.

Mitigation: Do not announce prompt content, response content, secrets, or sensitive user data; keep messages short and non-sensitive.

Risk: The server security verdict is suspicious because the skill combines persistent behavior changes with voice-announcement automation.

Mitigation: Review the skill and its configuration before deployment, and limit execution to trusted workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wililam/skills/audio-announcement-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/wililam)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell, Python, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke text-to-speech playback and write local configuration and audio cache files.]

## Skill Version(s):

2.2.0 (source: release metadata, artifact metadata, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
