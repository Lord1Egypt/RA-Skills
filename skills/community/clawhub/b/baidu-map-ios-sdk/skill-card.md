## Description:

Guides agents in integrating and using Baidu Map iOS SDK, BMKLocationKit, and BaiduWalkNaviKit for maps, location, walking and cycling navigation, search, routes, annotations, and overlays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan, configure, and implement Baidu Maps features in iOS apps, including SDK setup, privacy consent, coordinate handling, map display, location, search, route rendering, and walking or cycling navigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can affect global developer tooling, package sources, Pod resolution, or Xcode build protections.

Mitigation: Review before installing; prefer a project-local Gemfile with pinned CocoaPods and Pod versions, keep trusted package sources unless an organizational mirror is intentional, avoid unrestricted pod update, and do not disable Xcode User Script Sandboxing without approving a temporary exception.

Risk: Generated iOS code may request location or camera permissions unnecessarily or initialize Baidu SDK components before required user consent.

Mitigation: Verify generated app code requests only needed permissions and shows the required privacy consent flow before map, location, search, or navigation SDK calls.

Risk: SDK examples can become incompatible with the locally installed Baidu SDK version or project headers.

Mitigation: Use the SDK version and headers installed in the target project as the source of truth, run xcodebuild after code changes, and correct API or import mismatches before release.

## Reference(s):

- [Baidu Maps iOS SDK Reference Index](artifact/references/reference.md)
- [CocoaPods Integration](artifact/references/cocoapods.md)
- [Project Configuration](artifact/references/project-config.md)
- [BMKMapView Map View](artifact/references/mapview.md)
- [BMKLocationKit Location](artifact/references/location.md)
- [Navigation](artifact/references/navi.md)
- [Route Planning](artifact/references/route.md)
- [Search Services](artifact/references/search.md)
- [Annotations](artifact/references/annotations.md)
- [Overlays](artifact/references/overlays.md)
- [Assets](artifact/references/assets.md)
- [Class Index](artifact/references/class-index.md)
- [Map UI Standards](artifact/references/ui-standards.md)
- [Utility Components](artifact/references/utils.md)
- [Baidu LBS Open Platform](https://lbsyun.baidu.com/)
- [ClawHub Skill Page](https://clawhub.ai/baidu-maps/skills/baidu-map-ios-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Objective-C or Swift snippets, CocoaPods and xcodebuild commands, and configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify iOS project files when asked to implement Baidu Maps features, then build with xcodebuild until compilation succeeds.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
