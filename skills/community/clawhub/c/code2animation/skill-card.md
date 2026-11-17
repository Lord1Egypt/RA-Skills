## Description:

Enables agents to create, preview, narrate, and render code-driven animated videos with synchronized TTS audio and transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etrobot](https://clawhub.ai/user/etrobot)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to assemble video projects from HTML/CSS footage, generate narration, preview timing, and render portrait or landscape MP4 outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsanitized project IDs can expose command execution and file-access paths.

Mitigation: Use only trusted project IDs and confine project directories until projectId validation, shell execution handling, and path confinement are fixed.

Risk: The local dev server and rendering workflow are unsafe to expose to untrusted users or networks in their current state.

Mitigation: Run on a trusted machine and network only; do not expose the dev server before iframe isolation and remote script loading issues are resolved.

Risk: Project text and narration content may be sent to the Microsoft Edge TTS service during audio generation.

Mitigation: Avoid sensitive project text, secrets, or API keys in projects processed by the TTS workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/etrobot/skills/code2animation)
- [Artifact skill documentation](artifact/skill.md)
- [Artifact README](artifact/README.md)
- [Artifact rendering scripts README](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript/JavaScript, HTML/CSS, JSON configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project files, audio timing JSON, MP4 render artifacts, and local preview commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
