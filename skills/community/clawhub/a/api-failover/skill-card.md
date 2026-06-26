## Description: <br>
Detect AI API/provider/model failures and route requests to healthy fallback providers or downgraded models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqh2333](https://clawhub.ai/user/zqh2333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add AI API failover, health checks, retry policy, circuit breakers, downgrade routing, and local OpenAI-compatible proxy behavior around configured model providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read provider configuration and inherited credentials while running a local API proxy. <br>
Mitigation: Install only when that behavior is intended, protect environment files and state paths, and review provider configuration before use. <br>
Risk: Prompts may be sent to configured fallback providers during failover or downgrade routing. <br>
Mitigation: Review the configured provider order and avoid sensitive workloads unless those fallback providers are approved to receive the data. <br>
Risk: Binding the proxy beyond localhost can expose the local API entrypoint without the protections expected for a network service. <br>
Mitigation: Keep the proxy bound to localhost unless authentication and network controls are added. <br>


## Reference(s): <br>
- [API Failover ClawHub Release](https://clawhub.ai/zqh2333/api-failover) <br>
- [Publisher Profile](https://clawhub.ai/user/zqh2333) <br>
- [Configuration Example](references/config-example.yaml) <br>
- [Real-World Configuration Example](references/config-realworld-example.yaml) <br>
- [Production Configuration Template](references/config-production.yaml) <br>
- [Activation Checklist](references/activation-checklist.md) <br>
- [Test Scenarios](references/test-scenarios.md) <br>
- [Real-World Setup Notes](references/realworld-notes.md) <br>
- [Delivery Summary](references/delivery-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples, Python scripts, shell commands, and JSON proxy responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local configuration, routing state, and a localhost OpenAI-compatible proxy when the user runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
