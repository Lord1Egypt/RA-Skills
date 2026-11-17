## Description:

A Chinese AI video generation skill that helps agents create text-to-video and image-to-video clips with Tongyi Wanxiang Wan2.6 and Kling V2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and agent users can use this skill to turn prompts or image URLs into short AI-generated video clips, poll asynchronous generation tasks, and optionally download the resulting video file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags public image uploads with embedded ImgURL credentials and insufficient scoping or warnings.

Mitigation: Review before installing, use only non-sensitive image files, replace or remove embedded ImgURL credentials, and avoid arbitrary-path uploads until file validation, size limits, workspace restrictions, and explicit confirmation are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dadaniya99/skills/cn-video-gen)
- [Kling AI API Documentation](https://klingai.kuaishou.com/api/docs)
- [Tongyi Wanxiang Video Synthesis API Endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API examples, task status text, video URLs, and optional local MP4 file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous video generation task polling; image-to-video workflows may require uploading a local image to a public image host before generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
