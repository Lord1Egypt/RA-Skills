## Description: <br>
Cclaw helps agents create comedy writing drafts, generate FFmpeg-based video editing commands, and prepare comedy poster briefs for common show and platform formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kreator666](https://clawhub.ai/user/kreator666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and content teams use Cclaw to draft standup, sketch, manzai, parody, satire, and script material, then turn related requests into video-editing commands or poster-generation briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The video-editing workflow can ask an agent to execute FFmpeg on user-supplied files without clear confirmation or safety boundaries. <br>
Mitigation: Require review of the exact input path, output path, and FFmpeg command before execution, and write outputs to new files in a controlled workspace. <br>
Risk: Local-path development artifacts and weak path or argument validation can make generated video and poster workflows brittle or unsafe. <br>
Mitigation: Remove local development artifacts and add explicit confirmation, non-overwrite defaults, and path or argument validation before deployment. <br>


## Reference(s): <br>
- [Cclaw ClawHub page](https://clawhub.ai/kreator666/cclaw) <br>
- [Comedy theory index](references/comedy-theory.md) <br>
- [Comedy templates index](references/comedy-templates.md) <br>
- [Video tool workflow](modules/tools/video/README.md) <br>
- [Poster tool workflow](modules/tools/poster/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with generated drafts, design briefs, and inline command or code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose FFmpeg commands and media-generation steps that should be reviewed before execution] <br>

## Skill Version(s): <br>
1.10.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
