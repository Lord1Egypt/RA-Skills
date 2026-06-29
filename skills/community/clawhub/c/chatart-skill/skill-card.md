## Description: <br>
ChatArt helps an agent generate videos, create images from text prompts, edit images, and replace characters in videos from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chatart-ai](https://clawhub.ai/user/chatart-ai) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and developers use ChatArt to create or edit images and videos, replace video characters, check credits, and retrieve generated media through an authenticated ChatArt account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles account credentials, device identity, uploads, and remote media fetching. <br>
Mitigation: Review before installing, use only media approved for ChatArt processing, avoid internal or private URLs, and prefer a patched version that documents uploads clearly. <br>
Risk: Login or account details may appear in agent logs until debug output is removed. <br>
Mitigation: Use isolated credentials, redact auth responses and logs, and prefer a patched version that removes or masks sensitive debug output. <br>
Risk: Account switching and logout behavior may confuse local credential deletion with remote device unbinding. <br>
Mitigation: Review authentication behavior before deployment and use a version that separates local logout from remote device unbind. <br>
Risk: Dependency versions are not fully pinned. <br>
Mitigation: Pin and review dependency versions before production deployment. <br>


## Reference(s): <br>
- [ChatArt Skill Page](https://clawhub.ai/chatart-ai/skills/chatart-skill) <br>
- [ChatArt](https://www.chatartpro.com) <br>
- [Auth Module](references/auth.md) <br>
- [Video Generation Module](references/video_gen.md) <br>
- [AI Image Module](references/ai_image.md) <br>
- [Character Replace Module](references/video_mimic.md) <br>
- [User Module](references/user.md) <br>
- [Error Handling Guide](references/error_handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated media result links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit ChatArt generation tasks, poll for completion, upload approved local media, and return generated image or video links.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
