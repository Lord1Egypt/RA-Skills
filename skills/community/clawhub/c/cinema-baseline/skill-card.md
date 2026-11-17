## Description:

Provides a baseline of Chinese cinemas keyed by standard cinema codes, with pre-aligned HaHa ticketing-channel identities for local cinema matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rascalagnt001](https://clawhub.ai/user/rascalagnt001)

### License/Terms of Use:

MIT-0

## Use Case:

Cinema Agent developers and operators use the baseline to identify and normalize Chinese cinemas across local records and the HaHa ticketing channel. Unmatched cinemas remain available for manual review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The publisher's right to distribute the cinema dataset is unconfirmed.

Mitigation: Verify with the publisher that the dataset is intended to be public before production use.

Risk: The declared gene.json integrity hash does not match the supplied file.

Mitigation: Ask the publisher to correct the hash and verify package integrity before relying on the release.

## Reference(s):

- [Cinema Baseline on ClawHub](https://clawhub.ai/rascalagnt001/skills/cinema-agent)

## Skill Output:

**Output Type(s):** [Structured data, Guidance]

**Output Format:** [JSON cinema records and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes 13,276 baseline cinemas, 11,454 with pre-aligned HaHa identities; unmatched records require review. Rule-based confidence and MGeo scores use different scales.]

## Skill Version(s):

1.0.0 (source: ClawHub release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
