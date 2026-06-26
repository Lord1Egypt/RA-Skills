## Description: <br>
Baidu Map JSAPI GL provides Baidu Maps JSAPI WebGL guidance for map initialization, overlays, layers, events, styling, route planning, local search, geocoding, coordinate conversion, and performance-oriented 3D map development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to build and debug Baidu Maps JSAPI WebGL applications, including map pages, overlays, interactive events, custom styles, tile layers, route planning, local search, geocoding, and coordinate conversion. It also guides users who need to obtain or troubleshoot a browser-side Baidu Maps AK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baidu Maps AK values can be exposed or abused if pasted into prompts, source control, or unrestricted browser applications. <br>
Mitigation: Keep real keys out of prompts and repositories, use BMAP_JSAPI_KEY only through approved configuration, and restrict keys with domain or IP allowlists and quotas. <br>
Risk: Map, route, search, geocoding, and coordinate-conversion examples may send precise addresses or coordinates to Baidu services. <br>
Mitigation: Get appropriate user consent before using precise location data and avoid submitting unnecessary personal or sensitive locations. <br>
Risk: Tile-layer examples include non-HTTPS endpoint patterns that could expose map traffic or be blocked by secure pages. <br>
Mitigation: Prefer HTTPS tile endpoints and validate third-party tile service terms before deployment. <br>
Risk: InfoWindow and custom overlay examples can render HTML supplied by application data. <br>
Mitigation: Sanitize user-controlled content before placing it into InfoWindow or custom overlay HTML. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baidu-maps/baidu-map-jsapi-gl) <br>
- [Baidu Maps Open Platform](https://lbsyun.baidu.com/) <br>
- [Baidu Maps AK console](https://lbsyun.baidu.com/apiconsole/key) <br>
- [基础类](references/base-classes.md) <br>
- [通用常量](references/constants.md) <br>
- [地图初始化](references/map-init.md) <br>
- [覆盖物通用操作](references/overlay-common.md) <br>
- [Marker 点标记](references/marker.md) <br>
- [Polyline 折线](references/polyline.md) <br>
- [Polygon 多边形](references/polygon.md) <br>
- [Circle 圆形](references/circle.md) <br>
- [CustomOverlay 自定义覆盖物](references/custom-overlay.md) <br>
- [InfoWindow 信息窗口](references/info-window.md) <br>
- [地图事件](references/map-events.md) <br>
- [覆盖物事件](references/overlay-events.md) <br>
- [个性化地图样式](references/map-style.md) <br>
- [XYZLayer 第三方图层](references/xyz-layer.md) <br>
- [MVTLayer 矢量瓦片图层](references/mvt-layer.md) <br>
- [路径规划通用配置](references/route-common.md) <br>
- [DrivingRoute 驾车路线规划](references/driving-route.md) <br>
- [WalkingRoute 步行路线规划](references/walking-route.md) <br>
- [RidingRoute 骑行路线规划](references/riding-route.md) <br>
- [TransitRoute 公交路线规划](references/transit-route.md) <br>
- [LocalSearch 本地检索](references/local-search.md) <br>
- [Geocoder 地理编码](references/geocoder.md) <br>
- [Convertor 坐标转换](references/convertor.md) <br>
- [获取密钥（AK）](references/get-ak.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and HTML code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Baidu Maps JSAPI browser AK, represented in metadata as BMAP_JSAPI_KEY.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
