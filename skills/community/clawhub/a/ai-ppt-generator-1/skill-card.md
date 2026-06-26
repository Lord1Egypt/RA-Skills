## Description: <br>
Generate PPT with Baidu AI and smart template selection based on content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create presentation decks from a topic through Baidu AI, either with a selected template or an automatically chosen template style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PPT topics or supplied content are sent to Baidu's service for presentation generation. <br>
Mitigation: Avoid confidential, regulated, or proprietary material unless organizational policy permits sending it to Baidu. <br>
Risk: The skill requires a Baidu API key for external service access. <br>
Mitigation: Use a dedicated, revocable Baidu API key where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tigertamvip/ai-ppt-generator-1) <br>
- [Baidu Qianfan AI PPT API](https://qianfan.baidubce.com/v2/tools/ai_ppt/) <br>
- [Baidu Qianfan PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status or final PPT URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; generation can take 2-5 minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
