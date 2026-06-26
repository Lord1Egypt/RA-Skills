## Description: <br>
ClawBrain Boost configures OpenClaw to use ClawBrain models with memory, data-fidelity checks, automatic fault tolerance, and writing assistance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelfeng](https://clawhub.ai/user/michaelfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to route default model traffic to ClawBrain, choose performance tiers, and apply memory, data-fidelity, and response-quality behaviors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes OpenClaw model traffic through a third-party provider. <br>
Mitigation: Install only when that provider routing is intended, and review the provider's privacy and billing terms before use. <br>
Risk: The skill requires a provider API key. <br>
Mitigation: Protect the API key, avoid sharing it in prompts or logs, and rotate it if exposed. <br>
Risk: The skill advertises automatic long-term memory without detailed privacy, consent, or deletion controls in the artifact. <br>
Mitigation: Confirm controls to inspect, disable, or delete stored memory before relying on memory features. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/michaelfeng/clawbrain-boost) <br>
- [ClawBrain homepage](https://clawbrain.dev) <br>
- [ClawBrain dashboard](https://clawbrain.dev/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve third-party provider routing and an API key.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
