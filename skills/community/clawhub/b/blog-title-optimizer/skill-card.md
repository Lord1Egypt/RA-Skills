## Description:

AI-powered blog title optimizer. Generate SEO-friendly, click-worthy headlines that drive traffic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icepopma](https://clawhub.ai/user/icepopma)

### License/Terms of Use:

MIT

## Use Case:

External users and content creators use this skill to generate SEO-oriented blog title options for a supplied topic and optional target keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can attempt automatic SkillPay billing before title generation.

Mitigation: Review the paid workflow before installation and require explicit user confirmation through a safer payment flow before routine use.

Risk: The package embeds a merchant key and may pass topic text to a local OpenClaw agent.

Mitigation: Remove or rotate the embedded key and avoid submitting sensitive topics unless the local agent and payment flow are trusted.

Risk: The security guidance reports dependency and install paths that should be pinned and moved to trusted HTTPS sources.

Mitigation: Pin dependencies and use trusted HTTPS package sources before deploying the skill.

Risk: The inspected JavaScript failed Node syntax checking and may not run as published.

Mitigation: Run syntax and functional checks in a controlled environment before enabling the skill for users.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/icepopma/skills/blog-title-optimizer)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text numbered list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seven title variations; optional keyword constraint.]

## Skill Version(s):

1.0.7 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
