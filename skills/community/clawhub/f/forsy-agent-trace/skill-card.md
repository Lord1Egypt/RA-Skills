## Description: <br>
Forsy Agent Trace helps agents capture authentic work as structured traces with steps, tools, observations, feedback, failures, artifacts, outcomes, and learning signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forsy](https://clawhub.ai/user/forsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and agent researchers use this skill to document real AI-agent workflows as structured local JSON traces for inspection, failure analysis, tool-use trajectory analysis, evaluation construction, and dataset preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trace files can record sensitive task details, including private prompts, customer data, internal URLs, credentials, or proprietary content. <br>
Mitigation: Review trace files before sharing them and redact or omit sensitive data unless it is intentionally kept private. <br>
Risk: A trace can overstate evidence quality if reconstructed steps, validation level, or confidence are described too strongly. <br>
Mitigation: Use the documented trace mode, validation level, and confidence fields conservatively, and only describe activity that actually occurred or can be reconstructed from reliable evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/forsy/forsy-agent-trace) <br>
- [Forsy publisher profile](https://clawhub.ai/user/forsy) <br>
- [Forsy Trace Schema v0.1](schema/forsy_trace_schema_v0_1.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Guidance, Files] <br>
**Output Format:** [Structured JSON trace files with supporting Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local trace records and optional supporting artifact references; users should review and redact sensitive content before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
