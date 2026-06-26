## Description: <br>
Generate PPT with Baidu AI. Smart template selection based on content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binbin](https://clawhub.ai/user/binbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate slide decks from a topic, either by choosing a Baidu AI presentation template or by letting the skill select a template category automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation topics and optional source content are sent to Baidu AI during generation. <br>
Mitigation: Avoid confidential, regulated, or proprietary material unless that use is approved for the deployment environment. <br>
Risk: The skill requires a Baidu API key to call external presentation-generation APIs. <br>
Mitigation: Provide BAIDU_API_KEY through the agent environment or an approved secret store, and do not place the key in prompts, logs, or checked-in files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binbin/ai-ppt-generator-1-1-3) <br>
- [Baidu AI PPT API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/) <br>
- [Baidu AI PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON generation status or final PPT URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY; PPT generation may take 2-5 minutes and can return a Baidu-hosted PPT URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 1.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
