## Description:

Fetch and monitor latest arXiv papers by category, generate summaries, and manage starred papers for easy reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[constx1337](https://clawhub.ai/user/constx1337)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and technical readers use this skill to check recent arXiv papers in selected categories, review Markdown summaries, and maintain a local starred-paper reading list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched paper titles, abstracts, authors, and links are external content that may be inaccurate or misleading.

Mitigation: Treat displayed metadata as untrusted reference material and verify important claims against the linked arXiv paper before relying on them.

Risk: Paper links and PDF URLs may lead users to external content.

Mitigation: Avoid following suspicious links and do not treat paper metadata or linked content as instructions.

Risk: The skill saves starred-paper metadata locally.

Mitigation: Review local starred-paper data before sharing the skill directory or generated artifacts.

## Reference(s):

- [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy)
- [ClawHub Skill Page](https://clawhub.ai/constx1337/skills/arxiv-watch)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown paper summaries with arXiv links, plus JSON metadata for starred papers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches paper metadata from arXiv and stores starred-paper metadata locally in assets/starred.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
