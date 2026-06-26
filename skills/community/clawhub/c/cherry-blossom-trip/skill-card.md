## Description: <br>
Plan cherry blossom viewing trips, including Japan sakura forecasts, Wuhan cherry gardens, and other blooming destinations with peak timing, viewing spots, and related travel booking support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to plan cherry blossom trips and retrieve real-time travel options, prices, points of interest, and booking links through the flyai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and trust a global third-party flyai CLI package. <br>
Mitigation: Review the @fly-ai/flyai-cli package before installation, install it only in an approved environment, and confirm `flyai --version` before running travel queries. <br>
Risk: Raw travel requests may be retained in a hidden local `.flyai-execution-log.json` file when file writes are available. <br>
Mitigation: Avoid entering passport, payment, account, or highly personal itinerary details unless logging is disabled or the local execution log is reviewed and deleted as needed. <br>
Risk: Travel prices, availability, and seasonal bloom information can become stale or misleading if the CLI is unavailable or returns incomplete data. <br>
Mitigation: Use only current flyai CLI output for user-facing results, retry or simplify failed requests, and clearly mark partial or unavailable data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/cherry-blossom-trip) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include detailUrl booking links, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence; artifact frontmatter reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
