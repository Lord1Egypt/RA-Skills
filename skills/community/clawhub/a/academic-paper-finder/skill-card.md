## Description:

Search biomedical literature, get citation counts, and import selected papers to Zotero or EndNote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merdeng](https://clawhub.ai/user/merdeng)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, students, and developers use this skill to find biomedical papers by DOI, title, author, or keyword; retrieve metadata and citation counts; and prepare records for Zotero or EndNote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, DOIs, PMIDs, and paper metadata are sent to PubMed, OpenAlex, and Zotero.

Mitigation: Use the skill only when sharing that bibliographic information with those services is acceptable.

Risk: Zotero import uses user credentials and can add items to a library, including multiple records during batch import.

Mitigation: Use a Zotero API key with the minimum needed permissions and review batch imports before running them.

Risk: Logs and errors may contain item identifiers or bibliographic metadata.

Mitigation: Avoid sharing logs unless they have been reviewed for sensitive or unwanted paper metadata.

## Reference(s):

- [Academic Paper Finder on ClawHub](https://clawhub.ai/merdeng/skills/academic-paper-finder)
- [Zotero API Key Settings](https://www.zotero.org/settings/keys/new)
- [Zotero Web API](https://api.zotero.org)
- [NCBI Entrez E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/)
- [OpenAlex Works API](https://api.openalex.org/works)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, RIS files]

**Output Format:** [Markdown guidance with shell commands, JSON-capable search output, and RIS files for EndNote import.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call PubMed, OpenAlex, and Zotero APIs; Zotero import requires ZOTERO_API_KEY and ZOTERO_USER_ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
