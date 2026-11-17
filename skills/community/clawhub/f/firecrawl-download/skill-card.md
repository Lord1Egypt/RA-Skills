## Description:

Download an entire website as local files, including markdown, screenshots, or multiple formats per page, by combining site mapping and scraping into organized local directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to save websites or documentation sections as organized local files for offline reference, bulk content extraction, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an unpinned npm-resolved Firecrawl CLI.

Mitigation: Use it only when the Firecrawl package source is trusted, and review the command before execution.

Risk: Bulk downloads can write many files to disk while skipping confirmation.

Mitigation: Set explicit target domains, include or exclude paths, and page limits before running automated downloads.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Configuration]

**Output Format:** [Markdown guidance with Firecrawl CLI command examples and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces nested local directories under .firecrawl/ and may include markdown, links, screenshots, or multiple files per page.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
