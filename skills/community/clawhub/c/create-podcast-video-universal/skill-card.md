## Description: <br>
CreateVideo Podcast to Video helps agents turn user-provided audio or text into vertical videos with background footage, optional ListenHub text-to-speech, ffmpeg media merging, and short content-analysis notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyken](https://clawhub.ai/user/jackyken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, social media operators, and developers use this skill to create 9:16 narrated videos from podcast-style scripts or existing narration, with optional Chinese TTS and reusable background templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User media and generated project files are processed locally with ffmpeg and ffprobe. <br>
Mitigation: Use trusted media inputs, keep ffmpeg current, and run work in the documented project directory so generated files are easy to inspect and remove. <br>
Risk: Text-to-speech mode sends script content to the external ListenHub MCP server. <br>
Mitigation: Avoid confidential, sensitive personal, or sensitive business content unless the user trusts the TTS provider and its handling of submitted text. <br>
Risk: The ListenHub MCP server is installed with an npm command. <br>
Mitigation: Review or pin the npm package before use, especially in managed or production environments. <br>


## Reference(s): <br>
- [CreateVideo Podcast to Video on ClawHub](https://clawhub.ai/jackyken/create-podcast-video-universal) <br>
- [jackyken ClawHub Publisher Profile](https://clawhub.ai/user/jackyken) <br>
- [ListenHub MCP Reference](references/listenhub-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration steps, generated file paths, and optional analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create MP4 video, voice audio, temporary files, and a Chinese content-analysis text file under video-projects/.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
