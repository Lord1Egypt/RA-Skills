## Description: <br>
百度地图官方 UI 交互组件，提供地点自动补全（PlaceAutocomplete）、地点检索（PlaceSearch）、地点详情（PlaceDetail）和路径规划（RoutePlan）组件的使用参考，快速实现地图界面，大幅提升开发效率。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill as reference documentation for integrating Baidu Map JSAPI UI components for place autocomplete, place search, place detail display, and route planning in map applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Baidu Maps API key. <br>
Mitigation: Restrict the BMAP_JSAPI_KEY to intended domains, services, and quotas before using examples. <br>
Risk: Map searches and route planning can send searches, coordinates, waypoints, destination names, or POI identifiers to Baidu services. <br>
Mitigation: Provide appropriate user notice or consent before sending location-related data. <br>
Risk: Examples reference external Baidu and CDN dependencies. <br>
Mitigation: Review those dependencies and pin approved delivery paths before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baidu-maps/baidu-map-jsapi-ui-kit) <br>
- [快速开始](references/getting-started.md) <br>
- [PlaceAutocomplete 地点自动补全组件](references/place-autocomplete.md) <br>
- [PlaceSearch 地点检索组件](references/place-search.md) <br>
- [PlaceDetail 地点详情组件](references/place-detail.md) <br>
- [RoutePlan 路径规划组件](references/route-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown reference guidance with JavaScript, TypeScript, HTML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Baidu Maps JSAPI key via BMAP_JSAPI_KEY.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
