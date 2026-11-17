## Description:

通过产品照片检索外观相近的设计专利，并展示相似度排序、专利附图和逐件外观比较。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External product designers, sellers, and manufacturers can submit a product image to find visually similar design patents and review potential design conflicts before listing or production. Results are a preliminary similarity screen, not a legal infringement determination.

### Deployment Geography for Use:

Global; searches China by default, with optional image-based searches for the United States and South Korea and text-only searches for Japan and Taiwan.

## Known Risks and Mitigations:

Risk: A harmful server response could expose the API key or overwrite images outside the download folder.

Mitigation: Prefer a corrected release that restricts authenticated downloads to trusted destinations, validates filenames, and protects saved keys.

Risk: Product images are sent to PatentMax and may contain confidential designs.

Mitigation: Review PatentMax's privacy policy before submitting confidential designs.

Risk: A successful search costs ¥1.

Mitigation: Confirm the search and its fee before proceeding.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/design-image-search)
- [PatentMax API documentation](https://api.ip930.com/features/api-platform)
- [Skill FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV, HTML]

**Output Format:** [Patent search summary with visual comparisons, a CSV comparison table, and a self-contained HTML image gallery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks visually similar design patents and describes visible similarities and differences; results are preliminary and are not a legal infringement opinion.]

## Skill Version(s):

1.0.3 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
