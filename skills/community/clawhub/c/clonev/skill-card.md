## Description:

Clonev generates cloned-voice speech from a 6-30 second WAV voice sample and text using Coqui XTTS v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[instant-picture](https://clawhub.ai/user/instant-picture)

### License/Terms of Use:


## Use Case:

External users, developers, and agent operators use Clonev to generate OGG speech audio in a target voice from authorized voice samples, supplied text, and a language code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice recordings are sensitive biometric data and may be copied into a persistent voice-samples directory.

Mitigation: Use only your own voice or voices with explicit permission, and delete retained samples under the configured voice-samples directory after use.

Risk: Generated speech can be misused for third-party impersonation or deception.

Mitigation: Avoid celebrity or third-party impersonation, restrict use to authorized voices, and disclose synthetic audio where appropriate.

Risk: The skill runs a mutable Docker image for voice synthesis.

Mitigation: Pin and harden the Docker image before production use.

## Reference(s):

- [Complete Reference Guide](references/complete-guide.md)
- [Clonev ClawHub Skill Page](https://clawhub.ai/instant-picture/skills/clonev)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Audio]

**Output Format:** [Shell command invocation returning an OGG audio file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires text, a WAV voice sample path, and a language code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
