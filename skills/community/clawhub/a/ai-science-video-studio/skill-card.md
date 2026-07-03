## Description: <br>
Creates an eight-stage AI science explainer video workflow for Mandarin educational videos using digital-human segments, voice cloning, Pillow-rendered slides, karaoke subtitles, FFmpeg compositing, and audio/video QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, educators, and developers use this skill to plan and assemble Mandarin AI science explainer videos that combine a presenter avatar, narrated slides, subtitles, transitions, and QA checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may operate through an authenticated Google browser profile. <br>
Mitigation: Use a dedicated browser profile for video generation and avoid exposing unrelated signed-in accounts or sensitive sessions. <br>
Risk: The workflow uses personal voice references and portrait images for cloning or digital-human generation. <br>
Mitigation: Use only voices and portraits that the user owns or has permission to use, and keep consent records with the project assets. <br>
Risk: The scripts can process local media files, overwrite outputs, and invoke FFmpeg on supplied paths. <br>
Mitigation: Run the workflow in a dedicated project directory, review input and output paths before execution, and avoid untrusted media files. <br>
Risk: The subtitle workflow may install Python packages at runtime. <br>
Mitigation: Review runtime package installation before proceeding and prefer a pinned, isolated Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/ai-science-video-studio) <br>
- [Script format reference](references/script_format.md) <br>
- [Professional QA review checklist](references/qa_checklist.md) <br>
- [Known pitfalls and solutions](references/pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON snippets, Python and shell commands, and generated media file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local media assets, subtitle frame directories, analysis reports, and final MP4 outputs when the user runs the workflow scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
