## Description: <br>
AI PPT generate helps an agent use Baidu/Qianfan PPT APIs to query presentation themes, generate markdown outlines, and produce downloadable PPT file URLs from user topics or resource links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiduQianfanGroup](https://clawhub.ai/user/baiduQianfanGroup) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill through an OpenClaw agent to turn a topic, optional resource URL, and selected Baidu PPT theme/template into a generated outline and final PPT download URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PPT topics, generated outlines, and referenced document or template URLs are sent to Baidu/Qianfan. <br>
Mitigation: Avoid confidential or regulated documents unless approved by the user's organization. <br>
Risk: The skill requires a Baidu API key for external API calls. <br>
Mitigation: Use a dedicated Baidu API key where possible and keep it out of prompts, logs, and shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baiduQianfanGroup/ai-ppt-generate) <br>
- [Baidu Qianfan PPT theme API](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme) <br>
- [Baidu Qianfan PPT outline API](https://qianfan.baidubce.com/v2/tools/ai_ppt/generate_outline) <br>
- [Baidu Qianfan PPT generation API](https://qianfan.baidubce.com/v2/tools/ai_ppt/generate_ppt_by_outline) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [JSON responses and markdown outline content from Python command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY; outline and PPT generation responses may stream as JSON event data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-02-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
