## Description: <br>
End-to-end Volcengine Ark Seedance video generation using ARK_API_KEY and the bundled Node.js runner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iunclear](https://clawhub.ai/user/iunclear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and tool-using agents use this skill to generate and manage Volcengine Ark Seedance video tasks, including text-to-video, image-to-video, polling, downloads, task inspection, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, remote URLs, and selected local media can be sent to Volcengine Ark during generation. <br>
Mitigation: Use only inputs that are approved for Ark processing, and disclose local media uploads before execution. <br>
Risk: Task deletion can remove Ark task records when the delete command is used with a task ID. <br>
Mitigation: Review task IDs carefully before deletion and prefer inspection or listing before destructive task management. <br>
Risk: Generated video and last-frame URLs may expire before assets are saved locally. <br>
Mitigation: Use the run or create-with-wait workflow and download outputs promptly into the workspace output directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iunclear/ark-seedance-video-generation) <br>
- [Ark Video API Notes](references/ark-video-api.md) <br>
- [Video Models](references/video-models.md) <br>
- [Video Models JSON](references/video-models.json) <br>
- [Payload Patterns](references/payload-patterns.md) <br>
- [Ark create video task API sample](https://www.volcengine.com/docs/82379/1520757) <br>
- [LAS Seedance video generation supported model list](https://www.volcengine.com/docs/6492/2165104) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown status report with shell command usage and generated local JSON or media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and ARK_API_KEY; generated request.json is intended to be sanitized before storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
