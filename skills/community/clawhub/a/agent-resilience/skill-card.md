## Description: <br>
Agent resilience patterns for surviving context loss, capturing critical details, and self-improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinian5216](https://clawhub.ai/user/xinian5216) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve important task state, recover from context loss, and apply resilience practices during long or complex sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause broad conversation details or raw messages to be written to persistent local memory files. <br>
Mitigation: Use it only when persistent local task memory is desired, and define rules to skip secrets, personal data, customer data, credentials, and proprietary material. <br>
Risk: Persisted memory files may retain sensitive or stale context longer than intended. <br>
Mitigation: Routinely inspect, rotate, or delete the memory files and clear task state when starting unrelated work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xinian5216/agent-resilience) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, files] <br>
**Output Format:** [Markdown guidance and local memory file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files such as SESSION-STATE.md and working-buffer.md when applied by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
