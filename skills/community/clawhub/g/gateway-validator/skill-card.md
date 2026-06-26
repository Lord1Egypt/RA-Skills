## Description: <br>
Validate OpenClaw gateway configuration changes before applying them to production by testing changes on an isolated gateway when possible or checking provider connectivity directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loopintoai](https://clawhub.ai/user/loopintoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to validate OpenClaw gateway model, provider, API key, and gateway setting changes before applying them to a production configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use live provider API keys during validation. <br>
Mitigation: Use test or least-privileged API keys where possible and confirm before any live provider test. <br>
Risk: The skill can overwrite OpenClaw gateway configuration and attempt a gateway restart. <br>
Mitigation: Review the exact configuration diff first, keep the generated backup, and require confirmation before apply or restart actions. <br>
Risk: A configured baseUrl could direct validation traffic to an untrusted endpoint. <br>
Mitigation: Verify every configured baseUrl is trusted before running provider or gateway checks. <br>
Risk: Gateway startup checks may not prove completions work end to end. <br>
Mitigation: Run an actual completion validation before treating a gateway change as production-ready. <br>


## Reference(s): <br>
- [Gateway Validator on ClawHub](https://clawhub.ai/loopintoai/gateway-validator) <br>
- [Publisher profile](https://clawhub.ai/user/loopintoai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with validation results, command suggestions, and configuration change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live provider API checks and gateway restart commands when invoked by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
