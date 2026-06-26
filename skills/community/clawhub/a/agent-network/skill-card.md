## Description: <br>
Agent Network is a multi-agent group chat collaboration system for structured communication, task delegation, decision voting, and group coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtimeschange](https://clawhub.ai/user/howtimeschange) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build local multi-agent collaboration workflows with group chat, mentions, task assignment, voting, and coordinator-managed message routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message routing, local persistence, task and decision mutation, and optional webhook forwarding can expose or act on sensitive collaboration data. <br>
Mitigation: Use only trusted local deployments unless group membership checks, authenticated agent identity, retention and deletion controls, mutation audit logging, and explicit webhook opt-in or redaction are added. <br>


## Reference(s): <br>
- [Advanced Usage Guide](artifact/references/ADVANCED.md) <br>
- [Database Schema](artifact/references/schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local SQLite-backed workflow guidance and CLI usage patterns.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
