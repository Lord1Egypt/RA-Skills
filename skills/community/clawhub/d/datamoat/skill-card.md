## Description:

Back up, analyze, and reuse ChatGPT, Claude, Codex, Cursor, DeepSeek, Qwen, and OpenClaw data, skills, and attachments locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[max-ng](https://clawhub.ai/user/max-ng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI tool users use this skill to check DataMoat protection status, install the local DataMoat desktop app, and route backup, export, analysis, restore, and reuse work into the local UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and runs a desktop app that can begin background capture of sensitive local AI conversation records before desktop setup is complete.

Mitigation: Review the security summary before installation, get explicit user approval before running installers, and keep password, recovery, and unlock steps inside the local desktop UI.

Risk: Install verification and consent controls are limited for a tool that handles sensitive local records.

Mitigation: Prefer signed or pinned releases that fail closed on missing checksums and ask the user to choose data sources before capture starts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/max-ng/skills/datamoat)
- [DataMoat Official Site](https://datamoat.org)
- [DataMoat Latest Release Manifest](https://downloads.datamoat.org/releases/latest/manifest.json?s=skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reports local protection status, installer outcomes, and next-step guidance for the DataMoat desktop UI.]

## Skill Version(s):

2.0.9 (source: server release metadata, released 2026-06-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
