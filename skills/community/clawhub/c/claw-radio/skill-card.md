## Description:

Operate a radio station. Teaches you how to be an AI radio host and work with the claw radio cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vossenwout](https://clawhub.ai/user/vossenwout)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate a local AI radio station with the claw-radio CLI: configure dependencies, build playlists, queue host banter, start playback, poll cues, and stop the session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can overwrite existing Docker/SearxNG container state or files under ~/.openclaw/searxng.

Mitigation: Check for an existing searxng container and existing ~/.openclaw/searxng files before setup, back them up, and review each install step before running it.

Risk: The setup relies on mutable third-party installs, including Homebrew packages, Docker/Colima, media tools, and a latest-tagged SearxNG container.

Mitigation: Use only if those dependencies are acceptable in the target environment, and pin the Docker image and CLI version where practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vossenwout/skills/claw-radio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides a single persistent tmux-controlled CLI session.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
