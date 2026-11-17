## Description:

Guides an agent to create a short animated film with a custom WebGL2 path tracer, code-generated scenes and score, and an optional interactive browser page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn a story into an animated short rendered by a path tracer the agent writes, with a synthesized score and optional live browser page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports an exposed, unauthenticated rendering endpoint that may overwrite files outside its output folder; its analysis was incomplete.

Mitigation: Follow the scanner guidance: consider avoiding installation until the endpoint and file-write risk are reviewed and corrected and analysis is complete; if proceeding, review the installer version and package provenance first.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vargai/skills/code-path-traced-film)
- [Example film: The Smallest Star](https://s3.varg.ai/files/194b94d0-58ff-4e8b-91de-4f1959d04013/file_8d3b65611ed8.mp4)
- [Skill guide](https://varg.ai/how-to/skills/code-path-traced-film)
- [Rendering commands](artifact/references/commands.md)
- [Look and lighting notes](artifact/references/look.md)
- [Score brief](artifact/references/score-brief.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Source code, PNG frames, an MP4 film with synthesized score and captions, and an optional single-file interactive HTML page]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Film length, story, visual style, and delivery options are guided by the user's brief.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
