## Description:

Convert EPUB ↔ PDF bidirectionally. EPUB→PDF preserves layout for analysis; PDF→EPUB compresses and reflows for distribution and ereaders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bunsdev](https://clawhub.ai/user/bunsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and document workflows use this skill to convert EPUB files into PDFs for layout-preserving analysis and convert PDFs into reflowable EPUB files for distribution or ereader use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on calibre being installed as a local system dependency.

Mitigation: Confirm calibre is installed from a trusted package source before running conversion commands.

Risk: Converted documents may contain copyrighted or confidential material.

Mitigation: Convert, store, and redistribute only documents the user is allowed to handle, and avoid shared research folders unless access controls and licensing are clear.

Risk: PDF to EPUB conversion can lose structure for scanned or fixed-layout PDFs.

Mitigation: Inspect the generated EPUB in an ereader or calibre viewer and use the documented fallback path when conversion quality is poor.

## Reference(s):

- [EPUB ↔ PDF Converter on ClawHub](https://clawhub.ai/bunsdev/skills/epub-to-pdf)
- [pdftotext manual page](https://manpages.ubuntu.com/manpages/xenial/man1/pdftotext.1.html)
- [Calibre Handbook](https://manual.calibre-ebook.com/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local document conversion commands and quality-check guidance; converted files depend on the user's source documents and local calibre installation.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
