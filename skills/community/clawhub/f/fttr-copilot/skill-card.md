## Description: <br>
Connect OpenClaw to the FTTR Copilot cloud-control system through ConnectRPC for device lookup, alert triage, network diagnostics, and FTTR operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fttrai](https://clawhub.ai/user/fttrai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and support engineers use this skill to query authenticated FTTR Copilot device data, triage alerts, inspect network topology and station metrics, and run customer-authorized FTTR diagnostics or real-time device commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive customer device data and bearer-token access to FTTRAI APIs. <br>
Mitigation: Install only from the trusted publisher, keep FTTRAI_AUTH_TOKEN secret, and avoid sharing logs or screenshots that contain tool output. <br>
Risk: A misconfigured FTTRAI_RPC_URL could send requests or credentials to an untrusted endpoint. <br>
Mitigation: Keep FTTRAI_RPC_URL on a trusted HTTPS endpoint and review any endpoint override before use. <br>
Risk: Alias updates and real-time commands can affect a specific customer device. <br>
Mitigation: Confirm the exact device identifier, MAC address, or alias before running update_device_alias or real-time command tools. <br>


## Reference(s): <br>
- [FTTR Copilot ClawHub release page](https://clawhub.ai/fttrai/fttr-copilot) <br>
- [FTTRAI ConnectRPC endpoint](https://fms-main.fttrai.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON CLI examples and structured JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an FTTRAI bearer token and can return customer device data, diagnostics, alerts, topology, metrics, suggestions, traces, errors, and command sequence identifiers.] <br>

## Skill Version(s): <br>
0.1.6 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
