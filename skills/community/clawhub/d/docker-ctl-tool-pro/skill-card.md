## Description:

Container diagnostics skill for Docker and Podman that helps agents inspect containers in bulk, diagnose failures, review historical trends, manage remote hosts, and prepare compliance-oriented reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Operations engineers, DevOps teams, and container platform maintainers use this skill to inspect Docker or Podman environments, diagnose container issues, audit security posture, and generate operational reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run remote SSH commands and inspect container hosts with broad authority.

Mitigation: Use only on authorized hosts, prefer non-root SSH accounts, require explicit host allowlists, and enforce strict SSH host-key checking.

Risk: Bulk host actions, remote execution, scheduled audits, and long retention can expand operational blast radius.

Mitigation: Avoid --hosts all, remote exec, scheduled audits, and long retention unless each behavior is intended, approved, and scoped to a controlled environment.

Risk: Configuration files and generated reports may expose operational details or credentials.

Mitigation: Protect local configuration files, store reports only in controlled locations, and review outputs before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/docker-ctl-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, diagnostic findings, and report-generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe PDF, Excel, or HTML report outputs when the requested workflow involves audit or inspection reports.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
