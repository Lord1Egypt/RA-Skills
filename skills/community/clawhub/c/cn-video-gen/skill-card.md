## Description: <br>
Generates short AI video clips from text prompts or image inputs using Tongyi Wanxiang workflows and Kling V2 guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, operators, and developers use this skill to prepare text-to-video or image-to-video requests, poll generation tasks, and retrieve generated video outputs from supported Chinese video-generation providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user media to configured video providers, a public image-hosting service, and Feishu. <br>
Mitigation: Use only media approved for those services and add an explicit confirmation step before upload, sharing, or download actions. <br>
Risk: The release includes an embedded default upload token for the image-hosting workflow. <br>
Mitigation: Remove or rotate the embedded token and require users to provide their own credentials through environment variables. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dadaniya99/cn-video-gen) <br>
- [Tongyi Wanxiang video generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis) <br>
- [Kling API documentation](https://klingai.kuaishou.com/api/docs) <br>
- [ImgURL upload API](https://www.imgurl.org/api/v2/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/API parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce provider task IDs, video URLs, and optionally downloaded MP4 files when credentials and output paths are configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
