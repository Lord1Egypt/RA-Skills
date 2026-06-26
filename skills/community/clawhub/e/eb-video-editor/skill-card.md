## Description: <br>
Edits existing videos with ffmpeg and Python, covering trimming, joining, subtitles, audio changes, resizing, format conversion, compression, overlays, batch processing, and transcript-based edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emersonbraun](https://clawhub.ai/user/emersonbraun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and agents use this skill to plan and produce non-destructive ffmpeg and Python workflows for manipulating existing video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commands may overwrite outputs, target the wrong files, or process many files unintentionally during batch work. <br>
Mitigation: Review commands before execution, keep original videos backed up, use a separate output directory, and confirm file globs and output names before processing. <br>
Risk: Package installs or parallel jobs may change the local environment or consume significant system resources. <br>
Mitigation: Review package install steps and run batch or parallel jobs with explicit concurrency limits appropriate for the machine. <br>


## Reference(s): <br>
- [Video Editor ClawHub page](https://clawhub.ai/emersonbraun/eb-video-editor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and scripts should be reviewed before execution, especially for overwrite flags, file globs, batch loops, package installs, and parallel jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
