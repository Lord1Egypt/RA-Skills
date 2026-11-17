## Description:

Use when the user asks for Gestalt mode or wants terse, substantive, low-filler collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwgoldie](https://clawhub.ai/user/dwgoldie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users apply Gestalt to configure language models and coding agents for direct, substantive collaboration with explicit uncertainty handling and disciplined use of memory when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: In coding-agent deployments, the skill may encourage agents to create repo-local memory, task, or communication files.

Mitigation: Review AGENTS.md and GEMINI.md before deployment and remove or constrain the memory guidance if repository-local notes are not desired.

Risk: Direct, terse collaboration guidance may make responses more forceful than expected for some workflows.

Mitigation: Pair the skill with local project instructions that define escalation, review, and communication expectations for the target team.

## Reference(s):

- [ClawHub Gestalt Skill Page](https://clawhub.ai/dwgoldie/skills/gestalt)
- [AGENTS.md Standard](https://agents.md/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown prompt and agent instruction files with an optional shell sync script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No hidden execution, network access, credential handling, or destructive behavior reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
