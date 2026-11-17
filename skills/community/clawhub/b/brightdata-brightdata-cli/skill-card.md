## Description:

Guides agents in using the Bright Data CLI to scrape websites, search web engines, extract structured platform data, manage proxy zones, and check account budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose and run Bright Data CLI commands for web scraping, SERP search, structured data pipelines, account status checks, and CLI configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports high-impact unverified installers and floating package execution.

Mitigation: Review installation commands before use and prefer a pinned, verified Bright Data CLI installation method.

Risk: The skill can guide authentication to Bright Data, and credentials may persist locally after login.

Mitigation: Authenticate only on trusted machines and remove stored credentials when they are no longer needed.

Risk: The skill may send user-supplied URLs or platform data requests through Bright Data services.

Mitigation: Avoid sending secrets, private or internal URLs, or sensitive personal data unless the user has authorization.

## Reference(s):

- [Bright Data CLI command reference](references/commands.md)
- [Bright Data CLI pipeline types reference](references/pipelines.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown, Code]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to produce JSON, CSV, NDJSON, screenshots, or files when invoking Bright Data CLI commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
