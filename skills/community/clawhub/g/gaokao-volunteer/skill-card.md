## Description: <br>
Gaokao Volunteer helps users plan Chinese Gaokao college applications with rank-based matching, score-delta analysis, university recommendations, reach/match/safety planning, and volunteer-plan checks across provincial exam models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External students, families, and admissions advisors use this skill to collect Gaokao profile details, compare score and rank signals, classify reach/match/safety choices, and generate college application guidance or reports for Chinese provincial admissions workflows. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports, temporary profile files, and web searches may expose Gaokao score, rank, province, subject, and preference details. <br>
Mitigation: Avoid names, ID numbers, account credentials, and other direct identifiers; delete exported reports and temporary profile files when they are no longer needed. <br>
Risk: Admission guidance can become inaccurate when batch lines, one-score-one-rank tables, provincial rules, or historical admissions data are stale or incomplete. <br>
Mitigation: Verify current-year batch lines, rank tables, province rules, and admissions data against official exam-authority sources before acting on any recommendation. <br>
Risk: Reach/match/safety classifications and admission probabilities are estimates and may mislead users if treated as guarantees. <br>
Mitigation: Present recommendations as AI-assisted reference material, include plain-language uncertainty and disclaimers, and keep final decisions with the user or their advisor. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/gaokao-volunteer) <br>
- [Server-resolved GitHub repository](https://github.com/bettermen/gaokao-volunteer) <br>
- [Server-resolved source commit](https://github.com/bettermen/gaokao-volunteer/commit/a5ef7e08dc08c5b687142fc8e6bc62a9e3104a64) <br>
- [Province rules reference](artifact/references/province_rules.json) <br>
- [University basics reference](artifact/references/university_basics.json) <br>
- [Major catalog reference](artifact/references/major_catalog.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON intermediate results, and optional HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports and local intermediate files may contain score, rank, province, subject, and preference details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
