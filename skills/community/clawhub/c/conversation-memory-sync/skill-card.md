## Description: <br>
Automatically syncs and maintains detailed conversation logs and activity digests across agent sessions for persistent memory and context recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harvnk](https://clawhub.ai/user/Harvnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure persistent local memory logs and compact activity digests so agents can reference prior sessions, decisions, and commitments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can preserve private user and agent conversation history in persistent local Markdown files. <br>
Mitigation: Enable it only for intended agents and transcript paths, redact secrets or personal data before retention, and define deletion rules for generated logs. <br>
Risk: The artifact describes helper scripts that are not included in the submitted files. <br>
Mitigation: Obtain and review the referenced scripts before scheduling them or relying on generated memory files. <br>
Risk: Persisted memory logs may later be treated as trusted instructions by an agent. <br>
Mitigation: Treat generated logs as reference material and require agents to validate retrieved context against current user instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Harvnk/conversation-memory-sync) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated Markdown log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or maintains CONVERSATION_LOG.md and ACTIVITY_DIGEST.md when the referenced sync scripts are available and scheduled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
