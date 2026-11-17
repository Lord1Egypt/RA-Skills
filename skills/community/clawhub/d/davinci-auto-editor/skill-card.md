## Description:

Generate DaVinci Resolve import packages from local media plus a cloud editing API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video automation users use this skill to scan local media, request a cloud editing plan, and prepare a DaVinci Resolve timeline import package. It is aimed at workflows where local execution should stay limited to media indexing, EDL generation, import guidance, and execution reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send an API key and detailed local media metadata to the configured cloud editing service, and the sample endpoint uses unencrypted HTTP.

Mitigation: Use only a trusted HTTPS API endpoint, avoid sensitive media folders unless that sharing is acceptable, and rotate any key already sent over HTTP.

Risk: Unversioned package execution can make it harder to review the exact code that will run.

Mitigation: Use a pinned package version or a reviewed local artifact when invoking the skill.

Risk: Generated EDL output is intended for basic timeline import and may require manual review or relinking in DaVinci Resolve.

Mitigation: Validate with sample media first, import source clips into the Resolve Media Pool, and manually review the timeline before relying on the edit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/afengzi/skills/davinci-auto-editor)
- [Project Homepage](https://github.com/imfengziaaa/video-auto-editor-skills)
- [README](README.md)
- [Skill Instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [files, text, json, shell commands, configuration, guidance]

**Output Format:** [JSON, CMX3600 EDL text, plain-text import guidance, and terminal JSON status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a Resolve import package under _davinci_auto_editor/<taskId>/ next to the configured media folder.]

## Skill Version(s):

0.2.1 (source: release evidence, manifest.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
