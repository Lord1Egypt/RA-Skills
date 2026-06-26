## Description: <br>
Helps an agent search academic sources, screen abstracts, analyze citation context, and summarize the top relevant papers for a research topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArthurNie](https://clawhub.ai/user/ArthurNie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to turn a research question into a ranked set of academic papers with bibliographic metadata, citation signals, publication status, and a short synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics may be sent to external academic or search services. <br>
Mitigation: Avoid entering sensitive unpublished research questions or confidential project details unless the connected search services are approved for that use. <br>
Risk: Broad triggers such as research, cite, or citation may activate the skill on general research requests. <br>
Mitigation: Narrow activation language or confirm intent before using the skill when the user is not specifically asking for academic literature discovery. <br>
Risk: Academic search results can be misrepresented if paper identity, publication status, or metadata are not verified. <br>
Mitigation: Use the skill's built-in checks for real retrieved papers, DOI or arXiv identifiers, publication status, and open-access availability before presenting final results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ArthurNie/academic-search) <br>
- [arXiv API endpoint](http://export.arxiv.org/api/query) <br>
- [Semantic Scholar paper search API](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [Google Scholar search](https://scholar.google.com/scholar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research summary with ranked paper entries, bibliographic metadata, citation notes, open-access status, and synthesis sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected outputs emphasize verified academic papers, publication status, persistent identifiers, and cross-paper synthesis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
