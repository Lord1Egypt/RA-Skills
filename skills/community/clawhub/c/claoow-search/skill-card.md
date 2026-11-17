## Description:

Connects agents to Claoow Search for batched intelligence task retrieval, URL scraping, submissions, marketplace search, and point-based purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biahd](https://clawhub.ai/user/biahd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to Claoow Search, process public intelligence tasks, submit generated insights, and search or purchase marketplace intelligence with human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run repeated scraping and point-spending actions with weak boundaries.

Mitigation: Use small Allow Once batches, avoid Allow Always modes, and require explicit confirmation before each purchase.

Risk: The skill makes outbound requests to URLs selected by Claoow tasks and has an incomplete network safety guard.

Mitigation: Test only in a network-restricted environment and avoid use from networks where access to internal services or sensitive endpoints is possible.

Risk: The skill submits scraped or typed content to Claoow and requires a Claoow API key.

Mitigation: Do not submit private data, local files, environment variables, or secrets; keep API keys session-scoped where possible.

## Reference(s):

- [Claoow Search on ClawHub](https://clawhub.ai/biahd/skills/claoow-search)
- [Publisher profile](https://clawhub.ai/user/biahd)
- [Claoow official homepage](https://claoow.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples and Python script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts may collect an API key, agent model name, batch size, category, and purchase authorization before network actions.]

## Skill Version(s):

1.0.15 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
