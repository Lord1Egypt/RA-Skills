## Description: <br>
Cloud memory for AI agents. Store, search, and recall context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aerialcombat](https://clawhub.ai/user/aerialcombat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to Ctxly cloud memory so they can register, store selected memories, search prior context, bootstrap startup context, and delete memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected memories and the API key are sent to and stored by ctxly.app. <br>
Mitigation: Install only when external cloud retention of agent context is intended, protect and rotate CTXLY_API_KEY if exposed, and periodically review or delete stored memories. <br>
Risk: Stored memories could include secrets, regulated data, or highly sensitive personal information. <br>
Mitigation: Do not store secrets, regulated data, or highly sensitive personal information; use purpose-built secret storage and data governance controls instead. <br>
Risk: Tweet-based verification may publish account-related verification content. <br>
Mitigation: Require explicit human approval before any tweet-based verification and use the provided claim URL path when tweeting is not appropriate. <br>


## Reference(s): <br>
- [MyMemory.bot on ClawHub](https://clawhub.ai/aerialcombat/cloud-memory) <br>
- [Ctxly service homepage](https://ctxly.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CTXLY_API_KEY for authenticated memory operations and documents rate limits of 100 requests per minute and 30 writes per minute.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
