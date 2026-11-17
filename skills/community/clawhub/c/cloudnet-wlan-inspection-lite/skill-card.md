## Description:

Cloudnet AI Inspection guides agents through a six-step Cloudnet WLAN inspection workflow using mcporter and Cloudnet MCP API calls, then produces Chinese Markdown and DOCX inspection reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudnet-skills](https://clawhub.ai/user/cloudnet-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Network operations engineers and administrators use this skill for quick Cloudnet WLAN health inspections, including AC health, problem distribution, access success rate, Cloudnet issue reasoning, AP online rate, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloudnet API keys may be exposed or persisted during configuration and inspection.

Mitigation: Use a narrowly scoped, revocable key; avoid printing files that contain secrets; verify where mcporter stores credentials; and remove or rotate the token after use.

Risk: Global npm or pip installs and unpinned dependencies can affect the host environment.

Mitigation: Install dependencies in an isolated environment and prefer pinned package versions.

Risk: Generated WLAN inspection reports may influence operational decisions.

Mitigation: Review report findings and recommendations against the source Cloudnet data before making network changes.

## Reference(s):

- [Cloudnet AI Inspection on ClawHub](https://clawhub.ai/cloudnet-skills/skills/cloudnet-wlan-inspection-lite)
- [Cloudnet MCP server endpoint](https://oasis.h3c.com/mcp-server/api/sse)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON report data, and Chinese MD/DOCX report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow depends on Cloudnet API access through mcporter and may create local reports and intermediate JSON files.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
