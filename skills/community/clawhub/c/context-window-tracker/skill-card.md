## Description: <br>
Tracks and reports OpenClaw context window usage with a breakdown of token consumption, remaining capacity, and estimated turns left. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[99rebels](https://clawhub.ai/user/99rebels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect current session context usage, understand what is consuming tokens, and decide whether there is enough room to continue a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session metadata and transcripts to report context usage. <br>
Mitigation: Use it only in trusted ClawHub or OpenClaw environments, and avoid exposing reports that contain sensitive session-derived details. <br>
Risk: Some counts are estimates, including per-file system prompt breakdowns, turns remaining, and thinking token handling for some providers. <br>
Mitigation: Treat the report as operational guidance rather than an exact accounting record, and rely on provider or platform billing records for authoritative cost review. <br>


## Reference(s): <br>
- [Context Window Tracker Homepage](https://github.com/99rebels/context-window-tracker) <br>
- [Data Sources](references/data-sources.md) <br>
- [Thinking / Reasoning Tokens](references/thinking-tokens.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with compact and detailed context reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compact mode reports usage percentage, remaining turns, and cache data; detailed mode adds token breakdowns, trends, session statistics, and thinking status.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
