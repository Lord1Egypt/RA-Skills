## Description:

AI Persona OS helps OpenClaw agents set up and operate a persistent persona workspace with identity, memory, heartbeat checks, security guidance, escalation routines, templates, and optional scheduling support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to configure an OpenClaw workspace with reusable persona files, memory conventions, operating rules, and optional automation templates for ongoing agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace memory files may store sensitive user or project context over time.

Mitigation: Keep credentials and sensitive material out of ~/workspace, review generated memory files, and use the skill only in workspaces with clear ownership controls.

Risk: The included security-audit workflow may surface credential-like strings in command output.

Mitigation: Review audit results locally and avoid sharing raw output unless it has been checked for secrets.

Risk: Optional scheduled reports or heartbeat automation can expose private workspace summaries if sent to unverified destinations.

Mitigation: Prefer local, non-delivering cron jobs and enable delivery integrations only after verifying destination, audience, and access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earlvanze/skills/ai-persona-os-brendan)
- [Publisher profile](https://clawhub.ai/user/earlvanze)
- [Soul MD Maker reference](references/soul-md-maker.md)
- [Heartbeat automation reference](references/heartbeat-automation.md)
- [Never forget protocol reference](references/never-forget-protocol.md)
- [Proactive playbook reference](references/proactive-playbook.md)
- [Security patterns reference](references/security-patterns.md)
- [Author homepage](https://jeffjhunter.com)
- [AI Persona Method](https://aipersonamethod.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core setup writes local Markdown workspace files under ~/workspace; optional cron and gateway actions require explicit user opt-in.]

## Skill Version(s):

1.6.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
