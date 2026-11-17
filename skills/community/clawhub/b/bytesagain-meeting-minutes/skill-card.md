## Description:

Record, manage, and export meeting minutes from the terminal, including decisions, action items, attendees, and formatted reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams can use this skill to run meeting records from the command line, capture decisions, assign action items, review prior outcomes, and export minutes as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting records may contain sensitive information stored as local files.

Mitigation: Use the skill only on trusted machines and review storage permissions before recording confidential meetings.

Risk: Markdown exports may write meeting content to a temporary system directory.

Mitigation: Review export paths and avoid exporting confidential meetings on shared machines until storage and export behavior are hardened.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/loutai0307-prog/skills/bytesagain-meeting-minutes)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text and Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores meeting records as local files and exports selected meetings to Markdown.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
