## Description: <br>
ClawGuard Threat Detector provides real-time behavioral monitoring, attack pattern detection, MITRE ATT&CK mapping, and AI-powered anomaly detection for OpenClaw runtime environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stardreaming](https://clawhub.ai/user/stardreaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to monitor OpenClaw sessions for suspicious commands, sensitive file access, network activity, prompt injection, and attack chains, producing allow, alert, or block guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local monitoring may expose commands, prompts, file paths, and network metadata. <br>
Mitigation: Use the skill only where this monitoring is acceptable, require explicit opt-in, and define retention and redaction controls before deployment. <br>
Risk: Threat details may be forwarded to an undeclared sibling learning module. <br>
Mitigation: Disable or remove the self-improving-safety integration unless that module is explicitly trusted and governed. <br>
Risk: Blocking or remediation behavior can affect normal workflows if detections are inaccurate. <br>
Mitigation: Review detections before enabling automated blocking and keep human approval in the response path for sensitive environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stardreaming/clawguard-detector) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/stardreaming) <br>
- [ClawGuard threat-detect homepage](https://github.com/clawguard/threat-detect) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-style alert examples and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces threat classifications such as BLOCK, ALERT, or ALLOW with severity and confidence where supported.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
