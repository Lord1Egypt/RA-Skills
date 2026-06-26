## Description: <br>
Ai Ppt Generate.Skip2 helps agents create PowerPoint outlines and downloadable presentation files through Baidu's AI PPT APIs using user topics, themes, templates, and optional resource URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lulu-owo](https://clawhub.ai/user/lulu-owo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query presentation themes, generate an editable markdown outline, and request a downloadable PPT file from Baidu. It is suited for agents that need to assemble presentation drafts from a topic and optional document or image resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation topics, outlines, and linked documents or templates may be sent to Baidu. <br>
Mitigation: Use only approved material and avoid confidential inputs unless sharing them with Baidu is permitted. <br>
Risk: The skill requires a BAIDU_API_KEY for API calls. <br>
Mitigation: Provide the key through the runtime environment and avoid committing or logging credentials. <br>
Risk: Generated outlines or PPT content may require review before use. <br>
Mitigation: Review generated outlines and downloaded presentation files for accuracy, suitability, and policy compliance before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lulu-owo/ai-ppt-generate-skip2) <br>
- [Publisher profile](https://clawhub.ai/user/lulu-owo) <br>
- [Baidu AI PPT theme query endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme) <br>
- [Baidu AI PPT outline generation endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/generate_outline) <br>
- [Baidu AI PPT presentation generation endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/generate_ppt_by_outline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses, markdown outlines, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a downloadable PPT file URL after successful outline and presentation generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
