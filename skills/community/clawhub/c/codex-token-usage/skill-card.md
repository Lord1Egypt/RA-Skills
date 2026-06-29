## Description: <br>
Summarizes Codex token usage from local Codex Desktop or CLI session JSONL logs for a requested reporting period. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helenalhq](https://clawhub.ai/user/helenalhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit local Codex token usage over a defined period, including totals, cached input, output, reasoning output, peak day, and busiest week. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script reads local Codex session logs, which may contain sensitive workflow metadata. <br>
Mitigation: Run it only against logs you intend to analyze, and use --codex-home to limit the log directory when needed. <br>
Risk: Reports are computed from local JSONL token_count events and may be incomplete if the selected Codex log directory is missing, partial, or outside the requested date range. <br>
Mitigation: Choose an explicit date range and Codex home path for audits that need reproducible totals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helenalhq/codex-token-usage) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown table or structured JSON, with shell commands for invoking the bundled report script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports aggregate token metrics for a selected local date range and can localize Markdown labels in English or Chinese.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
