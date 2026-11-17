## Description:

跨境一套素材多区域本地化。一套素材 → 多语言文案、尺码换算表、区域合规标识。当用户说「跨境本地化」「多语言」「翻译上架」「海外版本」「英文版主图」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border sellers and listing teams use this skill to adapt product copy, size charts, and product images for selected regional marketplaces. It also provides platform image checks and prompts for common labeling requirements; those prompts are not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports 60% coverage, with some files only partly inspected, and notes behavior that does not clearly match the localization description.

Mitigation: Review the incompletely inspected code and confirm the image-checking and generation behavior fits your needs before installing.

Risk: Prompts and supplied images may be sent to an external image-generation service.

Mitigation: Choose a provider whose data-handling practices suit the images and prompts you plan to submit.

Risk: The security guidance flags an unpinned npx reference.

Mitigation: Check the referenced package and version before running it.

## Reference(s):

- [Platform Image Specifications](references/platform-specs.md)
- [Provider CLI Reference](references/provider-cli.md)
- [Cross-border Localize on ClawHub](https://clawhub.ai/dlazyai/skills/cross-border-localize)

## Skill Output:

**Output Type(s):** [Text, Markdown, Image files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables and prompts, image files, shell commands, and platform-check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-English text in generated images needs manual review; size conversions are approximate and should be checked against the brand's measurements.]

## Skill Version(s):

1.0.30 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
