## Description: <br>
Generates structured system prompts from Live Neon agent beliefs and responsibilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register Live Neon identities, manage beliefs and responsibilities, review generated identity changes, and build markdown system prompts for use with LLM agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects agents to a remote, persistent prompt-identity system that can store conversation-derived observations. <br>
Mitigation: Use it only when users and administrators have opted in, avoid sending sensitive conversation details or private source content, and review observations before processing them into identity changes. <br>
Risk: Bulk approvals, consensus changes, or scheduled heartbeats can alter agent or organization prompt identity through remote state changes. <br>
Mitigation: Require human review before bulk approvals, group or organization consensus changes, and automated heartbeat workflows. <br>
Risk: The Live Neon token grants access to organization-scoped identity and prompt-management APIs. <br>
Mitigation: Protect LIVE_NEON_TOKEN as a secret, scope access to trusted agents, and rotate or re-register tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liveneon/agent-prompt-builder) <br>
- [Live Neon Agent platform](https://persona.liveneon.ai) <br>
- [Live Neon homepage](https://liveneon.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plain markdown system prompts and Live Neon API workflow guidance; requires Live Neon API access and LIVE_NEON_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
