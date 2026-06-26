## Description: <br>
帮助在 HarmonyOS NEXT 上使用百度地图鸿蒙 SDK 进行开发，覆盖地图展示与交互、覆盖物绘制、POI/AOI 检索、路线规划、导航、前台/后台定位、地址与 POI 获取等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build HarmonyOS NEXT applications with Baidu Map SDK packages. It helps select compatible packages, configure permissions and assets, implement map/search/navigation/location features, and check SDK APIs while producing code and setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to change Baidu SDK dependencies, rewrite imports, and run install or build commands. <br>
Mitigation: Require confirmation before ohpm uninstall/install, bulk import rewrites, and build commands, then review diffs after any package migration. <br>
Risk: The skill can involve API keys, precise location, route text, device identifiers, and background location permissions. <br>
Mitigation: Treat those values as sensitive data, avoid exposing them in prompts or logs, and review requested permissions before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baidu-maps/baidu-map-harmonyos-sdk) <br>
- [Baidu HarmonyNEXT SDK FAQ](https://lbsyun.baidu.com/faq/api?title=harmonynextsdk) <br>
- [Baidu Map HarmonyOS SDK Reference](references/reference.md) <br>
- [API Module Index](references/api/modules.md) <br>
- [Package Management Guide](references/guidelines/package-management.md) <br>
- [Build and Test Guide](references/guidelines/build-and-test.md) <br>
- [Location SDK Guide](references/guidelines/location-sdk-guide.md) <br>
- [Walk/Ride Navigation SDK Guide](references/guidelines/walkride-sdk-guide.md) <br>
- [Asset Reference](references/assets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with ArkTS/TypeScript, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dependency migration steps, permission configuration, SDK API references, and build or ArkTSCheck commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
