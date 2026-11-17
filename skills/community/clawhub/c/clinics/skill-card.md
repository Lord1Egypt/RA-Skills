## Description:

Find nearby clinics. Invoke when user asks for a clinic near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to find nearby clinics from an authorized location, with optional radius, limit, and filters such as open_now, min_rating, or keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location data can expose sensitive user whereabouts if requested or retained unnecessarily.

Mitigation: Request location only for a nearby clinic search and avoid retaining precise coordinates; use coarse or short-lived location handling where practical.

Risk: Clinic information may be incomplete, outdated, or unsuitable for urgent medical decisions.

Mitigation: Ask users to verify clinic details through a trusted source before relying on them for medical needs.

Risk: External provider limits or outages may prevent complete nearby-clinic results.

Mitigation: Surface clear provider and rate-limit errors, and use short-lived caching within service limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/clinics)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Structured nearby-clinic results with clear error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-authorized location; supports radius, result limit, and optional filters.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
