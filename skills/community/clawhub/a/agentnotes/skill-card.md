## Description: <br>
Log OpenClaw tasks to AgentNotes for SparkNotes rollups (success, failures, what happened). Use after cron jobs, channel replies, or multi-step sessions. Requires AGENTNOTES_API_KEY and AGENTNOTES_AGENT_ID env vars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattmerrick](https://clawhub.ai/user/mattmerrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send concise OpenClaw task summaries, step logs, and failure status to AgentNotes for hourly and daily SparkNotes rollups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task summaries, log messages, run metadata, and errors are sent to an external AgentNotes service. <br>
Mitigation: Log only sanitized high-level summaries and avoid secrets, tokens, personal data, raw transcripts, regulated data, and detailed stack traces. <br>
Risk: The skill requires a sensitive AgentNotes API key and agent identifier in environment configuration. <br>
Mitigation: Store credentials in the OpenClaw skill environment, restrict access to local configuration files, and rotate the API key if it is exposed. <br>
Risk: The verification command displays a prefix of the API key and sends a test log entry. <br>
Mitigation: Run verification only in private terminals and avoid shared CI logs until the key-display behavior is fixed. <br>
Risk: The installer replaces an existing local AgentNotes skill directory. <br>
Mitigation: Review the install script and back up local modifications before upgrading over an existing installation. <br>


## Reference(s): <br>
- [ClawHub Agentnotes listing](https://clawhub.ai/mattmerrick/agentnotes) <br>
- [Publisher profile](https://clawhub.ai/user/mattmerrick) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime helper scripts send API requests to AgentNotes and print short status strings or run identifiers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
