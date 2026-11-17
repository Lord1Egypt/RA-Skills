## Description:

Dlazy Audio音频生成 helps agents choose and run dLazy CLI audio models for text-to-speech, music, sound effects, voice cloning, and pipeline-based audio generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and automation teams use this skill to generate narration, music, sound effects, and cloned-voice audio through dLazy-hosted models from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run CLI commands as part of audio generation workflows.

Mitigation: Review generated commands before execution and limit use to intentional dLazy audio generation tasks.

Risk: Local audio, video, or image files may be uploaded to the dLazy service.

Mitigation: Confirm files are appropriate to upload and avoid sending sensitive, private, or unauthorized media.

Risk: API keys may be exposed if pasted into chat, logs, command history, or URLs.

Mitigation: Use the documented auth flow or environment variables, do not echo keys, and rotate any key that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dlazy-audio)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files, JSON]

**Output Format:** [Markdown guidance with bash command blocks and dLazy JSON result envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audio file paths or hosted output URLs from dLazy.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.3.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
