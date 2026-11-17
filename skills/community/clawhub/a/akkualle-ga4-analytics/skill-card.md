## Description:

Provides Google Analytics 4 metrics for akku-alle.de, including page views, users, sessions, top pages, and traffic sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akkualle](https://clawhub.ai/user/akkualle)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners or analysts can ask an agent to retrieve recent GA4 traffic metrics for akku-alle.de, including visitor, session, page, and traffic-source summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to run an unbundled absolute-path executable that receives Google Analytics credential access.

Mitigation: Install only when the executable is trusted and integrity-verified; prefer an auditable source package or a pinned, hash-checked binary.

Risk: GA4 credentials could grant access beyond the intended property.

Mitigation: Use a least-privilege read-only Google service account limited to the intended GA4 property.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akkualle/skills/akkualle-ga4-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analytics summary with tables and bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_APPLICATION_CREDENTIALS and GA4_PROPERTY_ID for the intended GA4 property.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
