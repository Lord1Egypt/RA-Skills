## Description:

Create professional cinematic scripts for AI video generation with character consistency, cinematography guidance, prompt generation, YouTube metadata, and optional Google Drive or local storage export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[praveenspeaks](https://clawhub.ai/user/praveenspeaks)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and agents use this skill to turn story concepts into cinematic scripts, shot-by-shot prompts, character and voice consistency guides, era-aware validation, and shareable project exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store story project state and write exported project files to local storage when configured.

Mitigation: Run it in an intended workspace and review storage destinations before saving or sharing generated project files.

Risk: The skill can call Google OAuth and Drive APIs when Drive storage is connected.

Mitigation: Review Google Drive permissions during OAuth and disconnect storage when access is no longer needed.

Risk: Server security evidence notes packaging and dependency hygiene issues for development or CI use.

Mitigation: Update development dependencies and review package configuration before using the repository in development or CI.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/praveenspeaks/skills/cinematic-script-writer)
- [Cinematic Script Writer README](skills/cinematic-script-writer/README.md)
- [Cinematic Script Writer Skill Instructions](skills/cinematic-script-writer/SKILL.md)
- [Storage Usage Example](skills/cinematic-script-writer/EXAMPLE-STORAGE.md)
- [Consistency Usage Example](skills/cinematic-script-writer/EXAMPLE-CONSISTENCY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown and structured text for scripts, prompts, character references, voice guidelines, metadata, and exported project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store story state in memory and export project files locally or to Google Drive when configured]

## Skill Version(s):

1.4.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
