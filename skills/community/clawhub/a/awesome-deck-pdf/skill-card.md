## Description:

Turn design references, templates, URLs, screenshots, or style keywords into polished HTML slide decks and export them as high-quality 1440x900 PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karinecsy-collab](https://clawhub.ai/user/karinecsy-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and presentation authors use this skill to guide an agent through style extraction, content outlining, HTML slide generation, and PDF export. It is useful when a user wants a deck that follows a provided PowerPoint template, screenshot, website style, or plain-language design direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and export workflow carries local execution risk because it depends on Node.js, Puppeteer or Chrome, python-pptx, and shell setup commands.

Mitigation: Install only in a trusted project, prefer pinned dependency versions, and avoid sudo unless intentional system setup is required.

Risk: Exporting untrusted HTML or sensitive internal URLs through a browser automation workflow can expose local or private content.

Mitigation: Do not export untrusted HTML or sensitive internal URLs without isolation; use a clean directory or container for export work.

Risk: The exporter creates and deletes fixed helper paths in the working directory.

Mitigation: Run the exporter in a clean project directory or container so helper-file cleanup cannot affect unrelated work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/karinecsy-collab/skills/awesome-deck-pdf)
- [Installation Guide](references/install.md)
- [Export PDF Guide](references/export_pdf_guide.md)
- [Design Template](references/DESIGN_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, Python, and shell command blocks; final artifacts are slides.html and slides.pdf.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated slide deck is designed for fixed 1440x900 output and uses Puppeteer screenshot-and-compose for PDF export.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
