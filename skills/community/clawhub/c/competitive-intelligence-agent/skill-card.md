## Description:

Monitors competitors across pricing, social media, online reviews, and product changes, then distills updates into a concise weekly briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcvanstad](https://clawhub.ai/user/marcvanstad)

### License/Terms of Use:

MIT-0

## Use Case:

External business, product, pricing, marketing, and strategy teams use this skill to monitor configured competitors and receive alerts or weekly briefings about pricing, social media, reviews, product changes, hiring, and news. The generated reports support competitive response planning and market-positioning decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraped pages, reviews, and social posts are untrusted external content that may be inaccurate, misleading, or adversarial.

Mitigation: Treat collected content only as evidence, add safeguards against instruction-following from external text, and review generated recommendations before acting on them.

Risk: Scraping configured sources may violate site terms, laws, or customer commitments if enabled without approval.

Mitigation: Confirm each source can be monitored before enabling collectors, API access, proxies, screenshots, or scheduled sweeps.

Risk: Delivery and scraping configuration can expose Slack, email, Telegram, API, or proxy secrets if placeholders are replaced directly in files.

Mitigation: Store secrets outside committed configuration, restrict delivery-channel access, and rotate any credential that is exposed.

Risk: Reports, raw data, and screenshots may retain sensitive company or competitive information.

Mitigation: Minimize retained data, enforce the configured retention window, and restrict access to output directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcvanstad/skills/competitive-intelligence-agent)
- [README](README.md)
- [Analysis configuration](reference/config/analysis.yaml)
- [Delivery configuration](reference/config/delivery.yaml)
- [Scraping configuration](reference/config/scraping.yaml)
- [Target configuration](reference/config/targets.yaml)
- [Full sweep script](reference/scripts/full-sweep.sh)
- [Weekly report template](reference/templates/weekly_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON data files, screenshots, shell command examples, and YAML configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports scheduled or on-demand competitive intelligence sweeps, alerts, and briefings from configured public sources.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
