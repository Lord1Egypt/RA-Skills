## Description:

Reviews structured .xlsx cloud-migration cutover manuals and produces a risk-focused Markdown or JSON report covering maintenance notices, traffic switching, source-database read-only handling, Alibaba Cloud application restart strategy, and rollback decision conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, DBAs, and migration engineers use this skill to review structured Excel cutover manuals for application cloud migration and big-data stack migration before execution. It helps identify missing review dimensions, high-priority cutover risks, rollback-readiness gaps, and remediation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cutover manuals and generated reports can contain infrastructure identifiers or operationally sensitive details.

Mitigation: Run the skill only on manuals you intend to review locally, keep redaction enabled, and encrypt or restrict access to any JSON or unredacted outputs.

Risk: The review is based on rule and keyword matching and can miss business-specific migration risks or overstate findings.

Mitigation: Use the report as review input only, then confirm key items through manual review, rehearsal, and an expert cutover-readiness meeting.

Risk: The skill reads a user-selected workbook and writes report files to the chosen output directory.

Mitigation: Provide only the intended .xlsx manual, inspect generated reports before sharing, and avoid running with broader file access than needed.

## Reference(s):

- [Usage Guide](artifact/references/usage-guide.md)
- [Review Standard](artifact/references/review-standard.md)
- [RAM Permission Declaration](artifact/references/ram-policies.md)
- [Version History](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown report by default, optional JSON report, and a concise text summary with score, risk level, reviewed Sheet mapping, and next steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided .xlsx cutover manual and writes local report files; redaction is enabled by default.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
