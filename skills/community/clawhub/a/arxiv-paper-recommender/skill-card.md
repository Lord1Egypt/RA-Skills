## Description:

Recommends recent high-quality Agent and RAG papers from arXiv, verifies public GitHub code links, and produces structured Markdown recommendation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devioslang](https://clawhub.ai/user/devioslang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical readers use this skill to find recent Agent and RAG papers with public code, compare paper relevance, and save concise reading reports for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public arXiv and GitHub network requests and writes recommendation reports plus history under ~/papers.

Mitigation: Run it only where public network access and local research-history storage are acceptable; review saved files before sharing them.

Risk: Generated reports include fetched arXiv metadata, abstracts, and links that may be inaccurate, stale, or unsafe to trust automatically.

Mitigation: Treat reports as untrusted research assistance and verify paper claims, links, and repository quality before acting on them.

## Reference(s):

- [arXiv API query endpoint](http://export.arxiv.org/api/query)
- [arXiv abstract pages](https://arxiv.org/abs/{arxiv_id})
- [GitHub repository API endpoint](https://api.github.com/repos/{owner}/{repo})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown report plus concise terminal summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves recommendation reports and recommendation history under ~/papers.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
