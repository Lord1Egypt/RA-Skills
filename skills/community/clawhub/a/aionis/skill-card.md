## Description: <br>
Connect OpenClaw to Aionis using write/context/policy/feedback memory loop APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cognary](https://clawhub.ai/user/Cognary) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to connect OpenClaw workflows to Aionis for long-term memory, cited context retrieval, memory-based tool routing, and feedback-driven policy adaptation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can start a persistent local Docker service and store Aionis credentials in local runtime files. <br>
Mitigation: Review the bootstrap before installing, keep runtime files private, avoid exposing admin tokens to routine agent tasks, and remove the container and volume when persistence is no longer needed. <br>


## Reference(s): <br>
- [Aionis OpenClaw integration documentation](https://doc.aionisos.com/public/en/integrations/04-openclaw) <br>
- [ClawHub Aionis skill page](https://clawhub.ai/Cognary/aionis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON request examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes request, commit, decision, and run IDs when present, plus the base URL and scope used for the run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and publish notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
