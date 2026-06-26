## Description: <br>
Daily self-improvement for AI agents that fetches curated Agent Vitamins briefs and turns relevant items into owner-approved recommendations and implementation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[menkesu](https://clawhub.ai/user/menkesu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent owners use this skill to keep an AI agent current with ecosystem practices by reviewing daily briefs, selecting relevant improvements, and applying approved changes intentionally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external MCP package and Agent Vitamins service for brief content. <br>
Mitigation: Install only if the publisher and service are trusted, and prefer pinning or verifying the npm package before use. <br>
Risk: The full brief workflow uses a subscription API token. <br>
Mitigation: Store the token in secure configuration or environment storage and avoid exposing it in prompts, logs, or shared files. <br>
Risk: Recommended improvements may change agent behavior, files, memory, or configuration. <br>
Mitigation: Require the agent to show exact commands, changed files, memory updates, and rollback steps before approving execution. <br>


## Reference(s): <br>
- [Agent Vitamins](https://agentvitamins.com) <br>
- [ClawHub release page](https://clawhub.ai/menkesu/agent-vitamins) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with concise recommendations, setup JSON snippets, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full briefs require a subscription API token; proposed improvements require owner approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
