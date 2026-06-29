## Description: <br>
Baidu Map RTOS SDK (mapsdk-rtos) application-layer integration guidance and code generation for initialization, authentication, map control, overlays, search, route planning, offline maps, navigation, and Canvas adapter work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Baidu Map RTOS SDK public APIs into RTOS or macOS simulator applications. It helps produce guidance, C/C++ examples, shell commands, and configuration steps for authentication, map rendering, overlays, search, navigation, offline maps, and platform Canvas adapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated code may handle AK or license values, location data, offline map downloads, file paths, or SDK delete/download APIs. <br>
Mitigation: Install only when authorized to use Baidu mapsdk-rtos materials, and review generated code before running it in an SDK or device environment. <br>
Risk: Application-layer examples may need platform-specific adaptation for RTOS, macOS simulator, Canvas, threading, storage, and networking behavior. <br>
Mitigation: Validate generated C/C++ against the target platform adapter, UI-thread rendering path, cache paths, and SDK callback behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baidu-maps/skills/baidu-map-rtos-skills) <br>
- [README_EN.md](README_EN.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Initialization, authentication, and Canvas adapter](references/init-auth.md) <br>
- [Platform Adapter and Canvas implementation](references/adapter-build.md) <br>
- [Map control and overlays](references/overlay-map-control.md) <br>
- [Search, navigation, offline maps, and mapAPP demos](references/search-navi-offline.md) <br>
- [End-to-end runnable examples](references/demo.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with C/C++ code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated code should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
