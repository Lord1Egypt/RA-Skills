## Description: <br>
Give your AI agent a soul -- beliefs, values, voice, and boundaries that persist across every conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to register with Live Neon, manage persistent agent identity, sync content sources, discover and review beliefs, and fetch identity prompts for use across LLM runtimes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived observations, user corrections, source quotes, and connected content may be sent to Live Neon for persistent analysis. <br>
Mitigation: Use an explicit opt-in policy, avoid secrets and personal data, and get user or administrator approval before running sync, observe, discovery, or heartbeat workflows. <br>
Risk: The bearer token provides organization-scoped API access. <br>
Mitigation: Store the token only in approved environment or secret storage, limit who can read it, and replace it if exposure is suspected. <br>
Risk: Proactive triggers and scheduled heartbeat workflows can submit observations repeatedly without a fresh prompt from the user. <br>
Mitigation: Disable or ignore proactive submissions unless recurring data flow has been approved, and review pending beliefs and responsibilities before promotion. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/liveneon/agent-soul-manager) <br>
- [Publisher profile](https://clawhub.ai/user/liveneon) <br>
- [Live Neon platform](https://persona.liveneon.ai) <br>
- [Live Neon homepage](https://persona.liveneon.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API request examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Live Neon token plus curl and jq; API responses can include identity, belief, responsibility, job, status, and prompt data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
