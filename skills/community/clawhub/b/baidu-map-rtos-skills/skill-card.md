## Description: <br>
Helps developers integrate Baidu Map RTOS SDK (mapsdk-rtos) application layers by producing guidance and code for authentication, map component setup, overlays, search, navigation, offline maps, Canvas adapters, and mapAPP demos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or troubleshoot RTOS map applications against the public mapsdk-rtos APIs. It supports initialization and authentication, Canvas adapter implementation, map controls and overlays, POI and route search, offline maps, navigation, and macOS simulator demo extension. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated integration code may handle license keys, authentication flow, local paths, UI-thread callbacks, and map rendering state incorrectly if applied without review. <br>
Mitigation: Review generated code against the initialization order, Canvas binding, callback-thread, and troubleshooting guidance before use, and provide credentials only when clearly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baidu-maps/skills/baidu-map-rtos-skills) <br>
- [Skill definition](SKILL.md) <br>
- [Initialization, authentication, and Canvas adapter](references/init-auth.md) <br>
- [Platform Adapter and Canvas implementation](references/adapter-build.md) <br>
- [Map state, overlays, and touch](references/overlay-map-control.md) <br>
- [Search, navigation, offline maps, and mapAPP demos](references/search-navi-offline.md) <br>
- [End-to-end demo examples](references/demo.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with C/C++ code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance and code examples for application-layer integration; it does not directly execute SDK APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
