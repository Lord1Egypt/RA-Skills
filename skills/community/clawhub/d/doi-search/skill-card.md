## Description: <br>
Retrieves bibliographic metadata for articles, book chapters, and books by resolving a supplied DOI or searching the Crossref REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlosdelfino](https://clawhub.ai/user/carlosdelfino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, librarians, and developers use this skill to look up DOI-linked bibliographic metadata or find likely DOI matches from publication details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DOI values, search terms, and any optional User-Agent contact email are sent to DOI.org or Crossref. <br>
Mitigation: Tell users before lookup when sensitive terms may be disclosed, and use a public contact alias if adding mailto information. <br>
Risk: Crossref search results can return uncertain or incorrect matches when the user provides incomplete metadata. <br>
Mitigation: Compare title, authors, year, work type, and source before presenting a likely DOI, and state when the match is uncertain. <br>


## Reference(s): <br>
- [Crossref REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) <br>
- [DOI resolver](https://doi.org/) <br>
- [Crossref Works API endpoint](https://api.crossref.org/works) <br>
- [ClawHub skill page](https://clawhub.ai/carlosdelfino/doi-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with DOI metadata and optional inline curl commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and curl; DOI values, search terms, and optional User-Agent contact email are sent to DOI.org or Crossref.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
