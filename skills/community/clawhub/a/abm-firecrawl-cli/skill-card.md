## Description:

Helps agents choose and run Firecrawl CLI commands to scrape pages, crawl sites, discover URLs, search and scrape results, and extract structured data from websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and research agents use this skill to collect website content with Firecrawl CLI workflows. It is suited for single-page scraping, multi-page crawling, URL discovery, web search with scraping, autonomous data gathering, and structured extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to scrape, crawl, search, and extract content from websites, which can collect data outside the user's authorization or intended scope.

Mitigation: Use the skill only for authorized sites and data, keep crawl limits and extraction scope narrow, and avoid collecting personal or sensitive data without a valid basis.

Risk: Firecrawl commands require FIRECRAWL_API_KEY, and exposing this key can compromise the user's Firecrawl account.

Mitigation: Treat FIRECRAWL_API_KEY as a secret, keep it in the environment rather than outputs or shared files, and avoid including it in prompts, logs, or copied command transcripts.

Risk: The skill instructs agents to read local product marketing context before asking questions, which can influence prompts or outputs sent to Firecrawl.

Mitigation: Read local product marketing context only when it is needed for the task and the user is comfortable with that context influencing external Firecrawl requests or results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-firecrawl-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/mariokarras)
- [Firecrawl](https://firecrawl.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs, extraction method labels, extracted page content, crawl result sections, and Firecrawl API key setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
