## Description:

高德地图JSAPI专业版 helps agents produce AMap JSAPI v2.0 code and guidance for WebGL map rendering, vector layers, real-time traffic, batch geocoding, custom styles, truck routing, and commercial map applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate, review, and troubleshoot AMap JSAPI map application code for logistics, location-service SaaS, smart-city visualization, traffic overlays, geocoding, and routing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The activation scope may be broader than the stated AMap JSAPI purpose.

Mitigation: Use the skill only for map integration, routing, traffic, geocoding, visualization, and closely related AMap development tasks.

Risk: The skill requests read, write, and command execution tools.

Mitigation: Approve file writes or command execution only when the requested action is clearly needed for the current AMap development task.

Risk: AMap API keys and security secrets may be exposed if copied into generated source or logs.

Mitigation: Keep keys in environment variables or platform secret storage and review generated code before committing or sharing it.

## Reference(s):

- [Detailed AMap JSAPI examples](references/detail.md)
- [AMap Web API endpoint](https://webapi.amap.com)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/amap-jsapi-tool-pro)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript code blocks, JSON response examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file writes or command execution when building or testing AMap JSAPI examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
