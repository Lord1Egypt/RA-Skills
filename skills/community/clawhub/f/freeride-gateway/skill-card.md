## Description: <br>
FreeRide Gateway helps agents detect and configure a local OpenAI-compatible gateway that routes chat completion requests across configured free-tier AI providers with failover. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaivpidadi](https://clawhub.ai/user/shaivpidadi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check whether FreeRide is running, point OpenAI-compatible clients at the local gateway, discover available models, and troubleshoot provider or key failover. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-checking guidance can expose provider API keys if full environment variable values are printed. <br>
Mitigation: Use redacted presence checks and avoid commands that print full provider environment variables. <br>
Risk: The skill points to an unpinned remote curl-to-shell installer. <br>
Mitigation: Prefer PyPI or source installation with pinned versions and hashes before running setup commands. <br>
Risk: Telemetry is described as enabled by default. <br>
Mitigation: Review the telemetry disclosure and consider disabling telemetry before first use. <br>
Risk: Bind, auto, and watcher commands can change agent configuration or run background behavior. <br>
Mitigation: Require explicit user approval before running those commands and review the resulting configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaivpidadi/freeride-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/shaivpidadi) <br>
- [FreeRide PyPI project](https://pypi.org/project/freeride-gateway/) <br>
- [FreeRide GitHub repository listed by the skill](https://github.com/Shaivpidadi/FreeRideV3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, bash commands, configuration snippets, and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct agents to inspect local services, environment variables, and provider configuration; credential values should be redacted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
