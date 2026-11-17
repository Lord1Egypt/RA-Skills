## Description:

Converts a FridayParts blog title and short summary into platform-specific English social posts for Facebook, Instagram, X, and a TikTok opening hook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuxirui677](https://clawhub.ai/user/zhuxirui677)

### License/Terms of Use:

MIT-0

## Use Case:

Content and marketing operators use this skill to repurpose a FridayParts blog title and summary into four channel-ready social outputs. It is aimed at English-language posts for North American mechanics, farmers, and contractors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated repair or fault-diagnosis posts could be misleading if published without review.

Mitigation: Review generated posts before publishing, especially where safety or equipment damage is involved, and preserve cautious language such as can, may, or could.

Risk: Outputs may not fit a workspace or audience if the model settings or English-only North American positioning are changed.

Mitigation: Confirm the configured model, temperature, token limit, and intended audience in the GetClawHub workspace before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuxirui677/skills/fp-blog-to-social)
- [FridayParts Blog](https://fridayparts.com/blog)
- [Import guide](artifact/docs/如何导入GetClawHub.md)
- [Example outputs](artifact/examples/example_blog_to_social.md)
- [Platform style checklist](artifact/reference/平台风格checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style text divided into Facebook, Instagram, X, and TikTok hook sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are English social copy with platform-specific length, hashtag, tone, and safety-language constraints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
