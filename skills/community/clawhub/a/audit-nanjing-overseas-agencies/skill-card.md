## Description:

Bilingual, evidence-led audit support for Nanjing study-abroad, immigration, overseas-identity, and private-entry/exit agencies, including entity checks, comparisons, scoring, complaint review, and protective contract clauses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cod1doc](https://clawhub.ai/user/cod1doc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, consumer advocates, and advisors use this skill to audit Nanjing overseas-study and immigration agencies from public evidence, map brands to legal entities, compare risks, score agencies, review complaints and marketing claims, and draft protective contract clauses. Its outputs support research and decision-making, not legal advice.

### Deployment Geography for Use:

Global; audit subject matter is Nanjing, China agencies.

## Known Risks and Mitigations:

Risk: The skill's audit output may be mistaken for legal advice or a final finding about an agency.

Mitigation: Treat the output as research support and independently verify licensing, registry, complaint, and contract claims from official sources.

Risk: Agency registration, licensing, policy, and complaint information can change after the baseline date.

Mitigation: Reverify mutable claims against current official sources for each audit and include access dates.

Risk: Low evidence coverage can make rankings or scores misleading.

Mitigation: Publish evidence coverage with each score, mark low-coverage scores as provisional, and avoid ranking agencies when coverage is below the required threshold.

Risk: A passing structured validation result does not prove the underlying audit facts are correct.

Mitigation: Use the validator as a format check only, then manually review source quality, dates, and attribution before relying on the report.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cod1doc/skills/audit-nanjing-overseas-agencies)
- [Legal and Evidence Baseline](references/legal-evidence-baseline.md)
- [Report Template](references/report-template.md)
- [Scoring Rubric](references/scoring-rubric.md)
- [State Council cancellation notice](https://www.gov.cn/zhengce/content/2017-01/21/content_5161879.htm)
- [National Immigration Administration notice](https://www.nia.gov.cn/n794014/n1050181/n1050479/c788143/content.html)
- [National Enterprise Credit Information Publicity System](https://www.gsxt.gov.cn/)
- [Nanjing Market Regulation enterprise archive query](https://amr.nanjing.gov.cn/xcxt/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports with optional structured JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese-first output when requested; scores require source-backed deductions and evidence coverage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
