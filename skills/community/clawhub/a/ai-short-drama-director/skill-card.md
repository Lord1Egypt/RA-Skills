## Description:

AI Short Drama Director helps an agent turn a user-provided script or story into a complete AI short-drama video workflow covering script analysis, character and scene assets, storyboard design, first frames, video clips, and post-production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to plan and execute an AI-assisted short-drama production workflow from a script, including prompts, storyboard assets, clip generation steps, subtitles, background music, and final video assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may ask the agent to run an unscoped system package installation command for ffmpeg.

Mitigation: Require explicit approval before any apt-get command is run, and prefer a disposable or project-specific workspace.

Risk: The workflow generates many local media and intermediate files during short-drama production.

Mitigation: Run it in a workspace with sufficient disk space and review generated images, clips, subtitles, and final video before sharing or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/ai-short-drama-director)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON indexes, prompt text, shell commands, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged local outputs under output/, including analysis notes, asset lists, storyboard indexes, frames, video clips, subtitles, music, a final video, and a production report.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
