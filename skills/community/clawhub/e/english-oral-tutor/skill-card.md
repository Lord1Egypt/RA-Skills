## Description:

English Oral Tutor helps an OpenClaw agent run sustained 30-minute English speaking practice for a B1 middle-school learner, with timed lesson phases, grammar correction, vocabulary teaching, topic rotation, and session logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiyicom](https://clawhub.ai/user/zhiyicom)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and tutoring teams use this skill to configure a conversation tutor for recurring English oral practice with a B1 learner. The skill guides lesson pacing, open-ended questioning, vocabulary teaching, grammar correction, topic deduplication, and end-of-session records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The timing plugin can affect more than the intended tutor agent or session.

Mitigation: Review before installing and scope the timing plugin to the intended agent and session.

Risk: The bundle can persist a child's lesson transcripts and conversation history without clear consent or retention controls.

Mitigation: Add explicit consent, retention, and deletion controls before storing transcripts, especially for a child.

Risk: The plugin includes a hard-coded hook log and developer-specific paths.

Mitigation: Remove the hard-coded hook log and replace developer-specific paths before deployment.

Risk: The optional browser voice userscript uses microphone input and text-to-speech output.

Mitigation: Enable the userscript only when microphone and TTS use are acceptable for the learner and environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhiyicom/skills/english-oral-tutor)
- [Share bundle README](README.md)
- [Skill design](SKILL.md)
- [Runtime prompt rules](workspace/SOUL.md)
- [Topic library](topic-library/topic-library.md)
- [Tutor timing plugin](plugin/tutor-timing/index.js)
- [Optional voice userscript](voice/openclaw-voice-userscript.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, prompt rules, JavaScript plugin code, browser userscript code, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional browser voice controls and file-based session records for conversation history and teaching transcripts.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
