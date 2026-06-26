## Description: <br>
AIPing Media generates images and videos with AIPing, downloads results to /tmp, and can send selected media through Feishu with a CDN link fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoruilee](https://clawhub.ai/user/haoruilee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate AI images or short videos from prompts, save the media locally, and deliver it to a Feishu user or chat when credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated media are sent to AIPing, and selected media can be sent to Feishu. <br>
Mitigation: Use the skill only when those services are approved for the content being processed. <br>
Risk: Misconfigured Feishu credentials or recipient IDs can send media to the wrong destination or fail delivery. <br>
Mitigation: Use least-privilege Feishu app permissions and verify the open_id or chat_id before sending. <br>
Risk: Generated files may remain in /tmp after the workflow finishes. <br>
Mitigation: Clear sensitive generated image or video files from /tmp when they are no longer needed. <br>


## Reference(s): <br>
- [AIPing Media on ClawHub](https://clawhub.ai/haoruilee/aiping-media) <br>
- [AIPing Supported Models](references/models.md) <br>
- [AIPing API](https://aiping.cn/api/v1) <br>
- [Feishu Open Platform API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON responses with local file paths or CDN URLs, plus downloaded image/video files and optional Feishu messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is stored under /tmp; Feishu delivery requires AIPING_API_KEY, FEISHU_APP_ID, and FEISHU_APP_SECRET.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
