## Description:

Reviews influencer content submissions against STAR pre-publish criteria, computes a profile-weighted SQS, checks disclosure, claim, brand-safety, and authenticity vetoes, and returns constructive revision feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, brand reviewers, and campaign operators use this skill to assess creator submissions before publication against a campaign brief, approved claims, disclosure obligations, platform requirements, and STAR scoring criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit decisions can be misleading when campaign briefs, approved claims, platform requirements, or creator authenticity evidence are missing.

Mitigation: Mark applicable missing items as unknown or needs-input, and avoid a gate verdict or score when required evidence or verified runtime support is unavailable.

Risk: Sponsored-content disclosure, claim, brand-safety, or authenticity failures can create compliance and brand risk.

Mitigation: Treat documented STAR veto failures as blockers that cannot be offset by creative quality or production value.

Risk: Persistent audit artifacts may contain sensitive campaign or creator information.

Mitigation: Write audit artifacts only with user approval and validate the complete draft before persistence.

## Reference(s):

- [Creator Content Auditor on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/creator-content-auditor)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Standalone Auditor Runtime](references/auditor-runtime.md)
- [Quality Review Aids](references/quality-review-aids.md)
- [Content Reviewer Templates](references/review-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown audit report with typed status fields, SQS findings, item-level evidence notes, creator feedback, and optional JSON-backed audit artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent audit artifacts are written only with user permission; standalone fallback returns observations without a score when verified runtime is unavailable.]

## Skill Version(s):

19.0.0 (source: server evidence release.version, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
