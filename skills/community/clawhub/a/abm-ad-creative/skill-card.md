## Description:

Generates and iterates paid advertising creative, including headlines, descriptions, primary text, full ad variations, and performance-informed recommendations across major ad platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, growth practitioners, and agents use this skill to create platform-specific ad copy, test angles, and iterate creative from performance data for Google Ads, Meta, LinkedIn, TikTok, and Twitter/X.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents beyond copywriting into ad-account workflows, including campaign upload or creation.

Mitigation: Require explicit user confirmation before any campaign upload, campaign creation, or account-changing action.

Risk: The skill references generative media workflows, including voice and audio generation, that can raise consent or licensing concerns.

Mitigation: Use only consented or licensed voices, brand assets, and media inputs, and review applicable platform and legal requirements before publication.

Risk: The skill includes copy-paste remote execution and local development command guidance.

Mitigation: Inspect commands, repositories, and third-party packages before running them, and pin dependencies where practical.

Risk: Generated ad creative may exceed platform limits or fail platform policy review if not checked before launch.

Mitigation: Validate character counts, claims, disclaimers, and previews in the target ad platform before using generated creative.

## Reference(s):

- [Platform Specs Reference](artifact/references/platform-specs.md)
- [Generative AI Tools for Ad Creative](artifact/references/generative-tools.md)
- [ClawHub Skill Page](https://clawhub.ai/mariokarras/skills/abm-ad-creative)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, lists, CSV blocks, and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform character counts, trimmed alternatives, CSV-ready rows, iteration reports, visual production guidance, and recommendations for what to test next.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
