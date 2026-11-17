## Description:

Deprecated ClawHub skill-quality auditor for agent skills, preserved for backward compatibility after being renamed to skill-deep-audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this deprecated compatibility skill to audit agent skill directories for quality, safety, portability, documentation, dependency, and packaging issues. New use should migrate to skill-deep-audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the skill mixes read-only audit claims with target-directory writes.

Mitigation: Review before installing, expect audit-report writes into the target directory, and do not allow the fix workflow unless modification of audited skill files is intended.

Risk: Unsafe shell command templates may be affected by user-supplied paths containing shell metacharacters.

Mitigation: Use only trusted, simple target paths and avoid paths containing shell metacharacters.

Risk: The skill may optionally query Hub tooling and can back up and modify audited skill files during the fix workflow.

Mitigation: Run it in an environment where optional Hub queries are acceptable, and start the fix workflow only after explicit review of the proposed file changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/better-skill-audit)
- [Replacement skill listing](https://clawhub.com/skills/skill-deep-audit)
- [Check rules](references/check-rules.md)
- [Controlled domains](references/controlled-domains.md)
- [Audit report template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and concise text guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audit scoring, findings, remediation guidance, and optional fix-workflow instructions.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
