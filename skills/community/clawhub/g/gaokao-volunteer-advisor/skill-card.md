## Description:

A Chinese-language gaokao application advisor that helps families analyze school, major, safety, employment, and cost tradeoffs and produce structured Markdown analysis or a single-file HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifenglei](https://clawhub.ai/user/lifenglei)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially gaokao candidates and families, use this skill to evaluate Chinese college application options, build rush/stable/safe volunteer lists, investigate schools and majors, and prepare a shareable decision report. It is intended to support family review, not to guarantee admission or submit applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can include unescaped user or web text that may execute in a browser.

Mitigation: Review this skill before installing if HTML reports will be generated or shared; require HTML escaping or safe templating for every dynamic value and avoid pasting untrusted HTML-like content into report fields until fixed.

Risk: Gaokao guidance may affect real application outcomes if treated as a guarantee or final authority.

Mitigation: Use the skill's required reminders: verify all admissions plans, rules, major requirements, fees, and final choices against the current provincial examination authority and target school admissions documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lifenglei/skills/gaokao-volunteer-advisor)
- [README](artifact/README.md)
- [Admission Rules](artifact/references/admission-rules.md)
- [School Evaluation Dimensions](artifact/references/c1-dimensions.md)
- [Search Playbook](artifact/references/c2-search-playbook.md)
- [Authoritative Data Sources](artifact/references/c3-sources.md)
- [School Selection Strategy](artifact/references/p1-select-school.md)
- [Major Selection Strategy](artifact/references/p2-select-major.md)
- [Employment Analysis Guidance](artifact/references/p5-employment.md)
- [Special Admission Types](artifact/references/special-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, guidance]

**Output Format:** [Structured Markdown during analysis and a single-file HTML report for final output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite data sources and query dates, flag uncertain information, avoid admission guarantees, and require official verification before final submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
