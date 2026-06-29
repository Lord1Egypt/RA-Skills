## Description: <br>
Deprecated ClawHub skill-quality auditor that performs L1/L2 static and dry-run checks, scores agent skills, and produces Markdown audit reports with optional explicitly authorized fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this deprecated compatibility slug to audit agent skill directories against a seven-dimension quality checklist, produce a Markdown scorecard, and review suggested fixes before migrating to skill-deep-audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security review reports conflicting instructions about when the skill may write or edit files. <br>
Mitigation: Use the skill in read-only audit mode by default; run fix mode only after explicit approval, on a scoped workspace, and with version control or separate backups. <br>
Risk: Generated audit reports and fix suggestions may be incorrect or misleading if static checks misclassify a skill's behavior. <br>
Mitigation: Review reported ERR and WARN items before acting, and manually verify any finding that affects code, security controls, or release decisions. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/songhonglei/better-skill-audit) <br>
- [Check rules](artifact/references/check-rules.md) <br>
- [Controlled domains](artifact/references/controlled-domains.md) <br>
- [Audit output template](artifact/references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit reports with score tables, findings, fix guidance, and concise terminal summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write AUDIT-{date}.md scorecards; fix mode may edit audited skill files only after explicit user approval and backup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; deprecated compatibility slug) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
