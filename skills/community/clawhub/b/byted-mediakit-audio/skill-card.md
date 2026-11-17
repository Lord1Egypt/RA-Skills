## Description:

Provides MediaKit CLI guidance for audio processing, including vocal/background separation and audio metadata probing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcvnebot](https://clawhub.ai/user/volcvnebot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run MediaKit CLI audio workflows for separating vocals from background audio and retrieving audio container and stream metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can expose MediaKit API keys through shell commands or plaintext configuration.

Mitigation: Use environment variables or a safer credential store, and avoid placing API keys directly in command history or shared config files.

Risk: The skill depends on a globally installed MediaKit CLI without a pinned version in the release evidence.

Mitigation: Install a pinned and verified version of the CLI before use and re-run version checks during setup.

Risk: Cloud-mode media processing may upload local or sensitive media files.

Mitigation: Use trusted inputs and avoid sensitive local files unless remote processing is intended and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcvnebot/skills/byted-mediakit-audio)
- [MediaKit shared rules](reference/shared.md)
- [Separate voice reference](reference/separate-voice.md)
- [Probe audio metadata reference](reference/probe-audio-metadata.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cloud workflows may return task_id and request_id values that require follow-up polling; local metadata probing can return final results directly.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
