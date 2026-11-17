## Description:

Elfa AI helps agents use the Elfa API for crypto social intelligence, market-context analysis, API integration guidance, and condition-based monitoring or trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nero-sensei](https://clawhub.ai/user/nero-sensei)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to query Elfa crypto social intelligence, generate Elfa API examples, and configure automated market monitoring workflows. Users should review and confirm any live trading or trade-capable automation before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help create persistent automated trading plans and place real trades.

Mitigation: Require manual confirmation before live orders or trade-capable Auto queries, use preview and validation first, and apply small sizes with conservative cooldowns and maxTriggers.

Risk: Credential handling for API keys, HMAC secrets, and agent secrets can expose sensitive access if secrets are passed through command-line options or logs.

Mitigation: Keep trade credentials restricted, read secrets from environment variables, and avoid passing secrets through command-line options such as --hmac-secret.

## Reference(s):

- [Elfa Documentation](https://docs.elfa.ai)
- [Elfa API](https://api.elfa.ai)
- [Elfa OpenAPI Swagger](artifact/references/swagger.json)
- [ClawHub Skill Page](https://clawhub.ai/nero-sensei/skills/elfa-ai)
- [ClawHub Publisher Profile](https://clawhub.ai/user/nero-sensei)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, credential setup guidance, and validation or preview steps for trade-capable workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
