## Description:

Custom TTS using Gemini 2.5 Flash for high-quality, persona-driven voice output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhe1991](https://clawhub.ai/user/yangzhe1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate persona-driven audio from text through Gemini 2.5 Flash TTS when a GEMINI_API_KEY is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text provided to the skill is sent to Google's Gemini API using the configured GEMINI_API_KEY.

Mitigation: Use the skill only with text that is acceptable to send to the Gemini API, and avoid submitting sensitive content unless that use is approved.

Risk: The documented --voice option does not control the generated voice in the current implementation, which always uses Puck.

Mitigation: Do not rely on custom persona voice selection until the implementation is fixed or verified.

Risk: Generated audio is written as output_voice.<type> in the current working directory.

Mitigation: Run the command from an intended output directory or move/rename the generated file after creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangzhe1991/skills/gemini-tts)
- [Gemini TTS API endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance and command-line usage that produce an audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and writes generated audio to output_voice.<type> in the working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
