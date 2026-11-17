## Description:

Create AI avatar and talking head videos with OmniHuman, Fabric, and PixVerse models through the inference.sh CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

External developers and content teams use this skill to generate avatar, talking-head, lipsync, dubbing, marketing, education, social media, and corporate videos from image, audio, text-to-speech, or video inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow executes a mutable remote installer.

Mitigation: Use a pinned, inspectable CLI download with independent checksum or signature verification before installation.

Risk: The related skill installation examples are optional and unpinned.

Mitigation: Pin related skill installs to known versions before adding them to an agent environment.

Risk: Avatar, voice, and video workflows may involve private biometric or personal media.

Mitigation: Submit media only when provider handling is understood and consent has been obtained from people depicted or recorded.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/ai-avatar-video)
- [inference.sh](https://inference.sh)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline)
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming)
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs infsh CLI workflows for avatar generation, lipsync, text-to-speech chaining, transcription, and dubbing.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
