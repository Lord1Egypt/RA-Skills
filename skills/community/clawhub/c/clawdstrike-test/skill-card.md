## Description: <br>
Security audit and threat model for OpenClaw gateway hosts. Use to verify OpenClaw configuration, exposure, skills/plugins, filesystem hygiene, and to produce an OK/VULNERABLE report with evidence and fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misirov](https://clawhub.ai/user/misirov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect local OpenClaw gateway hosts, collect bounded verification evidence, and produce an actionable OK/VULNERABLE audit report with redacted evidence and safe remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local verification bundle and generated audit report may contain sensitive host, path, configuration, or security posture details. <br>
Mitigation: Review verified-bundle.json before sharing it, keep it out of public or synced folders, and delete it when it is no longer needed. <br>
Risk: Audit collection touches local OpenClaw configuration and runtime evidence. <br>
Mitigation: Use the bundled verified collector and its strict allowlist; apply fixes only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/misirov/clawdstrike-test) <br>
- [Required Checks](references/required-checks.md) <br>
- [Report Format](references/report-format.md) <br>
- [Evidence Template](references/evidence-template.md) <br>
- [Verified Allowlist](references/verified-allowlist.md) <br>
- [Threat Model](references/threat-model.md) <br>
- [Redaction Rules](references/redaction.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, Security analysis] <br>
**Output Format:** [Markdown security report with redacted evidence excerpts and safe remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local verified-bundle.json evidence file through the bundled collector; report evidence should remain redacted and local.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
