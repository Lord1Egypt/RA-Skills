## Description:

Anjuke/58 housing data collection and comparison pipeline that gathers rental listing and detail data, extracts contact phone numbers, resolves community coordinates with Amap poiInfo, calculates distance with haversine, and generates a sorted, filtered Excel comparison report.

This skill is for research and development only.

## Publisher:

[shiqixiangxiang-collab](https://clawhub.ai/user/shiqixiangxiang-collab)

### License/Terms of Use:

MIT

## Use Case:

External developers and analysts use this skill to collect and compare rental listings near a target location, including structured listing fields, contact data, coordinates, distance, and budget-filtered Excel output. The artifact describes personal housing research and learning use rather than production scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in local Chrome session over the Chrome DevTools Protocol.

Mitigation: Use a dedicated Chrome profile with no unrelated accounts or sensitive sessions, and keep the CDP port bound to the local machine.

Risk: The pipeline scrapes rental listings and contact phone numbers from third-party services.

Mitigation: Confirm that the intended scraping, reuse, and contact-data collection comply with applicable laws, platform terms, and user consent requirements before running it.

Risk: Generated JSON files, HTML captures, screenshots, and spreadsheets may contain personal contact information.

Mitigation: Store outputs in a controlled local directory, sanitize spreadsheets before sharing or opening in untrusted contexts, and delete files containing phone numbers when no longer needed.

Risk: Dependencies are specified with lower bounds rather than pinned exact versions.

Mitigation: Pin and review dependency versions before installation in shared, production, or sensitive environments.

Risk: The artifact describes avoiding verification challenges during scraping.

Mitigation: Do not use the pipeline to bypass access controls or anti-abuse systems; stop execution if verification or authorization requirements appear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shiqixiangxiang-collab/skills/anjuke-scraper)
- [README](README.md)
- [Amap](https://www.amap.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python script usage, JSON intermediate files, and Excel workbook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local JSON artifacts, captured HTML, optional verification screenshots, and a budget-filtered Excel workbook containing rental comparison rows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
