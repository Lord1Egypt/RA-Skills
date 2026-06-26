## Description: <br>
Query and troubleshoot Fing Local API monitoring agents for local network device inventory, presence, online/offline state, people/presence where supported, and read-only homelab network checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naamah75](https://clawhub.ai/user/naamah75) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, homelab operators, and their agents use this skill to query a trusted local Fing API for network health, device inventory, online/offline state, and supported people or presence diagnostics. It is intended for read-only troubleshooting and summary-first checks of local monitoring agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal sensitive local network inventory, including device names, IP addresses, MAC addresses, and presence information. <br>
Mitigation: Prefer summary output, share detailed device or people data only in the operator's direct context, and avoid proactive disclosure unless it indicates an actionable issue. <br>
Risk: The Fing API key grants access to local network device data and is passed to the local API as a query parameter. <br>
Mitigation: Keep FING_API_KEY private, avoid logging full command lines or URLs containing the key, and connect only to localhost or a trusted local or LAN Fing agent. <br>


## Reference(s): <br>
- [Fing Local API summary](references/api-summary.md) <br>
- [Fing Local API documentation](https://www.fing.com/integrations/local-api/) <br>
- [ClawHub skill page](https://clawhub.ai/naamah75/fing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper produces summarized or raw read-only Fing API responses for devices, people, and health summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
