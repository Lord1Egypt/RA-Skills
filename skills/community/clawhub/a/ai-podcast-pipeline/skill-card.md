## Description: <br>
Create Korean AI podcast packages from QuickView trend notes, including dual-host script writing, Gemini multi-speaker TTS audio generation, subtitle timing and render fixes, thumbnail and MP4 packaging, and YouTube title and description output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeong-wooseok](https://clawhub.ai/user/jeong-wooseok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators and automation-focused developers use this skill to turn QuickView trend notes into Korean podcast production packages with scripts, dual-speaker audio, subtitles, thumbnail assets, preview media, and publishing metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The thumbnail step runs an undeclared external helper with the user's environment and API key. <br>
Mitigation: Review the nano-banana-pro helper and its dependencies before enabling thumbnail generation, or run packaging with image generation disabled until that helper is trusted. <br>
Risk: Source notes and dialogue text may be sent to Gemini for text-to-speech or thumbnail generation. <br>
Mitigation: Avoid confidential source notes and use a dedicated Gemini API key with limited quota. <br>
Risk: Media generation commands can overwrite existing output files. <br>
Mitigation: Choose output directories deliberately and review generated paths before running the build scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeong-wooseok/ai-podcast-pipeline) <br>
- [Podcast Script Prompt Template](references/podcast_prompt_template_ko.md) <br>
- [Thumbnail Guidelines](references/thumbnail_guidelines_ko.md) <br>
- [Workflow Runbook](references/workflow_runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated media or text file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces podcast scripts, MP3 audio, SRT subtitles, MP4 videos, thumbnail images, preview media, topic lists, YouTube title options, and descriptions.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
