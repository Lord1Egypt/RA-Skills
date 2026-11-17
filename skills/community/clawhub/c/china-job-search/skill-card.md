## Description:

Searches Chinese recruitment platforms including BOSS Zhipin, Zhaopin, and 51job with filters for keyword, location, salary range, experience, and platform.

This skill is for research and development only.

## Publisher:

[jarryk](https://clawhub.ai/user/jarryk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and compare Chinese job listings by role, location, salary, experience, and platform. Results should be checked against original platform links because security evidence flags mixed live and synthetic data.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Search results may combine live data with synthetic fallback data, and documentation may overstate live platform searching.

Mitigation: Treat results as leads only, preserve source indicators where available, and verify important details on the original platform links.

Risk: The skill can create local JSON or CSV exports, caches, databases, and test files.

Mitigation: Run it in a controlled workspace and review generated files before sharing, retaining, or relying on them.

Risk: The skill performs third-party recruitment-site scraping behavior and includes scraping-circumvention guidance.

Mitigation: Review target site terms, robots rules, request rates, and organizational policy before enabling live requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jarryk/skills/china-job-search)
- [README](README.md)
- [API Reference](references/API_REFERENCE.md)
- [Quick Start](references/QUICK_START.md)
- [Deployment Guide](references/DEPLOYMENT_GUIDE.md)
- [Final Test Report](references/FINAL_TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Files]

**Output Format:** [Structured job listings as tables, JSON objects, or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform, job title, company, salary, location, experience, education, skills, publish time, and detail URL when available; some results may be synthetic fallback data.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
