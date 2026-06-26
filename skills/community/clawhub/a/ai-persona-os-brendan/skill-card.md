## Description: <br>
AI Persona OS helps OpenClaw agents create and operate a local persona workspace with SOUL.md profiles, memory files, heartbeat checks, preset assistants, persona galleries, and optional automation templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to bootstrap and maintain an OpenClaw workspace with persona identity, memory, operating rules, status checks, escalation patterns, and guided persona selection. It is intended for local assistant customization and recurring operational hygiene rather than model training. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores broad personal and work context in local workspace memory files and can resurface or modify that context during assistant operation. <br>
Mitigation: Keep secrets, credentials, sensitive HR/legal/financial details, and unnecessary personal information out of USER.md and MEMORY.md; review archive, prune, rewrite, and memory changes before approval. <br>
Risk: Optional cron, heartbeat override, Discord or gateway configuration, email/calendar access, and channel scans can broaden what the agent reads or changes. <br>
Mitigation: Require the agent to show exactly what it will read or change before enabling optional automation or external integrations, and confirm each external action explicitly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/earlvanze/ai-persona-os-brendan) <br>
- [Author homepage](https://jeffjhunter.com) <br>
- [AI Persona Method](https://aipersonamethod.com) <br>
- [SOUL.md Maker reference](references/soul-md-maker.md) <br>
- [Heartbeat automation reference](references/heartbeat-automation.md) <br>
- [Never-forget protocol reference](references/never-forget-protocol.md) <br>
- [Proactive playbook reference](references/proactive-playbook.md) <br>
- [Security patterns reference](references/security-patterns.md) <br>
- [Security note](SECURITY_NOTE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, generated workspace files, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core setup writes local Markdown workspace state under ~/workspace; cron jobs and gateway changes are optional and require explicit user approval.] <br>

## Skill Version(s): <br>
1.6.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
