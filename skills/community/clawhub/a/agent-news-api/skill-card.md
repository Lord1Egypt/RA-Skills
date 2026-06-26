## Description: <br>
A set of free and premium AI enriched global news streams for agents, provided by agentnewsapi.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentnewsdev](https://clawhub.ai/user/agentnewsdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to fetch delayed free news signals, paid real-time news signals, WebSocket firehose updates, and API credit balances for event monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a raw Solana private key for onboarding and paid API access. <br>
Mitigation: Prefer a pre-created AGENT_NEWS_API_KEY, avoid exposing SOLANA_PRIVATE_KEY unless required, and keep wallet credentials scoped to this use case. <br>
Risk: Premium news fetches and long-running streams can consume paid credits without strong point-of-use controls. <br>
Mitigation: Set external budget or approval controls, check credit balance before high-frequency use, and monitor premium stream duration. <br>
Risk: Payment setup depends on the configured API URL and deposit address. <br>
Mitigation: Verify the API URL and deposit address independently before funding or allowing autonomous premium access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentnewsdev/agent-news-api) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses from CLI/API calls, with setup guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require AGENT_NEWS_API_KEY; premium onboarding can use SOLANA_PRIVATE_KEY and paid SOL credits.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata; artifact frontmatter/package.json report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
