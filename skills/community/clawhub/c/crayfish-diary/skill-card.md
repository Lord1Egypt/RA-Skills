## Description:

A WorkBuddy skill for quick diary and memo recording with automatic year/month/day directory organization, supporting Chinese and English start and stop triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[italks](https://clawhub.ai/user/italks)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to capture diary, memo, meeting-note, or todo content in an agent workspace and store it as organized Markdown entries with daily summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diary and memo content is saved as persistent local Markdown files and summarized in daily README files.

Mitigation: Use explicit start and stop phrases, avoid recording secrets, and review or delete generated diary files when they should not persist.

Risk: The included manual publish script can push an entire local skill directory to GitHub without an allowlist or confirmation.

Mitigation: Review or remove scripts/publish.sh unless publishing is intentional, and inspect exactly what it would commit and push before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/italks/skills/crayfish-diary)
- [README.md](artifact/README.md)
- [README_CN.md](artifact/README_CN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown diary entries, daily Markdown summaries, and brief text confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent local Markdown files organized by year, month, and day.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
