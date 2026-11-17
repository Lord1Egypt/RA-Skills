## Description:

Main orchestrator for the OpenAlgernon personal study system; it starts study sessions, briefs available materials and recent activity, handles /algernon help, and routes study commands to the appropriate sub-skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniovfranco](https://clawhub.ai/user/antoniovfranco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to coordinate OpenAlgernon study sessions, load study context, inspect due-card status, and route study intents to specialized OpenAlgernon sub-skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenAlgernon study memory and recent study logs when a study session starts or when materials are requested.

Mitigation: Install it only where the agent is intended to access that local study state, and review the memory briefing before acting on it.

Risk: Broad study-related phrasing may be interpreted and routed to another OpenAlgernon skill.

Mitigation: Use explicit /algernon commands or clear study-mode commands when possible, and confirm unexpected routing before continuing.

## Reference(s):

- [Algernon Orchestrator ClawHub listing](https://clawhub.ai/antoniovfranco/skills/algernon-orchestrator)
- [Publisher profile](https://clawhub.ai/user/antoniovfranco)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with inline bash commands and command-routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read OpenAlgernon memory files, recent conversation logs, and sqlite study state when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
