## Description: <br>
CrawlHub helps agents use the CrawlHub REST API to discover endpoints, authenticate requests, extract structured public data from social and messaging platforms, and interpret results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolflabs88](https://clawhub.ai/user/wolflabs88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data teams use this skill to integrate CrawlHub into research, monitoring, market intelligence, brand intelligence, and public social-data collection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires CrawlHub credentials or tokens for authenticated API use. <br>
Mitigation: Keep credentials out of prompts and logs, store tokens securely, refresh them through the documented flow, and use least-privilege team API keys. <br>
Risk: Data extraction from social and messaging platforms can create compliance, authorization, or platform-policy risk. <br>
Mitigation: Use the skill only for authorized public-data collection and review each collection workflow against applicable legal, privacy, and platform requirements. <br>
Risk: Execution endpoints and subscription or billing endpoints can incur costs or change account state. <br>
Mitigation: Require explicit approval before execution at scale, subscription changes, API-key changes, team changes, profile updates, write operations, or delete operations. <br>
Risk: Rate limits, retries, and upstream failures can cause duplicate requests, incomplete results, or unexpected billing. <br>
Mitigation: Check plan limits before running jobs, monitor request logs and billing transactions, use idempotent request identifiers for retries, and apply exponential backoff for busy or failing endpoints. <br>


## Reference(s): <br>
- [CrawlHub ClawHub page](https://clawhub.ai/wolflabs88/crawlhub-reseller) <br>
- [CrawlHub API base URL](https://api.thecrawlhub.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline HTTP examples, shell commands, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint-selection guidance, authentication steps, retry guidance, error handling, and result interpretation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
