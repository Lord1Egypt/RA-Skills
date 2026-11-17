## Description:

Gaokao 360To3 helps students plan Chinese Gaokao college applications by asking structured questions about family context, personal strengths, score range, interests, and risk preference, then recommending three career and major directions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zify9000](https://clawhub.ai/user/zify9000)

### License/Terms of Use:

MIT-0

## Use Case:

Students, families, and education counselors use this skill after Gaokao results or during high-school planning to structure admissions conversations and identify three suitable career and major paths. The guidance is framed as planning support and should be reviewed with current admissions and employment data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for income, family resources, location, education goals, and personal-profile details that may be sensitive.

Mitigation: Tell users these answers are optional, ask only for the minimum useful detail, and discourage names or uniquely identifying information.

Risk: The skill promises data-grounded recommendations but the required reference files are not present in the artifact.

Mitigation: Supply and review the required references before student use, and lower confidence or pause recommendations when current data is unavailable.

Risk: Admissions and employment guidance can become stale or overconfident.

Mitigation: Review recommendations against current admissions rules and employment data, especially before each Gaokao season.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zify9000/skills/gaokao-360to3)
- [Server-resolved source repository](https://github.com/zify9000/gaokao-360To3)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversation with structured questions, ranked recommendations, reasons, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces three recommended career and major directions; quality depends on the required reference data files being present and current.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
