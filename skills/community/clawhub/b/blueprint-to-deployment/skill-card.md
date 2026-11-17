## Description:

This skill helps agents turn planning outputs into deliverable workspace documentation, handoff maps, and deployment onboarding guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beachanger](https://clawhub.ai/user/beachanger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill after they have an agent blueprint, architecture plan, MVP boundary, or next actions and need the agent to write those assets into the target workspace. It also prompts the agent to provide a handoff map and continue into platform deployment intake for channels such as Telegram, Feishu, or Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to create or update planning and handoff documents in the wrong target workspace.

Mitigation: Confirm the target workspace path and intended file list before allowing edits.

Risk: Writing under a skills/ directory can change agent behavior if the generated content is later loaded as a skill.

Mitigation: Review and scan any generated skill files before enabling or deploying them.

Risk: The skill is written in Chinese, which can make review harder for teams that do not read Chinese.

Mitigation: Have a Chinese reader or trusted translation workflow review the skill behavior before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beachanger/skills/blueprint-to-deployment)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown guidance with workspace file paths and deployment intake steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create or update planning and handoff documents in a target agent workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
