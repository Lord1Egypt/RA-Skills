## Description:

Proactively updates a concise session summary every 15 turns or on tool loops to manage context size and preserve key decisions and progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabatech-dev](https://clawhub.ai/user/sabatech-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long-running OpenClaw sessions concise by periodically updating SESSION-STATE.md with recent progress, decisions, blockers, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent rolling summaries may retain user preferences, decisions, or workspace context beyond the immediate turn.

Mitigation: Use the skill only where SESSION-STATE.md is isolated to the intended workspace and user.

Risk: Summaries could capture secrets, prompt-like instructions, or sensitive personal data if agents are not constrained.

Mitigation: Instruct agents to exclude secrets, prompt-like instructions, and sensitive personal data from retained summaries.

Risk: Automatic state maintenance may occur without the level of consent some teams require for persistent project memory.

Mitigation: Review the skill before installation and enable it only for workflows where persistent session memory is expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sabatech-dev/skills/alfred-rolling-summarization)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with a SESSION-STATE.md rolling summary template and prompt instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are intended to stay under 500 characters total, with each section under 200 characters.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact Version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
