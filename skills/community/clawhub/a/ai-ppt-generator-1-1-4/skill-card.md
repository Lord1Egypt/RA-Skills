## Description: <br>
Generate PowerPoint presentations with Baidu AI and smart template selection based on content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zou-cc](https://clawhub.ai/user/zou-cc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate PowerPoint presentations from a topic, optionally choosing a template or allowing the script to select one automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation topics and content are sent to Baidu AI, and generated presentations may be hosted by Baidu. <br>
Mitigation: Use a dedicated Baidu API key where possible and avoid submitting secrets, regulated data, private documents, or confidential business material unless Baidu processing and hosted output are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zou-cc/ai-ppt-generator-1-1-4) <br>
- [Baidu Qianfan AI PPT API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output from the generation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; generation may take 2-5 minutes and returns a hosted PPT URL when complete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
