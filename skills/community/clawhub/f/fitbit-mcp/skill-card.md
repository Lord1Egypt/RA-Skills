## Description: <br>
Connect an MCP-compatible agent to local Fitbit activity, sleep, heart-rate, HRV, SpO2, breathing, weight, food, and water data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users of MCP-compatible agents use this skill to install, configure, verify, and troubleshoot Fitbit MCP while preserving explicit consent and avoiding exposure of private health data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth tokens and may expose sensitive health and wellness data to an enabled agent. <br>
Mitigation: Review Fitbit OAuth scopes before use, keep user consent explicit, avoid printing tokens or private data, and confirm trust in the linked repository and package before installation. <br>
Risk: Live provider actions or writes could affect user data if run without review. <br>
Mitigation: Use connection_status, manifest, doctor, privacy_audit, and dry-run surfaces first, and require explicit approval before write operations or live provider actions. <br>


## Reference(s): <br>
- [Fitbit MCP ClawHub page](https://clawhub.ai/davidmosiah/fitbit-mcp) <br>
- [Fitbit MCP repository](https://github.com/davidmosiah/fitbitmcp) <br>
- [Fitbit MCP docs](https://wellness.delx.ai/connectors/fitbit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup, authentication, privacy-audit, dry-run, and troubleshooting guidance for MCP-compatible agents.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
