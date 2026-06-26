## Description: <br>
Context Doctor helps an agent report current conversation context usage, token trends, large tool-output consumers, remaining capacity, and optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Context Doctor during long sessions to check conversation health, identify high token consumers, estimate remaining turns, and decide when to compact or reduce large tool outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads session-level metadata such as token counts, tool-call counts, and tool-output sizes. <br>
Mitigation: Use it in sessions where inspecting that metadata is acceptable, and keep reports focused on aggregate usage rather than conversation content. <br>
Risk: Broad trigger phrases or optional heartbeat checks could invoke diagnostics unintentionally. <br>
Mitigation: Prefer explicit invocations such as "context doctor" and leave automatic heartbeat checks disabled unless periodic diagnostics are desired. <br>
Risk: The skill may recommend compaction or output-limiting actions based on context health. <br>
Mitigation: Review recommendations before acting; Context Doctor diagnoses and advises but does not automatically compact. <br>


## Reference(s): <br>
- [Context Doctor on ClawHub](https://clawhub.ai/wavmson/ctx-doctor) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown diagnostic report with summary statistics, rankings, forecasts, and optimization suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic output based on session metadata and conversation structure; no automatic compaction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
