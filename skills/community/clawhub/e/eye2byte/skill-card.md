## Description:

Give your agent eyes - capture screenshots, voice, and annotations from any screen, monitor, or device via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolverin0](https://clawhub.ai/user/wolverin0)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to give an agent explicit, user-requested visual and audio context from a local or remote screen for debugging, UI review, transcription, and short workflow observation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen, audio, transcript, and recent-context capture may expose private or sensitive information.

Mitigation: Use only after explicit user request, prefer a specific window, region, or monitor, and avoid all-monitor capture unless it is necessary.

Risk: The release installs an unpinned third-party package that handles sensitive local capture data.

Mitigation: Install only when the package source is trusted and review the package before deployment in sensitive environments.

Risk: Remote SSE use depends on EYE2BYTE_MCP_TOKEN as a bearer token.

Mitigation: Treat the token as a secret, avoid logging or sharing it, and rotate it if exposure is suspected.

Risk: Captured data is stored locally under the user's Eye2byte output directory.

Mitigation: Use the configured cleanup window, reduce retention for sensitive work, or manually remove captures after use.

## Reference(s):

- [Eye2byte GitHub homepage](https://github.com/wolverin0/Eye2byte)
- [Eye2byte PyPI package](https://pypi.org/project/eye2byte/)
- [ClawHub skill page](https://clawhub.ai/wolverin0/skills/eye2byte)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured text or markdown context packs, analyses, and transcriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize screenshots, short screen clips, voice recordings, existing image files, audio files, and recent capture context.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter: 0.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
