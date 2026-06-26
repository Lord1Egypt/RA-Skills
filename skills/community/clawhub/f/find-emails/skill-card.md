## Description: <br>
Crawl websites locally with crawl4ai to extract contact emails, accepting multiple URLs and returning domain-grouped results for clear attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lukem121](https://clawhub.ai/user/Lukem121) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to crawl authorized websites or local markdown captures and extract public contact email addresses. It supports single-site and batch collection workflows where results need to stay grouped by source domain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill crawls websites and extracts public contact emails, which can create legal, privacy, or terms-of-service risk if used on sites the operator is not authorized to crawl. <br>
Mitigation: Use only on authorized sites, respect robots.txt and site terms, and keep page and depth limits conservative. <br>
Risk: Collected email lists may include irrelevant, stale, or unintended addresses. <br>
Mitigation: Review any saved email list before using it for outreach or downstream processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lukem121/find-emails) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable markdown-style text or JSON with per-domain email mappings and source paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted results to a user-specified output file; crawling scope is controlled by URL patterns, maximum depth, and maximum page settings.] <br>

## Skill Version(s): <br>
0.1.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
