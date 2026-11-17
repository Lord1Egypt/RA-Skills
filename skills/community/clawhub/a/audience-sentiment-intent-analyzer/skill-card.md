## Description:

Analyze comments, DMs, and replies across YouTube, TikTok, Instagram, and email to extract buying intent, pain points, and churn signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, agencies, product teams, and marketing leaders use this skill to turn social, email, and manual audience feedback into sentiment trends, intent classifications, content gaps, churn signals, and response recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private DMs, email, and customer messages may be analyzed or forwarded to an external AI provider without adequate consent or redaction.

Mitigation: Require explicit opt-in for private message and email analysis, redact personal or confidential data before model calls, and limit API credentials to read-only, source-specific scopes.

Risk: Reports, raw samples, or Slack alerts may expose sensitive audience content to additional systems or viewers.

Mitigation: Disable raw samples and Slack payloads for private content unless approved, and restrict report access to reviewers with a business need.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/audience-sentiment-intent-analyzer)
- [Publisher profile](https://clawhub.ai/user/ncreighton)
- [Skill homepage from artifact frontmatter](https://github.com/ncreighton/empire-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON reports and Markdown guidance, with configuration examples and optional shell commands for setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sentiment scores, intent classifications, persona updates, content-gap recommendations, raw text samples, and optional Slack alerts.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
