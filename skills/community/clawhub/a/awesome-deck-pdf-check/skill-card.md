## Description:

Turn a user-provided design style into a polished HTML slide deck and export it as a high-quality PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karinecsy-collab](https://clawhub.ai/user/karinecsy-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to turn PPTX templates, screenshots, website URLs, or style keywords into user-reviewed HTML slide decks and PDF exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PDF exporter renders user-selected HTML in Chromium with the browser sandbox disabled.

Mitigation: Run the exporter only on trusted HTML and prefer an isolated workspace or container.

Risk: Dependency and browser installation steps can introduce under-scoped install risk.

Mitigation: Use pinned dependencies and a lockfile, and avoid sudo unless an administrator approves it.

Risk: The exporter deletes fixed temporary paths named _pdf_pages and _slides.html.

Mitigation: Run the exporter from a dedicated project directory where those temporary names cannot collide with valuable files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/karinecsy-collab/skills/awesome-deck-pdf-check)
- [DESIGN_TEMPLATE.md](references/DESIGN_TEMPLATE.md)
- [export_pdf_guide.md](references/export_pdf_guide.md)
- [install.md](references/install.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, shell commands, and generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single-file HTML deck first, then a 1440x900 PDF through the bundled Puppeteer exporter when shell access is available.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
