## Description:

Provides a Dahua Cloud Open IoT Python client and CLI for managing device lifecycle, GB28181 onboarding, SD cards, WiFi, callbacks, ringtones, image decryption, and related operations across 43 API endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dolynkdeveloper](https://clawhub.ai/user/dolynkdeveloper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integrators use this skill to automate Dahua Cloud Open IoT device onboarding, status checks, configuration, storage operations, WiFi updates, callbacks, and related surveillance or IoT operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dahua Cloud credentials can administer real devices.

Mitigation: Use least-privilege credentials, store them outside project files, and rotate credentials after testing or when access changes.

Risk: Default verbose logging and command-line arguments can expose device passwords, SecretKeys, request payloads, or API responses.

Mitigation: Avoid passing real secrets on the command line, disable verbose logging for production SDK use, and redact terminal output before sharing logs.

Risk: Delete, SD-card format, WiFi, callback, and password operations can affect production devices.

Mitigation: Test on non-production devices first and require human confirmation of device identifiers and operation targets before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dolynkdeveloper/skills/dahua-cloud-open-iot-basic-general-kit)
- [Publisher Profile](https://clawhub.ai/user/dolynkdeveloper)
- [Dahua Cloud Developer Platform](https://open.cloud-dahua.com/)
- [API Reference](references/api_reference.md)
- [API Coverage](API_COVERAGE.md)
- [Quickstart](QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; CLI and SDK calls return JSON-like API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Dahua Cloud ProductId, AccessKey, and SecretKey environment variables and network access to Dahua Cloud APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
