## Description:

CSV转JSON转换器 helps an agent inspect CSV files and convert CSV files or CSV strings into JSON through the Xiaobenyang-backed service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data operators use this skill to inspect CSV structure and convert CSV files or inline CSV content into JSON for downstream agent workflows. The skill requires a Xiaobenyang API key and relies on an external API service for conversion operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV contents or file paths may be sent to the external Xiaobenyang service.

Mitigation: Use this skill only with data approved for that external service, and avoid sensitive CSV data unless data-handling terms and user consent are clear.

Risk: The skill requires a Xiaobenyang API key and stores it in a local .env file.

Mitigation: Use a scoped key where possible, restrict access to the .env file, and rotate the key if exposure is suspected.

Risk: Server security evidence flags mismatch and under-disclosure around external API behavior.

Mitigation: Review the publisher's documentation and security posture before deployment, and add an explicit notice before sending CSV data externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/csv2json)
- [Xiaobenyang API key site](https://xiaobenyang.com)
- [Xiaobenyang MCP service](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [JSON responses and JSON file paths, usually summarized by the agent as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key; CSV content or file paths may be sent to an external service.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
