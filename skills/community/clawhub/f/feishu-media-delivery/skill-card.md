## Description: <br>
Feishu Media Delivery helps agents send existing local images and MP4 videos to Feishu/Lark users using the correct image and media message flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhy2015](https://clawhub.ai/user/zhy2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and multimodal agents use this skill after generating an image or video locally, when the result must be delivered to a Feishu/Lark user or chat without using the wrong message type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials are required to upload and send media. <br>
Mitigation: Protect the app secret, keep Feishu app permissions narrowly scoped, and avoid exposing credential values in prompts, logs, or shared files. <br>
Risk: The scripts send user-supplied local files to a recipient open_id. <br>
Mitigation: Verify the recipient open_id and local file path before execution, and confirm delivery using the returned Feishu response rather than local process success alone. <br>
Risk: Dependency behavior can change if package versions are resolved differently. <br>
Mitigation: Install with the bundled lockfile and review dependency updates before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhy2015/feishu-media-delivery) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files, Feishu app credentials, and recipient open_id values; successful delivery should be confirmed from Feishu API responses.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
