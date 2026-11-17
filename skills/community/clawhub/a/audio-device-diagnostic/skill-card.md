## Description:

Audio device diagnostic skill that lists available audio input devices and checks whether devices are working.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose audio input problems, list available microphones, confirm PyAudio device IDs, and choose a working input device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing PyAudio can introduce dependency risk if the package version or environment is not reviewed.

Mitigation: Install PyAudio in a normal, isolated Python environment and consider pinning a reviewed version.

Risk: The skill's troubleshooting guidance is primarily in Chinese, which may lead to misunderstanding for non-Chinese users.

Mitigation: Review a translation before relying on the troubleshooting guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/audio-device-diagnostic)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audio input device listings, troubleshooting guidance, and dependency installation commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
