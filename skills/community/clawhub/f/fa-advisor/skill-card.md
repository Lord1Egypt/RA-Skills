## Description:

Professional Financial Advisor (FA) skill for primary market financing that provides AI-powered project assessment, pitch deck generation, valuation analysis, and investor matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

External startup founders, investors, and developers use this skill to prepare fundraising materials, evaluate investment readiness, estimate startup valuations, match investors, and generate due diligence or investment memo outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated report paths may be influenced by company or project names and can write outside the intended output folder.

Mitigation: Sanitize company names, reject path separators or traversal segments, and confirm the final export path before writing files.

Risk: Fundraising materials, financial statements, and PDFs can contain confidential business data.

Mitigation: Use the skill only in a trusted local environment, provide the minimum necessary data, and redact sensitive details before processing or sharing outputs.

Risk: Valuations, investor matches, and investment recommendations are advisory estimates.

Mitigation: Have qualified finance, legal, and accounting reviewers validate assumptions and conclusions before using outputs for business decisions.

Risk: Untrusted PDFs can expose file-processing and OCR workflows to unsafe or unexpected content.

Mitigation: Process only trusted PDFs when possible, scan files before use, and isolate PDF parsing from sensitive directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/fa-advisor)
- [Publisher Profile](https://clawhub.ai/user/zhenstaff)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Repository README](https://github.com/ZhenRobotics/openclaw-financial-analyst/blob/main/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python code examples and optional generated Markdown or PDF documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include investment readiness scores, pitch deck outlines, valuation reports, investor match lists, outreach strategy, business plans, due diligence checklists, and local report files.]

## Skill Version(s):

0.1.0 (source: frontmatter, pyproject.toml, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
