## Description: <br>
Gives OpenClaw agents persistent memory across conversations by organizing long-term facts, preferences, action items, learned patterns, and daily logs in workspace markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billyhetech](https://clawhub.ai/user/billyhetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an OpenClaw agent save, retrieve, summarize, and prune persistent user and project memory across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists user context and may automatically save personal details such as names, preferences, locations, family details, project context, or inferred patterns. <br>
Mitigation: Review the auto-save behavior before installation, limit what the agent is allowed to remember, and avoid storing sensitive data. <br>
Risk: Stored memory can become stale, duplicated, or larger than intended over time. <br>
Mitigation: Use the included memory hygiene guidance for deduplication, archiving, size limits, and user confirmation before overwriting conflicting facts. <br>


## Reference(s): <br>
- [Memory Hygiene Reference](references/memory-hygiene.md) <br>
- [ClawHub skill page](https://clawhub.ai/billyhetech/basic-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Text] <br>
**Output Format:** [Markdown memory entries and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates MEMORY.md and daily markdown logs in the local OpenClaw workspace; confirms saved entries and asks before deleting remembered topics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
