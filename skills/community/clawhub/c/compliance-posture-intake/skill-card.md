## Description:

Compliance Posture Intake guides healthcare organizations through a structured HIPAA posture assessment, analyzes administrative compliance documents, and produces a posture report with maturity stage, enterprise blockers, prioritized gaps, and a 30/60/90 day roadmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare operators, compliance teams, and advisors use this skill to run a structured HIPAA readiness intake, optionally review administrative compliance documents, and create a shareable posture report for planning, consultation, or account setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share sensitive compliance records or actual patient PHI during the intake.

Mitigation: Limit uploads to policies, procedures, BAAs, risk assessments, and other administrative records; do not provide actual patient PHI; use an agent environment appropriate for sensitive compliance material.

Risk: Generated posture reports may contain sensitive business and compliance information.

Mitigation: Store generated .docx reports in an approved location and review the report before sharing it with teams, consultants, or external recipients.

Risk: State-law findings and optional product or consultation mapping may be context dependent.

Mitigation: Use general business descriptions for web searches, review optional Rote or consultation sections before sharing, and confirm state-specific obligations with qualified compliance or legal counsel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dangsllc/skills/compliance-posture-intake)
- [Rote Compliance](https://rotecompliance.com)
- [Dang's Solutions consultation](https://dangssolutions.com/book-consultation)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Conversational text and Markdown/Word-style report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a polished .docx posture report when the agent environment supports document creation; outputs should be reviewed before external sharing.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact frontmatter lists 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
