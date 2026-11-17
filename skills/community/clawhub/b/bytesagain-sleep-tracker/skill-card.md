## Description:

Sleep Tracker helps agents provide sleep analysis, improvement tips, schedule planning, environment optimization, nap guidance, and sleep journaling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill through an agent to log sleep and health habits, review sleep timing and streaks, plan bedtimes and naps, and receive general wellness suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles health-related sleep and wellness information and can produce advice that users may treat as medical guidance.

Mitigation: Present outputs as general wellness guidance and direct users to qualified professionals for persistent sleep problems or medical concerns.

Risk: Sleep journal entries may contain sensitive personal information and one bundled script stores them in /tmp/sleep_journal.txt.

Mitigation: Avoid recording sensitive medical details and prefer a private per-user storage location before using the journal workflow.

Risk: Security evidence flags inconsistent scope and under-disclosed plaintext local logging.

Mitigation: Review the storage behavior and disclose local log locations before deployment or use.

## Reference(s):

- [Sleep Tracker on ClawHub](https://clawhub.ai/loutai0307-prog/skills/bytesagain-sleep-tracker)
- [loutai0307-prog ClawHub profile](https://clawhub.ai/user/loutai0307-prog)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local sleep or wellness logs when the bundled shell scripts are executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
