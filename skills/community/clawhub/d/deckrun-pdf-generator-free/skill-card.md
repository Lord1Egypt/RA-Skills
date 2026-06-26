## Description: <br>
Generate a presentation-quality PDF slide deck from Deckrun Markdown, with no authentication required and a public URL valid for 90 days. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shivarammysore](https://clawhub.ai/user/shivarammysore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, technical writers, and agent workflows use this skill to turn Deckrun Markdown into a 16:9 PDF slide deck through the Deckrun free generation endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide Markdown is sent to an external service that returns a public PDF link. <br>
Mitigation: Use only content that is appropriate for external processing and public-link access. <br>
Risk: Sensitive, regulated, personal, or confidential business material could be accidentally exposed through the generated PDF. <br>
Mitigation: Do not submit secrets, personal data, regulated information, or confidential business material to the free public endpoint. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shivarammysore/deckrun-pdf-generator-free) <br>
- [AgenticDecks Homepage](https://agenticdecks.com) <br>
- [Deckrun Free Web UI](https://free.agenticdecks.com) <br>
- [Deckrun Free OpenAPI Spec](https://free.agenticdecks.com/.well-known/openapi.yaml) <br>
- [Deckrun Slide Format Schema](https://agenticdecks.com/schemas/v1/deckrun-slide-format.schema.json) <br>
- [Deckrun Free MCP Server](https://smithery.ai/servers/agenticdecks/deckrun-free) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Files, Guidance] <br>
**Output Format:** [Deckrun Markdown submitted as JSON, with a JSON response containing a public PDF URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free tier output is watermarked, supports up to 10 slides and 50 KB Markdown, and the public PDF URL is valid for 90 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
