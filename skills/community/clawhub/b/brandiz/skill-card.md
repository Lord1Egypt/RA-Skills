## Description:

Make, schedule and post a business's social media posts, posters and reels through Brandiz.io, its AI content studio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anas660](https://clawhub.ai/user/anas660)

### License/Terms of Use:

MIT-0

## Use Case:

External business owners and their AI agents use this skill to create brand-aligned social media copy, posters, carousels and reels, and to manage approvals, scheduling, publishing and performance through Brandiz.io.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `npx brandiz` CLI may access configured credentials and local files; the security scan rates the release benign but notes this risk.

Mitigation: Review the package before use, provide only credentials and local access you are comfortable with, and never print, log or store the API key in a project file.

Risk: The security scan was partial because two local references could not be matched to bundled artifacts.

Mitigation: Review the referenced files and repeat the security review if those artifacts become available.

## Reference(s):

- [Brandiz agent guide](https://www.brandiz.io/agents?ref=claude-code)
- [Brandiz API reference](https://www.brandiz.io/developers?ref=claude-code)

## Skill Output:

**Output Type(s):** [Text, Images, Videos, API Calls, Guidance]

**Output Format:** [Structured responses, social media copy, posters, carousels, reels, schedules and performance summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Making posters or reels may use the business's package; scheduling and posting depend on the connected account's permissions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
