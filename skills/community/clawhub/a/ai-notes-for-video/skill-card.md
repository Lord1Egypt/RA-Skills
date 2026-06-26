## Description: <br>
Baidu Netdisk AIVideoNotes helps agents submit local or online videos to Baidu's AI video note service and retrieve transcript, outline, and image-text notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ide-rea](https://clawhub.ai/user/ide-rea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Baidu AI video-note tasks, poll task status, and return generated notes for education videos, meetings, short-form content analysis, and key information extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos, accessible video URLs, task IDs, and generated notes are sent to Baidu or the configured OpenClaw/Baidu proxy environment. <br>
Mitigation: Use the skill only for content appropriate for that processing path, and avoid confidential, regulated, or proprietary recordings unless Baidu's handling terms meet the user's requirements. <br>
Risk: The skill requires a Baidu API key. <br>
Mitigation: Use a dedicated or least-privilege key where possible and keep it in environment configuration rather than command history or source files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ide-rea/ai-notes-for-video) <br>
- [Baidu Qianfan API Base](https://qianfan.baidubce.com/v2) <br>
- [Baidu AppBuilder BOS Upload Endpoint](https://appbuilder.baidu.com/v2/tools/bos/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON-formatted task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; video-note generation is asynchronous and may require polling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
