## Description:

ACE音乐生成-专业版 guides agents through commercial AI music production workflows, including batch generation, cover creation, segment repainting, long-form output, and audio-input-driven generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and enterprise content teams use this skill to configure ACE Music Pro workflows for generating, repainting, covering, exporting, and organizing AI-produced music assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell execution and file-writing access while its command wrappers are unspecified.

Mitigation: Review before installing, require concrete vetted command wrappers, and avoid unattended shell execution until invocation guidance is narrowed.

Risk: Broad or mismatched triggers could cause the skill to be used outside explicit ACE music-generation tasks.

Mitigation: Restrict use to ACE music generation workflows and require human review for unrelated video, media conversion, or protected-content processing requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ace-music-tool-pro)
- [ACE Music API endpoint](https://api.acemusic.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline bash command examples and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated audio file paths, status codes, logs, and export or archival steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
