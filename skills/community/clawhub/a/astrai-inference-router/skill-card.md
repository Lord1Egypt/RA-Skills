## Description: <br>
Route all LLM calls through Astrai for 40%+ cost savings with intelligent routing and privacy controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beee003](https://clawhub.ai/user/beee003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route LLM requests through Astrai for provider selection, failover, budget tracking, and optional region or privacy controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says this skill sends prompts and provider API keys to Astrai. <br>
Mitigation: Install only if you intentionally trust Astrai with both prompts and provider keys; use restricted or low-limit keys, monitor provider billing, and revoke or rotate keys when disabling the skill. <br>
Risk: The security evidence says the documentation understates or contradicts the provider-key and local PII-stripping risk. <br>
Mitigation: Do not rely on stated local PII stripping unless the publisher adds code that performs it before routing; avoid sensitive prompts or verify preprocessing before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beee003/astrai-inference-router) <br>
- [Astrai service](https://as-trai.com) <br>
- [Astrai chat completions endpoint](https://as-trai.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [Routed LLM responses, request configuration, and JSON-like routing status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests through Astrai, forwards configured provider keys in request headers, and can apply region, privacy mode, and daily budget settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
