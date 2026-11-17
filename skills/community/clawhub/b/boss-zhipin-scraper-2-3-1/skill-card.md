## Description:

Searches BOSS Zhipin job listings through a dedicated browser, exports job and salary data, and summarizes results for job-market research.

This skill is for research and development only.

## Publisher:

[eatmoreduck](https://clawhub.ai/user/eatmoreduck)

### License/Terms of Use:

MIT

## Use Case:

Individual job seekers and researchers use this skill to collect BOSS Zhipin listings by keyword, city, and filters, then review salaries, job descriptions, and aggregate hiring trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional login-state import can copy browser cookies beyond BOSS Zhipin into a persistent scraper profile.

Mitigation: Sign in manually using the dedicated browser; use login-state import only with informed consent.

Risk: Persistent job data and exported CSV files may expose sensitive search information or require cautious opening.

Mitigation: Protect the local results directory and inspect exported CSV files before opening them in spreadsheet software.

Risk: Installing unpinned scraper code could introduce unexpected behavior.

Mitigation: Pin and review the installation source before running the scraper.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/eatmoreduck/skills/boss-zhipin-scraper-2-3-1)
- [ClawHub publisher profile](https://clawhub.ai/user/eatmoreduck)

## Skill Output:

**Output Type(s):** [JSON, CSV, Markdown, Shell commands]

**Output Format:** [Structured job-listing files and text summaries with job-market prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Job listings can include plaintext salary and job descriptions; CSV export and aggregate analysis are optional.]

## Skill Version(s):

2.3.1 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
