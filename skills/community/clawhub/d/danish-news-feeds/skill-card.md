## Description: <br>
Aggregates Danish news RSS sources into category-based unified feeds with deduplication, source ranking, and RSS 2.0 output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and run a Danish RSS aggregation workflow that publishes category-specific feeds for readers, websites, or downstream news monitoring tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A helper script weakens HTTPS protections by disabling certificate and hostname verification. <br>
Mitigation: Avoid using aggregate_feeds.py until TLS verification is restored; prefer reviewed code paths that preserve HTTPS verification. <br>
Risk: Generated feeds republish third-party RSS content. <br>
Mitigation: Review source terms and treat generated RSS entries as third-party content before public redistribution. <br>
Risk: Cron jobs or detached containers can create ongoing background fetching. <br>
Mitigation: Enable scheduled refresh only when continuous polling is intended and monitor the configured feed list. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Broedkrummen/danish-news-feeds) <br>
- [Comprehensive Danish RSS Feeds](artifact/comprehensive_feeds.md) <br>
- [Feed Configuration](artifact/feeds.json) <br>
- [Generated Combined RSS Example](artifact/combined_danish_news.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, RSS/XML files] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python scripts, JSON configuration, and RSS 2.0 XML output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public third-party RSS content, deduplicates articles, ranks sources by configured authority, and can be scheduled for recurring refreshes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
