## Description:

Professional design studio for creating covers, banners, avatars, logos, mockups, portfolios and GIF animations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosoonpi-ai](https://clawhub.ai/user/mosoonpi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, freelancers, and developers use this skill to generate marketplace covers, social banners, avatars, logos, mockups, GIF banners, watermarks, SVG assets, and design quality checks from agent-guided prompts or local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pipeline runs can use predictable intermediate filenames such as *_draft.png and *_improved_1.png, which may collide with existing files in reused output paths.

Mitigation: Run generation in a fresh output directory or choose explicit unique output paths, then review generated files before reuse.

Risk: The skill reads selected images or CSV files and writes generated assets to local paths.

Mitigation: Use trusted input files, avoid unnecessary sensitive source assets, and constrain outputs to a known project directory.

Risk: Several script messages and help text are in Russian, which may make warnings or errors easier to miss for non-Russian readers.

Mitigation: Review command options and outputs carefully, and translate messages before operational or customer-facing use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mosoonpi-ai/skills/design-studio)
- [Professional Design Rules](references/design-rules.md)
- [Color Palettes](references/color-palettes.md)
- [Font Pairings](references/font-pairings.md)
- [Professional Design Knowledge Base](references/knowledge-base.md)
- [SVG Element Library](references/svg_elements/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with inline shell commands plus generated PNG, GIF, SVG, TXT, and local output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local design assets and quality reports produced from user prompts, selected images, CSV files, palettes, fonts, and command options.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
