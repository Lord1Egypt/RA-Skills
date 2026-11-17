## Description:

Find and summarize arXiv.org preprints--keyword/category search, abstracts, PDF links. Use for literature scans, paper IDs, or quick orientation (not peer-review, not medical/legal advice).

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and other users use this skill to find arXiv preprints by keyword, category, or paper ID and receive concise abstract summaries with paper links. It is intended for quick literature orientation, with preprint status and non-peer-reviewed limitations called out when relevant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries arXiv and may optionally fetch PDFs, creating disclosed network activity.

Mitigation: Use it only when external arXiv lookups and selective PDF retrieval are acceptable for the task.

Risk: Paper results are arXiv preprints and may not be peer reviewed, final, or reliable for high-stakes decisions.

Mitigation: Treat summaries as orientation only and review the original paper and other sources before relying on claims.

Risk: The skill can optionally save notable paper notes to a research log or memory file.

Mitigation: Ask before persisting research notes when the user does not want research logs retained.

## Reference(s):

- [arXiv API query endpoint](https://export.arxiv.org/api/query)
- [ClawHub skill page](https://clawhub.ai/codenova58/skills/arxiv-papers)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with paper metadata and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include arXiv IDs, titles, authors, abstract summaries, abstract links, PDF links, and preprint-status caveats.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
