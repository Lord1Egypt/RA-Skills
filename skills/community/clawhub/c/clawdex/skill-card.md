## Description:

Security check for ClawHub skills powered by Koi. Query the Clawdex API before installing any skill to verify it's safe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wearekoi](https://clawhub.ai/user/wearekoi)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to check ClawHub skill verdicts through Koi's Clawdex service before installing new skills or reviewing already installed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Koi's external Clawdex service and may disclose checked skill names, including installed skill names during an audit loop.

Mitigation: Review which skill names will be sent before running checks, and avoid querying names that reveal sensitive internal usage.

Risk: Clawdex verdicts may be incomplete security input for unknown or unaudited skills.

Mitigation: Treat verdicts as one review signal and perform manual review before installing unknown skills.

## Reference(s):

- [Clawdex by Koi on ClawHub](https://clawhub.ai/wearekoi/skills/clawdex)
- [Koi](https://www.koi.ai/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable verdict interpretation and review guidance for benign, malicious, or unknown Clawdex API results.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
