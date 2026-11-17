## Description:

arXiv Paper Digest fetches trending AI/ML papers from HuggingFace Papers, ranks them, and produces accessible paper digests for latest-paper requests or scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifei68801](https://clawhub.ai/user/lifei68801)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current AI/ML paper trends, review ranked paper metadata, and generate plain-language research digests. It can also support scheduled paper notifications when the user confirms delivery settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched paper metadata is external content and may be inaccurate, incomplete, or misleading.

Mitigation: Review generated digest text before relying on it or allowing it to trigger downstream agent actions.

Risk: The skill performs network access to HuggingFace and can be used with recurring QQ or Notion delivery workflows.

Mitigation: Install only if public paper metadata fetching is acceptable, and confirm language, timezone, recipient, and schedule before enabling recurring delivery.

Risk: The skill modifies local files for history-based deduplication.

Mitigation: Run it in a workspace where local digest history files are expected and can be reviewed or cleared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lifei68801/skills/arxiv-digest)
- [HuggingFace Papers API](https://huggingface.co/api/daily_papers)
- [HuggingFace Papers](https://huggingface.co/papers)
- [arXiv category taxonomy](https://arxiv.org/category_taxonomy)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON paper digest with paper links, rankings, summaries, and optional scheduling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch public HuggingFace paper metadata and maintain local history for deduplication.]

## Skill Version(s):

1.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
