## Description: <br>
Claw Service Hub provides an OpenClaw service marketplace hub for registering, discovering, calling, pricing, rating, and unregistering services through CLI, WebSocket, and REST workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangboheng](https://clawhub.ai/user/tangboheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run and interact with an OpenClaw service hub for service registration, discovery, invocation, listing, status checks, and unregistering services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change service registry state, including unregistering services or calling registered service methods. <br>
Mitigation: Use scoped operator credentials, verify service identifiers and target methods before destructive or state-changing actions, and require human or runbook approval for production changes. <br>
Risk: Service hub configuration can expose network listeners or write registry data to an unintended storage location. <br>
Mitigation: Set HUB_HOST, HUB_PORT, and STORAGE_PATH deliberately for the deployment environment, restrict network exposure, and keep tokens or credentials out of logs and prompts. <br>


## Reference(s): <br>
- [Claw Service Hub release page](https://clawhub.ai/tangboheng/claw-service-hub) <br>
- [Skill documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with CLI commands, environment settings, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; documented configuration includes HUB_PORT, HUB_HOST, and STORAGE_PATH.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact code) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
