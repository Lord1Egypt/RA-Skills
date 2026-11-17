## Description:

Automates writing and managing content and settings for blogs running the awesome-poetize-open fork of POETIZE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leapya](https://clawhub.ai/user/leapya)

### License/Terms of Use:

MIT-0

## Use Case:

Blog owners and developers use the agent to draft and publish posts, manage blog content and settings, and review analytics for an awesome-poetize-open instance. It is limited to that open-source POETIZE fork.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious with high confidence, citing local-file uploads and actions that can change blog or payment data; some analysis was incomplete.

Mitigation: Review the skill and its behavior before installation, and restrict use to a blog and data you intend to manage.

Risk: The blog API key can grant administrative access, and generated configuration can contain the key in plaintext.

Mitigation: Use a least-privilege, revocable key, store it in protected environment or credential storage, and protect generated configuration files from sharing or repository commits.

Risk: Publishing, uploads, visibility, comments, theme, SEO, and payment settings can change live blog state; local image references may be uploaded during publishing.

Mitigation: Confirm the exact target and action before live changes, use draft previews when appropriate, and inspect local image paths before publishing.

Risk: The optional evaluation command sends the skill text to a user-supplied external LLM endpoint.

Mitigation: Use the evaluation only with explicit opt-in after verifying the destination host and deciding that sending the skill text there is acceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/leapya/skills/awesome-poetize-open-blog-automation)
- [awesome-poetize-open project](https://github.com/LeapYa/awesome-poetize-open)
- [Skill documentation](https://github.com/LeapYa/awesome-poetize-open/tree/main/skills/poetize-blog-automation)

## Skill Output:

**Output Type(s):** [Text and Markdown, Shell commands, Configuration, Blog API results]

**Output Format:** [Markdown, JSON, shell command text, and text returned by blog operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create drafts or perform blog changes when explicitly requested and confirmed.]

## Skill Version(s):

2.5.2 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
