## Description: <br>
Check current session's context window usage, including model name, estimated token usage, and context window utilization percentage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when users ask how much context remains, how full the context window is, or whether compaction should be considered. It summarizes session context usage and gives threshold-based guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The summary may reveal session metrics such as model name, token usage, and cache information if shared outside the conversation. <br>
Mitigation: Share context summaries only with intended recipients and avoid copying session metrics into public logs or reports unless needed. <br>
Risk: The skill depends on current session status data being available; without it, context usage could be incomplete. <br>
Mitigation: State when session status data is unavailable instead of estimating or inventing usage values. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes model name, used and total context tokens, cache information, and a status label when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
