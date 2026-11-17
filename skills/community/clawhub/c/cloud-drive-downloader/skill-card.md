## Description:

Routes user-provided cloud-drive links and other download tasks through local or optional remote engines using agent, MCP, CLI, Web UI, and browser-extension entry points, without bypassing authentication or platform limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to route authorized cloud-drive downloads across macOS, Windows, and Linux through an agent, MCP, CLI, Web UI, or browser extension. It can create a dry-run plan or send a requested download to a configured local or remote engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan flags potential API-token exposure and automatic handling of clipboard and browser links.

Mitigation: Treat the scan as unresolved; review the source and extension permissions before installation, limit credentials, and enable clipboard or browser entry points only when needed.

Risk: The scan warns that the skill may perform broader transfer and remote-service actions than its download description suggests.

Mitigation: Review requested actions and destinations, use a dry-run plan first, and authorize only the remote services and transfers needed for the task.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/cloud-drive-downloader)
- [Agent calls and privacy boundaries](artifact/references/20-Agent调用与隐私.md)
- [MCP and agent interface](artifact/references/23-MCP与Agent接口.md)
- [Supported drive matrix](artifact/references/40-网盘支持矩阵.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON plans and status, downloaded files, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run plans are available; actual downloads use the configured destination and engine.]

## Skill Version(s):

0.20.2 (source: server-resolved release, CHANGELOG, released 2026-11-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
