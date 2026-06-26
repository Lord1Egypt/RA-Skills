## Description: <br>
Guides agents through integrating the AMap Android LLM Agent SDK for natural-language map and navigation interactions, including SDK setup, AI queries, result handling, AMap app linking, transport modes, logging, lifecycle management, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs-amap](https://clawhub.ai/user/lbs-amap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to have an agent generate Android code and configuration for AMap LLM Agent SDK integration. It helps implement natural-language navigation queries, route and POI result handling, LinkClient communication with the AMap app, transport mode switching, lifecycle cleanup, logging, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated code may start precise location updates or high-accuracy tracking without enough user consent context. <br>
Mitigation: Require Android runtime permission checks, explicit in-app consent, and privacy-policy acknowledgement before starting location updates; limit high-accuracy updates to active navigation or user-requested map tasks. <br>
Risk: Generated LinkClient or navigation code may change navigation, route, or authentication state based on agent output. <br>
Mitigation: Require user confirmation before starting or stopping navigation, switching routes, changing command destination, launching authentication, or opening the AMap app download flow. <br>
Risk: Generated logging or telemetry examples may expose prompts, routes, POIs, session IDs, or location details. <br>
Mitigation: Redact sensitive fields, disable verbose logging in production, and only collect route, POI, prompt, session, or location data after clear user notice. <br>
Risk: Generated dependency snippets may use SDK coordinates that need publisher verification before production use. <br>
Mitigation: Verify the publisher and Android SDK dependency coordinates with official AMap sources before installing packages or shipping generated code. <br>


## Reference(s): <br>
- [Quick Start](api/quick-start.md) <br>
- [Agent Query](api/agent-query.md) <br>
- [Query Result Handling](api/query-result.md) <br>
- [LinkClient and AMap App Communication](api/link-client.md) <br>
- [Transport Mode Switching](api/transport-mode.md) <br>
- [Logger Configuration](api/logger.md) <br>
- [Lifecycle Management](api/lifecycle.md) <br>
- [Core Classes](references/core-classes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Voice Commands](references/voice-commands.md) <br>
- [AMap Open Platform Console](https://console.amap.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Java, Gradle, XML, text prompt, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Android dependency coordinates, SDK initialization flows, navigation and location handling, LinkClient operations, logging setup, lifecycle cleanup, and troubleshooting checks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
