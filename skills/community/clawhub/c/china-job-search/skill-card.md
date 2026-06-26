## Description: <br>
Searches Chinese recruitment platforms including BOSS Zhipin, Zhaopin, and 51job with keyword, location, salary, and experience filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarryk](https://clawhub.ai/user/jarryk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search and compare job listings in the Chinese recruitment market from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job-search keywords and locations may be sent to third-party recruitment sites. <br>
Mitigation: Use non-sensitive search terms and review the target platform behavior before running networked searches. <br>
Risk: Search results may include simulated or fallback listings. <br>
Mitigation: Treat results as unverified and confirm any job listing through the official recruitment platform before acting on it. <br>
Risk: The skill can save or export job-search artifacts locally. <br>
Mitigation: Review export settings, avoid storing sensitive searches, and delete generated JSON or CSV files when no longer needed. <br>
Risk: Some artifact guidance discusses anti-bot or scraping-evasion techniques. <br>
Mitigation: Respect recruitment-site terms, robots.txt, and rate limits; disable or review scripts that rotate user agents or attempt bypass behavior. <br>


## Reference(s): <br>
- [API Reference](references/API_REFERENCE.md) <br>
- [Deployment Guide](references/DEPLOYMENT_GUIDE.md) <br>
- [Quick Start](references/QUICK_START.md) <br>
- [Final Summary](references/FINAL_SUMMARY.md) <br>
- [Final Test Report](references/FINAL_TEST_REPORT.md) <br>
- [BOSS Zhipin](https://www.zhipin.com) <br>
- [Zhaopin](https://sou.zhaopin.com) <br>
- [51job](https://search.51job.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Structured job-search results as JSON or Markdown-style tables, with optional command-line usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include platform, title, company, salary, location, experience, education, skills, URL, publish time, company size, and company type.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
