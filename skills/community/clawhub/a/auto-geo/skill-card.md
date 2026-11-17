## Description:

GEO Optimizer helps users plan generative engine optimization campaigns by researching AI-search citations, prioritizing publishable high-authority platforms, collecting SEO inputs, drafting platform-adapted Markdown content, and giving publishing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forevip](https://clawhub.ai/user/forevip)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, SEO, and content teams use this skill to identify where AI search engines cite public content for a product or topic, then generate compliant Markdown drafts and publishing checklists for those platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch links or use browser/login-state actions during research.

Mitigation: Require explicit user confirmation before link fetches or browser actions, and do not provide confidential or access-controlled URLs unless they are intended to be fetched.

Risk: The skill may push WeChat official-account drafts through another skill.

Mitigation: Require user confirmation before any WeChat draft push, and review generated content for accuracy, disclosure, and platform compliance before publication.

Risk: The skill can install or update an external paid execution skill and may involve WeChat Pay or refund flows.

Mitigation: Require explicit confirmation before SkillHub CLI installation, fore-vip-auto installation or update, paid execution, payment, or refund steps.

Risk: Generated marketing content may contain unsupported claims or regulated-industry compliance issues.

Mitigation: Review facts, source dates, advertising disclosures, and medical, financial, education, or platform-specific restrictions before using the drafts.

## Reference(s):

- [Platform source database](references/platforms.md)
- [SEO question and intake template](references/seo-template.md)
- [GEO writing guide](references/writing-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown report with tables, platform-specific content drafts, publishing suggestions, and follow-up checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include citation-source analysis, prioritized publishing targets, compliance notes, and instructions for manual or assisted publishing workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
