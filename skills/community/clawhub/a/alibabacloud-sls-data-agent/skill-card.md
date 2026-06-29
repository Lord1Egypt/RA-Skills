## Description: <br>
Invokes Alibaba Cloud SLS DataAgent to answer natural-language SLS data questions with data acquisition, processing, analysis, conclusions, and visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to ask natural-language questions about Alibaba Cloud SLS projects and receive structured analysis, charts, and reusable session context. It is suited for log analysis, SLS query assistance, dashboard help, and LoongCollector-related investigation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions and SLS project context are sent to Alibaba Cloud using the user's configured cloud credentials. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials limited to the required DataAgent actions and SLS scope, and avoid including secrets, regulated data, or unrelated private content in questions. <br>
Risk: An analysis may target the wrong SLS project or logstore if configuration values are missing or stale. <br>
Mitigation: Confirm the SLS project, region, logstore, and digital employee before execution; stop and ask the user when required values are missing. <br>
Risk: Operational recommendations or generated analysis may be incomplete, misleading, or based on an empty DataAgent response. <br>
Mitigation: Base conclusions only on returned content between the answer delimiters, retry once with the same thread if the answer is empty, and review any operational action through normal change-management processes. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [SLS DataAgent API Reference](references/api-reference.md) <br>
- [STAROps RAM Policy Notes](references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is pipe-delimited text or JSONL events from the SLS DataAgent script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing pipe mode includes a THREAD line, optional DataAgent URL, and answer delimiters for parsing follow-up context.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
