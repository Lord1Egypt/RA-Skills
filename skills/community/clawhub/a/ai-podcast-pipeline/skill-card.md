## Description:

Create Korean AI podcast packages from QuickView trend notes, including dual-host script writing, Gemini multi-speaker TTS audio, subtitle timing and rendering fixes, thumbnail and MP4 packaging, and YouTube title and description output for full or compressed editions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeong-wooseok](https://clawhub.ai/user/jeong-wooseok)

### License/Terms of Use:


## Use Case:

Content creators and agent users use this skill to turn QuickView AI trend notes into Korean podcast production packages. It guides script generation, Gemini multi-speaker TTS, Korean subtitles, subtitled video rendering, thumbnails, and YouTube publishing metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Thumbnail generation can invoke another local skill while passing an environment that may include credentials.

Mitigation: Review the referenced image generator before use, run with --no-image when image generation is not needed, or isolate execution with only the required environment variables.

Risk: TTS generation sends podcast script content to Google Gemini.

Mitigation: Only process scripts that are acceptable to send to Gemini and remove sensitive content before running TTS.

Risk: The skill requires API credentials and runs local media tooling.

Mitigation: Provide API keys through environment variables, avoid exposing keys in prompts or logs, and review commands before execution.

## Reference(s):

- [Podcast Script Prompt Template](artifact/references/podcast_prompt_template_ko.md)
- [Workflow Runbook](artifact/references/workflow_runbook.md)
- [Thumbnail Guidelines](artifact/references/thumbnail_guidelines_ko.md)
- [ClawHub Skill Page](https://clawhub.ai/jeong-wooseok/skills/ai-podcast-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands, file paths, and generated media assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce podcast scripts, MP3 audio, Korean SRT subtitles, subtitled MP4 video, PNG thumbnails, topic files, and YouTube title and description text.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
