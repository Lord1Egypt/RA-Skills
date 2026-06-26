## Description: <br>
Trace and debug a single OpenClaw conversation session. Use when you need to analyze openclaw logs, correlate them with the current session context, inspect workflow steps, summarize module activity, or produce a structured trace report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leoluo0814](https://clawhub.ai/user/leoluo0814) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use ClawTrace to inspect one OpenClaw conversation session, correlate JSON logs with current session context, and produce an evidence-based Markdown trace report with timing, module, warning, error, and optimization details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw logs and current session context can include sensitive conversation content and operational details. <br>
Mitigation: Use the skill only in workspaces where the agent is authorized to inspect local logs and review generated reports before sharing them outside the workspace. <br>
Risk: Trace reports could expose raw operational details if generated without summarization. <br>
Mitigation: Follow the artifact guidance to produce summarized Markdown and avoid outputting raw logs, raw JSON, or verbatim log lines. <br>


## Reference(s): <br>
- [ClawTrace on ClawHub](https://clawhub.ai/leoluo0814/clawtrace) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown trace report with overview metrics, module summary, step table, and evidence-based suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should avoid raw logs, raw JSON, and verbatim log lines; uncertain values should be marked as Unknown, Estimated, or Not available.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
