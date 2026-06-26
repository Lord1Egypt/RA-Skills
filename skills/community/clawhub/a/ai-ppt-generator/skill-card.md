## Description: <br>
Generate PPT with Baidu Wenku AI. Smart template selection based on content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ide-rea](https://clawhub.ai/user/ide-rea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate Baidu Wenku AI PowerPoint decks from a topic, optionally choosing a template or letting the skill select a style based on the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PPT topics or supplied content are sent to Baidu for processing and remote deck generation. <br>
Mitigation: Avoid confidential, regulated, or sensitive material unless organizational policy allows that data sharing. <br>
Risk: The skill requires a Baidu API key for remote API calls. <br>
Mitigation: Provide BAIDU_API_KEY only through the environment and rotate or revoke it according to local credential policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ide-rea/ai-ppt-generator) <br>
- [Baidu Qianfan AI PPT API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/) <br>
- [Baidu Qianfan AI PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands; scripts emit JSON progress updates and a final PPT URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; generation may take 2-5 minutes.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
