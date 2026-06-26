## Description: <br>
实时竞品监控虾 helps agents track competitor prices, reviews, promotions, and product launches, then produce alerts and periodic competitor reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Commercial and operations teams use this skill to monitor public competitor pricing, review signals, promotions, and launch activity, then summarize changes into alerts and weekly or monthly reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store competitor targets, product URLs, alert thresholds, owners, and price history in a local SQLite database. <br>
Mitigation: Confirm this storage is approved for the team and avoid adding sensitive internal notes to competitor records. <br>
Risk: Feishu alerts can expose competitor monitoring details to visible workspaces or channels. <br>
Mitigation: Use approved Feishu workspaces and channels and minimize sensitive information in alert messages. <br>
Risk: Replacing the simulated fetcher with live scraping can introduce platform compliance, rate-limit, cookie, proxy, and credential-storage risks. <br>
Mitigation: Review platform rules, rate limits, session handling, proxy use, and credential storage before enabling real collection. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/competitor-monitor-claw) <br>
- [Competitor Analysis Framework](references/competitor-analysis-framework.md) <br>
- [Industry Benchmarks](references/industry-benchmarks.md) <br>
- [Platform Scraping Rules](references/platform-scraping-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite price history; the bundled script uses simulated fetch data until replaced with approved collection logic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
