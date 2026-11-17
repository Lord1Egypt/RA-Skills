## Description:

Map RTOS SDK - 高德地图嵌入式 Map SDK 接入助手，支持栅格/矢量 Map 地图渲染、覆盖物绘制、轨迹导航及适配器实现指南。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs-amap](https://clawhub.ai/user/lbs-amap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate the AMap WatchSDK/RTOS map SDK into embedded or iOS-adapter projects, including SDK initialization, device activation, map rendering, overlays, navigation callbacks, and required platform adapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated integration code can be wrong if examples are copied without checking the installed SDK headers.

Mitigation: Verify every generated type, enum, struct field, function signature, and callback against the actual WatchSDK header files before compiling or shipping.

Risk: Device activation requires network access and sends device identifiers or license-related data.

Mitigation: Document what identifiers are sent during activation, add required location and privacy disclosures, and confirm that activation behavior matches the application's privacy policy.

Risk: Map SDK calls can fail or behave incorrectly when lifecycle and threading requirements are not followed.

Mitigation: Keep SDK calls on the documented main flow thread, follow the initialize-activate-create-render-destroy lifecycle, and handle documented error codes explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lbs-amap/skills/amap-rtos-sdk)
- [AMap Open Platform Console](https://console.amap.com/)
- [RTOS Map SDK Skills User Guide](README.md)
- [RTOS 地图 SDK Skills 使用文档](README_zh.md)
- [Quick Start](api/quick-start.md)
- [iOS Integration](api/ios-integration.md)
- [Lifecycle Management](api/lifecycle.md)
- [Adapter Implementation](api/adapters.md)
- [Map Operations](api/map-operations.md)
- [Overlays](api/overlays.md)
- [Navigation](api/navigation.md)
- [Adapter Requirements](references/adapter-requirements.md)
- [Core Types](references/core-types.md)
- [Error Codes](references/error-codes.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with C, Objective-C, Swift, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration guidance and example code that should be checked against the actual SDK headers before use.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
