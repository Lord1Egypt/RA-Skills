## Description:

Convert written medical content into podcast or video scripts optimized for audio delivery, including pronunciation guides, timing markers, and audio-friendly structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and medical content teams use this skill to convert medical or scientific text into audio-ready scripts for podcasts, educational videos, lectures, audiobooks, and voiceover narration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install manifest and shipped code do not match the security claims.

Mitigation: Review before installing; do not run pip install -r requirements.txt as written, and remove the file or leave it comment-only.

Risk: The converter can read input files and overwrite output files reachable by the process.

Mitigation: Run it only on trusted input and output paths inside a workspace with appropriate file permissions.

Risk: Generated medical scripts may preserve or introduce incorrect medical wording because the skill transforms text and does not verify clinical facts.

Mitigation: Have qualified subject matter reviewers validate medical accuracy before recording or publishing.

## Reference(s):

- [Audio Script Writer - References](references/guidelines.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/audio-script-writer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [JSON from the bundled CLI, or audio-script prose with pacing cues, pronunciation notes, and timing metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes target duration, estimated duration, word count, speaking pace, style, pronunciation notes, and formatting notes when using the bundled CLI.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
