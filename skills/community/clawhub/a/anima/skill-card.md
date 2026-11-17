## Description:

Anima generates 16:9 interactive avatar videos with character sprites, synthesized speech, emotion-based scene rendering, text overlays, and optional Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmyaoyuan](https://clawhub.ai/user/hmyaoyuan)

### License/Terms of Use:

ISC

## Use Case:

Developers and agent operators use this skill to turn structured dialogue scripts into avatar video clips, optionally generate sprite variants, and deliver finished videos through Feishu/Lark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted script text, target IDs, paths, or CSV entries can reach shell commands and may execute local commands or overwrite files.

Mitigation: Run only with scripts, CSV files, target IDs, and paths you fully trust; prefer a sandboxed account and review inputs before execution.

Risk: Feishu delivery and Gemini batch generation use shell calls with externally influenced values.

Mitigation: Avoid those paths until shell calls are replaced with safe argument-array subprocess calls or native HTTP APIs and filenames and recipient IDs are validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmyaoyuan/skills/anima)
- [Publisher profile](https://clawhub.ai/user/hmyaoyuan)
- [Fish Audio API dashboard](https://fish.audio/dashboard/api)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions]

**Output Format:** [MP4 video files, PNG sprite assets, temporary audio/frame files, console output, and optional Feishu media messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg, Node dependencies, and user-provided API credentials for Fish Audio, optional Gemini sprite generation, and optional Feishu delivery.]

## Skill Version(s):

3.3.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
