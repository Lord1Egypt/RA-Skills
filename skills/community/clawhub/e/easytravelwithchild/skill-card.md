## Description:

Helps parents plan family trips by searching family-friendly hotels and packages, comparing playground quality and supervision needs, and suggesting age- and personality-appropriate activities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dutxueyu](https://clawhub.ai/user/dutxueyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to prepare parent-friendly itineraries that compare family hotels, package options, child supervision needs, and nearby activities. The skill is aimed at weekend and holiday family trips where hotel amenities, child age, personality, budget, and booking data affect the recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented setup pulls mutable third-party code and installs a global CLI.

Mitigation: Review and pin the installer, remote skill revision, and flyai-cli version before installing.

Risk: Destination, dates, budget, family details, and search keywords may be sent to FlyAI/Fliggy and reflected in commercial booking links.

Mitigation: Use a least-privileged environment and avoid entering unnecessary sensitive family or travel details.

Risk: Hotel prices, package availability, and booking links can change after retrieval.

Mitigation: Review live booking pages and confirm prices, availability, and supervision details before purchase or travel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dutxueyu/skills/easytravelwithchild)
- [FlyAI skill installation repository](https://github.com/alibaba-flyai/flyai-skill)
- [Family hotel rating standards](artifact/references/hotel-rating-standards.md)
- [Child venue classification guide](artifact/references/venue-classification.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown itinerary card with comparison tables, price notes, booking links, and concise recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke shell scripts to retrieve current hotel and package data before producing recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
