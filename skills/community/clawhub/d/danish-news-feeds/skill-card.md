## Description:

Danish News Feeds aggregates Danish RSS sources into category-based RSS feeds for combined, national, regional, sports, business, technology, and English-language Denmark news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

External users, developers, and operators can use this skill to configure or run a Danish RSS aggregation workflow that combines multiple news sources into category-based RSS outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feed-integrity weaknesses may expose users to untrusted or modified feed content.

Mitigation: Review the skill before installation, keep TLS verification enabled, and treat feeds that cannot use verified HTTPS as untrusted or remove them.

Risk: Generated XML may include externally sourced article content.

Mitigation: Serialize XML with a safe XML library and validate output before publishing feeds.

Risk: Unpinned dependencies and scheduled execution can make behavior change over time.

Mitigation: Pin dependencies, use a fixed release version, and add the cron job only when scheduled background refreshes are intended.

Risk: Documentation may overstate current behavior or differ from the scripts.

Mitigation: Align documentation with the implemented scripts before relying on advertised feed counts, refresh behavior, or hosting steps.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/broedkrummen/skills/danish-news-feeds)
- [Skill documentation](artifact/SKILL.md)
- [Feed catalog](artifact/comprehensive_feeds.md)
- [Feed configuration](artifact/feeds.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python code, JSON configuration, shell commands, and generated RSS XML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow writes RSS XML feed files and can be scheduled by cron when intentionally enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
