## Description: <br>
Generates vertical podcast-style videos from user-provided scripts by creating two-speaker podcast audio with ListenHub MCP, looping a template video with ffmpeg, and producing a concise content analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyken](https://clawhub.ai/user/jackyken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and agent users use this skill to turn Chinese podcast or short-video scripts into vertical MP4 videos with generated two-speaker audio, selected background templates, and reusable promotional copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a ListenHub API key and installation of an external MCP package. <br>
Mitigation: Use a revocable ListenHub API key and review the MCP package before installing it. <br>
Risk: User scripts and source content may be sent to the ListenHub service for podcast generation. <br>
Mitigation: Avoid submitting confidential or sensitive scripts to the service. <br>
Risk: Incorrect speaker IDs, language settings, template files, or output locations can produce unwanted media or files in the wrong place. <br>
Mitigation: Confirm language, speaker IDs, template video files, and output directory before generating media. <br>


## Reference(s): <br>
- [CreateVideo Skill Page](https://clawhub.ai/jackyken/create-podcast-video) <br>
- [ListenHub MCP Calling Guide](references/listenhub-guide.md) <br>
- [Explosive Dialogue Copywriting Template](references/copywriting-explosive-dialogue.md) <br>
- [Copywriting Template Reference](references/copywriting-template.md) <br>
- [ListenHub Website](https://marswave.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown status summary with shell commands, generated MP4 and MP3 files, and a text content-analysis file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a dated task directory containing template media, generated podcast audio, the final MP4 video, and content analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
