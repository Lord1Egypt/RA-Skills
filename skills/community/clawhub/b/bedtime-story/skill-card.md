## Description:

Generates personalized multi-character Chinese bedtime stories from a child's name, age, and interests, with optional text-to-speech synthesis into MP3 audio and continuation state across episodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delong-liu-bupt](https://clawhub.ai/user/delong-liu-bupt)

### License/Terms of Use:

MIT-0

## Use Case:

External users can generate customized Chinese bedtime story episodes for children using a child's name, age, and interests. The skill is also useful for creating serialized stories that preserve characters, world state, and plot summaries between runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child-related prompts and generated story content may be sent to configurable external LLM and TTS endpoints.

Mitigation: Use only trusted provider endpoints, minimize child-identifying inputs, and review provider privacy terms before use.

Risk: API credentials are loaded from environment variables or local .env files and used with configured service endpoints.

Mitigation: Run in a dedicated virtual environment or clean working directory, set only the required credentials, and avoid untrusted .env files.

Risk: Generated story state, text, and audio can retain child-associated details on disk.

Mitigation: Delete artifact/outputs when retention is not needed and restrict access to generated files.

## Reference(s):

- [Prompt Templates Reference](references/prompts_cn.md)
- [State Schema Reference](references/state_schema_cn.md)

## Skill Output:

**Output Type(s):** [text, audio, configuration]

**Output Format:** [Plain text story files, MP3 audio files, and JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can skip audio synthesis with --no-tts; continuation mode reads and updates local story state.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
