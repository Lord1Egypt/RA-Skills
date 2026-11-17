## Description:

Distill your bros -- from YOUR memories and descriptions. Captures how they talk, what makes them funny, their catchphrases, their energy. Feed it your own stories and observations. Self-learning -- gets more accurate with every description you share.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to build local, user-described profiles of friends, relatives, creators, or group-chat members and ask an agent to respond in the style captured from those memories. It supports profile-building, single-person style responses, and multi-profile group-chat simulations while keeping data local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plain-text local profiles may contain descriptions of real people.

Mitigation: Create and use profiles only on explicit user request, avoid sensitive private details, and delete a person's folder when the data is no longer needed.

Risk: Generated style responses could be confused with the real person being described.

Mitigation: Keep outputs clearly framed as simulations based on user-provided descriptions and do not use them to deceive others.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realteamprinz/skills/brother)
- [Publisher profile](https://clawhub.ai/user/realteamprinz)
- [README](artifact/README.md)
- [Bro profile template](artifact/BRO-PROFILE.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown profile content, JSONL observation logs, and conversational text replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles are stored as plain-text local files under ~/.brother-skill/bros/ when the agent follows the skill behavior.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
