## Description:

Use Chanjing TTS API to convert text to speech with file-based Chanjing credentials, optional API/configuration environment variables, and Python utility scripts for voice listing, task creation, and task polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzn1018](https://clawhub.ai/user/iamzn1018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate speech audio from text through the Chanjing TTS API. It supports listing available voices, creating synthesis tasks, polling for completion, and returning generated audio URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored Chanjing credentials may be sent to an endpoint selected by CHANJING_API_BASE.

Mitigation: Run only with CHANJING_API_BASE unset or pinned to the official HTTPS Chanjing API endpoint.

Risk: The skill stores app_id, secret_key, and refreshed access_token values in credentials.json.

Mitigation: Protect ~/.chanjing/credentials.json with owner-only permissions and do not commit or echo credential values.

Risk: An adjacent chanjing-credentials-guard login helper can be executed automatically when credentials are missing or invalid.

Mitigation: Inspect any adjacent chanjing-credentials-guard installation before allowing the skill to run.

Risk: Generated audio is obtained from URLs returned by the API response.

Mitigation: Validate returned download destinations as expected Chanjing media hosts before automatically downloading audio.

## Reference(s):

- [Chanjing API documentation](https://doc.chanjing.cc)
- [ClawHub skill page](https://clawhub.ai/iamzn1018/skills/chanjing-tts)
- [ClawHub publisher profile](https://clawhub.ai/user/iamzn1018)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text guidance with shell commands and JSON-capable script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can print voice tables, task IDs, full JSON voice data, or generated audio URLs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
