## Description:

Converts text to natural speech using ElevenLabs for clinical and healthcare use cases. Use when generating patient instructions, discharge summaries, medication reminders, multilingual health messages, or accessible voice content for the OpenClaw Clinical Hackathon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw developers building clinical or healthcare agents use this skill to turn patient-facing written content into spoken instructions, reminders, discharge information, education, and accessible multilingual messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical prompts may contain PHI or other sensitive patient data that could be sent to a third-party API or exposed in logs.

Mitigation: Send only organization-approved text, avoid PHI in prompts and logs unless third-party processing is explicitly approved, and follow applicable privacy and security policies.

Risk: The ElevenLabs API key could be exposed if stored directly in committed configuration or shared files.

Mitigation: Store ELEVENLABS_API_KEY in an environment variable or secret manager and avoid committing secret values to the skill or workspace.

Risk: README music guidance could be mistaken for reviewed runtime music-generation behavior.

Mitigation: Treat the music section as documentation only unless runtime music-generation instructions are separately added, reviewed, and scanned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arunnadarasa/skills/elevenlabsclaw)
- [ElevenLabs Text-to-Speech API](https://elevenlabs.io/docs/api-reference/text-to-speech)
- [ElevenLabs Healthcare use cases](https://elevenlabs.io/use-cases/healthcare)
- [OpenClaw Skills](https://docs.openclaw.ai/skills)
- [ClawHub CLI](https://docs.openclaw.ai/tools/clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY before the skill is loaded; generated speech depends on the configured ElevenLabs account, model, voice, and any available TTS tool.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
