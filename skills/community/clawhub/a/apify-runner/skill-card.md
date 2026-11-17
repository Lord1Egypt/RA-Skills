## Description:

Run any Apify Actor to scrape web data, including Instagram, TikTok, Reddit, and Twitter, with actor discovery, quality filtering, probe testing, batched execution, and result collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duxj4520](https://clawhub.ai/user/duxj4520)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to choose and run Apify Actors for web and social media data extraction from natural-language scraping requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify credentials may be exposed when tokens are passed on the command line or stored in configuration files.

Mitigation: Use a limited-scope Apify token through the APIFY_TOKEN environment variable, avoid command-line token arguments, and keep configuration files out of version control with restrictive file permissions.

Risk: Targets and scraping inputs may be sent to third-party Apify Actors.

Mitigation: Confirm the selected Actor and its destination before full execution, especially when target lists are sensitive.

Risk: Scraping jobs can run at scale through batching and may collect unintended data if inputs are too broad.

Mitigation: Run probe tests first, use narrow target lists and limits, and review output before using it downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duxj4520/skills/apify-runner)
- [Apify Actor documentation](https://apify.com/{actor_id}.md)
- [Apify Actor page](https://apify.com/{actor_id})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save scraped results as JSON when an output path is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
