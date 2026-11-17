## Description:

Helps developers integrate the Baidu Map Android SDK for Android map display, MapView and BaiduMap lifecycle handling, location, markers and overlays, POI search, route planning, walking and cycling navigation, privacy consent, and API key configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building Android applications that need Baidu map display, location, route planning, POI search, navigation, or related Gradle and AndroidManifest configuration. It produces implementation guidance with concrete Baidu SDK classes, method order, configuration snippets, and troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Android app guidance may involve location permissions and precise location handling.

Mitigation: Require clear user consent, request only needed permissions, and avoid unnecessary background or live location collection.

Risk: Shareable map links, route links, or POI links may disclose a user's location, route, or selected place.

Mitigation: Confirm exactly what location data is shared before creating or exposing links, and show users what will be sent.

Risk: Initializing Baidu SDK services before privacy consent can violate the skill's documented privacy sequence.

Mitigation: Call the Baidu privacy consent API before SDK initialization and delay location, search, or route requests until consent is granted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baidu-maps/skills/baidu-map-android-sdk)
- [百度地图 Android SDK 参考索引](references/reference.md)
- [百度地图 Android SDK 集成与核心 API 摘要](references/overview.md)
- [Gradle 集成 SDK](references/gradle.md)
- [工程配置](references/project-config.md)
- [地图容器与 BaiduMap](references/mapview.md)
- [显示定位](references/location.md)
- [点标记（Marker）](references/marker.md)
- [折线与多边形覆盖物](references/overlays.md)
- [POI 检索与地理编码](references/search.md)
- [路线规划](references/route.md)
- [坐标转换与坐标系](references/coordinate.md)
- [工具组件](references/tools.md)
- [错误码对照表](references/errorcode.md)
- [类与包速查](references/class-reference.md)
- [地图 UI 与交互约定](references/ui-standards.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Android, Gradle, XML, and Java code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privacy, location-permission, API-key, lifecycle, UI, and troubleshooting guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
