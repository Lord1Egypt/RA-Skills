## Description: <br>
Connects agents to the EVEZ AI OpenAI-compatible API for routing LLM calls through EVEZ models with setup examples for API keys, base URLs, and Python usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to configure agents or applications to call EVEZ AI models through an OpenAI-compatible endpoint, including chat, code, fast, and vision model examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key for an external AI service. <br>
Mitigation: Use a dedicated EVEZ API key and keep it in environment variables or a managed secret store. <br>
Risk: Prompts and image URLs are sent to the EVEZ service for processing. <br>
Mitigation: Review the provider's privacy and billing terms and avoid sending secrets or regulated data unless external processing is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-api-gateway) <br>
- [EVEZ API endpoint](https://evez-api2.fly.dev/v1) <br>
- [EVEZ API signup](https://evez-api2.fly.dev/signup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVEZ API key and sends prompts or image URLs to the EVEZ service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
