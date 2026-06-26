## Description: <br>
DataGuard DLP helps OpenClaw agents scan outbound data, detect sensitive patterns, manage domain allowlists, require approval for higher-risk transfers, and record audit events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffcgit](https://clawhub.ai/user/jeffcgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security-conscious operators use DataGuard DLP to reduce accidental credential, PII, and sensitive-data exposure from agent workflows. It is intended for environments where outbound agent actions should be scanned, risk-scored, logged, and sometimes gated on explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes that the skill appears to be a local DLP tool rather than malware, but its security-control claims need careful review before relying on it. <br>
Mitigation: Confirm OpenClaw hook support in the target environment and test in a sandbox that warnings, blocks, approvals, and audit records behave as expected. <br>
Risk: Sensitive local logging and context tracking can persist information about protected files, blocked transfers, override reasons, or false-positive reports. <br>
Mitigation: Restrict permissions on the skill directory, review or clear logs and context files regularly, keep data previews disabled, and avoid entering real secrets in reports or override reasons. <br>
Risk: Emergency override behavior can weaken enforcement if it is misunderstood or used too broadly. <br>
Mitigation: Treat override behavior as a break-glass path, verify it in a sandbox, keep the time window short, and review the audit trail after use. <br>


## Reference(s): <br>
- [DataGuard DLP on ClawHub](https://clawhub.ai/jeffcgit/dataguard-dlp) <br>
- [Skill Instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Runtime Configuration](config/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local audit logs, context records, allowlist or blocklist updates, override records, and false-positive reports when its scripts are run.] <br>

## Skill Version(s): <br>
2.2.0 (source: SKILL.md frontmatter, VERSION.text, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
