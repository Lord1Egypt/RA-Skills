## Description:

Fetches, filters, and analyzes real-time news from 28 technology, finance, AI, social, podcast, and essay sources, then prepares Simplified Chinese briefings and deep-dive reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run daily scans, topic-specific news searches, and multi-source briefings. It produces Simplified Chinese Markdown reports with source links, timestamps, heat signals, summaries, and optional deeper analysis from fetched article text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad outbound scraping and browser automation can visit untrusted third-party pages.

Mitigation: Run the skill in a restricted network environment and disable deep-fetch mode for untrusted or unnecessary sources.

Risk: Generated reports are derived from untrusted web content and may contain inaccurate or misleading claims.

Mitigation: Treat reports as untrusted summaries and verify important claims against the original source links before acting on them.

Risk: Dependency or browser automation behavior may change how external pages are fetched.

Mitigation: Pin dependencies, review updates before deployment, and keep generated report files out of sensitive directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/content-system-news-aggregator-skill)
- [Publisher profile](https://clawhub.ai/user/abigale-cyber)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Simplified Chinese Markdown reports with source links and inline command examples; fetch scripts may emit JSON as intermediate data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under reports/YYYY-MM-DD/; deep-fetch mode can add downloaded third-party article text for richer summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
