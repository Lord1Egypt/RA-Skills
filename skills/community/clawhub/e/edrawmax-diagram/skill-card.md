## Description:

Generates flowcharts, infographics, Gantt charts, and mind maps from natural-language prompts using EdrawMax AI APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xkweimeng](https://clawhub.ai/user/xkweimeng)

### License/Terms of Use:

Proprietary

## Use Case:

External users and developers use this skill to turn natural-language descriptions into editable diagrams, including process flows, infographics, project timelines, and mind maps. The skill returns generated image paths and diagram source code for previewing, sharing, or further editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can save untrusted or tampered remote PNG/SVG content locally.

Mitigation: Review before installing, open generated SVG files cautiously, and prefer a fixed version that keeps TLS verification enabled, restricts downloads to trusted EdrawMax or OSS hosts, limits file size, validates image content, and makes local saving explicit or optional.

Risk: Diagram prompts are sent to EdrawMax APIs.

Mitigation: Use only prompts that are appropriate to send to EdrawMax and avoid confidential or regulated data.

## Reference(s):

- [EdrawMax AI Skills API Reference](artifact/references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/xkweimeng/skills/edrawmax-diagram)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with local file paths, source code, and backup URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated PNG and SVG files locally after a successful API call.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
