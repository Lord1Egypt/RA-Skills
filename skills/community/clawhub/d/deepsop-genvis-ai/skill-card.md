## Description: <br>
Generates AI images and videos asynchronously through the AI Artist API from text prompts and optional reference media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images or short videos, choose AI Artist models, upload reference media, and return result links or downloads in chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference files, generated links, and uploaded media URLs may be sent to ai.deepsop.com. <br>
Mitigation: Avoid sensitive prompts or private media unless the provider's hosting, retention, and access controls are acceptable. <br>
Risk: Setting FEISHU_WEBHOOK_URL can notify that webhook with prompt text and result links for every run. <br>
Mitigation: Set FEISHU_WEBHOOK_URL only for an intended destination and restrict access to the receiving channel. <br>
Risk: The skill requires a personal AI_ARTIST_TOKEN credential. <br>
Mitigation: Store the token in environment or secret management and do not commit it to shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kukuoai/deepsop-genvis-ai) <br>
- [README](artifact/README.md) <br>
- [AI Artist API reference](artifact/references/api.md) <br>
- [Chat integration guide](artifact/references/chat-integration.md) <br>
- [Feishu integration guide](artifact/references/feishu-integration.md) <br>
- [AI Artist login](https://ai.deepsop.com/login?source=2) <br>
- [AI Artist registration](https://ai.deepsop.com/register?source=2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown links, URL strings, JSON status, and optional downloaded media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Polls asynchronous generation tasks to completion; can optionally send webhook notifications and download media locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
