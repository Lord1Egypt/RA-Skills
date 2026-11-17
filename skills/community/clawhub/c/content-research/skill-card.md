## Description:

Research trending topics and generate platform-specific content for Reddit, X/Twitter, Discord, and LinkedIn using topic-research and content-creation triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hazy2go](https://clawhub.ai/user/hazy2go)

### License/Terms of Use:

MIT

## Use Case:

External content creators, marketers, and OpenClaw users use this skill to research recent topic developments, summarize findings, and draft platform-specific posts for Reddit, X/Twitter, Discord, and LinkedIn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research summaries or social drafts may include inaccurate, outdated, or unsuitable claims.

Mitigation: Review generated findings and drafts before publishing, and verify source links for important claims.

Risk: Brand guidance files may expose sensitive account, campaign, or credential information if populated with secrets.

Mitigation: Keep secrets and sensitive account credentials out of brand-config.md and use only publishable brand guidance.

Risk: Broad trigger phrases may cause the skill to be selected when web research or social drafting was not intended.

Mitigation: Use explicit prompts and review auto-selection behavior in OpenClaw setups that choose skills from broad phrases.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [Content Research on ClawHub](https://clawhub.ai/hazy2go/skills/content-research)
- [Brand configuration template](examples/brand-config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries and ready-to-post social content drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research findings are filtered to recent items and content drafts are tailored by platform and optional brand voice guidance.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
