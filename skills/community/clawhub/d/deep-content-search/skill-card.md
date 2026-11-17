## Description:

Searches and extracts content from WeChat public articles, Zhihu, Douban, Toutiao, Baijiahao, Weibo, and Bilibili column sources, returning platform-labeled text or JSON results.

This skill is for research and development only.

## Publisher:

[lyl340321](https://clawhub.ai/user/lyl340321)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to search Chinese content platforms, extract full WeChat or Zhihu Daily article text where available, or return source-labeled summaries and links from platforms with anti-scraping limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and pasted URLs may be sent to Chinese search and content services.

Mitigation: Avoid private links, secrets, internal hostnames, and sensitive research terms; review queries and URLs before running the skill.

Risk: Weak WeChat URL validation can cause requests to unintended internal or arbitrary URLs.

Mitigation: Validate WeChat URLs strictly, block private-network destinations and redirects, and restrict execution to expected public hosts.

Risk: The --output option can overwrite user-chosen paths.

Mitigation: Confirm output paths before execution and avoid accepting arbitrary output paths from untrusted input.

Risk: Some platform results are summaries or links only because anti-scraping controls block full extraction.

Mitigation: Treat partial results as leads, preserve source labels, and verify important claims against the original source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyl340321/skills/deep-content-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text, JSON, or Markdown file output from a Python CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include platform labels and per-channel counts; the CLI can write output to a user-specified path with --output.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
