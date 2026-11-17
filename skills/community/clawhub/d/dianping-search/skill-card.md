## Description:

Dianping (大众点评) API skill for searching restaurants and businesses, viewing shop details, deals/coupons, and reading recommended dishes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fjsand](https://clawhub.ai/user/fjsand)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up Dianping restaurant and local-business information for Chinese cities, including ratings, addresses, recommended dishes, and deals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Dianping session cookies, which can expose account access if printed, logged, or shared.

Mitigation: Review the code before use, avoid passing real cookies through logged command lines, avoid exporting cookies in logged terminals, and rotate the Dianping session if values are exposed.

Risk: The release promotes a curl-to-bash installation pattern.

Mitigation: Inspect the installer and scripts before running them, and prefer a reviewed local install path over piping remote content directly to a shell.

## Reference(s):

- [Dianping](https://www.dianping.com/)
- [ClawHub Skill Page](https://clawhub.ai/fjsand/skills/dianping-search)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses with Markdown usage guidance and bash/Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use Dianping session cookies and may return error JSON when login renewal is required.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
