## Description: <br>
Cryptographic memory for AI agents with QSEAL tamper-evidence, zero-config demo mode, and scroll-native YAML storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdvegas21](https://clawhub.ai/user/sdvegas21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use ClawSeal to give agents persistent, tamper-evident memory for preferences, facts, insights, decisions, and general notes across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an always-on local memory service that stores long-term agent memories. <br>
Mitigation: Install only when persistent local memory is acceptable, and confirm how to stop, disable, and remove the launchd or systemd service. <br>
Risk: The local service has weak access controls and broad CORS behavior in the submitted artifact. <br>
Mitigation: Restrict or remove broad CORS and add authentication or a local token before real use. <br>
Risk: Stored memories may contain sensitive or regulated information. <br>
Mitigation: Avoid storing secrets or regulated personal data, and review retained memories before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdvegas21/clawseal) <br>
- [Skill API documentation](artifact/SKILL.md) <br>
- [OpenClaw integration guide](artifact/OPENCLAW_INTEGRATION.md) <br>
- [Demo conversation](artifact/demo_conversation.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with curl examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and retrieves local YAML-backed memory records through a local HTTP service.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
