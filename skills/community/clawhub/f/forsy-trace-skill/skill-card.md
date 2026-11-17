## Description:

Forsy Trace Skill helps agents capture authentic work as structured local traces with steps, tool use, observations, feedback, failures, artifacts, outcomes, and learning signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ray-r-ren](https://clawhub.ai/user/ray-r-ren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and evaluators use this skill to record real AI-agent workflows for inspection, process-supervision research, failure analysis, tool-use trajectory analysis, workflow auditing, dataset examples, and reusable agent work experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated traces may capture private prompts, credentials, customer data, internal URLs, or proprietary content.

Mitigation: Review trace.json and related artifacts before sharing; redact or exclude sensitive fields and files.

Risk: A trace may overstate what happened if the agent records steps without reliable evidence.

Mitigation: Record only live activity or reconstruction from reliable logs, files, conversation history, tool outputs, or artifacts, and lower confidence where evidence is incomplete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ray-r-ren/skills/forsy-trace-skill)
- [Forsy Trace Schema v0.1](schema/forsy_trace_schema_v0_1.json)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [Local JSON trace files following the Forsy Trace Schema v0.1, with optional structured artifact metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Traces should be reviewed and redacted before sharing.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
