## Description:

Blind-playtest a game build from a first-time player's perspective, then verify a complete run on its target runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT-0

## Use Case:

Game developers and QA practitioners use this skill to assess first-time playability, diagnose player-facing issues, and record evidence that a game build can be completed on its target runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan evidence is incomplete because some referenced files were absent from the bundle.

Mitigation: Review the unresolved references and scan the complete bundle before relying on the security assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/worldwonderer/skills/game-qa)
- [Publisher profile](https://clawhub.ai/user/worldwonderer)
- [Blind playtest method](artifact/references/blind-playtest-method.md)
- [Runtime QA contract](artifact/references/qa-contract.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [A Markdown playtest report and a JSON complete-run verification record, with practical QA guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The verification record covers six runtime checks and states any untested limitations.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
