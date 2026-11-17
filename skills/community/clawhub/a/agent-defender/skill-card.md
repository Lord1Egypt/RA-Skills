## Description:

Agent Defender is an AI agent security protection skill for static scanning, runtime protection, and DLP checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan AI skills or source files, monitor local agent behavior, and check or mask sensitive data before execution or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes background automation that can perform recurring code execution or rule mutation.

Mitigation: Review the skill before installing and do not enable daemon, cron, or systemd workflows unless their behavior is understood.

Risk: Maintenance workflows and backup restoration can be risky when fed untrusted archives.

Mitigation: Avoid restoring backup archives from untrusted sources and review backup contents before use.

Risk: Scanner whitelist logic can mark malicious content as safe.

Mitigation: Use this scanner as one defensive control and manually review findings before relying on deployment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caidongyun/skills/agent-defender)
- [Artifact README](artifact/README.md)
- [Quick Reference](artifact/QUICK_REFERENCE.md)
- [Security Capabilities Analysis](artifact/SECURITY_CAPABILITIES_ANALYSIS_20260407.md)
- [Sigma Specification](https://github.com/SigmaHQ/sigma)
- [YARA Documentation](https://virustotal.github.io/yara/)
- [MITRE ATT&CK](https://attack.mitre.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON scan results, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local security findings and suggested actions; runtime and daemon behavior should be reviewed before enabling.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
