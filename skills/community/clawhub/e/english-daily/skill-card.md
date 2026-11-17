## Description:

Daily English learning with spaced repetition, a built-in A1-B2 word bank, daily new words, quiz modes, streak tracking, and level progression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External learners use English Daily to practice vocabulary through daily word prompts, spaced repetition review, quiz sessions, streak tracking, and A1-B2 level progression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unchecked profile names or profile text can influence persistent MEMORY.md learning records and scheduled prompts.

Mitigation: Use only with trusted users or tighten validation for names and profile fields; reject markdown delimiters, newlines, quotes, backticks, and instruction-like profile content.

Risk: The skill stores learning progress persistently in MEMORY.md and can configure optional scheduled OpenClaw reminders.

Mitigation: Review the stored profile block and scheduled reminders before installation or use, and remove the relevant MEMORY.md profile block to clear learning data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiajiaoy/skills/english-daily)
- [OpenClaw](https://openclaw.ai)
- [README](README.md)
- [Skill definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and MEMORY.md profile blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning prompts, quizzes, progress summaries, MEMORY.md update blocks, and optional OpenClaw reminder configuration.]

## Skill Version(s):

1.1.0 (source: release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
