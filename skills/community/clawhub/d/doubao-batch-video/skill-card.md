## Description:

豆包批量视频生成 helps agents create batches of promotional short videos through Doubao web workflows, covering copy creation, prompt confirmation, video generation guidance, ffmpeg concatenation, audio mixing, and compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to plan Chinese short-video campaigns, confirm generated prompts, operate Doubao or fallback video generation, and assemble downloaded MP4 clips into final upload-ready videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in Doubao browser session, which may expose account state or cookies if reused on shared machines.

Mitigation: Use a dedicated Doubao/browser profile, avoid shared machines, and clear cookies or session data when the work is complete.

Risk: The local ffmpeg combine workflow processes files from an input directory and may behave unexpectedly on untrusted or poorly named video files.

Mitigation: Run the combine script only on video directories you control, with normal filenames and expected MP4 inputs.

## Reference(s):

- [Doubao web login and automation reference](references/doubao-login.md)
- [GEO video prompt reference](references/prompt-references.md)
- [Doubao website](https://www.doubao.com/)
- [Doubao video generator](https://www.doubao.com/video-generator)
- [ClawHub skill release page](https://clawhub.ai/hitjcl/skills/doubao-batch-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with command snippets and generated MP4 file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include prompt tables, browser automation steps, ffmpeg commands, and final or compressed MP4 files when the workflow is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
