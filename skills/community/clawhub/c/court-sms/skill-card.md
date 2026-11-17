## Description:

本技能应在用户收到法院短信（文书送达、立案通知、开庭提醒等）时使用，自动提取案号、当事人、下载链接，下载文书并归档到对应案件目录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

Legal professionals and their agents use this skill to process Chinese court SMS notices, extract case and delivery-link details, download available court documents, and organize the resulting files and records in the relevant case folder.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The release includes bundled archive records for legal-document processing.

Mitigation: Remove the archive records or replace them with fully synthetic examples before installing or publishing the skill.

Risk: The skill handles court links, access parameters, passwords, verification codes, downloads, and persistent case records.

Mitigation: Confirm target folders before writes, avoid storing raw SMS text or court access parameters, prefer user-entered authentication values, require HTTPS-only downloads, and pin Playwright or MCP dependencies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cat-xierluo/skills/court-sms)
- [Project Homepage](https://github.com/cat-xierluo/legal-skills)
- [SMS Pattern Reference](references/sms-patterns.json)
- [Archive Format](references/archive-format.md)
- [Report Format](references/report-format.md)
- [Attribution](references/ATTRIBUTION.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown status reports with inline shell commands, downloaded document files, and JSON archive records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write court-document PDFs and per-message JSON archive records, and may propose optional PDF merge or rename post-processing when split documents are detected.]

## Skill Version(s):

1.5.0 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
