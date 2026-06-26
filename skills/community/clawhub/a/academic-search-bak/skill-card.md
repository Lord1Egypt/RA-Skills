## Description: <br>
Systematically searches academic databases, screens abstracts, analyzes citation context, and returns a structured list of relevant scholarly papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xunhe730](https://clawhub.ai/user/xunhe730) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill to find and evaluate academic papers across arXiv, Google Scholar, and Semantic Scholar. It is intended for literature review, citation analysis, paper ranking, and concise research synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics may be sent to external search and academic database services. <br>
Mitigation: Avoid submitting sensitive or confidential research topics unless external service use is acceptable. <br>
Risk: Broad trigger phrases such as research, cite, or citation may activate the skill unintentionally. <br>
Mitigation: Tighten activation phrases or require an explicit academic-search request in deployments where accidental activation matters. <br>
Risk: Academic search outputs can mislead users if paper metadata, publication status, or findings are fabricated or stale. <br>
Mitigation: Verify retrieved papers against academic databases, disclose preprint or peer-review status, and include persistent identifiers when available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xunhe730/academic-search-bak) <br>
- [Skill definition](SKILL.md) <br>
- [Academic database APIs and paper structure](knowledge/domain.md) <br>
- [Academic search best practices](knowledge/best-practices.md) <br>
- [Academic search anti-patterns](knowledge/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown research summaries with ranked paper entries and synthesis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bibliographic metadata, publication status, identifiers, citation signals, open-access notes, and synthesis for up to five papers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
