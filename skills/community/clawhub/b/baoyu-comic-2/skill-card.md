## Description: <br>
Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and sequential image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nengnengZ](https://clawhub.ai/user/nengnengZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn source material into educational comics, including analysis, storyboard files, character definitions, image prompts, generated comic page images, and a merged PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local comic project files, including analysis, storyboard, prompts, images, and PDFs. <br>
Mitigation: Run it in the intended project workspace and review generated or overwritten files before sharing or committing them. <br>
Risk: Reusable preferences may be stored outside a single project and affect later comic-generation runs. <br>
Mitigation: Use project-level preferences when defaults should stay scoped to one workspace. <br>
Risk: The workflow invokes image generation and PDF assembly steps that can produce inaccurate visuals or malformed output. <br>
Mitigation: Review storyboards, prompts, generated pages, and the final PDF before publication. <br>
Risk: PDF assembly requires bun or npx and runs a local script over generated image files. <br>
Mitigation: Install runtime dependencies from trusted sources and run the script only on expected comic output directories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nengnengZ/baoyu-comic-2) <br>
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-comic) <br>
- [Workflow Reference](references/workflow.md) <br>
- [Partial Workflows Reference](references/partial-workflows.md) <br>
- [Auto Selection Reference](references/auto-selection.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, code, guidance] <br>
**Output Format:** [Markdown workflow outputs, image prompt files, generated image files, and PDF assembly commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local comic project directories containing analysis, storyboard, character definitions, prompts, page images, and a merged PDF.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence); artifact frontmatter version 1.56.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
