## Description:

Generate illustrated children's story videos with AI images and TTS narration using a local ComfyUI instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenlin0517](https://clawhub.ai/user/shenlin0517)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate themed children's story text, local ComfyUI illustration prompts and images, TTS narration, and draft video assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted story theme can lead to arbitrary shell command execution through the included script.

Mitigation: Review or patch the script before installing; replace os.system command strings with subprocess argument lists and treat the theme as untrusted input.

Risk: The skill writes generated story, image, audio, and draft video files under output/.

Mitigation: Run it in a controlled workspace and review generated files before reuse or publication.

Risk: The skill depends on local ComfyUI, FFmpeg, macOS say, and Python packages.

Mitigation: Use a virtual environment with pinned dependencies and confirm the local ComfyUI service is running before execution.

## Reference(s):

- [Comfy Story Video Reference README](artifact/references/README.md)
- [Basic ComfyUI Workflow](artifact/assets/basic_workflow.json)
- [ClawHub Skill Page](https://clawhub.ai/shenlin0517/skills/comfy-story-video)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands, configuration paths, and generated file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script writes story JSON, scene images, narration audio, and draft video assets under output/.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
