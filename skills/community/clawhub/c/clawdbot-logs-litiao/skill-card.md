## Description: <br>
Analyze Clawdbot logs and diagnostics. Use when the user asks about bot performance, response times, errors, session stats, token usage, API costs, or wants to debug slow responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local Clawdbot journal logs, session statistics, token usage, API costs, gateway status, and common error patterns while diagnosing slow or failing bot responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Clawdbot logs and session JSONL files can contain private conversation text, token usage, cost data, model details, and operational errors. <br>
Mitigation: Review and redact diagnostic output before sharing it, and avoid extracting recent message content unless it is specifically needed for troubleshooting. <br>
Risk: Commands that inspect user services and session files can expose machine-specific operational state. <br>
Mitigation: Run the commands only in trusted local environments and limit outputs to the minimum detail needed to diagnose the issue. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/clawdbot-logs-litiao) <br>
- [Publisher profile](https://clawhub.ai/user/litiao1224) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and summarized diagnostic output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostics may include sensitive local log and session details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
