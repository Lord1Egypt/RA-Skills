## Description:

Pre-generates demo content, caches generated story and media assets, and helps verify readiness before live presentations that depend on AI-generated content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and demo teams use this skill to seed demo caches before presentations, reducing reliance on live AI API calls during the demo. The bundled script generates story text, narration, sound effects, and optional image content, then stores the generated cache in Turso.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can send prompt and story data to external AI services and store generated content in Turso.

Mitigation: Use test credentials and a disposable Turso database for demos; avoid real names, children's content, customer data, or production credentials unless retention and deletion controls are in place.

Risk: The implementation is narrower than the high-level description and may not fully verify every demo coverage gap.

Mitigation: Treat the bundled script as a demo-seeding helper and add explicit playback, cache-miss, TTL, and scenario coverage checks before relying on it for a live presentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/demo-precacher)
- [Publisher profile](https://clawhub.ai/user/nissan)
- [ElevenLabs text-to-speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})
- [ElevenLabs sound generation API endpoint](https://api.elevenlabs.io/v1/sound-generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and command-oriented setup details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured API credentials and may produce cached JSON plus base64-encoded media when the script is run.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
