## Description:

AI Social Media Manager helps generate social media content calendars, posting-time recommendations, reply drafts, and performance analysis for multiple platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, content creators, brand marketers, and digital marketing teams can use this skill to draft content plans, recommend posting times, generate candidate replies, and summarize engagement metrics. Public posts and replies should be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation asks users to place social-media passwords, cookies, API keys, or access tokens in TOOLS.md.

Mitigation: Do not store real credentials in plaintext configuration. Use test accounts, keep secrets in a secure secret manager when integrating the skill, and rotate any credentials already exposed.

Risk: Posting, comment, and analytics functions are presented as platform capabilities while the security evidence identifies them as unverified or mock behavior.

Mitigation: Treat platform actions as unverified until the publisher documents real integrations and safe secret handling. Manually review posts, replies, and analytics before relying on them.

Risk: Generated replies or recommendations could be inaccurate, off-brand, or unsuitable for public audiences.

Mitigation: Require human review before publishing replies or acting on optimization recommendations, especially for customer-facing or regulated communications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/ai-social-media-manager-lvjunjie)
- [Artifact README](artifact/README.md)
- [API documentation](artifact/src/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON-like reports, JavaScript API results, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated content-calendar entries, posting-time suggestions, reply drafts, sentiment labels, engagement metrics, optimization recommendations, and configuration guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact package metadata states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
