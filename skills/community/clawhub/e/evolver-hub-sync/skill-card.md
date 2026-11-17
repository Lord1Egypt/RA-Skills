## Description:

Sync local Evolver genes and capsules with Evomap Hub using the A2A API endpoints, replacing the broken `evolver sync` CLI with working alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to sync local Evolver genes and capsules with Evomap Hub, inspect node information, and publish asset files through the Hub's A2A endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review is incomplete because only 3 of 4 components were fully inspected.

Mitigation: Request a complete inspection of the referenced script before installing; confirm why access to local Evomap credentials and the Hub is needed, and how the host limits that access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/147258xuan/skills/evolver-hub-sync)
- [Evomap Hub](https://hub.evomap.ai)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Console text and JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports sync and node information results; publish results depend on the supplied assets and Hub response.]

## Skill Version(s):

0.1.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
