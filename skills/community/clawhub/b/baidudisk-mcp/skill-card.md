## Description: <br>
Use Baidu Netdisk via mcporter and a stdio MCP server with hot-reload token file credentials for official 2.0 toolset operations and legacy aliases from OpenClaw without storing access_token in repo files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forevershu](https://clawhub.ai/user/forevershu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure a Baidu Netdisk MCP server, run mcporter commands, and perform token-backed file listing, search, upload, move, copy, rename, delete, quota, and media metadata operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an MCP tool broad Baidu Netdisk account access through token-backed file-management operations. <br>
Mitigation: Use a dedicated or least-privileged Baidu Netdisk token or account where possible, and require manual approval before uploads, moves, renames, batch operations, or deletes. <br>
Risk: Credential exposure could allow unauthorized access to the connected Baidu Netdisk account. <br>
Mitigation: Protect ~/.openclaw/credentials/baidudisk.json, keep tokens out of repository files, and rotate the token if exposure is suspected. <br>
Risk: Destructive or large batch file operations could modify or remove cloud files unexpectedly. <br>
Mitigation: Review batch inputs before execution, use dry_run where supported, keep destination prefixes constrained, and require the explicit delete confirmation behavior. <br>
Risk: URL-based uploads can fetch remote content into Baidu Netdisk. <br>
Mitigation: Review URLs before use and rely on the skill's HTTP(S)-only, non-localhost, non-private-address, size-limit, and timeout checks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/forevershu/baidudisk-mcp) <br>
- [Baidu Netdisk File API](https://pan.baidu.com/rest/2.0/xpan/file) <br>
- [Baidu Netdisk Multimedia API](https://pan.baidu.com/rest/2.0/xpan/multimedia) <br>
- [Baidu Netdisk Image Processing API](https://pan.baidu.com/rest/2.0/xpan/imageproc) <br>
- [Baidu Netdisk Category Info API](https://pan.baidu.com/api/categoryinfo) <br>
- [OpenAPI Generator](https://openapi-generator.tech) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-shaped MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Baidu Netdisk token-file credentials and may produce cloud-drive file operation results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
