## Description: <br>
Guides Android developers through Baidu Map Android SDK integration, including MapView lifecycle, privacy initialization, API key setup, coordinates, markers, POI search, route planning, and walking or cycling navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Android developers and engineers use this skill to integrate Baidu Maps features into Android apps with correct SDK setup, privacy consent flow, AK configuration, MapView lifecycle handling, location, overlays, search, and route-planning patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated examples can involve Baidu Maps API keys, Android location permissions, and user location data. <br>
Mitigation: Keep the AK scoped to the correct package and signing certificate, request Android location permissions only when needed, and ensure users consent to Baidu SDK privacy terms before SDK initialization. <br>
Risk: Generated sharing flows may create or expose location, POI, or route short links. <br>
Mitigation: Require explicit user confirmation before creating or sharing location, POI, or route links. <br>


## Reference(s): <br>
- [Baidu Map Android SDK Reference Index](references/reference.md) <br>
- [Gradle SDK Integration](references/gradle.md) <br>
- [Android Project Configuration](references/project-config.md) <br>
- [SDK Integration and Core API Overview](references/overview.md) <br>
- [MapView and BaiduMap](references/mapview.md) <br>
- [Location Display](references/location.md) <br>
- [Markers](references/marker.md) <br>
- [Overlays](references/overlays.md) <br>
- [POI and Geocoding Search](references/search.md) <br>
- [Route Planning and Overlays](references/route.md) <br>
- [Coordinate Systems and Conversion](references/coordinate.md) <br>
- [Map Utilities](references/tools.md) <br>
- [Error Codes](references/errorcode.md) <br>
- [Class and Package Reference](references/class-reference.md) <br>
- [Map UI and Interaction Standards](references/ui-standards.md) <br>
- [Gradle Release Checksums](https://gradle.org/release-checksums/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Android, Gradle, XML, and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privacy consent, API key, lifecycle, coordinate-system, permission, and troubleshooting checklists.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
