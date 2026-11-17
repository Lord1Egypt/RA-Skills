## Description:

Analyzes Chinese gaokao application plans across provinces by using student score, rank, subjects, preferences, official admissions data, and province-specific rules to evaluate, rank, redesign, or generate 志愿 choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luxinfeng](https://clawhub.ai/user/luxinfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External students, families, and admissions advisors use this skill to analyze or build China gaokao 志愿 plans, classify choices into 冲/稳/保/delete layers, and check province-specific admission modes, subject requirements, tuition, and transfer-major risk.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The user may provide sensitive educational details such as score, rank, subject track, preferences, tuition limits, or an application table.

Mitigation: Collect only the information needed for the analysis and avoid retaining or redistributing student-specific details outside the active planning task.

Risk: Admissions recommendations can be misleading if province policies, score lines, subject requirements, plans, tuition, or cutoff data are outdated or unofficial.

Mitigation: Verify final recommendations against official provincial and university admissions sources, cite data sources, and mark unverifiable items as 需复核.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luxinfeng/skills/gaokao-volunteer-risk-skill-cn-adaptive)
- [Publisher Profile](https://clawhub.ai/user/luxinfeng)
- [Admission Mode Reference](artifact/policies/admission_modes.md)
- [Input Schema Template](artifact/templates/input_schema.yaml)
- [Report Outline](artifact/templates/report_outline.md)
- [Final Verification Checklist](artifact/checklists/final_verification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables, citations, risk classifications, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires official source verification and marks unverifiable admissions data as 需复核.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
