## Description:

Generates a Codex-compatible custom Codex Pet from a source image by using RunComfy and ImageMagick to create spritesheet.webp and pet.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to create custom Codex Pet assets from a reference image without relying on Codex Pro or the Codex imagegen skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a third-party global npm CLI that may be unpinned.

Mitigation: Pin or verify the RunComfy CLI version before use and install it only from a trusted package source.

Risk: The RunComfy token may be exposed if handled casually in shell history, logs, or shared configuration.

Mitigation: Keep RUNCOMFY_TOKEN scoped, store it as a secret where possible, and avoid printing it in commands or logs.

Risk: An unsafe pet name could affect output paths when files are copied into the Codex pets directory.

Mitigation: Use only letters, numbers, underscores, or hyphens in pet names and confirm the final destination remains under the Codex pets directory.

Risk: The source image URL is processed through RunComfy and a model endpoint.

Mitigation: Use only images that are appropriate to send to the third-party service and treat externally supplied image URLs as untrusted.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/permew/skills/codex-pet)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=codex-pet)
- [RunComfy GPT Image 2 edit endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=codex-pet)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=codex-pet)
- [OpenAI hatch-pet skill reference](https://github.com/openai/skills/tree/main/skills/.curated/hatch-pet)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local pet.json and spritesheet.webp files through RunComfy and ImageMagick commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
