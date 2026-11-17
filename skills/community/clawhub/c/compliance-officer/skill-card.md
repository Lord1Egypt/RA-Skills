## Description:

Reviews marketing content, emails, landing pages, privacy policies, images, and URLs against FTC, HIPAA, GDPR, SEC 482, SEC Marketing, CCPA, COPPA, and CAN-SPAM rules with cited sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arberx](https://clawhub.ai/user/arberx)

### License/Terms of Use:

Apache-2.0

## Use Case:

Marketing, privacy, legal, and compliance teams use this skill to review marketing copy, emails, landing pages, privacy policies, images, or URLs against structured regulatory rules. It produces preliminary findings, cited rule explanations, compliance checklists, and draft disclosure language for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch user-provided URLs during review.

Mitigation: Use URL review only for public pages that are intended to be fetched by the agent.

Risk: Compliance findings may be incomplete or incorrect if treated as legal determinations.

Mitigation: Treat outputs as preliminary compliance guidance and route final decisions through qualified compliance or legal reviewers.

Risk: The install command in the artifact is not pinned to a specific installer version.

Mitigation: Install only from a trusted ClawHub or registry path and prefer pinned or verified installer versions when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arberx/skills/compliance-officer)
- [Agent Instructions](references/instructions.md)
- [CAN-SPAM Rules](references/rules-can-spam.json)
- [CCPA Rules](references/rules-ccpa.json)
- [COPPA Rules](references/rules-coppa.json)
- [FTC Claims Rules](references/rules-ftc-claims.json)
- [FTC Dark Patterns Rules](references/rules-ftc-dark-patterns.json)
- [FTC Endorsements Rules](references/rules-ftc-endorsements.json)
- [GDPR Rules](references/rules-gdpr.json)
- [HIPAA Rules](references/rules-hipaa.json)
- [SEC 482 Rules](references/rules-sec-482.json)
- [SEC Marketing Rules](references/rules-sec-marketing.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with findings, rule citations, suggested fixes, rule explanations, rule tables, or draft disclosure text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [URL review requires network access; findings are preliminary and should be reviewed by compliance or legal teams.]

## Skill Version(s):

1.1.0 (source: server release metadata and claw.json; SKILL.md metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
