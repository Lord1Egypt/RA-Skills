## Description: <br>
Generate AI videos, create storyboards, compose and download video clips, and check task progress via a ComfyUI MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxx07](https://clawhub.ai/user/wangxx07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to expose ComfyUI video-generation workflows through MCP for prompt-based video creation, storyboard generation, video composition, downloads, and progress checks. The skill may send prompts and workflows to Comfy Cloud depending on configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud API use may send prompts and workflows outside the local environment. <br>
Mitigation: Confirm Comfy Cloud use is intended, disclose the data flow to users, and configure credentials through environment-managed secrets. <br>
Risk: The MCP server can bind broadly by default. <br>
Mitigation: Bind the server to localhost unless remote access is intentionally secured. <br>
Risk: Generated or downloaded media can be written to local output paths. <br>
Mitigation: Restrict output paths and review generated files before use or redistribution. <br>
Risk: Unpinned or outdated dependencies can increase operational risk. <br>
Mitigation: Pin dependencies where practical and keep FastMCP, requests, aiohttp, and related packages updated. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangxx07/comfyui-mcp-skill) <br>
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) <br>
- [FastMCP](https://github.com/jlowin/fastmcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, API calls] <br>
**Output Format:** [MCP tool responses containing task IDs, status JSON, storyboard text, and downloaded video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media may be written under the configured output directory; ComfyUI or Comfy Cloud connectivity is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
