## Description:

Builds personalized user behavior profiles by analyzing OpenClaw conversation history, then generates profile data and response guidance for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chefroger](https://clawhub.ai/user/chefroger)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent developers use this skill to analyze recent local conversation history, generate a personal behavior profile, and tailor future agent responses. It is most useful when the user intentionally wants local personalization and is willing to review stored profile data and SOUL.md updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent OpenClaw session history and local memory files, then stores truncated conversation content in its data folder.

Mitigation: Run collection manually first, inspect the generated data, and delete the data folder if the stored content is not acceptable.

Risk: The daily profile update script can persistently inject a user profile block into SOUL.md.

Mitigation: Back up SOUL.md before use, avoid enabling the cron job unless automatic updates are intended, and review or remove the injected profile block after each run.

Risk: MEMORY.md writing is disabled by default but can be enabled in code.

Mitigation: Keep MEMORY writing disabled unless each memory update will be reviewed before it is retained.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chefroger/skills/behavior-persona)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions and Python-generated local JSON, Markdown reports, and prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local profile data and can update SOUL.md when run manually or via user-configured cron.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
