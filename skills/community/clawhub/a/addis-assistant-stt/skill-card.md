## Description:

Provides Speech-to-Text (STT) and text Translation using the Addis Assistant API (api.addisassistant.com). Use when the user needs to convert an audio file to text (specifically Amharic), or translate text between languages (e.g., Amharic to English). Requires 'x-api-key'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagmawibabi](https://clawhub.ai/user/dagmawibabi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to transcribe Amharic audio and translate text between supported language pairs through the Addis Assistant API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user audio and text to the Addis Assistant API.

Mitigation: Use it only when the user trusts Addis Assistant with the submitted content and avoid sensitive content unless approved.

Risk: The bundled scripts accept API keys as command-line arguments.

Mitigation: Prefer a revised version that reads API keys from an environment variable or secret store before installation.

Risk: The bundled scripts use endpoint strings without an explicit HTTPS scheme.

Mitigation: Prefer a revised version with explicit HTTPS endpoints.

## Reference(s):

- [Addis Assistant API Specifications](references/api_spec.md)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Plain text or JSON API responses returned by Python scripts and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an x-api-key and sends submitted audio or text to the Addis Assistant API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
