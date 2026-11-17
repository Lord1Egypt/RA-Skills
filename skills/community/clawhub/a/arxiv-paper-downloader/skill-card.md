## Description:

Download 47+ essential AI/ML papers from arXiv with pre-curated collections for agent testing, autonomous agents, and large language models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubindashen](https://clawhub.ai/user/liubindashen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to download curated arXiv paper collections or specific arXiv IDs, saving PDFs and download metadata locally for AI/ML and agent evaluation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted arXiv IDs may write outside the selected download folder.

Mitigation: Use trusted arXiv IDs and a dedicated output directory; validate IDs and enforce output-directory containment before broad use.

Risk: The downloader writes PDFs and metadata locally.

Mitigation: Run it only where local file creation is expected, review overwrite behavior, and inspect outputs before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liubindashen/skills/arxiv-paper-downloader)

## Skill Output:

**Output Type(s):** [Files, JSON, Text]

**Output Format:** [PDF files with JSON-like download status objects and metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes PDFs and download_metadata.json under the selected output directory.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
