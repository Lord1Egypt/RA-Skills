## Description:

Onboard an agent to Bright Data for live web work, product integration, MCP setup, authentication, or direct REST access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to choose the correct Bright Data setup path for web search, scraping, structured data, MCP tooling, credentials, or REST integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands can execute mutable external code and make persistent CLI or agent-skill changes.

Mitigation: Prefer pinned, reviewable install paths; inspect the skill bundle before placing it in an active agent directory.

Risk: Credential setup can expose API keys through shell history, URL query strings, local files, or version control.

Mitigation: Avoid pasting secrets into command history or URLs, keep .env files out of version control, and rotate any key that may have been exposed.

Risk: The release security verdict is suspicious because setup steps require substantial trust in external code and account configuration.

Mitigation: Install only when Bright Data is trusted for the deployment context and review security guidance before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meirk-brd/skills/brightdata-agent-onboarding)
- [Bright Data documentation](https://docs.brightdata.com)
- [Bright Data LLM documentation index](https://docs.brightdata.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline shell commands, REST examples, environment variables, and routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference API keys, zones, CLI commands, MCP endpoints, and REST requests that require human review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
