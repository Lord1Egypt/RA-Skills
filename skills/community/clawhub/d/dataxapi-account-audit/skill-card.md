## Description:

Audits a social media account's audience, posting pace, and recent post engagement, then returns a CSV table and an evidence-based report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Social media account owners and analysts use the skill to review follower counts, posting pace, and engagement for their own or a competitor's account, then compare recent posts and identify next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan rated the skill benign with medium confidence and noted an unpinned CLI installation reference. If the package were compromised, it could access environment credentials or files; some local references were unresolved in the partial scan.

Mitigation: Install a trusted, pinned CLI version and run it with only the credentials and file access needed for the audit.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-account-audit)

## Skill Output:

**Output Type(s):** [Files, Analysis, Markdown]

**Output Format:** [CSV table and Markdown account audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A recent-post snapshot; fields unavailable on a platform may be empty.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
