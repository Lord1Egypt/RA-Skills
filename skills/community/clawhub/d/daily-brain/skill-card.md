## Description:

Daily Brain provides daily brain-training prompts across logic, math, memory, and word challenges with adaptive difficulty, answer explanations, and local streak tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request a daily brain-training puzzle, submit an answer for explanation, view training statistics, or reset local progress. The skill is aimed at lightweight self-guided cognitive practice, not professional assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores training progress locally inside the skill directory.

Mitigation: Installers should preserve or back up data/progress.json when moving the skill, and should expect answer submissions to update that local file.

Risk: The reset command clears local streaks, answer history, and achievements.

Mitigation: Run node scripts/reset.js --confirm only when progress deletion is intended.

Risk: Optional daily push scheduling can create recurring prompts.

Mitigation: Review and approve any cron or scheduler setup separately before enabling daily reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosmofang/skills/daily-brain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-oriented text prompts for HTML puzzle, answer, and statistics cards, plus command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads bundled puzzle data and writes local progress state in data/progress.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
