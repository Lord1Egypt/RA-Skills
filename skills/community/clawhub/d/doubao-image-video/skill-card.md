## Description: <br>
Doubao Image Video helps agents generate Doubao images and videos, query asynchronous video tasks, wait for completion, and optionally download finished video files through Volcengine Ark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[156554395](https://clawhub.ai/user/156554395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to generate Doubao images, start text-to-video or image-to-video jobs, check task status, and retrieve completed videos with a configured Volcengine Ark API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced image URLs are sent to Volcengine Ark for generation. <br>
Mitigation: Use the skill only with data appropriate for that service and configure a dedicated or limited API key. <br>
Risk: Media generation and polling may incur provider usage costs. <br>
Mitigation: Monitor Volcengine Ark usage and choose endpoint, model, duration, resolution, and polling settings intentionally. <br>
Risk: The optional video download can write a file to the local workspace. <br>
Mitigation: Provide an intentional download path and avoid paths that could overwrite important files. <br>


## Reference(s): <br>
- [API Notes](references/api-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/156554395/doubao-image-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download a completed video file when the wait command is used with an explicit output path.] <br>

## Skill Version(s): <br>
0.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
