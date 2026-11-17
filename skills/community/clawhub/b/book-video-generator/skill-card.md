## Description:

Generates a three-minute book explainer video from a book title and author, including the review script, storyboard images, TTS narration, subtitles, cover art, and MP4 composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjun198711](https://clawhub.ai/user/chenjun198711)

### License/Terms of Use:

MIT

## Use Case:

Content creators and agent users use this skill to turn a book title and author into a short book explainer video with generated copy, illustrations, narration, subtitles, and a final MP4 file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install Python packages automatically during execution, and those dependencies are not pinned.

Mitigation: Run the skill in a dedicated virtual environment and pin or review dependencies before production use.

Risk: The workflow can send book prompts, generated text, images, or speech requests to external search, image, and TTS services.

Mitigation: Use approved providers and API keys, and avoid sending sensitive or restricted content to external services.

Risk: The bundled original workflow reference includes hard-coded third-party account ID values.

Mitigation: Review or remove references/workflow-original.yaml before reuse, or replace embedded account IDs with the user's own account values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenjun198711/skills/book-video-generator)
- [Prompts Reference](references/prompts.md)
- [Cross-Platform Guide](references/CROSS_PLATFORM.md)
- [Original Workflow Reference](references/workflow-original.yaml)
- [Optional Audio Assets](assets/README.md)
- [Online Demo](https://chenjun198711.github.io/book-video-generator/)
- [Agent Skills Open Standard](https://agentskills.io)
- [Volcengine Ark Console](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement)
- [Volcengine Speech Console](https://console.volcengine.com/speech/new)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON manifests, generated media assets, subtitles, and MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces intermediate images, audio, cover art, subtitle files, and a final MP4 under an output directory.]

## Skill Version(s):

2.8.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
