## Description:

script to video, screenplay to video, shot list to video — turn a script into a storyboarded, shot-by-shot video: break down scenes, generate shots, assemble, validate. Use when the user gives a script or scene breakdown and wants a video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn a script or scene breakdown into a storyboarded, multi-shot video, including character-consistent animation, audio, subtitles, and assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had medium confidence and partial Skillspector coverage; it noted a purpose mismatch around CLI authentication setup and organization project listing.

Mitigation: Review the setup and authentication instructions, inspect the whitespace-flagged section, and confirm you are comfortable configuring the CLI and listing organization projects before installing.

Risk: Messages and any attached local files are sent to dLazy services; attached files are uploaded to its media storage.

Mitigation: Review the service terms and avoid attaching material you do not want sent to the hosted service.

## Reference(s):

- [dLazy CLI repository](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video files, Text, Guidance]

**Output Format:** [Rendered video and CLI text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation runs through the dLazy storyboard project workflow.]

## Skill Version(s):

1.0.38 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
