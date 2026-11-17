## Description:

Recommend SEO-friendly, brandable domain names for an AI product idea, then verify current availability before returning candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daviddonecn](https://clawhub.ai/user/daviddonecn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, marketers, and developers use this skill to turn an AI product concept or keyword into a concise shortlist of brandable, SEO-aware domains with current availability status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain availability can change between lookup and registration, and DNS-clear results do not prove a domain is unregistered.

Mitigation: Confirm exact domains through a registrar or marketplace immediately before presenting final availability, and label weaker DNS-only checks as likely available rather than confirmed.

Risk: The artifact references a local candidate generator script that is not present in the release artifact.

Mitigation: Generate candidates manually or skip that helper step when the script is unavailable; do not block availability verification on the missing helper.

Risk: Domain recommendations may resemble existing trademarks or famous product names.

Mitigation: Avoid obvious conflicts using the skill's trademark-risk heuristics and state that recommendations are not legal clearance.

## Reference(s):

- [SEO And Brand Patterns](references/seo-brand-patterns.md)
- [ClawHub skill page](https://clawhub.ai/daviddonecn/skills/domain-recommender)
- [Project homepage](https://github.com/hilaraklesantosw-art/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with compact domain shortlists, naming rationale, and availability labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to 5 results; domain availability is time-sensitive and may require registrar confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
