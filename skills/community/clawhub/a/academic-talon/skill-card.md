## Description:

Academic Talon helps agents search academic papers, analyze PDFs with GROBID, generate BibTeX or TEI XML, archive records to Zotero, and manage local PDF access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigdogaaa](https://clawhub.ai/user/bigdogaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and research engineers use this skill to find academic papers, extract citation-ready metadata or structured PDF text, and archive papers into Zotero-backed libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local PDFs and document contents may be exposed if the PDF server is used on public or shared networks without protection.

Mitigation: Use the skill only on trusted machines and keep PDF serving private or behind authentication.

Risk: PDF contents are sent to the configured GROBID_API_URL for processing.

Mitigation: Run GROBID locally or on trusted infrastructure, and do not point GROBID_API_URL at an untrusted service.

Risk: The security evidence reports weak scoping around local PDFs and document contents.

Mitigation: Review before installing and treat sandbox claims as unreliable until path validation and symlink handling are verified.

## Reference(s):

- [Academic Talon on ClawHub](https://clawhub.ai/bigdogaaa/skills/academic-talon)
- [GROBID documentation](https://grobid.readthedocs.io/)
- [Zotero API key settings](https://www.zotero.org/settings/keys)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JSON responses with search results, BibTeX, TEI XML, PDF file paths, and Zotero archive status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, GROBID_API_URL, and Zotero credentials for archiving; optional search API keys enable additional sources.]

## Skill Version(s):

1.1.2 (source: server release metadata, released 2026-04-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
