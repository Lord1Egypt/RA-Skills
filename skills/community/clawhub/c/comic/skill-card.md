## Description:

Generate educational or narrative comic pages with structured art, tone, layout, and language decisions and bundled generation tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use Comic to turn source material into knowledge comics, tutorial comics, biography comics, educational comics, or multi-page narrative comic sequences with storyboard, character, prompt, image, PDF, and delivery packaging steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Comic prompts and approved reference assets are sent to WeryAI for generation.

Mitigation: Use only inputs approved for third-party processing and avoid sensitive or confidential prompt and reference content.

Risk: Security evidence reports that runtime behavior can expose the API key to unvalidated image URLs and can upload local files despite the skill instructions saying local paths are rejected.

Mitigation: Avoid local reference paths, inspect any referenced file before upload, and keep IMAGE_GEN_API_KEY in environment variables or restrict permissions on any persisted .env file.

Risk: Setup and dependency installation execute third-party package code.

Mitigation: Run setup and bootstrap only in a controlled project environment and review package changes before execution.

## Reference(s):

- [ClawHub Comic Skill Page](https://clawhub.ai/632657122/skills/comic)
- [Comic Dimensions Reference](references/dimensions.md)
- [Character Definition Template](references/character-template.md)
- [Storyboard Template](references/storyboard-template.md)
- [Prompt Template](references/prompt-template.md)
- [WeryAI Platform Reference](scripts/vendor/shared-image-generation/references/weryai-platform.md)
- [WeryAI API Keys](https://weryai.com/api/keys)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated working files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces storyboards, character prompts, page prompts, batch configuration, generated image files, PDFs, and delivery bundles through the bundled generation tooling.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
