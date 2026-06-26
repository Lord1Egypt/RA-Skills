## Description: <br>
Generate PPT with Baidu Wenku AI. Smart template selection based on content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate presentation decks from a topic through Baidu Wenku AI, either with a selected template or with automatic template selection based on the topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation topics, optional supplied content, and the Baidu API key are sent to Baidu's API. <br>
Mitigation: Use the skill only when that third-party processing is acceptable, and avoid sensitive, regulated, or proprietary material unless approved for Baidu processing. <br>
Risk: The local scripts require the Python requests package and a BAIDU_API_KEY environment variable. <br>
Mitigation: Confirm the runtime has python3, requests, and BAIDU_API_KEY configured before running the generation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuliyuan2026/ai-ppt-generator-local) <br>
- [Baidu AI PPT API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/) <br>
- [Baidu AI PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Baidu API status messages and, on successful completion, a PPT download URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
