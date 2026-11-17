## Description:

Generate AI music videos end to end by creating music with Suno, generating visuals with OpenAI, Seedream, Google or Seedance, and assembling the result with ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gprecious](https://clawhub.ai/user/gprecious)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to orchestrate AI-generated songs, visual scenes, subtitles and final music-video assembly from prompts and project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe script argument handling could let crafted inputs run local code.

Mitigation: Run the skill only in a constrained workspace, avoid untrusted text in script options, and review the scripts before using real credentials.

Risk: The workflow uses paid external generation APIs and API keys.

Mitigation: Use dry-run and cost checks first, confirm each paid generation step, and use limited API keys with non-sensitive prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gprecious/skills/ai-music-video)
- [SunoAPI Reference](references/sunoapi.md)
- [Visual Providers Reference](references/visual-providers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate local audio, subtitle, image, video and metadata files through the bundled scripts.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
