## Description:

Barbaric Growth guides an autonomous agent through GitHub trend discovery, repository analysis, memory curation, OpenMOSS task logging, and StarOffice status updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jokerli530](https://clawhub.ai/user/jokerli530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and autonomous-agent operators use this skill to run a recurring research workflow that discovers GitHub projects, analyzes README content, records reusable knowledge, and logs follow-up tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The background EvoMap monitor includes an embedded bearer secret.

Mitigation: Remove or rotate the bundled credential and require user-provided credentials before running the monitor.

Risk: Autonomous task creation and memory updates can persist GitHub-derived findings without explicit approval.

Mitigation: Require user approval before OpenMOSS task creation and before writing GitHub-derived findings into persistent memory.

Risk: GitHub README content is external untrusted reference data.

Mitigation: Treat fetched README content as data for analysis, not as instructions for the agent to follow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jokerli530/skills/barbaric-growth)
- [Publisher profile: jokerli530](https://clawhub.ai/user/jokerli530)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and status/log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local state files, phase logs, and API task records when executed by an agent.]

## Skill Version(s):

1.2.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
