## Description:

Dailylog records daily wins, challenges, and learnings with streak tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-productivity agents use Dailylog to capture plans, habits, reflections, reminders, weekly reviews, searchable activity, and local log exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal notes, plans, reminders, and exports are stored as plaintext under ~/.local/share/dailylog.

Mitigation: Avoid secrets or regulated data, use restrictive local file permissions or umask, and handle exported JSON/CSV/TXT files as sensitive copies of the log history.

## Reference(s):

- [Dailylog ClawHub skill page](https://clawhub.ai/ckchzh/skills/dailylog)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text CLI output and local log/export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores timestamped plaintext logs and exported JSON/CSV/TXT files under ~/.local/share/dailylog.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
