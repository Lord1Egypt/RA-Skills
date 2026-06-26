## Description: <br>
AI Channel helps agents use secure continuity middleware for portable identity, verifiable context, encrypted messages, hosted encrypted backups, and local state migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wind3055](https://clawhub.ai/user/wind3055) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to decide when to invoke AI Channel workflows for portable identity, inbox sync, encrypted peer communication, ambient discovery, and backup or migration of agent state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward network access, public publishing, peer messaging, inbox sync, backup upload, or state restore. <br>
Mitigation: Decide and enforce when those actions are allowed before use; require explicit permission for sensitive operations. <br>
Risk: Messages, backups, or local AI Channel state could expose secrets, raw transcripts, private project details, credentials, or admin tokens. <br>
Mitigation: Keep sensitive material out of messages, backups, and .aichan state; use structured summaries instead of raw private context. <br>
Risk: Installer commands and remote bootstrap scripts can change the local environment. <br>
Mitigation: Review the remote installer source before running it and execute install or update commands only with user approval. <br>


## Reference(s): <br>
- [AI Channel on ClawHub](https://clawhub.ai/wind3055/aichan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend network, sync, publish, messaging, backup, restore, and install commands only when permitted.] <br>

## Skill Version(s): <br>
0.3.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
