## Description:

CC Video Creation helps an agent create FactSage short-form videos by selecting a story, generating Manim or Ken Burns style animation, producing Edge TTS voiceover, assembling MP4 output, and optionally using the Kling AI web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content operators use this skill to produce FactSage social-video drafts and finished MP4 files from predefined historical story scripts. It provides commands and workflow guidance for local animation, voiceover generation, video assembly, and manual upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration text is sent to Edge TTS for voice generation.

Mitigation: Do not include secrets, private drafts, unpublished business plans, or sensitive personal data in voiceover scripts.

Risk: The scripts use shared temporary frame storage and local FactSage workspace paths during video rendering.

Mitigation: Run the skill in a trusted single-user workspace, review generated files before publishing, and fix the shared temporary frame directory before multi-user use.

Risk: The skill documentation references a published Kling AI account email for manual web UI use.

Mitigation: Use an authorized account controlled by the installer or organization instead of relying on the published email address.

Risk: Generated videos can contain factual or editorial claims from predefined story scripts.

Mitigation: Review video scripts, narration, captions, and final MP4 output before uploading to public platforms.

## Reference(s):

- [CC Video Creation on ClawHub](https://clawhub.ai/northcap-group/skills/cc-video-creation)
- [northcap-group ClawHub publisher profile](https://clawhub.ai/user/northcap-group)
- [Kling AI web UI](https://klingai.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated MP4 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local video, audio, frame, and segment files under the FactSage project workspace; may also provide prompts for manual Kling AI use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
