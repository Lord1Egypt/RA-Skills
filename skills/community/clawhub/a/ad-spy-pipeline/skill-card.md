## Description: <br>
Automates competitor ad scraping from ForePlay or Anstrex, adapts creatives with AI, and syncs paused campaigns to Facebook Ads for e-commerce brands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harvnk](https://clawhub.ai/user/Harvnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce advertising teams use this skill to monitor competitor ads, generate brand-specific creative variants, and stage paused Facebook campaigns for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced storm_pipeline_agent.py script is not included for review. <br>
Mitigation: Obtain and review the full script source before running it with real API keys. <br>
Risk: The workflow can make Facebook ad-account changes using credentials and can be scheduled for unattended daily operation. <br>
Mitigation: Use least-privilege tokens, start with a test or low-risk ad account, set clear campaign-creation limits, keep ads paused, and require manual approval before enabling cron. <br>
Risk: Competitor creatives may be scraped and sent to an external AI provider. <br>
Mitigation: Confirm rights, platform terms, and data handling requirements before scraping or submitting creatives to external services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Harvnk/ad-spy-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes a scheduled advertising workflow that depends on external service credentials and manual review before activation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
