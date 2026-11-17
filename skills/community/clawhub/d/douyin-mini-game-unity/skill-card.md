## Description:

Douyin mini-game Unity C# API ref - TT.* SDK (init/login/payment/ads/device/storage/UI), all C# equivalents of JS tt.* APIs. Payment requires server-side verify before production use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufengsheng](https://clawhub.ai/user/wufengsheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Unity games for Douyin Mini Game use this skill as a C# reference for TTSDK initialization, account APIs, payments, ads, device capabilities, storage, media, UI, and platform open capabilities.

### Deployment Geography for Use:

Global, subject to Douyin Mini Game platform availability and applicable local requirements.

## Known Risks and Mitigations:

Risk: Copy-pasteable storage and file examples may lead to unsafe file handling.

Mitigation: Add path validation and restrict reads and writes to approved application data locations before adapting examples.

Risk: Payment or ad reward examples may be mistaken for final reward authorization.

Mitigation: Use server-side verification for purchases and rewards, and treat client callbacks only as UI or status signals.

Risk: Logging examples may expose credentials, identifiers, or user data in production logs.

Mitigation: Redact sensitive values and keep diagnostic logs behind development-only build guards.

Risk: Recording examples may be used without checking user permission at the point of use.

Mitigation: Check the relevant recording permission before starting capture and avoid uploading recordings without explicit user consent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wufengsheng/skills/douyin-mini-game-unity)
- [Douyin Mini Game Unity C# API Overview](https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/api/c-api/api-overview)
- [Douyin Mini Game Payment Callback](https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/server/game-payment/payment-callback)
- [API Overview and Initialization](references/unity-core.md)
- [Account and Authorization](references/unity-account.md)
- [Payment](references/unity-payment.md)
- [Advertising](references/unity-ads.md)
- [System and Lifecycle](references/unity-system.md)
- [Device Capabilities](references/unity-device.md)
- [Storage and Files](references/unity-storage.md)
- [Media](references/unity-media.md)
- [UI and Rendering](references/unity-ui.md)
- [Open Capabilities](references/unity-open.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reference guidance with C# code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese-language API reference content for Unity TTSDK usage.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
