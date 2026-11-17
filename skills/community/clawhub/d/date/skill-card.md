## Description:

Date.skill is a dating memory co-pilot that helps users record local notes, build profiles, refresh important details, and generate thoughtful date or gift ideas from manually entered observations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use Date.skill as a local dating-memory assistant to organize details they personally remember from dates, prepare for future conversations, and reflect on relationship patterns without scraping or transmitting another person's private data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive dating and relationship details may be stored in local plain-text files.

Mitigation: Keep the storage directory private, avoid shared devices and broad backup sync, and record only information you would be comfortable protecting locally.

Risk: Profiles may retain personal information after the relationship context has ended.

Mitigation: Delete the person's profile folder when the relationship ends or the notes are no longer needed.

Risk: The skill could be misused to support surveillance or manipulative dating behavior.

Mitigation: Use only manually provided memories from normal conversation, do not add data from private accounts or monitoring, and decline requests for stalking, manipulation, or coercion.

## Reference(s):

- [ClawHub Date.skill listing](https://clawhub.ai/realteamprinz/skills/date)
- [Publisher profile](https://clawhub.ai/user/realteamprinz)
- [README](artifact/README.md)
- [Date profile template](artifact/templates/DATE-PROFILE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown profiles, JSONL date logs, and concise plain-text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores relationship notes locally under ~/.date-skill/people/ as plain-text Markdown and JSONL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
