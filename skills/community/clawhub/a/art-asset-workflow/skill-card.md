## Description:

Guides agents through generating game art assets such as UI icons, character concepts, and promotional posters, including tool selection, image sizes, prompt patterns, generation, splitting, cutout, and verification steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game-content creators use this skill to plan and run an AI-assisted workflow for producing game UI icons, single art assets, character concepts, and promotional art. It helps select generation tools, prompts, dimensions, post-processing steps, and image review checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes commands and API examples that may use local skills, local files, or user-provided OpenAI credentials.

Mitigation: Review commands and credential-dependent API calls before execution, and run them only in trusted environments.

Risk: The skill is a Chinese-language workflow guide, which may be misread by agents or reviewers who do not understand the source language.

Mitigation: Have a Chinese-proficient reviewer validate intended behavior, command usage, and generated prompts before operational use.

Risk: Generated image assets may have quality issues such as missing elements, inconsistent style, incorrect content, or clipping.

Mitigation: Use the artifact's required post-generation image review step and regenerate or adjust prompts when defects are found.

## Reference(s):

- [Art Asset Workflow on ClawHub](https://clawhub.ai/axelhu/skills/art-asset-workflow)
- [Publisher profile: axelhu](https://clawhub.ai/user/axelhu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes recommended image sizes, prompt guidance, workflow steps, quality checks, and tool-selection notes.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
