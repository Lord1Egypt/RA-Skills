## Description:

Uses the Chanjing TTS API to create a cloned voice from a user-provided public reference-audio URL, synthesize speech from text, and return generated audio URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzn1018](https://clawhub.ai/user/iamzn1018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to automate voice-clone text-to-speech workflows with Chanjing, including creating a custom voice, polling asynchronous jobs, and retrieving the generated audio URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling persists app_id, secret_key, access_token, and expire_in in credentials.json, and token refresh overwrites token fields on disk.

Mitigation: Keep CHANJING_CONFIG_DIR in a private user-owned directory, restrict file permissions, exclude credentials.json from version control and backups, and rotate credentials if exposure is suspected.

Risk: CHANJING_API_BASE can redirect requests carrying credentials, reference-audio URLs, synthesis text, tokens, and task identifiers to an environment-controlled API endpoint.

Mitigation: Leave CHANJING_API_BASE unset unless intentionally using a trusted HTTPS Chanjing-compatible endpoint.

Risk: Reference-audio URLs and generated output URLs cross service trust boundaries and may expose sensitive voice or text content to the configured API service.

Mitigation: Use only authorized reference audio, avoid sensitive synthesis text, and trust the configured API host and returned download URLs before use.

## Reference(s):

- [Chanjing documentation](https://doc.chanjing.cc)
- [Chanjing Open API endpoint](https://open-api.chanjing.cc)
- [ClawHub skill page](https://clawhub.ai/iamzn1018/skills/chanjing-tts-voice-clone)
- [Publisher profile](https://clawhub.ai/user/iamzn1018)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts print voice IDs, task IDs, and generated audio URLs as plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous API polling; generated audio is retrieved from API-returned URLs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
