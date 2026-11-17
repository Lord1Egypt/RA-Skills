## Description:

Runs an interactive Chinese detective mystery game where an agent generates a case, supports text or voice interrogation, tracks evidence, scores accusations, and can save or resume progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delong-liu-bupt](https://clawhub.ai/user/delong-liu-bupt)

### License/Terms of Use:

MIT-0

## Use Case:

External users can run this skill to play a Chinese-language interactive mystery game with generated suspects, clues, interrogations, evidence review, and accusation scoring. Developers can configure text-only or voice-enabled play with LLM, ASR, and TTS service credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys, player audio, and generated game dialogue to endpoints configured through environment variables.

Mitigation: Review endpoint configuration before use, avoid custom endpoint overrides unless the host is trusted, and prefer --no-asr or --no-tts when audio or dialogue should not be sent to remote services.

Risk: Local .env files can change which credentials and services are used at runtime.

Mitigation: Inspect or remove local .env files before running the skill and install it only from a trusted directory.

Risk: Runtime dependencies and remote model services affect execution behavior.

Mitigation: Install in an isolated environment with reviewed dependency versions and re-review the skill before deployment.

## Reference(s):

- [Prompt Templates](references/prompts_cn.md)
- [State Schema](references/state_schema_cn.md)
- [ClawHub Skill Page](https://clawhub.ai/delong-liu-bupt/skills/detective-mystery)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, Configuration]

**Output Format:** [Interactive console text with generated JSON case state, saved game files, optional MP3 audio, and a final case_report.json file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports easy, medium, and hard difficulty; optional text-only mode; optional custom suspects and voice configuration.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
