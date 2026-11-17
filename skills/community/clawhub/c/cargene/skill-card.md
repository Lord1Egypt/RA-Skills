## Description:

Helps agents research Japanese car history, confirmed parts fitment, and car services in Japan with source-linked answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soraozawa](https://clawhub.ai/user/soraozawa)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers, enthusiasts, and service researchers use this skill to look up Japanese vehicle generations, developers, sales figures, compatible aftermarket parts, and service shops in Japan, with sources for the findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms are sent to CarGene's public API.

Mitigation: Use non-sensitive queries; omit private addresses, account details, secrets, and unnecessary personal context.

Risk: An empty lookup may be mistaken for proof that no vehicle, part, or service exists.

Mitigation: Present empty results as unresearched or unavailable in CarGene, not as definitive absence.

## Reference(s):

- [CarGene](https://car-gene.com)
- [CarGene skill on ClawHub](https://clawhub.ai/soraozawa/skills/cargene)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Source-linked answers in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [An empty lookup means the subject may not have been researched yet.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
