## Description: <br>
商业化AI图片生成助手。40+场景模板, 30+风格词典, 智能意图识别, 结构化Prompt, 三引擎智能路由 (Wanx/Seedream4/Seedream5)。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yh22e](https://clawhub.ai/user/yh22e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language image requests into structured prompts, route them to configured Wanx or Seedream image providers, and return generated image links for business, social, product, and creative assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and any business, branding, or personal design details may be sent to configured external image providers, and to DeepSeek when LLM intent parsing is enabled. <br>
Mitigation: Configure only the provider keys intended for use and avoid placing secrets or sensitive details in prompts. <br>
Risk: Generated image links are returned by provider services and may point to provider-hosted output URLs. <br>
Mitigation: Open or save returned image URLs only when the provider output is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yh22e/beauty-image) <br>
- [Project homepage](https://github.com/xyva-yuangui/beauty-image) <br>
- [DashScope API keys](https://dashscope.console.aliyun.com/apiKey) <br>
- [Volcengine Ark API keys](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) <br>
- [DeepSeek API keys](https://platform.deepseek.com/api_keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and MEDIA_URL image links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured provider API keys; generated image URLs may be time-limited according to artifact documentation.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
