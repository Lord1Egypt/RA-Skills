## Description: <br>
Azure Gateway Cli helps agents configure and operate a local Azure OpenAI gateway with multi-endpoint routing, load balancing, failover, request caching, cost tracking, and tenant isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to prepare gateway configuration, startup commands, health checks, and operational guidance for Azure OpenAI proxy deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes inconsistent purpose text unrelated to Azure OpenAI gateway work. <br>
Mitigation: Use it only for Azure OpenAI gateway tasks and avoid the SEO and grading-schema sections. <br>
Risk: Gateway configuration can expose credentials, cached prompts, or tenant data if handled loosely. <br>
Mitigation: Keep API keys in environment variables and disable or tightly scope caching for sensitive prompts. <br>
Risk: The optional systemd setup can create a persistent local gateway service. <br>
Mitigation: Enable the service only when persistent startup is intended and document how to stop and remove it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-gateway-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service setup, health-check commands, cache configuration, and operational review guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
