## Description:

Routes an agent to Chanjing credential management, TTS, voice cloning, digital-human video, lip-sync, text-to-image/video, custom digital-human training, one-click video composition, and cartoon video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binkes](https://clawhub.ai/user/binkes)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to route Chanjing media creation requests into the appropriate product or orchestration workflow, including speech generation, voice cloning, digital-human videos, lip-sync, AI image/video generation, and composed short-form videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Chanjing account credentials and may exchange them for short-lived access tokens.

Mitigation: Provide credentials through the documented environment variables or local credential path, avoid pasting secret keys into chat or command-line history, and rotate credentials if exposed.

Risk: Media workflows can upload or download user media through Chanjing services and may incur service costs.

Mitigation: Review generated workflow inputs before rendering, confirm downloads before saving files locally, and keep CHANJING_API_BASE pointed at the official Chanjing endpoint.

Risk: Video composition workflows may invoke ffmpeg or ffprobe and write media artifacts to output or work directories.

Mitigation: Run the skill in a controlled workspace, set explicit output directories for media jobs, and review generated files before sharing or committing them.

## Reference(s):

- [Chanjing Documentation](https://doc.chanjing.cc)
- [ClawHub Skill Page](https://clawhub.ai/binkes/skills/chanjing-content-creation-skill)
- [Top-Level Runtime Contract](references/top-level-runtime-contract.md)
- [Orchestration Contract](orchestration/orchestration-contract.md)
- [One-Click Workflow Schema](orchestration/chanjing-one-click-video-creation/references/workflow-json-schema.md)
- [Chanjing AI Creation Reference](products/chanjing-ai-creation/reference.md)
- [Chanjing Video Compose Reference](products/chanjing-video-compose/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON task outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return remote media URLs or local file paths when Chanjing workflows complete.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
