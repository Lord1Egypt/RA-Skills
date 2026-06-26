## Description: <br>
China Vision analyzes images with Qwen2.5-VL-72B via SiliconFlow for scene analysis, object recognition, chart interpretation, food identification, and detailed descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to submit local images or image URLs with prompts for multimodal image understanding, including descriptions, scene analysis, chart interpretation, product recognition, and food identification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, image URLs, and prompts are sent to SiliconFlow/Qwen for processing. <br>
Mitigation: Use only images and prompts that are acceptable under SiliconFlow data handling terms; avoid sensitive personal, business, medical, financial, or regulated content unless those terms are acceptable. <br>
Risk: The model is billed by token usage and can consume paid API credits. <br>
Mitigation: Use a limited API key, spending controls, or other account-level limits for routine use. <br>
Risk: The skill requires a sensitive SiliconFlow API credential. <br>
Mitigation: Store SILICONFLOW_API_KEY in the agent environment and avoid pasting or committing the key in prompts, scripts, or logs. <br>


## Reference(s): <br>
- [ClawHub release page for china-vision](https://clawhub.ai/tobewin/china-vision) <br>
- [SiliconFlow API endpoint used by the skill](https://api.siliconflow.cn/v1/chat/completions) <br>
- [SiliconFlow console for API keys](https://cloud.siliconflow.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text or Markdown guidance with bash command examples and image-analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SILICONFLOW_API_KEY; may consume paid SiliconFlow tokens] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
