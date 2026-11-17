## Description:

Professional print design guidance for producing high-quality printed output from HTML/CSS for articles, resumes, reports, invoices, books, brochures, and other paper-ready documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javotillo](https://clawhub.ai/user/javotillo)

### License/Terms of Use:

MIT

## Use Case:

Developers and designers use this skill to create or review print-focused HTML/CSS for documents that need polished paper output, including resumes, invoices, reports, books, brochures, and articles. It helps agents provide guidance and code patterns for typography, page layout, pagination, print media rules, and print testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad requests about documents intended for paper.

Mitigation: Confirm the user wants print-focused or paged-media output before applying print-specific layout guidance.

Risk: Installer commands can create supply-chain exposure if run through an untrusted or unpinned path.

Mitigation: Use a trusted installation path or pinned installer version when installing the skill.

Risk: Generated print CSS can produce misleading pagination, clipped content, or poor readability if not checked in the target print environment.

Mitigation: Review print previews and generated PDFs, and test important documents on the intended paper size or printer.

## Reference(s):

- [Typography Reference](references/typography.md)
- [Layout Reference](references/layout.md)
- [Page Features Reference](references/page-features.md)
- [Locale Conventions Reference](references/locale.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with HTML/CSS examples and print configuration patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no credentials or tool access required by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
