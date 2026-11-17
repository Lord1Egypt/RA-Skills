## Description:

Search, explore, and run fal.ai generative AI models for image generation, video, audio, 3D, and related media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apekshik](https://clawhub.ai/user/apekshik)

### License/Terms of Use:

MIT

## Use Case:

Developers and creators use this skill to discover fal.ai models, inspect model schemas, submit generation jobs, check queued job status, upload input files, and retrieve generated media outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, parameters, and uploaded media are sent to fal.ai when models are searched, run, or files are uploaded.

Mitigation: Use the skill only with data approved for fal.ai processing, and avoid confidential files or sensitive personal media unless that use is authorized.

Risk: Generated outputs are saved locally in the fal session directory.

Mitigation: Periodically clean ~/.fal/sessions/${CLAUDE_SESSION_ID}/ when generated outputs should not remain on disk.

## Reference(s):

- [fal ClawHub Skill Page](https://clawhub.ai/apekshik/skills/fal)
- [fal.ai Models](https://fal.ai/models)
- [fal.ai Docs](https://docs.fal.ai)
- [Popular fal.ai Models Quick Reference](models-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media files may be downloaded to a local fal session directory.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
