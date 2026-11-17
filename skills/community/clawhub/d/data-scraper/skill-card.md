## Description:

Web page data collection and structured text extraction

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers, analysts, and operators use this skill to fetch public web pages, extract readable text or structured data, monitor page changes, and save scrape results for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs, including local, private-network, or cloud metadata addresses.

Mitigation: Restrict use to public, non-sensitive pages and block local file URLs, private network ranges, and cloud metadata endpoints before execution.

Risk: URLs, headers, cookies, or scraped content can be exposed through command history, process listings, stdout, or generated workspace event files.

Mitigation: Avoid real bearer tokens, session cookies, signed URLs, and sensitive pages; inspect and delete generated event files when scraped data may be sensitive.

## Reference(s):

- [Data Scraper ClawHub Skill Page](https://clawhub.ai/mupengi-bot/skills/data-scraper)
- [mupengi-bot ClawHub Publisher Profile](https://clawhub.ai/user/mupengi-bot)

## Skill Output:

**Output Type(s):** [text, markdown, json, csv, shell commands, files]

**Output Format:** [Plain text or HTML on stdout, structured JSON/CSV/Markdown data, and workspace event JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl-based fetching and may write scrape-result event files for downstream workflow consumers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
