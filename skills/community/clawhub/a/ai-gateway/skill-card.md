## Description: <br>
Access 340+ AI models through the Agnic AI Gateway for chat, image generation, and model listing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route AI chat, image generation, and model-discovery requests through Agnic's gateway, including calls to OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and other providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI prompts and image requests are sent to Agnic and downstream AI providers, which may expose sensitive or regulated information. <br>
Mitigation: Avoid sending secrets or regulated data, and review provider suitability before using the skill with sensitive prompts. <br>
Risk: Model calls can spend wallet funds from the user's USDC balance. <br>
Mitigation: Use a low-balance wallet or scoped token where possible, prefer free models for testing, and monitor spending. <br>
Risk: The skill can rely on sensitive credentials such as AGNIC_TOKEN for headless authentication. <br>
Mitigation: Store tokens in the environment or a secret manager, scope them where possible, and avoid pasting credentials into prompts or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/ai-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/agnicpay-prog) <br>
- [AI Gateway Models & Options Reference](reference/models-and-options.md) <br>
- [Agnic app](https://app.agnic.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce image files when the image command is used with an output path.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
