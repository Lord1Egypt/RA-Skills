## Description:

横幅插画生成工具专业版 helps design teams and content studios generate banner illustrations in batches with prompt templates, style presets, multi-size adaptation, collaboration, history, and export workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, design teams, and content studios use this skill to automate banner illustration generation, template reuse, multi-platform resizing, and local export workflows. It is intended for marketing assets, UI design, posters, and brand visuals rather than 3D modeling or animation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may rely on an external banner-gen-pro command or package that is outside the skill card evidence.

Mitigation: Confirm the selected command or package is trusted before installation or execution.

Risk: Image generation requires GEMINI_API_KEY, and leaked credentials could expose account access or usage quota.

Mitigation: Keep GEMINI_API_KEY in environment variables or secure secret storage, and do not commit it to shared files.

Risk: Generated prompts, reports, assets, and history may be stored locally under $HOME/banner-gen-pro.

Mitigation: Review workspace permissions and history retention settings before using sensitive prompts or assets.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML configuration examples, and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image assets and generation history under the configured banner-gen-pro workspace.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
