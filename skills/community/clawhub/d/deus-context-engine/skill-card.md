## Description: <br>
Context Engine maintains and restores conversation and project context across OpenClaw sessions, including active projects, pending tasks, notes, and summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deus-pandora](https://clawhub.ai/user/deus-pandora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep project continuity across sessions, restore previous context, switch between projects, and summarize active work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project memory persists across sessions and may retain sensitive notes, commands, or credentials if users save them. <br>
Mitigation: Avoid saving secrets, credentials, or sensitive commands; periodically review or remove the JSON files under /home/deus/.openclaw/workspace/memory/projects/. <br>


## Reference(s): <br>
- [Context Engine API Reference](references/API.md) <br>
- [ClawHub release page](https://clawhub.ai/deus-pandora/deus-context-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON command responses and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores project and session context in local JSON files under /home/deus/.openclaw/workspace/memory/projects/.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
