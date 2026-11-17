## Description:

Find nearby BnB stays when a user asks for local BnB or short-term rental options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to ask an agent for nearby BnB, short-term rental, or guesthouse options based on an authorized location, radius, result limit, and optional filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location data could expose precise user coordinates if retained or shared unnecessarily.

Mitigation: Request location only after user authorization and avoid retaining exact coordinates; blur coordinates when needed.

Risk: Provider availability or rate limits can prevent complete nearby-stay results.

Mitigation: Return clear provider or rate-limit errors and use short-term caching for similar location, category, and radius requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/bnb-stays)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text list of nearby stay results with standardized POI fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authorized location input and standardized response fields; default radius 5000 meters, default limit 20, maximum limit 50.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
