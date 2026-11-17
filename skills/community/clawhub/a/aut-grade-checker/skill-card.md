## Description:

Classifies vehicle driving-automation levels L0–L5 from driving-task, event-response, operating-domain, and takeover inputs, returning JSON decision support for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and vehicle-compliance reviewers use this offline decision-support tool to estimate a driving-automation level before preparing a compliance report. Its rule mapping and conclusions require human review against the official standard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared tool access is broader than the offline classifier needs and conflicts with its no-executable claim.

Mitigation: Review before installing; prefer running the Python script with explicit arguments and do not grant network, write, or shell authority unless separately justified.

Risk: An unverified rule mapping could lead to a misleading automation level in a compliance decision.

Mitigation: Manually verify the GB/T 40429-2021 rule mapping and review the output before using it for compliance decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/aut-grade-checker)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON with a level, responsibility, warnings, and status code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Incomplete inputs can produce a conservative level with warnings; invalid inputs produce an error. The bundled script and documentation report older versions than this release.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; bundled documentation and script report older versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
