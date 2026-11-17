## Description:

Creates complete short-form videos from a topic or workflow by generating script, storyboard, digital-human narration, AI video scenes, and a local MP4 through Chanjing Open API and local media tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binkes](https://clawhub.ai/user/binkes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a topic, script, or prepared workflow into a publishable short-form video with narration, storyboarded scenes, generated video clips, and local packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Chanjing API credentials and persists credential state on disk.

Mitigation: Keep credentials.json out of version control, restrict file permissions, and use a dedicated credentials directory.

Risk: Credentialed network handling is broader than the declared trust boundary and downloads media from API response URLs.

Mitigation: Use the official Chanjing API host, avoid untrusted shared or CI environments, and review downloaded media destinations before execution.

Risk: Rendering invokes local media tooling and writes intermediate files and final video outputs.

Mitigation: Run in a controlled workspace with an explicit output directory and review retained work files after completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binkes/skills/chanjing-one-click-video-creation)
- [Chanjing documentation](https://doc.chanjing.cc)
- [README](artifact/README.md)
- [Render rules](artifact/templates/render_rules.md)
- [Storyboard prompt rules](artifact/templates/storyboard_prompt.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON workflow structures, shell commands, and generated local media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow_result.json, intermediate work files, and final_one_click.mp4 when rendering succeeds.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
