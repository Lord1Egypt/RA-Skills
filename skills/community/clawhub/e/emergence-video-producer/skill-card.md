## Description:

Automated video production pipeline for product demos and academic tutorials using WebReel for browser recording, DashScope or Edge-TTS for narration, and FFmpeg for assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and product teams use this skill to turn an approved Markdown video script or storyboard into a tutorial, product demo, or academic presentation video. It supports browser walkthroughs and slide-style presentations with generated narration and FFmpeg assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audio helper loads local .env values before calling a network-capable text-to-speech subprocess.

Mitigation: Run the skill in a workspace without sensitive .env files, or remove dotenv loading and provide only the minimal narration service credentials required for the task.

Risk: Narration text, slide content, target URLs, and template background image fetches may be sent to external services.

Mitigation: Review planned video content and URLs before production, avoid confidential inputs, and use approved internal or local services where required.

Risk: Generated files may overwrite existing workspace outputs during video production.

Mitigation: Install and run the skill in a dedicated project workspace and choose output paths that can be safely replaced.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emergencescience/skills/emergence-video-producer)
- [Publisher Profile](https://clawhub.ai/user/emergencescience)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown storyboards, JSON recording configuration, Slidev Markdown, narration audio, and assembled video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires external tools such as WebReel, FFmpeg, Edge-TTS or DashScope credentials, and Pillow for some frame extraction workflows.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
