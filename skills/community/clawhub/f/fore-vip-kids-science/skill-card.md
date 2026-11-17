## Description:

Ten Thousand Whys answers children's science questions with age-appropriate explanations, per-section AI illustrations, and a shareable picture-book-style HTML page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onsoul](https://clawhub.ai/user/onsoul)

### License/Terms of Use:

MIT-0

## Use Case:

External parents, educators, and children use this skill to turn children's science questions into structured, age-appropriate explanations with paired illustrations and a previewable or shareable HTML page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML pages may include untrusted or adversarial question text.

Mitigation: Preview the HTML before sharing and require proper escaping and sanitization before publishing pages created from untrusted input.

Risk: Generated pages include fore.vip branding.

Mitigation: Review the branded footer before installation or publication and publish only when the branding is acceptable for the intended audience.

Risk: Generated pages may be published to shared services.

Mitigation: Share only after previewing the final HTML and confirming it contains age-appropriate content and no sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onsoul/skills/fore-vip-kids-science)
- [Publisher profile](https://clawhub.ai/user/onsoul)
- [fore.vip service site](https://fore.vip)
- [Image generation guide](references/image-gen-guide.md)
- [Layout guide](references/layout-guide.md)
- [Safety and age guide](references/safety-and-age-guide.md)
- [Share guide](references/share-guide.md)
- [IMA connection guide](references/ima-connect-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Structured Markdown plus a self-contained HTML page with paired generated illustrations when image generation is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate one child-safe 1024x1024 illustration per answer section and falls back to text if image generation is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
