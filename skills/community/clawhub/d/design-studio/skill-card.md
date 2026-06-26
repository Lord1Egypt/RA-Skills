## Description: <br>
Professional design studio for creating covers, banners, avatars, logos, mockups, portfolios and GIF animations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mosoonpi-ai](https://clawhub.ai/user/mosoonpi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and marketplace creators use this skill to generate local design assets such as freelance covers, social banners, logos, avatars, device mockups, watermarks, and animated GIF banners. It also supports batch generation from CSV and basic design-quality checks for contrast, balance, palette, and composition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local image generation and editing can create or overwrite files, including watermarking an input image when no separate output path is provided. <br>
Mitigation: Use explicit output directories, keep backups of important source images, and provide an output path for watermarking operations. <br>
Risk: Batch generation can create many files from CSV input and may amplify incorrect titles, styles, or output paths. <br>
Mitigation: Review CSV inputs and target directories before batch runs, then inspect generated summaries and sample outputs before publishing assets. <br>


## Reference(s): <br>
- [Design Studio on ClawHub](https://clawhub.ai/mosoonpi-ai/design-studio) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Design Rules](references/design-rules.md) <br>
- [Color Palettes](references/color-palettes.md) <br>
- [Font Pairings](references/font-pairings.md) <br>
- [Knowledge Base](references/knowledge-base.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated local image assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create PNG, SVG, GIF, and other local design files depending on the selected script and arguments.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
