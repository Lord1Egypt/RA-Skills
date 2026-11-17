## Description:

Generate a presentation-quality PDF slide deck from Deckrun Markdown. No authentication required. Free. Returns a public URL valid for 90 days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shivarammysore](https://clawhub.ai/user/shivarammysore)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill to turn Deckrun Markdown into a 16:9 PDF slide deck through the AgenticDecks free generation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown submitted for PDF generation is sent to AgenticDecks and the resulting PDF is exposed through a public link valid for 90 days.

Mitigation: Do not submit secrets, private business documents, personal data, or regulated content unless that exposure is acceptable.

## Reference(s):

- [AgenticDecks Homepage](https://agenticdecks.com)
- [Deckrun Free OpenAPI Spec](https://free.agenticdecks.com/.well-known/openapi.yaml)
- [Deckrun Slide Format Schema](https://agenticdecks.com/schemas/v1/deckrun-slide-format.schema.json)
- [Deckrun Free Web UI](https://free.agenticdecks.com)
- [Deckrun Free MCP Server](https://smithery.ai/servers/agenticdecks/deckrun-free)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown and JSON request/response examples with a public PDF URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PDFs are watermarked in the free tier and valid for 90 days.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
