## Description:

Technical GDPR compliance audit covering data mapping, encryption verification, access control review, data retention analysis, DPIA templates, and cross-border transfer assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1beekeeper](https://clawhub.ai/user/1beekeeper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and compliance teams use this skill to run technical GDPR audits of infrastructure and applications, including data mapping, encryption checks, access control review, retention analysis, DPIA preparation, and cross-border transfer assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan broadly across host filesystems and system services during a GDPR and security audit.

Mitigation: Restrict the audit target and run it only on systems you administer.

Risk: Audit reports may contain PII locations, secrets findings, and security gaps.

Mitigation: Use a restrictive umask or protected report directory and treat all generated reports as confidential.

Risk: Some checks may require elevated privileges or inspect sensitive host-level configuration.

Mitigation: Review and separately approve privileged checks, and use the least privilege needed for each audit phase.

Risk: The automated GDPR score can be mistaken for proof of compliance.

Mitigation: Independently review the underlying evidence and involve qualified compliance or legal reviewers before relying on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1beekeeper/skills/gdpr-security-auditor)
- [ClawHub Publisher Profile](https://clawhub.ai/user/1beekeeper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and generated local audit artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local findings, scorecards, DPIA templates, and report files under the configured audit directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
