## Description:

Generate AI videos, create storyboards, compose and download video clips, and check task progress through a ComfyUI MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxx07](https://clawhub.ai/user/wangxx07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this MCP skill to connect an agent to ComfyUI workflows for prompt-based video generation, storyboard creation, video composition, download, and task progress checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP service can expose powerful network-accessible tools if run over HTTP without access controls.

Mitigation: Use stdio or bind HTTP only to 127.0.0.1; place any network deployment behind authentication and firewalling.

Risk: Prompts and workflow data may be sent to the configured ComfyUI cloud endpoint.

Mitigation: Avoid sensitive prompts unless cloud transmission is intended, and review endpoint and API key configuration before use.

Risk: Download and FFmpeg composition tools work with local filesystem paths.

Mitigation: Run as an unprivileged user in an isolated workspace and confine input and output paths before shared or network-reachable deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxx07/skills/comfyui-mcp-skill)
- [Publisher profile](https://clawhub.ai/user/wangxx07)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [FastMCP](https://github.com/jlowin/fastmcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Configuration]

**Output Format:** [MCP tool responses with JSON dictionaries, strings, local file paths, and generated or composed video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation is asynchronous and commonly returns a prompt ID for later progress checks or download.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
