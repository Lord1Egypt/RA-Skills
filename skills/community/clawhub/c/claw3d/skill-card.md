## Description:

Unified 3D workflow: create models with AI, search Thingiverse, slice, and print; enable only the modules needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makermate](https://clawhub.ai/user/makermate)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and makers use claw3d to guide an agent through creating or finding 3D models, previewing them, slicing them to G-code, and optionally sending print jobs to configured printers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to control printers and local files.

Mitigation: Install it only in trusted OpenClaw environments, require clear human confirmation before physical printer actions, and restrict access to printer endpoints.

Risk: The workflow depends on external providers and API keys.

Mitigation: Use least-privilege key access, audit and pin the configured claw3d package, and keep provider credentials out of shared logs or workspaces.

Risk: Shared media directories can mix attachments or model outputs between users.

Mitigation: Use per-user or per-session storage where possible, enforce attachment ownership, and keep unique output names for generated files.

Risk: Generated or downloaded models may be unsafe or unsuitable for a specific printer.

Mitigation: Review previews, printer profiles, slicing settings, and G-code before starting a print.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/makermate/skills/claw3d)
- [Publisher profile: makermate](https://clawhub.ai/user/makermate)
- [OpenClaw 3D homepage](https://github.com/makermate/openclaw-3d)
- [FAL API keys](https://fal.ai/dashboard/keys)
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey)
- [Thingiverse app access](https://www.thingiverse.com/apps/create)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to produce or handle GLB, STL, G-code, preview media, and local configuration files through the claw3d CLI.]

## Skill Version(s):

1.0.0 (source: release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
