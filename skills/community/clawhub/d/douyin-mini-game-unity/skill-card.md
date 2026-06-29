## Description: <br>
Douyin Mini Game Unity provides a Unity C# reference for Douyin mini-game TT.* APIs covering initialization, login, payments, ads, device, storage, media, UI, and related platform capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wufengsheng](https://clawhub.ai/user/wufengsheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to look up Douyin mini-game Unity C# TT.* API usage and adapt Unity projects for Douyin mini-game platform features such as authentication, payments, ads, device capabilities, storage, media, and UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: C# snippets touching payments may be copied into production without server-side payment verification. <br>
Mitigation: Verify payments server-side and grant currency or items only after signed payment callbacks are confirmed. <br>
Risk: Examples involving identifiers, launch metadata, user information, clipboard, screen recording, or storage operations can expose sensitive data if adapted carelessly. <br>
Mitigation: Keep debug-command and logging guards, require user consent for clipboard and screen recording, and add explicit runtime checks around recording and destructive storage operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wufengsheng/skills/douyin-mini-game-unity) <br>
- [Official Douyin Unity C# API overview](https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/api/c-api/api-overview) <br>
- [Official Douyin account API documentation](https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/api/c-api/account) <br>
- [Official Douyin payment callback documentation](https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/server/game-payment/payment-callback) <br>
- [API overview and initialization](artifact/references/unity-core.md) <br>
- [Account and authorization](artifact/references/unity-account.md) <br>
- [Payment](artifact/references/unity-payment.md) <br>
- [Advertising](artifact/references/unity-ads.md) <br>
- [System and lifecycle](artifact/references/unity-system.md) <br>
- [Device capabilities](artifact/references/unity-device.md) <br>
- [Storage and files](artifact/references/unity-storage.md) <br>
- [Media](artifact/references/unity-media.md) <br>
- [Open capabilities](artifact/references/unity-open.md) <br>
- [UI and rendering](artifact/references/unity-ui.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with C# code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; examples require developer adaptation and security review before production use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
