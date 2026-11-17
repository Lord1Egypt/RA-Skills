## Description:

ClawGuard Threat Detector provides real-time behavioral monitoring, attack pattern detection, MITRE ATT&CK mapping, and AI-powered anomaly detection for OpenClaw runtime environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stardreaming](https://clawhub.ai/user/stardreaming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to inspect OpenClaw commands, file access, network requests, and prompts for suspicious runtime behavior. The skill returns allow, alert, or block guidance with threat details for detected command, file, network, prompt-injection, and attack-chain patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can analyze commands, file paths, URLs, and prompts, which may expose sensitive operational context to detection logic.

Mitigation: Install only in environments where this monitoring scope is acceptable, and review access to logs, command history, network data, and file paths before deployment.

Risk: Detected threat details can be sent to an automatic learning integration that may persist future safety rules without clear user approval.

Mitigation: Review or disable the automatic learning integration before allowing detections to update future safety rules.

Risk: The skill is designed to reduce runtime security risk but cannot guarantee complete protection.

Mitigation: Use it as a monitoring and decision-support layer, keep least-privilege controls in place, and review alert, block, and allow decisions before relying on them for enforcement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stardreaming/skills/clawguard-detector)
- [Publisher Profile](https://clawhub.ai/user/stardreaming)
- [Project Homepage from ClawDIS Metadata](https://github.com/clawguard/threat-detect)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with JSON-style alert examples and command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Threat analysis may include action labels such as ALLOW, ALERT, or BLOCK, confidence values, severity, MITRE technique IDs, and remediation guidance.]

## Skill Version(s):

3.0.0 (source: server release evidence, package.json, and _meta.json; artifact SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
