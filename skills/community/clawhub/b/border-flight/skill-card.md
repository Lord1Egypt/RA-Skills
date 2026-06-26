## Description: <br>
Search cross-border flights, international departures, visa-required routes, and related overseas travel options using Fliggy-powered flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and agent users use this skill to collect international route parameters, run flyai travel searches, and return booking-linked Markdown results with visa reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install an unpinned global npm CLI dependency. <br>
Mitigation: Verify or install @fly-ai/flyai-cli in an approved environment before use, and review the package source and version according to local dependency policy. <br>
Risk: Travel search prompts can contain sensitive itinerary details, and the skill may retain query logs in .flyai-execution-log.json. <br>
Mitigation: Avoid entering passport numbers or sensitive identity details in ordinary travel prompts, and inspect or delete .flyai-execution-log.json when local retention is not desired. <br>
Risk: If the CLI is unavailable or results lack booking links, the agent could provide stale or unsourced travel guidance. <br>
Mitigation: Only present results returned by flyai with detailUrl booking links; stop or report the retrieval failure when the CLI cannot provide valid results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/border-flight) <br>
- [Output templates and parameter collection](references/templates.md) <br>
- [International flight playbooks](references/playbooks.md) <br>
- [Failure recovery fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and booking links, with inline shell commands for setup, search, retry, or fallback steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data; user-facing results should include detailUrl booking links and should not expose raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
