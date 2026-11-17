## Description:

CNKI Scholar helps agents search Chinese and English academic papers, retrieve scholarly metadata, check open-access PDF availability, and generate citations using OpenAlex and Crossref-oriented workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaopanguo](https://clawhub.ai/user/shaopanguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users can use this skill to guide academic-paper searches, DOI lookups, metadata extraction, open-access availability checks, and citation generation for Chinese and English literature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scholarly search terms, DOI lookups, confidential project names, regulated personal data, or proprietary research topics may be sent to external academic services such as OpenAlex or similar providers.

Mitigation: Use only queries and identifiers that are appropriate to disclose to those services; avoid secrets, confidential project names, regulated personal data, and proprietary research terms unless disclosure is intended.

Risk: Academic metadata, citation counts, Chinese-language coverage, and open-access availability can be incomplete or differ across OpenAlex, Crossref, CNKI, and related sources.

Mitigation: Verify important bibliographic details, citation counts, and access status against authoritative publisher, DOI, institutional, or database records before relying on them.

## Reference(s):

- [CNKI Scholar on ClawHub](https://clawhub.ai/shaopanguo/skills/cnki-scholar)
- [OpenAlex API fields](artifact/references/openalex-fields.md)
- [Citation format templates](artifact/references/citation-formats.md)
- [OpenAlex Works API](https://api.openalex.org/works?search=QUERY&per_page=N)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands, API query examples, metadata summaries, and citation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paper titles, authors, publication years, venue names, DOI values, citation counts, open-access links, and formatted APA, BibTeX, GB/T 7714, or RIS citations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
