## Description: <br>
Routes LLM calls through a Vultr oracle instance with EVEZ-branded model endpoints and EVEZ-OS circuit integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run an OpenAI-compatible bridge that maps EVEZ model names to Vultr inference models and exposes local endpoints for model queries, circuit health, debate, knowledge, forge, scanner, and dashboard workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge exposes unauthenticated network endpoints that can trigger local services and mutate local state. <br>
Mitigation: Bind the service to a trusted interface such as localhost, place it behind authentication, and avoid exposing port 9110 to untrusted networks. <br>
Risk: The skill requires sensitive credentials for Vultr inference access. <br>
Mitigation: Use a limited Vultr API key, store it in environment variables, rotate it as needed, and avoid sending secrets in prompts. <br>
Risk: Bridge requests can forward prompts or commands to local EVEZ-OS services. <br>
Mitigation: Run only the local services you intend to expose and remove or protect mutation endpoints before broader deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-oracle-bridge) <br>
- [Vultr inference API endpoint](https://api.vultrinference.com/v1) <br>
- [EVEZ API fallback endpoint](https://evez-api2.fly.dev/v1) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Python service code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a Vultr API key, and local EVEZ-OS services for the bridge endpoints to function.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
