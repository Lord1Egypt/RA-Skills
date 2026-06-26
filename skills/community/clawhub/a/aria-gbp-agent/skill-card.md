## Description: <br>
Agent identity package for Aria 📍 — installs SOUL.md, IDENTITY.md, and AGENTS.md into an OpenClaw workspace to give an AI agent its personality, name, and operational rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install Aria, a Google Business Profile specialist identity, into an OpenClaw workspace. The package replaces workspace identity and operating-rule files for agents that manage, audit, and optimize Google Business Profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package changes an agent workspace's identity and operating rules. <br>
Mitigation: Back up existing SOUL.md, IDENTITY.md, AGENTS.md, and BOOTSTRAP.md before installation. <br>
Risk: The workspace memory behavior can expose personal context if used in shared sessions. <br>
Mitigation: Avoid storing secrets in MEMORY.md or daily memory notes, and keep MEMORY.md restricted to direct main-session use. <br>
Risk: Calendar, Google Business Profile, posting, or other external actions may affect accounts outside the local workspace. <br>
Mitigation: Restrict external-action tools or require explicit approval before posting, messaging, calendar changes, or profile updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/aria-gbp-agent) <br>
- [Publisher profile](https://clawhub.ai/user/maverick-software) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown identity files with installation shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs SOUL.md, IDENTITY.md, and AGENTS.md into an OpenClaw workspace; no API keys or MCP tools are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
