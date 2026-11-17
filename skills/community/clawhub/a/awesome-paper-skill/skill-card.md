## Description:

End-to-end pipeline for topic-driven literature research: collect papers from multiple sources, generate an Awesome-style README, and update/push to user GitHub repo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youjunzhao](https://clawhub.ai/user/youjunzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to gather papers for a topic, organize them into an Awesome-style README, and publish or update a GitHub repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publish step can create or update a GitHub repository and change repository visibility through an authenticated GitHub CLI session.

Mitigation: Use only an explicit repository owner and name, inspect the generated README before publishing, and run the publish step only when those repository changes are acceptable.

Risk: Paper retrieval depends on third-party research indexes and may have partial source failures or incomplete coverage.

Mitigation: Review coverage warnings and verify important papers before relying on or publishing the generated README.

## Reference(s):

- [arXiv API](https://export.arxiv.org/api/query)
- [Crossref Works API](https://api.crossref.org/works)
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search)
- [Awesome List Guidelines](https://github.com/sindresorhus/awesome)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown README, JSON paper list, and concise text summary with repository URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a GitHub repository and change its visibility through the authenticated gh session.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
