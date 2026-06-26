## Description: <br>
Logs high-signal corrections, tool failures, feature requests, and recurring workflow lessons to lightweight local learning files, then promotes only repeated or durable lessons into project instructions when authorized. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amitpnyc](https://clawhub.ai/user/amitpnyc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill in OpenClaw or similar workspaces to capture useful corrections, failures, and workflow lessons while context is fresh. It helps teams improve agent behavior over time while keeping durable instruction changes intentional and reviewable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local learning notes may contain sensitive project context if captured too broadly. <br>
Mitigation: Redact secrets and private data, prefer summaries over raw output, and review .learnings before sharing or committing it. <br>
Risk: Promoting lessons into high-authority instruction or memory files can steer future agent behavior incorrectly if the lesson is temporary or misunderstood. <br>
Mitigation: Require explicit authorization for durable instruction edits and promote only repeated, durable lessons in distilled form. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amitpnyc/amitpnyc-self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown log entries and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Append-only local learning files by default; durable instruction or memory edits only when authorized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
