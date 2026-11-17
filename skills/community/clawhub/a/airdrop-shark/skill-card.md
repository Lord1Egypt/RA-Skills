## Description:

Airdrop Shark helps agents list potential crypto airdrop projects, show simulated eligibility checks, and manage local snapshot reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gztanht](https://clawhub.ai/user/gztanht)

### License/Terms of Use:

MIT

## Use Case:

Developers and crypto users use this skill to browse a locally maintained airdrop project list, run non-authoritative eligibility examples, and create local snapshot reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents simulated crypto eligibility and expected airdrop values in a way that could be mistaken for verified financial guidance.

Mitigation: Treat eligibility, snapshot, and value outputs as informational only and verify claims against official project channels before acting.

Risk: The skill advertises paid unlocks and crypto payment addresses without server evidence of a verifiable entitlement process.

Mitigation: Do not send crypto for the advertised unlock unless the publisher provides a verifiable payment and access process outside the skill output.

Risk: Snapshot reminders are written to local workspace data when the reminder command is used.

Mitigation: Run the skill from a trusted workspace and avoid sharing generated reminder data if project activity timing is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gztanht/skills/airdrop-shark)
- [Publisher profile](https://clawhub.ai/user/gztanht)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Project configuration](artifact/config/projects.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal text with tables, status lines, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eligibility results and value ranges are informational and non-authoritative; reminders are stored locally when created.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
