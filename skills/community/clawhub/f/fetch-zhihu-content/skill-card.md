## Description:

Downloads Zhihu articles, answers, and question pages by URL, renders them with Playwright, and saves extracted content as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucky-dreamer](https://clawhub.ai/user/lucky-dreamer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch public Zhihu content from article, answer, or question URLs and save each page as a local Markdown file for offline reading or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper can open web addresses through local browser automation with weakened browser protections.

Mitigation: Use only trusted Zhihu URLs in an isolated environment and avoid running it near sensitive local services.

Risk: Redirects or loose URL parsing could take the browser outside the intended Zhihu content scope.

Mitigation: Enforce a strict Zhihu URL allowlist and validate redirects before broader use.

Risk: The browser launch configuration uses default --no-sandbox and includes anti-detection behavior.

Mitigation: Remove default --no-sandbox where possible and clearly disclose or remove anti-detection behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucky-dreamer/skills/fetch-zhihu-content)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands]

**Output Format:** [Markdown files with terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One output Markdown file per successfully fetched Zhihu URL.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
