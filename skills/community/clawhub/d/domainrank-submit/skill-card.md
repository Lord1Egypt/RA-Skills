## Description:

Submits website listings to DomainRank.app through its authenticated submission API, including support for batch submissions after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[domainrankhq](https://clawhub.ai/user/domainrankhq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit one or more websites to the DomainRank.app AI directory while reviewing the target site list, price plan, and expected credit use before requests are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website URLs and related metadata are sent to DomainRank.app during submission.

Mitigation: Confirm the destination service and review each site before making API requests.

Risk: Submissions may consume DomainRank account credits, especially when using pro or ultra price plans or batch submissions.

Mitigation: Review the pricePlan and expected total credit use with the user before submitting.

Risk: API credentials could be exposed if hardcoded into commands or files.

Mitigation: Pass the DomainRank API key through an environment variable or another secure credential mechanism.

## Reference(s):

- [DomainRank submission API endpoint](https://domainrank.app/api/submit-item)
- [DomainRank AI SEO skills](https://domainrank.app/ai-seo-skills)
- [ClawHub skill page](https://clawhub.ai/domainrankhq/skills/domainrank-submit)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided DomainRank API key and explicit confirmation before batch submissions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
