## Description:

Produce polished, print-ready PDFs from Markdown or HTML with Pandoc, WeasyPrint, reusable CSS, and a mandatory rendered-page review loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers, writers, and business users use this skill to turn Markdown or static HTML into designed PDFs for reports, proposals, briefs, CVs, invoices, letters, and dossiers. It also guides agents to rasterize and inspect every rendered page for layout defects before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command may resolve a mutable package source.

Mitigation: Install from a pinned or otherwise verified source, and do not run the npx install command with elevated privileges.

Risk: Private source files or generated page images may contain sensitive document content.

Mitigation: Keep source files and page images private, and process only documents suitable for local Pandoc, WeasyPrint, and PyMuPDF handling.

Risk: Rendered PDFs may still contain layout defects, clipped content, weak contrast, or awkward page breaks.

Mitigation: Rasterize every page, inspect the current page images, fix issues, and repeat the render-review loop before delivery.

## Reference(s):

- [Beautiful PDF Skill Page](https://clawhub.ai/antreasantoniou/skills/beautiful-pdf)
- [Document Type Guide](references/doc-types.md)
- [PDF Style Guide](references/style-guide.md)
- [Default PDF Stylesheet](assets/default.css)
- [PDF-to-PNG Review Helper](scripts/pdf-to-png.py)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown or static HTML source, CSS, PDF files, PNG page images, and concise review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the final page count, output path, and visual issues checked before delivery.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
