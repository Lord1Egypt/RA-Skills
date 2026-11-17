## Description:

Guides agents through privacy-safe enterprise Web UAT for SaaS, admin, internal business, and role-permission systems, covering acceptance baselines, RTM mapping, evidence collection, issue reporting, final review, and delivery packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

QA teams, delivery teams, and agents use this skill to plan, execute, document, and review enterprise Web UAT with privacy-safe evidence, traceability, role-permission coverage, and clear acceptance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled HTML report templates can render copied test content as active browser content if fields are inserted without escaping.

Mitigation: Use report generation that escapes scalar fields, sanitizes rich blocks, validates URLs, and keeps secrets, personal data, cookies, and tokens out of evidence.

Risk: Enterprise UAT can touch destructive actions, production data, notifications, payments, or configuration changes when scope and authorization boundaries are unclear.

Mitigation: Confirm safety boundaries before execution and default high-risk or irreversible actions to blocked unless the user explicitly authorizes them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jerryxn/skills/enterprise-web-uat)
- [Enterprise Web / SaaS GUI UAT Standards](artifact/references/uat-standards.md)
- [Final UAT Audit Checklist](artifact/references/audit-checklist.md)
- [Issue Writing Guide](artifact/references/issue-writing.md)
- [Report Structure Templates](artifact/references/report-structures.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, tables, structured checklists, issue records, RTM entries, evidence indexes, and optional HTML report package guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privacy-safe UAT delivery package structure and report template usage guidance when requested.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
