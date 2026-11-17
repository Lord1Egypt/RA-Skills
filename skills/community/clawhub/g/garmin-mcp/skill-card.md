## Description:

Connect an MCP-compatible agent to local Garmin Connect sleep, Body Battery, HRV, stress, activities, and training readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users of MCP-compatible agents use this skill to install, configure, and troubleshoot Garmin MCP access to Garmin Connect wellness and activity data while keeping credential handling local and explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned npm package as the MCP server and authentication helper for sensitive Garmin health data.

Mitigation: Pin a reviewed package version, verify package provenance before use, and reassess trust before accepting future package updates.

Risk: Garmin credentials, tokens, or private wellness data could be exposed during setup or troubleshooting.

Mitigation: Use the local helper/token flow, keep token files protected under ~/.garmin-mcp/, and avoid printing OAuth tokens, API keys, local token files, or private user data.

## Reference(s):

- [ClawHub Garmin MCP Skill Page](https://clawhub.ai/davidmosiah/skills/garmin-mcp)
- [Garmin MCP Repository](https://github.com/davidmosiah/garminmcp)
- [Garmin Connector Docs](https://wellness.delx.ai/connectors/garmin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include MCP client setup, safety boundaries, privacy checks, and troubleshooting steps.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
