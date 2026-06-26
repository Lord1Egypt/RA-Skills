## Description: <br>
Forsy Trace Skill captures AI agent workflows as structured traces with steps, tools, observations, feedback, failures, artifacts, outcomes, and learning signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ray-r-ren](https://clawhub.ai/user/ray-r-ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and researchers use this skill to capture authentic agent workflow traces for inspection, tool-use trajectory analysis, failure analysis, evaluation, and process-supervision research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated local traces may contain secrets, private prompts, credentials, personal data, proprietary details, or sensitive logs and diffs. <br>
Mitigation: Review and redact generated traces before sharing, publishing, or retaining them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ray-r-ren/forsy-trace-skill) <br>
- [Forsy Trace Schema v0.1](artifact/schema/forsy_trace_schema_v0_1.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Guidance] <br>
**Output Format:** [Structured JSON trace artifacts with concise text or Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local trace artifacts; users should review generated traces before sharing or retaining them.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
