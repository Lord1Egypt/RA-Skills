## Description:

Log OpenClaw tasks to AgentNotes for SparkNotes rollups (success, failures, what happened). Use after cron jobs, channel replies, or multi-step sessions. Requires AGENTNOTES_API_KEY and AGENTNOTES_AGENT_ID env vars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattmerrick](https://clawhub.ai/user/mattmerrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using OpenClaw use this skill to record high-level task summaries, success or failure status, and multi-step run notes in AgentNotes for later SparkNotes rollups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational summaries may include sensitive user, customer, or business details.

Mitigation: Keep summaries high level and avoid secrets, private message contents, credentials, or regulated data.

Risk: The skill sends API-authenticated requests to a configurable AgentNotes endpoint.

Mitigation: Use a trusted HTTPS AGENTNOTES_BASE_URL for remote services, restrict access to the API key, and rotate the key if it is exposed.

Risk: The verification script prints an API key prefix in command output.

Mitigation: Avoid running verification in shared logs until key-prefix printing is removed; redact verification output when troubleshooting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mattmerrick/skills/agentnotes)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON-style configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus AGENTNOTES_API_KEY and AGENTNOTES_AGENT_ID; sends high-level summaries to the configured AgentNotes endpoint.]

## Skill Version(s):

0.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
