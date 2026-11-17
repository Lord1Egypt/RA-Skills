## Description:

Screens public FDA FAERS adverse-event reports for potential drug–event safety signals using PRR, ROR, IC, and EBGM, with optional corroboration and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medstatstar](https://clawhub.ai/user/medstatstar)

### License/Terms of Use:

MIT

## Use Case:

Pharmacovigilance and clinical-trial safety professionals can screen public adverse-event data for potential drug–event signals, compare reporting patterns, and prepare findings for expert review. Results are screening evidence and do not establish causation or support treatment or regulatory decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scanners report possible machine-identifier and billing-data flows, network destinations beyond those described, and storage or file access outside the stated boundaries.

Mitigation: Before use, review whether those reported data flows, destinations, and file accesses are expected; limit network and filesystem access to what the task requires.

Risk: Scanner coverage was partial, so the suspicious verdict does not establish that the skill is safe or malicious.

Mitigation: Review the reported findings and skill behavior before installation, and use only with permissions appropriate to the data and environment.

Risk: FAERS disproportionality signals are affected by reporting bias, under-reporting, and confounding and do not establish causation.

Mitigation: Use outputs for signal screening only; corroborate with clinical evidence and qualified clinical or regulatory judgment.

## Reference(s):

- [Disproportionality methods](references/methods.md)
- [FAERS evidence hierarchy and claim boundaries](references/evidence-hierarchy.md)
- [FAERS data preparation](references/faers-data-prep.md)
- [Fetch pipeline and FAERS API field reference](references/fetch_pipeline.md)
- [FDA FAERS API](https://api.fda.gov/drug/event.json)
- [ClawHub release](https://clawhub.ai/medstatstar/skills/ct-safety)
- [Project homepage](https://github.com/medstatstar/ct-safety)

## Skill Output:

**Output Type(s):** [Analysis, Text, HTML reports, XLSX workbooks, Markdown and JSON backups]

**Output Format:** [Conversational summaries and downloadable reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drug and event query inputs; optional comparison, trend, label, and corroboration analyses.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
