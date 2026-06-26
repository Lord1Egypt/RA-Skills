## Description: <br>
Competitor Watch monitors public competitor websites, product pages, pricing, content, and social presence, then produces tiered diffs and alerts about meaningful changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[audsmith28](https://clawhub.ai/user/audsmith28) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Product, GTM, marketing, and founder teams use this skill to monitor public competitor pages, pricing, changelogs, and announcements so they can review meaningful changes without manually checking each source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured monitoring can store public webpage snapshots, raw diffs, and reports locally. <br>
Mitigation: Install only when local storage of monitored public page content is acceptable, and periodically review or clean ~/.config/competitor-watch according to retention needs. <br>
Risk: Frequent checks or broad competitor lists can create operational load or unwanted traffic patterns. <br>
Mitigation: Review configured URLs, tiers, check intervals, rate limits, and cron or heartbeat scheduling before enabling recurring monitoring. <br>
Risk: Competitor webpage text and generated alerts may contain untrusted content. <br>
Mitigation: Treat fetched page text, diffs, and alert summaries as data for human review, not as agent instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/audsmith28/competitor-watch) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/audsmith28) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON configuration, stored text snapshots, structured diff JSON, and alert summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local configuration and stores monitored public page snapshots, diffs, change logs, and reports under ~/.config/competitor-watch.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
