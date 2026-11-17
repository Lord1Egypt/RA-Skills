## Description:

Use Baidu Netdisk via mcporter and a stdio MCP server with hot-reload token file credentials for official 2.0 toolset operations and legacy aliases from OpenClaw without storing access tokens in repository files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forevershu](https://clawhub.ai/user/forevershu)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to connect agents to Baidu Netdisk through mcporter, manage files, list media and documents, upload content, and inspect user quota through MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged registration path delegates to an unaudited script outside the artifact package.

Mitigation: Do not run the registration wrapper until the missing installer script is resolved and reviewed; configure mcporter manually if deployment is required.

Risk: URL upload can fetch remote content and has a credible internal-network request risk.

Mitigation: Disable URL upload or restrict it to trusted domains until SSRF validation is fixed and reviewed.

Risk: A Baidu access token used by this skill can grant file-management access.

Mitigation: Use only a token approved for the intended workspace, keep it in a local credential file, and rotate or revoke it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forevershu/skills/baidudisk-mcp)
- [Baidu Netdisk file API](https://pan.baidu.com/rest/2.0/xpan/file)
- [Baidu Netdisk multimedia API](https://pan.baidu.com/rest/2.0/xpan/multimedia)
- [Baidu Netdisk image processing API](https://pan.baidu.com/rest/2.0/xpan/imageproc)
- [Baidu OpenAPI authorization endpoint](https://openapi.baidu.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Baidu Netdisk credential file or access token; batch file operations return structured status, summary, results, and errors envelopes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
