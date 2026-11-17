## Description:

Queries AliMail for internal employee email addresses and employee numbers by name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colin-megan](https://clawhub.ai/user/colin-megan)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized enterprise users and agents use this skill to look up internal AliMail directory records by employee name when they need contact or employee-number details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or automatic name searches can expose internal employee email addresses and employee numbers.

Mitigation: Install only where AliMail directory lookup is authorized, require explicit lookup requests, and add exact-match or minimum-length search controls before deployment.

Risk: Company OAuth credentials are required to query the directory service.

Mitigation: Store ALIMAIL_CLIENT_ID and ALIMAIL_CLIENT_SECRET as protected environment secrets and limit access to authorized runtime environments.

Risk: The dependency specification is not pinned to an exact requests version.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colin-megan/skills/alimail)
- [AliMail API endpoint](https://alimail-cn.aliyuncs.com)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 10 fuzzy name matches with name, email, employeeNo, and total count; errors are returned as JSON status objects.]

## Skill Version(s):

1.0.6 (source: server evidence, SKILL.md frontmatter, manifest.json, openapi.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
