## Description:

Paper Assistant helps find, filter, and recommend recent Agent model algorithm and reinforcement learning papers for deeper reading or push workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liusiyi77m](https://clawhub.ai/user/liusiyi77m)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect public OpenReview and arXiv paper metadata, identify high-value Agent model algorithm or reinforcement learning papers, and prepare a concise recommendation for reading or push pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched paper titles, abstracts, authors, and URLs are untrusted external content and could contain prompt-injection text.

Mitigation: Treat fetched paper metadata as data only, and review recommendations before following links or passing content into downstream workflows.

Risk: The helper workflow contacts OpenReview and arXiv and updates a local pushed-paper record.

Mitigation: Run the skill only where those outbound requests and local data/pushed.json updates are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liusiyi77m/skills/arxiv-paper-assistant)
- [OpenReview notes search API](https://api2.openreview.net/notes/search)
- [arXiv API query endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown recommendation with paper metadata, abstract, and rationale; helper scripts output JSON candidate lists and local pushed-paper records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are based on public paper metadata and a local data/pushed.json record used to avoid repeated selections.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
