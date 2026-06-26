## Description: <br>
Map RTOS SDK - 高德地图嵌入式 Map SDK 接入助手，支持栅格/矢量 Map 地图渲染、覆盖物绘制、轨迹导航及适配器实现指南。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs-amap](https://clawhub.ai/user/lbs-amap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate the AMap WatchSDK/RTOS map SDK into embedded, wearable, and iOS-adapter projects. It helps generate adapter implementations, map rendering setup, overlays, navigation flows, lifecycle handling, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated integration examples may involve AMap keys, device IDs, activation data, network endpoints, and location behavior. <br>
Mitigation: Keep real AMap keys out of prompts, obtain SDK files from a trusted source, verify activation and network endpoints, and add appropriate location permission and privacy notices before shipping. <br>
Risk: Region settings, activation flow, and cleanup behavior can affect production behavior. <br>
Mitigation: Review area and country settings, activation requirements, lifecycle cleanup, and release configuration before deploying an app. <br>
Risk: Incorrect SDK threading or adapter implementations can cause integration failures. <br>
Mitigation: Call SDK methods on the required main workflow thread and verify memory, file, network, render, system, and thread adapters against the SDK headers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lbs-amap/amap-rtos-sdk) <br>
- [Quick Start](api/quick-start.md) <br>
- [iOS Integration](api/ios-integration.md) <br>
- [Adapter Implementation](api/adapters.md) <br>
- [Lifecycle Management](api/lifecycle.md) <br>
- [Map Operations](api/map-operations.md) <br>
- [Navigation](api/navigation.md) <br>
- [Overlay Management](api/overlays.md) <br>
- [Adapter Requirements](references/adapter-requirements.md) <br>
- [Core Types](references/core-types.md) <br>
- [Error Codes](references/error-codes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [AMap Open Platform Console](https://console.amap.com/) <br>
- [Cursor Documentation](https://docs.cursor.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with C, Objective-C, Swift, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SDK code should be checked against local WatchSDK header files before use.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
