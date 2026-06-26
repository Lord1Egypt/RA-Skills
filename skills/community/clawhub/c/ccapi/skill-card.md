## Description: <br>
Use CCAPI as an OpenAI-compatible unified API gateway for text, image, video, and audio generation across multiple AI providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[littleblackone](https://clawhub.ai/user/littleblackone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when integrating CCAPI into applications, changing OpenAI SDK configuration to call a single gateway for multiple model providers and modalities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CCAPI API keys could be exposed if copied into shared code or logs. <br>
Mitigation: Store keys in a secret manager or environment variable and avoid hardcoding them in examples, repositories, or shared notebooks. <br>
Risk: Prompts, files, or generated media may be sent through a third-party gateway and routed to provider services. <br>
Mitigation: Review CCAPI's privacy, routing, and provider terms before sending sensitive or regulated data. <br>
Risk: Provider routing and pay-per-use pricing can create unexpected model behavior or costs. <br>
Mitigation: Review the current model list and pricing, use explicit provider/model IDs, and apply normal spend controls before production use. <br>


## Reference(s): <br>
- [CCAPI documentation](https://docs.ccapi.ai) <br>
- [CCAPI model showcase](https://ccapi.ai/models) <br>
- [CCAPI pricing](https://ccapi.ai/pricing) <br>
- [CCAPI dashboard and API keys](https://ccapi.ai/dashboard) <br>
- [ClawHub skill page](https://clawhub.ai/littleblackone/ccapi) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/littleblackone) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, TypeScript, JSON, and cURL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces integration guidance and example API calls; it does not execute commands itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
