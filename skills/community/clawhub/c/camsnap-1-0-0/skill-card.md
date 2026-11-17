## Description:

Capture frames or clips from RTSP/ONVIF cameras.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xspeter](https://clawhub.ai/user/0xspeter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and technically capable external users use this skill to run camsnap commands for discovering RTSP/ONVIF cameras, capturing snapshots or short clips, monitoring motion events, and checking camera setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Camera credentials may be exposed through reusable command history, shared transcripts, or permissive configuration files.

Mitigation: Use a dedicated low-privilege camera account, avoid placing real passwords in reusable commands, and restrict permissions on camsnap configuration files.

Risk: Captured snapshots and clips may contain sensitive video or image data.

Mitigation: Save media only to controlled locations and apply local retention, access-control, and sharing policies before using the skill.

Risk: Installation depends on an unpinned third-party Homebrew tap and executable.

Mitigation: Review the upstream tap and package before installation, and pin or otherwise control the installed camsnap version in managed environments.

## Reference(s):

- [Camsnap homepage](https://camsnap.ai)
- [ClawHub skill page](https://clawhub.ai/0xspeter/skills/camsnap-1-0-0)
- [Publisher profile](https://clawhub.ai/user/0xspeter)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the camsnap binary, ffmpeg on PATH, camera network access, and user-provided camera configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
