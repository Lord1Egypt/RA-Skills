## Description:

An arXiv paper search engine designed specifically for scientific researchers. Supports dual modes: "Broad Search" and "Top-Tier Strict Filtering", along with relevance and date sorting. Automatically checks for duplicates, downloads PDFs, and maintains a local CSV paper library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tartykisser](https://clawhub.ai/user/tartykisser)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and AI practitioners use this skill to search arXiv for AI papers, filter results by broad relevance or top-tier venue acceptance, download selected PDFs, and maintain a local deduplicated paper library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact arXiv, download PDFs, and create or append files in a local paper_list library.

Mitigation: Use a controlled workspace, monitor disk usage for large downloads, and review saved files before relying on them.

Risk: Top-tier filtering depends on arXiv comment metadata and agent review of venue matches.

Mitigation: Review selected papers and venue acceptance claims before using the results for formal research decisions.

Risk: Runtime behavior depends on Python packages used for arXiv access and HTTP downloads.

Mitigation: Pin and review dependencies before installation in shared or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tartykisser/skills/ai-paper-researcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown summary with shell command usage and JSON results from the arXiv CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or append local CSV records and save downloaded PDF files in a paper_list library.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
