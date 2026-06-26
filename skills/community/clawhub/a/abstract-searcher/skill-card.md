## Description: <br>
Add abstracts to .bib file entries by searching academic databases (arXiv, Semantic Scholar, CrossRef) with browser fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to enrich BibTeX bibliographies by finding missing abstracts from public academic indexes and adding them to .bib entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bibliography titles and author names may be sent to public academic APIs during abstract lookup. <br>
Mitigation: Use the skill only for bibliographies that can be queried against public academic services. <br>
Risk: The browser fallback can operate through a logged-in Chrome session and may expose institutional or personal browser context to searched sites. <br>
Mitigation: Prefer the API-only script; when browser fallback is needed, use a separate Chrome profile with minimal logins and approve each site explicitly. <br>
Risk: Fetched abstracts may be mismatched to similarly titled papers. <br>
Mitigation: Verify that each returned abstract matches the intended paper title before accepting the generated BibTeX. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EasonC13/abstract-searcher) <br>
- [arXiv API](http://export.arxiv.org/api/query?search_query=...) <br>
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1/paper/search?query=...) <br>
- [Crossref Works API](https://api.crossref.org/works?query.title=...) <br>
- [OpenAlex Works API](https://api.openalex.org/works?search=...) <br>
- [Google Scholar](https://scholar.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated BibTeX text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces modified BibTeX entries on stdout and progress or summary messages on stderr when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
