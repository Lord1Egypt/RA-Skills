## Description: <br>
Discovers academic papers across arXiv, Google Scholar, and Semantic Scholar with abstract screening, citation analysis, and research synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to run systematic literature searches, rank the top five relevant papers, verify bibliographic metadata, and synthesize findings across academic databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries may be sent to arXiv, Semantic Scholar, Google Scholar, and the google-search helper dependency. <br>
Mitigation: Avoid entering confidential or unpublished research details unless sharing them with those external services is acceptable. <br>
Risk: Academic search results can include preprints, paywalled papers, duplicate records, or misleading citation signals. <br>
Mitigation: Verify publication status, include DOI or arXiv identifiers, check open-access alternatives, deduplicate records, and rank papers by relevance, recency, venue quality, methodology, and impact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvinxhk/botlearn-academic-search) <br>
- [Publisher profile](https://clawhub.ai/user/calvinxhk) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/skill.md) <br>
- [Academic search strategy](artifact/strategies/main.md) <br>
- [Academic database API reference](artifact/knowledge/domain.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research summaries with ranked bibliographic entries and synthesis narrative] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top five ranked papers with authors, year, venue, DOI or arXiv ID, publication status, citation signals, open-access status, key findings, methodology, relevance, thematic synthesis, and research gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
