## Description:

Provides compliant summaries of Aliyun public product information, pricing, service announcements, and read-only console-visible billing overviews without performing account operations or handling sensitive credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize Aliyun product specifications, pricing links, billing trends visible in their own console, and service announcements. The skill is intended for read-only information organization and excludes account changes, access bypass, API calls, paid-service actions, and credential handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in console pages can expose billing details or other account-specific information.

Mitigation: Keep use read-only, review console-derived summaries before sharing, and omit credentials, access keys, account IDs, and other sensitive identifiers.

Risk: Automated access to Aliyun pages may exceed platform or account expectations.

Mitigation: Respect Aliyun access limits and use the skill only for visible information summaries, not account operations, API calls, or paid-service actions.

## Reference(s):

- [Aliyun Homepage](https://www.aliyun.com/)
- [Aliyun Console](https://home.console.aliyun.com/)
- [Aliyun Help Center](https://help.aliyun.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain-text summaries with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only summaries should avoid credentials, access keys, account IDs, and other sensitive identifiers.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
