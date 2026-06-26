## Description: <br>
Manage A2A sessions with other OpenClaw agents for agent-to-agent communication, capability queries, coordination, and information exchange. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saullockyip](https://clawhub.ai/user/saullockyip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, inspect, reuse, and delete OpenClaw A2A sessions, then send messages through the built-in sessions_send tool using the required sender and reply routing format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared agent-to-agent messages can expose conversation context or confidential information if used carelessly. <br>
Mitigation: Use private repositories, verify partner agent IDs before pairing, avoid sending secrets or confidential data, and review any watch or cron setup before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/saullockyip/a2a-chatting) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with shell commands and message-format examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output includes agent lists, session IDs, session metadata, and status messages.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
