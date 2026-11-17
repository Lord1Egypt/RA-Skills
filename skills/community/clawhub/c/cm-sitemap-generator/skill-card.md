## Description:

Generate XML sitemaps by crawling a website or scanning local files, with page discovery, local lastmod dates, and optional robots.txt generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to generate sitemap.xml content from a live website or a local HTML/Markdown tree, and optionally create a robots.txt file that references the sitemap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler disables HTTPS certificate verification.

Mitigation: Use the skill only for intended public or trusted targets until TLS verification is fixed; avoid sensitive internal sites and untrusted networks.

Risk: Redirects may move crawling outside the intended same-domain boundary.

Mitigation: Review crawl targets and results before relying on them, and avoid targets where redirect behavior is unknown.

Risk: The --output and --robots options write files in the workspace.

Mitigation: Check output paths before execution and review generated sitemap.xml and robots.txt files before publishing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated sitemap output may be XML, text, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write sitemap.xml and robots.txt files when output options are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and script __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
