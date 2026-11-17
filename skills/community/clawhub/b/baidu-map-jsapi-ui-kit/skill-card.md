## Description:

百度地图官方 UI 交互组件，提供地点自动补全（PlaceAutocomplete）、地点检索（PlaceSearch）、地点详情（PlaceDetail）和路径规划（RoutePlan）组件的使用参考，帮助开发者快速实现地图界面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill as a reference for integrating Baidu Maps JSAPI UI Kit components into web map applications, including autocomplete, place search, place details, and driving route planning. It is most useful when an agent needs to produce implementation guidance, setup steps, or example JavaScript/TypeScript code for these UI components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, selected POIs, place UIDs, and route coordinates may be sent to Baidu Maps when applications use the documented components.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering sensitive location data in examples or production workflows.

Risk: Examples show CDN loading for the UI Kit, which can introduce supply-chain exposure if assets change unexpectedly.

Mitigation: For production apps, pin @baidumap/jsapi-ui-kit to a reviewed version and pin or self-host CDN assets with SRI where practical.

Risk: The examples require a Baidu Maps JSAPI key through BMAP_JSAPI_KEY or an API script URL.

Mitigation: Store and configure the key deliberately, apply provider-side restrictions where available, and avoid committing secrets into source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baidu-maps/skills/baidu-map-jsapi-ui-kit)
- [快速开始](artifact/references/getting-started.md)
- [PlaceAutocomplete 地点自动补全](artifact/references/place-autocomplete.md)
- [PlaceSearch 地点检索](artifact/references/place-search.md)
- [PlaceDetail 地点详情](artifact/references/place-detail.md)
- [RoutePlan 路径规划](artifact/references/route-plan.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JavaScript, TypeScript, HTML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BMAP_JSAPI_KEY and a loaded Baidu Maps JS API instance for examples that call Baidu services.]

## Skill Version(s):

1.0.5 (source: server release evidence; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
