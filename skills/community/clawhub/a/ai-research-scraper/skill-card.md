## Description:

Summarizes recent AI research and product-development news from known AI and technology sources, with concise summaries and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kernix0421](https://clawhub.ai/user/kernix0421)

### License/Terms of Use:


## Use Case:

External users, developers, and product researchers use this skill to quickly review recent AI product-development and research updates from selected technology sources without reading full articles first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper invokes an external tavily-search skill to gather AI news results.

Mitigation: Install only a trusted and pinned tavily-search dependency, protect it from modification, and run this skill with limited filesystem and environment access.

Risk: The artifact includes translation scripts for Google, Baidu, Youdao, and Microsoft services that may send text to third-party providers if used.

Mitigation: Remove or disable unused translation scripts unless translation is required, and do not pass sensitive prompts, private notes, or proprietary content to translation providers.

Risk: The release has no license identifier in the server evidence or artifact documentation.

Mitigation: Confirm licensing and terms before commercial deployment or redistribution.

## Reference(s):

- [API Reference](references/api_reference.md)
- [Configured Websites](references/websites.txt)
- [ClawHub Skill Page](https://clawhub.ai/kernix0421/skills/ai-research-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown-style summaries with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are intentionally concise and depend on external search, news, and optional translation services.]

## Skill Version(s):

1.8.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
