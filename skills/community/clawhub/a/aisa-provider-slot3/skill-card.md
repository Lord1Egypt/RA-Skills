## Description: <br>
Configure AIsa as an OpenAI-compatible provider endpoint for OpenClaw and compatible runtimes, including API key setup, endpoint configuration, model selection, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure AIsa as a model provider, set AISA_API_KEY, point compatible runtimes at the AIsa API endpoint, choose model IDs, and troubleshoot provider behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive AIsa API key. <br>
Mitigation: Use a dedicated, revocable key and avoid exposing real secrets in shell history, logs, screenshots, or shared configuration. <br>
Risk: Model requests are routed to an external provider endpoint. <br>
Mitigation: Confirm AIsa's current privacy, retention, routing, and downstream-provider terms before sending sensitive or regulated data. <br>
Risk: Pricing, model availability, quotas, and model-specific constraints can change. <br>
Mitigation: Re-check AIsa's current pricing page, model catalog, account limits, and model-specific settings before production use. <br>
Risk: Runtime defaults or fallback chains could route traffic through unintended models. <br>
Mitigation: Review the final provider configuration, default model, and fallback settings after setup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aisadocs/aisa-provider-slot3) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa API reference](https://aisa.one/docs/api-reference) <br>
- [AIsa pricing](https://marketplace.aisa.one/pricing) <br>
- [AIsa Provider Configuration Examples](references/config-examples.md) <br>
- [AIsa Pricing Notes](references/pricing.md) <br>
- [AIsa Chinese Guide](references/guide-zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided AISA_API_KEY and routes model requests to the AIsa OpenAI-compatible API endpoint.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
