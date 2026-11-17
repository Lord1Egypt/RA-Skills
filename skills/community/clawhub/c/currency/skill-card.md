## Description:

Your personal Currency assistant. Track, analyze, and manage all your travel planning needs from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use Currency to record, review, search, and export travel planning notes from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises broad currency, weather, routing, booking, and reminder assistance but behaves primarily as a local travel-entry logger.

Mitigation: Treat entries and outputs as personal notes, and verify currency, weather, routing, booking, or reminder decisions with authoritative tools before relying on them.

Risk: Travel plans, booking notes, routes, budgets, and journal entries may be retained in plaintext local files.

Mitigation: Avoid storing sensitive itinerary or booking details unless local retention is acceptable, and review or delete the local data directory when needed.

Risk: CSV exports can carry spreadsheet-opening risks when user-entered values are later opened in spreadsheet software.

Mitigation: Inspect exports before sharing and open CSV output in tools or modes that do not evaluate spreadsheet formulas.

## Reference(s):

- [Currency on ClawHub](https://clawhub.ai/ckchzh/skills/currency)
- [Publisher Profile](https://clawhub.ai/user/ckchzh)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Command-line text with local log and export files in JSON, CSV, or TXT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores plaintext travel entries under ~/.local/share/currency.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
