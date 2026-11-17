## Description:

Generates digital avatar assets and talking-head video clips from a text description or authorized person photo using supported avatar-video backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliviapp8](https://clawhub.ai/user/oliviapp8)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and video teams use this skill to create avatar IDs, optional cloned voice IDs, and talking-head video clips for narration workflows. It is intended for workflows where source photos, voice samples, scripts, and provider terms have been reviewed before upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used with real-person photos or voice samples, creating consent and impersonation risk.

Mitigation: Use only media the operator owns or has explicit permission to use, and document consent before creating avatars or cloned voices.

Risk: Provider API credentials may be exposed if copied into shared or checked-in configuration files.

Mitigation: Store credentials in a secret manager or environment-specific secure configuration and avoid committing provider keys.

Risk: Backend providers may apply different privacy, retention, and commercial-use terms to uploaded personal media.

Mitigation: Review each selected provider's privacy, retention, and commercial-use terms before uploading personal photos, voice samples, or scripts.

## Reference(s):

- [Backend Setup Guide](references/backend-setup.md)
- [Kling AI](https://klingai.kuaishou.com/)
- [Kling API Documentation](https://docs.qingque.cn/)
- [Jimeng](https://jimeng.jianying.com/ai-tool/home)
- [Jimeng API Documentation](https://www.volcengine.com/docs/jimeng/)
- [HeyGen API Documentation](https://docs.heygen.com/reference/)
- [D-ID API Documentation](https://docs.d-id.com/reference/)
- [Synthesia API Documentation](https://docs.synthesia.io/reference/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with structured YAML-style result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider-specific avatar IDs, voice IDs, preview URLs, rendered video URLs, and backend configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
