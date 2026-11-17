## Description:

AI-native GRC (Governance, Risk, and Compliance) for OpenClaw that manages controls, evidence, risks, policies, vendors, incidents, assets, training, vulnerabilities, access reviews, questionnaires, compliance scoring, reports, dashboards, trust center pages, and security scans across 13 frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailnike](https://clawhub.ai/user/mailnike)

### License/Terms of Use:

MIT

## Use Case:

Compliance, security, and audit teams use this skill to manage GRC workflows in OpenClaw, including framework activation, evidence tracking, gap analysis, risk management, reporting, and local security checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can work with cloud and identity-provider credentials.

Mitigation: Do not paste secrets into chat; prefer short-lived, read-only, provider-native authentication and verify the active account before running integrations.

Risk: The skill stores a local GRC database and local credential files under ~/.openclaw/grc.

Mitigation: Install only in environments where local storage of this compliance and credential material is acceptable.

Risk: Security scanners operate against user-provided URLs and domains.

Mitigation: Run URL scanners only against domains you control or are authorized to assess.

Risk: Evidence exports may contain sensitive compliance material.

Mitigation: Review generated evidence ZIP contents before sharing them with auditors or third parties.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/mailnike/skills/auditclaw-grc)
- [AuditClaw Homepage](https://www.auditclaw.ai)
- [OpenClaw](https://openclaw.ai)
- [Source Repository Declared by Skill](https://github.com/avansaber/auditclaw-grc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and generated local files such as HTML reports, dashboards, trust center pages, and evidence ZIP exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses are intended to be concise human-facing summaries; local scanners and exports operate on user-provided targets and files.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
