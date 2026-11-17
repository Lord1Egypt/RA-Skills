## Description:

Searches arXiv by keyword or submitted-date range, fetches papers by arXiv ID or URL, converts papers into Markdown and PDF files, and maintains daily topic archives with summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elio040208](https://clawhub.ai/user/elio040208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical readers use this skill to find arXiv papers, ingest a specific paper into local Markdown and PDF artifacts, and generate review-oriented summaries or recurring topic archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, date windows, and paper IDs are sent to arXiv when the skill searches or fetches papers.

Mitigation: Use the skill only when sharing those queries with arXiv is acceptable, and avoid including sensitive information in search keywords.

Risk: Paper text and generated Markdown can contain untrusted instructions or misleading claims.

Mitigation: Treat fetched paper content as source material, ground summaries in generated files, and review claims against paper.md or the original PDF before relying on them.

Risk: Broad topic syncs can download multiple PDFs and Markdown files into the workspace.

Mitigation: Use narrow topic limits and monitor workspace disk usage during repeated or backfill syncs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elio040208/skills/arxiv-paper-reader)
- [Search Result Handling](references/search-usage.md)
- [Summary Template](references/summary-format.md)
- [Topic configuration example](references/topics.example.json)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands, plus generated JSON, Markdown, PDF, and summary files in the workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result files, paper artifacts, metadata JSON, topic run manifests, and daily archive summaries are written under user-selected or default workspace artifact directories.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
