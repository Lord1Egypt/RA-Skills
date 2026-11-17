## Description:

Creates and changes DocSpring page designs, templates whose PDFs DocSpring lays out from a JSON layout of sections, text with fields, images, tables, form fields and codes, which the Page Designer also edits. Covers the layout format, repeating sections and tables, conditions, the fields DocSpring adds, previews and publishing. Use when the user wants a PDF designed from their data (an invoice, certificate or letter) without HTML or a Word document, or to change a page design, or when a project has template_type "page_designer" or a layout with sections. Not for HTML templates (docspring-html-templates), Word documents (docspring-word-templates), existing PDFs (docspring-pdf-templates) or app code (docspring-api-integration).

This skill is ready for commercial/non-commercial use.

## Publisher:

[docspring](https://clawhub.ai/user/docspring)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to create or revise DocSpring page designs that produce data-driven PDFs, preview each page, and publish changes when approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automated security review is benign but incomplete, and some local references were not resolved.

Mitigation: Consider the scan limitation and review the skill before installation, as the security guidance recommends.

Risk: Replacing a page layout can overwrite concurrent edits or remove elements if based on an outdated layout.

Mitigation: Fetch the latest layout immediately before editing, preserve existing IDs, and ask the user to close the Page Designer first.

Risk: A preview can expose real submission data, and changes to an unpublished template can affect submissions immediately.

Mitigation: Use made-up sample data for previews, check the draft and published status, and publish only after the user agrees.

## Reference(s):

- [DocSpring page designer overview](https://docspring.com/docs/page-designer/overview/)
- [Page designer layout format](https://docspring.com/docs/page-designer/layout-format/)
- [Page designer layout JSON Schema](https://docspring.com/schemas/page-designer/layout.v1.json)
- [DocSpring API documentation](https://docspring.com/docs/api/)
- [ClawHub skill release](https://clawhub.ai/docspring/skills/docspring-page-designer)

## Skill Output:

**Output Type(s):** [JSON, Configuration, API Calls, Guidance]

**Output Format:** [JSON page layouts with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DocSpring template and field updates; preview and publication depend on user approval.]

## Skill Version(s):

1.9.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
