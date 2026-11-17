## Description:

Curated skill bundle for medical device companies, digital health startups, and pharma R&D teams that configures Regulatory Affairs, Clinical, R&D, and Quality agents for FDA/CE compliance, clinical documentation, and pharmacovigilance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers, regulatory affairs, clinical, quality, and medtech operations teams use this skill to configure firm-style agent workflows for regulated healthcare tasks such as FDA/CE compliance, submission preparation, adverse-event triage, pharmacovigilance, and quality documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned companion skill installation for sensitive healthcare workflows.

Mitigation: Review or pin the ClawHub installer and each companion skill version before installation.

Risk: The skill uses session-orchestration tools in contexts that may involve PHI, adverse-event reports, audit trails, or regulatory work.

Mitigation: Use a restricted sandbox with no production credentials until companion skills and session-orchestration permissions are separately approved.

Risk: Generated regulatory, clinical, quality, or pharmacovigilance outputs may be inaccurate or incomplete.

Mitigation: Require qualified human review before using outputs in submissions, reportability decisions, audits, or patient-data workflows.

## Reference(s):

- [Firm Medtech Pack on ClawHub](https://clawhub.ai/romainsantoli-web/skills/firm-medtech-pack)
- [romainsantoli-web publisher profile](https://clawhub.ai/user/romainsantoli-web)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, JSON configuration snippets, and prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include regulated-workflow guidance and should be reviewed before use with PHI, adverse-event reports, audit trails, or regulatory submissions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
