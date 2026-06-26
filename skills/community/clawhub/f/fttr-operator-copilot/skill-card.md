## Description: <br>
Connect OpenClaw to the FTTR Copilot operator cloud-control APIs through ConnectRPC for managed-device lookup, alert operations, regional stats, network diagnostics, and real-time FTTR query commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fttrai](https://clawhub.ai/user/fttrai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and agent users use this skill to query FTTRAI-managed devices, alerts, regional statistics, network diagnostics, and authorized real-time FTTR device information through an Operator identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive FTTRAI operator bearer token and can expose operator-scoped device, alert, and network data. <br>
Mitigation: Install it only for agents that should access FTTRAI operator data, use a least-privileged token, and store the token only in the required environment variable. <br>
Risk: The alert tool can mark alerts as read, which changes FTTRAI state. <br>
Mitigation: Require explicit user confirmation before calling mark_alerts_as_read. <br>
Risk: Real-time device query tools can issue Operator-authorized commands and may return pending sequence identifiers. <br>
Mitigation: Confirm the target device identifier and user intent before issuing real-time query commands, and report pending sequence identifiers clearly. <br>
Risk: Changing the RPC endpoint can route operator credentials and requests to an unintended service. <br>
Mitigation: Keep the default trusted HTTPS endpoint unless the replacement endpoint is controlled and approved. <br>


## Reference(s): <br>
- [FTTR Operator Copilot ClawHub listing](https://clawhub.ai/fttrai/fttr-operator-copilot) <br>
- [fttrai publisher profile](https://clawhub.ai/user/fttrai) <br>
- [README](README.md) <br>
- [Usage examples](examples/usage.md) <br>
- [Default FTTRAI Operator ConnectRPC endpoint](https://fms-main.fttrai.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON CLI responses with concise operator-facing text or Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an FTTRAI operator bearer token; some tools can mark alerts as read or send authorized real-time device query commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
