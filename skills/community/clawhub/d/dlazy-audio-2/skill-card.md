## Description:

Dlazy Audio音频生成 helps agents use the dlazy CLI to invoke hosted audio models for text-to-speech, music, sound effects, voice cloning, and pipeline-based audio generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and automation teams use this skill to select and run dlazy CLI commands that generate speech, music, sound effects, multi-role dialogue, and cloned-voice audio from text or media inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private media or voice recordings may be uploaded to dLazy-hosted services.

Mitigation: Only provide files suitable for hosted processing and review privacy requirements before use.

Risk: Voice-cloning workflows can enable deceptive or unauthorized voice use.

Mitigation: Use voice cloning only with clear speaker permission and lawful, non-deceptive purposes.

Risk: API keys can be exposed if pasted into chat, logs, or command history.

Mitigation: Use the dlazy auth flow or environment variables, avoid echoing keys, and rotate or revoke keys if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dlazy-audio-2)
- [dLazy service website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated audio file paths or hosted output URLs returned by dlazy CLI JSON envelopes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
