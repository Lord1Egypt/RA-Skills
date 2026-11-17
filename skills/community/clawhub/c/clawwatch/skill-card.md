## Description:

Crypto and stock price watchlist tracker for adding or removing tracked assets, checking prices, setting price alerts, getting market overviews, and viewing the Crypto Fear & Greed Index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goarstne](https://clawhub.ai/user/goarstne)

### License/Terms of Use:


## Use Case:

External users and agents use ClawWatch to manage crypto and stock watchlists, fetch current prices, check configured alerts, export watchlist data, and summarize market status from CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and running an external clawwatch CLI package that is not pinned in the artifact.

Mitigation: Review the package before installation and prefer an isolated virtual environment.

Risk: API keys entered through shell commands may be exposed on shared machines.

Mitigation: Avoid entering API keys through shell history on shared systems and follow local secret-handling practices.

Risk: Watchlist, cached price data, and possibly configuration can persist under ~/.clawwatch.

Mitigation: Treat local ClawWatch files as user data and remove or protect them according to the deployment environment.

## Reference(s):

- [ClawWatch ClawHub page](https://clawhub.ai/goarstne/skills/clawwatch)
- [ClawWatch API Notes & Quirks](references/api-notes.md)
- [ClawWatch CLI Reference](references/cli-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise text or Markdown with inline shell commands and summaries of JSON CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use --json CLI output for agent parsing and natural-language summaries.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
