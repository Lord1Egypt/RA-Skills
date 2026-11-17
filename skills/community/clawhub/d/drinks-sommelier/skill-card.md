## Description:

Expert sommelier for beers and wines. Load when the user asks for advice, talks about, or sends images related to beers or wines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johell1ns](https://clawhub.ai/user/johell1ns)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to evaluate available beers or wines from a shelf, menu, list, or image against their recorded taste preferences and receive scored recommendations with rationale, pairings, and products to avoid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps local notes about the user's beer and wine preferences.

Mitigation: Install only when local preference tracking is acceptable, and ask the agent not to save preferences for one-off recommendations.

Risk: The skill relies on web searches for product details, so recommendation quality depends on available and accurate online information.

Mitigation: Review the sourced product details and treat unavailable or uncertain product information as a limitation rather than a recommendation basis.

Risk: The skill references preference data files that may be absent in the packaged artifact.

Mitigation: Review or create the missing preference files before use, and initialize the taste profile before relying on recommendations.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/Johell1NS/drinks-sommelier/tree/main/skills/drinks-sommelier)
- [ClawHub skill page](https://clawhub.ai/johell1ns/skills/drinks-sommelier)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown recommendations with scored rankings and concise rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preference indices, food pairings, products to avoid, clarifying questions, and updates to local preference notes.]

## Skill Version(s):

0.1.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
