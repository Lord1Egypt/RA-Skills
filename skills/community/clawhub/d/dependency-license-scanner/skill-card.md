## Description:

Summarizes declared licenses from a hand-built dependency list to support preliminary OSS license review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to summarize licenses explicitly listed alongside dependencies when preparing vendoring decisions or a draft SBOM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing or incorrect license declarations can make the summary misleading for compliance decisions.

Mitigation: Verify licenses against authoritative package metadata and license texts before relying on the summary.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hmahmadcs/skills/dependency-license-scanner)
- [SPDX License List](https://spdx.org/licenses/)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text, one dependency and declared license per line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses UNKNOWN when no license is provided; does not discover or validate licenses against package registries.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
