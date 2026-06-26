## Description: <br>
百度地图 iOS SDK 与 BMKLocationKit 集成与开发规范，覆盖地图、定位、步骑行导航、检索、路线、标注与覆盖物，并帮助开发者输出专业地图方案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Baidu Map, BMKLocationKit, BaiduWalkNaviKit, search, route planning, overlays, annotations, and CocoaPods configuration into iOS applications. It provides implementation guidance, configuration steps, sample code, and validation reminders for privacy consent, coordinates, map layout, and SDK compatibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Baidu map credentials and matching Bundle Identifier configuration. <br>
Mitigation: Use an iOS application AK scoped to the intended bundle, replace placeholders before testing, avoid committing secrets in shared repositories, and rotate any exposed keys. <br>
Risk: Location examples can be incomplete without app-specific privacy consent and permission handling. <br>
Mitigation: Add iOS permission prompts, required Info.plist usage strings, and an in-app privacy consent step before initializing map or location SDKs. <br>
Risk: Generated code or project configuration may not match the installed SDK headers. <br>
Mitigation: Build with xcodebuild and resolve compiler errors against the local SDK version before shipping the app. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/baidu-maps/baidu-map-ios-sdk) <br>
- [百度 LBS 控制台](https://lbsyun.baidu.com/) <br>
- [百度地图 iOS SDK 参考索引](references/reference.md) <br>
- [CocoaPods 集成](references/cocoapods.md) <br>
- [工程配置](references/project-config.md) <br>
- [BMKMapView 地图视图](references/mapview.md) <br>
- [百度 iOS 定位 SDK（BMKLocationKit）](references/location.md) <br>
- [路线规划](references/route.md) <br>
- [导航](references/navi.md) <br>
- [检索服务](references/search.md) <br>
- [覆盖物 (Overlay)](references/overlays.md) <br>
- [标注 (Annotation)](references/annotations.md) <br>
- [地图 UI 标准](references/ui-standards.md) <br>
- [类速查表](references/class-index.md) <br>
- [工具组件](references/utils.md) <br>
- [图片资源](references/assets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Objective-C snippets, shell commands, configuration notes, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CocoaPods setup, Info.plist keys, privacy consent steps, Baidu AK and Bundle Identifier reminders, xcodebuild validation commands, and SDK-specific API guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
